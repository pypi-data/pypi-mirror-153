"""
Placeholder
"""
import base64
import json
import re
from collections import namedtuple
import logging
import traceback
from jupyterlab_infinstor import servicedefs
import builtins
import configparser
import os
from os.path import expanduser
from os.path import sep as separator
import datetime
from jupyterlab_infinstor.cognito_utils import perform_infinstor_login, token_renewer,\
        check_for_custom_token,read_token_file, get_customerinfo, setup_token_for_mlflow,\
        bootstrap_config_values_from_mlflow_rest_if_needed
from infinstor import infin_boto3
import boto3

#  from dataclasses import dataclass

import tornado.gen as gen
from tornado import ioloop
from botocore.exceptions import NoCredentialsError
from notebook.base.handlers import IPythonHandler, utcnow, APIHandler
from notebook.utils import url_path_join
from traitlets import Unicode
from traitlets.config import SingletonConfigurable

import logging
import sys
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlunparse, urlparse, quote, unquote

from jupyterlab_infinstor.proxy import MlflowProxyHandler

from zipfile import ZipFile
import zipfile as zipfile_mod
import pathlib
import io
import urllib.parse
import time
import subprocess

class LoginHandler(APIHandler):  # pylint: disable=abstract-method
    """
    handle api requests to change auth info
    """
    @gen.coroutine
    def get(self, path=""):
        """
        Checks if the user is already authenticated
        against an s3 instance.
        """
        muri = os.getenv('MLFLOW_TRACKING_URI')
        if (not muri):
            print('ERROR!ERROR!ERROR: MLFLOW_TRACKING_URI must be set')
            sys.exit(255)
        bootstrap_config_values_from_mlflow_rest_if_needed()
        if (check_for_custom_token()):
            response_json = get_customerinfo()
            self.setup_vars(response_json)
            rv = json.dumps({"authenticated": True, "service": builtins.service,\
                        "mlflowTrackingUri": muri, \
                        "product": builtins.product, "cognitoUsername": builtins.cognito_username})
            builtins.log.info('LoginHandler.get: not previously logged in. logged in using custom token. ret=' + rv)
            self.finish(rv)
        else:
            tokfile = os.path.join(os.path.expanduser("~"), ".infinstor", "token")
            ftoken, _, token_time, _, service, id_token = read_token_file(tokfile)
            muri = os.getenv('MLFLOW_TRACKING_URI')
            pmuri = urllib.parse.urlparse(muri)
            if (pmuri.scheme.lower() != 'infinstor'):
                raise Exception(f"environment variable MLFLOW_TRACKING_URI={muri} has an invalid value or the url scheme != infinstor.  Set the environment variable correctly and restart the process")
            cognito_domain = pmuri.hostname[pmuri.hostname.index('.')+1:]
            url = 'https://' + pmuri.hostname + '/api/2.0/mlflow/infinstor/get_version'
            headers = { 'Authorization': 'None' }
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                resp = response.json()       
            except HTTPError as http_err:
                builtins.log.error(f"Caught Exception: {http_err}: {traceback.format_exc()}" )
                return None
            except Exception as err:
                builtins.log.error(f"Caught Exception: {err}: {traceback.format_exc()}" )
                return None
            rv = json.dumps({"authenticated": False, "mlflowTrackingUri": muri, "serviceDnsName": resp['serviceDnsName'] + '.' + cognito_domain})
            builtins.log.info('LoginHandler.get:' + rv)
            self.finish(rv)

    @gen.coroutine
    def post(self, path=""):
        """
        Sets s3 credentials.
        """
        req = json.loads(self.request.body)
        builtins.accesstoken = req["accesstoken"]
        builtins.refreshtoken = req["refreshtoken"]
        builtins.clientid = req["clientid"]
        builtins.service = req["service"]
        builtins.idToken = req["idToken"]
        setup_token_for_mlflow()
        builtins.log.info("LoginHandler.post: Entered. setup token")
        response_json = get_customerinfo()
        builtins.log.info(str(response_json))
        self.setup_vars(response_json)
        self.finish(json.dumps({"success": True, "service": builtins.service, "product": builtins.product, "user": response_json}))
        

    def get_clientid(self, service):
        url = 'https://' + builtins.serviceserver + '/assets/serviceconfig.js'
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_err:
            builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
            raise
        except Exception as err:
            builtins.log.error(f'Other error occurred: {err}', exc_info=True)
            raise
        builtins.log.info('successfully downloaded serviceconfig from ' + str(url))
        s1 = response.text[response.text.index('CliClientId: "') + len('CliClientId: "'):]
        s2 = s1[:s1.index('"')]
        builtins.log.info('clientid from serviceconfig=' + s2)
        return s2

    def setup_vars(self, response_json):
        builtins.cognito_username = response_json['userName']
        builtins.infinStorAccessKeyId = unquote(response_json.get('InfinStorAccessKeyId'))
        builtins.infinStorSecretAccessKey = unquote(
                response_json.get('InfinStorSecretAccessKey'))
        productCode = response_json.get('productCode')
        builtins.product = "Starter"
        for code in productCode:
            if code == "9fcazc4rbiwp6ewg4xlt5c8fu":
                builtins.product = "Premium"

class LogoutHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        tokfile = os.path.join(os.path.expanduser("~"), ".infinstor", "token")
        with open(tokfile, 'w') as wfile:
            wfile.write("Token=" + builtins.accesstoken + "\n")
            wfile.write("RefreshToken=" + builtins.refreshtoken + "\n")
            wfile.write("ClientId=" + builtins.clientid + "\n")
            wfile.write("Service=" + builtins.service + "\n")
            wfile.write("IdToken=" + builtins.idToken + "\n")
            wfile.close()
        rv = json.dumps({"success": True })
        builtins.log.info('LogoutHandler.post:' + rv)
        self.finish(rv)

class TokenHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def get(self, path=""):
        rv = json.dumps({"Authorization": builtins.accesstoken, "Idtoken": builtins.idToken })
        self.finish(rv)

class CondaEnvHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def get(self, path=""):
        try:
            output = subprocess.check_output("conda env list --json", shell=True, encoding='utf-8')
            outputJson = json.loads(output)
            self.finish(json.dumps({"success": True, "envs": outputJson["envs"]}))
        except Exception as err:
            builtins.log.error("Exception caught: %s", err, exc_info=True)
            self.finish(json.dumps({"success": False, "message": str(err)}))

    @gen.coroutine
    def post(self, path=""):
        try:
            req = json.loads(self.request.body)
            envName = req["envName"]
            output = subprocess.check_output("conda env export --no-builds -n " + envName, shell=True)
            rv = json.dumps({ "success": True, "env": output.decode('utf-8') })
            self.finish(rv)
        except Exception as err:
            builtins.log.error("Exception caught: %s", err, exc_info=True)
            self.finish(json.dumps({"success": False, "message": str(err)}))

class InfinSnapHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        try:
            req = json.loads(self.request.body)
            builtins.log.info("InfinSnapHandler.post: Entered. infinstor_time_spec ="
                    + req["InfinSnapHostname"])
            builtins.s3_resource = boto3.resource("s3", infinstor_time_spec=req["InfinSnapHostname"])
            self.finish(json.dumps({"success": True}))
        except Exception as err:
            builtins.log.error("Exception caught: %s", err, exc_info=True)
            self.finish(json.dumps({"success": False, "message": str(err)}))

class InfinSliceHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        try:
            req = json.loads(self.request.body)
            builtins.log.info("InfinSliceHandler.post: Entered. infinstor_time_spec="
                    + req["InfinSliceHostname"])
            builtins.s3_resource = boto3.resource("s3", infinstor_time_spec=req["InfinSliceHostname"])
            self.finish(json.dumps({"success": True}))
        except Exception as err:
            builtins.log.error("Exception caught: %s", err, exc_info=True)
            self.finish(json.dumps({"success": False, "message": str(err)}))

class AddLabelHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)

        labelname = req["labelname"]
        bucketname = req["bucketname"]
        if 'pathinbucket' in req:
            pathinbucket = req["pathinbucket"]
        else:
            pathinbucket = ""
        timespec = req["timespec"]
        delimiter = "/"

        payload = "label=" + labelname + "&bucketname=" + bucketname \
                + "&delimiter=" + delimiter + "&prefix=" + pathinbucket \
                + "&timespec=" + timespec + '&clientType=browser'
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/addlabel'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('addlabel success!')
                self.finish(json.dumps({"success": True}))
                break

class ListLabelsHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/listlabels'
            try:
                response = requests.post(url, data="&clientType=browser", headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('listLabelsHandler: listlabels success!')
                builtins.log.info(response.json())
                self.finish(json.dumps({"success": True, "AllLabels": response.json()}))
                break

class UseLabelHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            req = json.loads(self.request.body)
            labelname = req["labelname"]
            payload = "label=" + labelname + '&clientType=browser'

            url = 'https://' + builtins.apiserver + '/listlabels'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
                labels = resp_json['labels']
                first_label = labels[0]
                timespec = first_label['timespec']
                if timespec.find('-') == -1:
                    builtins.log.info("uselabel: Setting up boto3 for InfinSnap")
                    infinStorEndpoint = 'https://' + timespec + '.s3proxy.' \
                        + builtins.service + ':443/'
                else:
                    builtins.log.info("uselabel: Setting up boto3 for InfinSlice")
                    infinStorEndpoint = 'https://' + timespec + '.s3proxy.' \
                        + builtins.service + ':443/'
                builtins.s3_resource = boto3.resource(
                    "s3",
                    aws_access_key_id=builtins.infinStorAccessKeyId,
                    aws_secret_access_key=builtins.infinStorSecretAccessKey,
                    endpoint_url=infinStorEndpoint
                )
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                builtins.log.error(exc_type, fname, exc_tb.tb_lineno)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('uselabel: listlabels success')
                self.finish(json.dumps({"success": True, "AllLabels": resp_json}))
                break

class AddXformHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)

        xformname = req["xformname"]
        xformcode = req["xformcode"]

        code_str = unquote(xformcode)
        code_str_lines = code_str.splitlines()
        clean_code = ''
        for one_line in code_str_lines:
            if (one_line == '%reset -f'):
                continue
            if (one_line == 'from infinstor import test_infin_transform # infinstor'):
                continue
            if (one_line.startswith('input_data_spec') and one_line.endswith('# infinstor')):
                continue
            if (one_line.startswith('rv = test_infin_transform') and one_line.endswith('# infinstor')):
                continue
            clean_code += (one_line + '\n')
        # print(clean_code)

        payload = "xformname=" + xformname + "&xformcode=" + quote(clean_code)

        if 'conda_env' in req:
            payload = payload + "&conda_env=" + req["conda_env"]

        if 'dockerfile' in req:
            payload = payload + "&dockerfile=" + req["dockerfile"]

        # {
        #    "xform_local_files": {
        #       "xform_local_files_zip":"zipfile_base64encoded"
        #       "xform_local_files_zip_filelist": {
        #           "./file1": { },
        #           "./file2": { }
        #       }
        #    }
        # }
        if 'xform_local_files' in req:
            xform_local_files = req["xform_local_files"]
            if 'xform_local_files_zip_filelist' in xform_local_files:
                # example temp zip file: /tmp/xform_local_files_gdw5w6j2.zip
                # note that we cannot use the processid to create temporary files since this is a coroutine, which is a light weight thread: if multiple coroutines execute concurrently, then filenames based on processID will overlap (same name used by multiple threads) and will cause issues.
                with io.BytesIO() as bytesfile:
                    with ZipFile(bytesfile, 'w', compression=zipfile_mod.ZIP_LZMA) as myzip:
                        for file in  xform_local_files['xform_local_files_zip_filelist']:
                            # get file details
                            file_stat = pathlib.Path(file).stat()
                            xform_local_files['xform_local_files_zip_filelist'][file]['size'] = file_stat.st_size
                            xform_local_files['xform_local_files_zip_filelist'][file]['lastmodifiedtime'] = file_stat.st_mtime_ns
                            builtins.log.info(f'file to be compressed={file} with len={file_stat.st_size} with modification time={file_stat.st_mtime_ns}')

                            # add it to zip file
                            myzip.write(file)

                    builtins.log.info(f'length of zip archive = {len(bytesfile.getbuffer())}')
                    
                    # reset file position to 0.
                    bytesfile.seek(0)
                    
                    # base64 encode zipfile
                    xform_local_files_zip_b64 = base64.b64encode(bytesfile.read())

                # convert from bytes to a string..
                # to send as x-www-form-urlencoded, need to url encode the string, since base64 has '+' and '/' and the former needs to be URL encoded
                xform_local_files['xform_local_files_zip'] = xform_local_files_zip_b64.decode("utf-8")

                xform_local_files_jsonstr = json.dumps(xform_local_files)

                # to send as x-www-form-urlencoded, need to url encode the string, since base64 has '+' and '/' and the former needs to be URL encoded
                payload = payload + "&xform_local_files=" + quote(xform_local_files_jsonstr) + '&clientType=browser'

        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/addxform'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('addxform success!')
                self.finish(json.dumps({"success": True}))
                break

class DeleteXformHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)

        xformname = req["xformname"]

        payload = "xformname=" + xformname + '&clientType=browser'
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/deletexform'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('deletexform success!')
                self.finish(json.dumps({"success": True}))
                break

class ListXformsHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/listxforms'
            try:
                response = requests.post(url, data="clientType=browser", headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('listXformsHandler: listxforms success!')
                # print(response.json())
                self.finish(json.dumps({"success": True, "AllXforms": response.json()}))
                break

class ConformAccountHandler(APIHandler):
    @gen.coroutine
    def post(self, path=""):
        try:
            req = json.loads(self.request.body)
            email = req["email"]
            username = req["username"]
            session = req["Session"]
            password = req["new_password"]
            clientid = req["clientid"]
            payload = "{\n"
            payload += "    \"ChallengeResponses\" : {\n"
            payload += "        \"userAttributes.email\" : \"" + email + "\",\n"
            payload += "        \"NEW_PASSWORD\" : \"" + password + "\",\n"
            payload += "        \"USERNAME\" : \"" + username + "\"\n"
            payload += "    },\n"
            payload += "    \"ChallengeName\" : \"NEW_PASSWORD_REQUIRED\",\n"
            payload += "    \"ClientId\" : \"" + clientid + "\",\n"
            payload += "    \"Session\" : \"" + session + "\"\n"
            payload += "}\n"
            builtins.log.info("payload" + payload)

            # populate builtins.region if needed
            cognito_utils.bootstrap_config_values_from_mlflow_rest_if_needed()

            url = 'https://cognito-idp.' + builtins.region + '.amazonaws.com:443/'

            headers = {
                    'Content-Type': 'application/x-amz-json-1.1',
                    'X-Amz-Target' : 'AWSCognitoIdentityProviderService.RespondToAuthChallenge'
                    }
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()

            self.finish(json.dumps({"success": True, "message": str(response.json)}))
        except Exception as err:
            builtins.log.error(f'Exception caught: {err}', exc_info=True)
            self.finish(json.dumps({"success": False, "message": str(err)}))

class AddPeriodicRunHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)

        name = req["periodicRunName"]
        experiment_id = self.create_mlflow_experiment(name)
        run = json.loads(req["periodicRunJson"])
        # Add experiment id to json
        run['experiment_id'] = experiment_id
        quoted_run_json = quote(json.dumps(run))

        payload = "periodicRunName=" + name + "&periodicRunJson=" + quoted_run_json + '&clientType=browser'
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/addmodifyperiodicrun'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('addperiodicrun success!')
                self.finish(json.dumps({"success": True}))
                break

    def create_mlflow_experiment(self, experiment_name):
        for retry in range(2):
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            if (builtins.accesstoken.startswith('Custom')):
                headers['Authorization'] = builtins.accesstoken
            else:
                headers['Authorization'] = 'Bearer ' + builtins.accesstoken

            url = 'https://' + builtins.mlflowserver +\
                    '/Prod/2.0/mlflow/experiments/get-by-name?experiment_name=' +\
                    quote(experiment_name)
            try:
                response = requests.get(url, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred in get-by-name: {http_err}', exc_info=True)
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred in get-by-name: {err}', exc_info=True)
                break
            else:
                builtins.log.info('addperiodicruns: get-by-name success')
                return resp_json['experiment']['experiment_id']

        for retry in range(2):
            payload = '{ "name": "' + experiment_name + '" }'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            if (builtins.accesstoken.startswith('Custom')):
                headers['Authorization'] = builtins.accesstoken
            else:
                headers['Authorization'] = 'Bearer ' + builtins.accesstoken

            url = 'https://' + builtins.mlflowserver + '/Prod/2.0/mlflow/experiments/create'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('addperiodicruns: create_mlflow_experiment success!')
                return resp_json['experiment_id']

class ListPeriodicRunsHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/listperiodicruns'
            try:
                response = requests.post(url, data="clientType=browser", headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('listPeriodicRunsHandler: listperiodicruns success!')
                builtins.log.info(response.json())
                self.finish(json.dumps({"success": True, "AllPeriodicRuns": response.json()}))
                break

class DeletePeriodicRunHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)

        periodicRuns = req["periodicRuns"]

        payload = "periodicRuns=" + ",".join(periodicRuns)
        payload += '&clientType=browser'
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/deleteperiodrun'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                builtins.log.info('deleteperiodicruns success!')
                self.finish(json.dumps({"success": True}))
                break

class AddTransformGraphHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)
        dag_name = req["dagName"]
        graphJson = json.loads(req["dagJson"])
        # Add experiment id to json
        quoted_graph_json = quote(json.dumps(graphJson))

        payload = "dagName=" + dag_name  + "&dagJson=" + quoted_graph_json + '&clientType=browser'

        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/addmodifydag'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                print('adddag success!')
                self.finish(json.dumps({"success": True}))
                break

class ListTransformGraphHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/listdags'
            try:
                response = requests.post(url, data="clientType=browser", headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                print('listdag: listdag success!')
                print(response.json())
                self.finish(json.dumps({"success": True, "dag": response.json()}))
                break

class RunTransformGraphHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)
        graphJson = json.loads(req["dagJson"])
        quoted_graph_json = quote(json.dumps(graphJson))

        payload = "dagid=" + req["dagid"] + "&dagJson=" + quoted_graph_json + '&clientType=browser'
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.apiserver + '/rundag'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                builtins.log.error(f'Other error occurred: {err}', exc_info=True)
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                print('Transform Graph Run success!')
                self.finish(json.dumps({"success": True}))
                break

class DeleteDagHandler(APIHandler):  # pylint: disable=abstract-method
  @gen.coroutine
  def post(self, path=""):
      req = json.loads(self.request.body)

      payload = "dagid=" + req["dagid"] + '&clientType=browser'
      for retry in range(2):
          headers = {
              'Content-Type': 'application/x-www-form-urlencoded',
              'Authorization': builtins.accesstoken,
              'Idtoken': builtins.idToken
              }

          url = 'https://' + builtins.apiserver + '/deletedag'
          try:
              response = requests.post(url, data=payload, headers=headers)
              resp_json = response.json()
              response.raise_for_status()
          except HTTPError as http_err:
              builtins.log.error(f'HTTP error occurred: {http_err}', exc_info=True)
              self.finish(json.dumps({"success": False, "message": str(http_err)}))
              break
          except Exception as err:
              builtins.log.error(f'Other error occurred: {err}', exc_info=True)
              self.finish(json.dumps({"success": False, "message": str(err)}))
              break
          else:
              print('deletedag success!')
              self.finish(json.dumps({"success": True}))
              break

class listVMHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }

            url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/projects/list-singlevm'
            try:
                response = requests.get(url, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                print('listVM: listVM success!')
                print(response.json())
                self.finish(json.dumps({"success": True, "vms": response.json()}))
                break

class getRunStatusHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)
        if 'dag_execution_id' in req:
            query = '?dagid=' + req["dagid"] +'&dag_execution_id=' + req["dag_execution_id"]
        else:
            query = '?dagid=' + req["dagid"]

        for retry in range(2):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': builtins.accesstoken,
                'Idtoken': builtins.idToken
                }
            url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/runs/getdagexecinfo' + query
            try:
                response = requests.get(url, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                print('Dag Execution: Execution success!')
                print(response.json())
                self.finish(json.dumps({"success": True, "dag_execution": response.json()}))
                break

class stopVMHandler(APIHandler):  # pylint: disable=abstract-method
    @gen.coroutine
    def post(self, path=""):
        req = json.loads(self.request.body)
        if 'do_terminate' in req:
            payload = '{ "do_terminate": "' + req["do_terminate"] + '", "instance_type": "' + req["instance_type"] + '", "periodic_run_name": "' + req["periodic_run_name"] + '"}'
        else:
            payload = '{ "instance_type": "' + req["instance_type"] + '", "periodic_run_name": "' + req["periodic_run_name"] + '"}'

        for retry in range(2):
            headers = {
              'Content-Type': 'application/x-www-form-urlencoded',
              'Authorization': builtins.accesstoken,
              'Idtoken': builtins.idToken
            }

            url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/projects/stop-singlevm'
            try:
                response = requests.post(url, data=payload, headers=headers)
                resp_json = response.json()
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                self.finish(json.dumps({"success": False, "message": str(http_err)}))
                break
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.finish(json.dumps({"success": False, "message": str(err)}))
                break
            else:
                print('stopVM success!')
                self.finish(json.dumps({"success": True}))
                break

class S3ResourceNotFoundException(Exception):
    pass


# TODO: use this
#  @dataclass
#  class S3GetResult:
#  name: str
#  type: str
#  path: str


def parse_bucket_name_and_path(raw_path):
    if "/" not in raw_path[1:]:
        bucket_name = raw_path[1:]
        path = ""
    else:
        bucket_name, path = raw_path[1:].split("/", 1)
    return (bucket_name, path)

Content = namedtuple("Content", ["name", "path", "type", "mimetype","last_modified", "size"])

# call with
# request_prefix: the prefix we sent to s3 with the request
# response_prefix: full path of object or directory as returned by s3
# returns:
# subtracts the request_prefix from response_prefix and returns
# the basename of request_prefix
# e.g. request_prefix=rawtransactions/2020-04-01 response_prefix=rawtransactions/2020-04-01/file1
# this method returns file1
def get_basename(request_prefix, response_prefix):
    request_prefix_len = len(request_prefix)
    response_prefix_len = len(response_prefix)
    response_prefix = response_prefix[request_prefix_len:response_prefix_len]
    if (response_prefix.endswith("/")):
        response_prefix_len = len(response_prefix) - 1
        response_prefix = response_prefix[0:response_prefix_len]
    return response_prefix

def do_list_objects_v2(s3client, bucket_name, prefix):
    list_of_objects = []
    list_of_directories = []
    try:
        prefix_len = len(prefix)
        response = s3client.list_objects_v2(Bucket=bucket_name,
                Delimiter="/",
                EncodingType='url',
                Prefix=prefix,
                )
        if 'Contents' in response:
            contents = response['Contents']
            for one_object in contents:
                obj_key = one_object['Key']
                get_last_modified = one_object['LastModified']
                last_modified = get_last_modified.strftime('%m/%d/%Y %H:%M:%S')
                size = one_object['Size']
                obj_key_basename = get_basename(prefix, obj_key)
                if len(obj_key_basename) > 0:
                    list_of_objects.append(Content(obj_key_basename, obj_key, "file", "json", last_modified, size))
        if 'CommonPrefixes' in response:
            common_prefixes = response['CommonPrefixes']
            for common_prefix in common_prefixes:
                prfx = common_prefix['Prefix']
                prfx_basename = get_basename(prefix, prfx)
                list_of_directories.append(Content(prfx_basename, prfx, "directory", "json", "", ""))
    except Exception as e:
        builtins.log.error(f'Exception caught: {e}', exc_info=True)
        traceback.print_exc()

    return list_of_objects, list_of_directories;

def do_get_object(s3client, bucket_name, path):
    try:
        response = s3client.get_object(Bucket=bucket_name, Key=path)
        if 'Body' in response:
            if 'ContentType' in response:
                content_type = response['ContentType']
            else:
                content_type = 'Unknown'
            streaming_body = response['Body']
            data = streaming_body.read()
            return content_type, data
        else:
            return None
    except Exception as e:
        builtins.log.error(f'Exception caught: {e}', exc_info=True)
        traceback.print_exc()
        return None

def get_s3_objects_from_path(s3, path):

    if path == "/":
        # requesting the root path, just return all buckets
        if builtins.product == "Starter":
            test = boto3.resource("s3")
            all_buckets = test.buckets.all()
            result = [
                {"name": bucket.name, "path": bucket.name, "type": "directory"}
                for bucket in all_buckets
            ]
            if isinstance(result, list):
                result.sort(key=lambda x: x.get('name'))
            return result
        else:
            all_buckets = s3.buckets.all()
            result = [
                {"name": bucket.name, "path": bucket.name, "type": "directory"}
                for bucket in all_buckets
            ]
            if isinstance(result, list):
                result.sort(key=lambda x: x.get('name'))
            return result
    else:
        bucket_name, path = parse_bucket_name_and_path(path)
        s3client = s3.meta.client
        if (path == "" or path.endswith("/")):
            list_of_objects, list_of_directories = do_list_objects_v2(s3client, bucket_name, path)
            directories = list(list_of_directories)
            objects = list(list_of_objects)
            result = directories + objects
            result = [
                {
                    "name": content.name,
                    "path": "{}/{}".format(bucket_name, content.path),
                    "type": content.type,
                    "mimetype": content.mimetype,
                    "last_modified": content.last_modified,
                    "size": content.size
                }
                for content in result
            ]
            return result
        else:
            object_content_type, object_data = do_get_object(s3client, bucket_name, path)
            if object_content_type != None:
                result = {
                    "path": "{}/{}".format(bucket_name, path),
                    "type": "file",
                    "mimetype": object_content_type,
                }
                result["content"] = base64.encodebytes(object_data).decode("ascii")
                return result
            else:
                result = {
                    "error": 404,
                    "message": "The requested resource could not be found.",
                }

class S3Handler(APIHandler):
    """
    Handles requests for getting S3 objects
    """

    @gen.coroutine
    def get(self, path=""):
        """
        Takes a path and returns lists of files/objects
        and directories/prefixes based on the path.
        """

        # boto3.set_stream_logger('boto3.resources', logging.DEBUG)
        # boto3.set_stream_logger('botocore', logging.DEBUG)
        try:
            builtins.log.info("S3Handler.post: Using keyId =" + builtins.infinStorAccessKeyId
                    + ", s3_resource " + str(builtins.s3_resource))
            result = get_s3_objects_from_path(builtins.s3_resource, path)
        except S3ResourceNotFoundException as e:
            builtins.log.error(f'Exception caught: {e}', exc_info=True)
            result = {
                "error": 404,
                "message": "The requested resource could not be found.",
            }
        except Exception as e:
            builtins.log.error(f'Exception caught: {e}', exc_info=True)
            result = {"error": 500, "message": str(e)}
        self.finish(json.dumps(result))


def _jupyter_server_extension_paths():
    return [{"module": "jupyterlab_infinstor"}]

def token_renewer_task():
    token_renewer()

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication):
        handle to the Notebook webserver instance.
    """
    builtins.log = nb_server_app.log

    web_app = nb_server_app.web_app
    base_url = web_app.settings["base_url"]
    endpoint = url_path_join(base_url, "s3")
    handlers = [
        (url_path_join(endpoint, "files") + "(.*)", S3Handler),
        (url_path_join(endpoint, "login") + "(.*)", LoginHandler),
        (url_path_join(endpoint, "infinsnap") + "(.*)", InfinSnapHandler),
        (url_path_join(endpoint, "infinslice") + "(.*)", InfinSliceHandler),
        (url_path_join(endpoint, "addlabel") + "(.*)", AddLabelHandler),
        (url_path_join(endpoint, "listlabels") + "(.*)", ListLabelsHandler),
        (url_path_join(endpoint, "uselabel") + "(.*)", UseLabelHandler),
        (url_path_join(endpoint, "addxform") + "(.*)", AddXformHandler),
        (url_path_join(endpoint, "deletexform") + "(.*)", DeleteXformHandler),
        (url_path_join(endpoint, "listxforms") + "(.*)", ListXformsHandler),
        (url_path_join(endpoint, "conformaccount") + "(.*)", ConformAccountHandler),
        (url_path_join(endpoint, "addperiodicrun") + "(.*)", AddPeriodicRunHandler),
        (url_path_join(endpoint, "listperiodicruns") + "(.*)", ListPeriodicRunsHandler),
        (url_path_join(endpoint, "deleteperiodrun") + "(.*)", DeletePeriodicRunHandler),
        (url_path_join(endpoint, "addtransformgraph") + "(.*)", AddTransformGraphHandler),
        (url_path_join(endpoint, "listtransformgraph") + "(.*)", ListTransformGraphHandler),
        (url_path_join(endpoint, "runtransformgraph") + "(.*)", RunTransformGraphHandler),
        (url_path_join(endpoint, "deletetransformgraph") + "(.*)", DeleteDagHandler),
        (url_path_join(endpoint, "listvm") + "(.*)", listVMHandler),
        (url_path_join(endpoint, "getRunStatus") + "(.*)", getRunStatusHandler),
        (url_path_join(endpoint, "stopvm") + "(.*)", stopVMHandler),
        (url_path_join(endpoint, "logout") + "(.*)", LogoutHandler),
        (url_path_join(endpoint, "getconda") + "(.*)", CondaEnvHandler),
        (url_path_join(endpoint, "getToken") + "(.*)", TokenHandler),
        (url_path_join(endpoint, r'/mlflowproxy/(\d+)(.*)'), MlflowProxyHandler,\
                {'absolute_url': False})
    ]
    web_app.add_handlers(".*$", handlers)
    tr = ioloop.PeriodicCallback(token_renewer_task, 180000)
    tr.start()
