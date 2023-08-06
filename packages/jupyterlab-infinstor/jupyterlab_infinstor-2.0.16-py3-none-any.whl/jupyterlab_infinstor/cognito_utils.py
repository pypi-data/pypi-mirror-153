from dataclasses import dataclass
import jsons
import requests
from requests.exceptions import HTTPError
import json
import builtins
import os
from os.path import expanduser
from os.path import sep as separator
import time
from typing import Any, Dict, List, NoReturn, Tuple
import traceback
import time
import urllib.parse

# TODO: DUPLICATED: have copies in other .py files. refactor later
def readJsonFileAndDeser(filename:str, cls) -> Tuple[str,Any]:
    """
    Reads the specified json file and deserializes it into the 'cls' that is specified.  Returns the read json(as a string) and the deserialized instance
    """
    # use empty json as the default
    filecontents = '{}'
    try:
        if os.path.isfile(filename):   # check for file existence before attempting to open() below since open() raises an exception if file not found
            with open(filename, "r") as f:
                filecontents:str = f.read()   #read the contents of the url            
    except Exception as e:
        builtins.log.error(f"Caught exception: {e}: " + traceback.format_exc())
        
    return (filecontents, jsons.loads(filecontents, cls))
    

# TODO: DUPLICATED: have copies in other .py files. refactor later
# {
#     "rclocal_shutdowndelay": 115,
#     "clientlib_verbose": false,
#     "server_extension_cognito_utils_verbose": false
# }
@dataclass
class InfinstorConfig(jsons.JsonSerializable):
    rclocal_shutdowndelay:int = 15                         # delay in minutes
    clientlib_verbose:bool = False                         
    server_extension_cognito_utils_verbose:bool = False

def set_verbose_flag():
    state_json_fname = os.path.join(os.path.expanduser("~"), ".infinstor", "config.json")
    infin_config:InfinstorConfig; jsonstr:str; (jsonstr, infin_config) = readJsonFileAndDeser(state_json_fname, InfinstorConfig)
    return infin_config.server_extension_cognito_utils_verbose

verbose = set_verbose_flag()

def _get_token_file_name():
    return os.path.join(expanduser("~"), ".infinstor", "token")
    
def read_token_file(tokfile=None):
    if not tokfile: tokfile = _get_token_file_name()
        
    fclient_id = None
    ftoken = None
    frefresh_token = None
    ftoken_time = None
    fservice = None
    fidtoken = None
    try:
        with (open(tokfile)) as fp:
            for count, line in enumerate(fp):
                if (line.startswith('ClientId=')):
                    fclient_id = line[len('ClientId='):].rstrip()
                if (line.startswith('Token=')):
                    ftoken = line[len('Token='):].rstrip()
                if (line.startswith('RefreshToken=')):
                    frefresh_token = line[len('RefreshToken='):].rstrip()
                if (line.startswith('TokenTimeEpochSeconds=')):
                    ftoken_time = int(line[len('TokenTimeEpochSeconds='):].rstrip())
                if (line.startswith('Service=')):
                    fservice = line[len('Service='):].rstrip()
                if (line.startswith('IdToken=')):
                    fidtoken = line[len('IdToken='):].rstrip()
    except FileNotFoundError as ferr:
        # tokenfile does not exist
        builtins.log.info(f"tokenfile {tokfile} does not exist")
    except Exception as err:
        builtins.log.error(f"while opening token file {tokfile}, caught exception: {err}: {traceback.format_exc()}")

    return ftoken, frefresh_token, ftoken_time, fclient_id, fservice, fidtoken

def write_token_file(tokfile, token_time, token, refresh_token, client_id, service, idToken):
    os.makedirs(os.path.dirname(tokfile), exist_ok=True)
    with open(tokfile, 'w') as wfile:
        wfile.write("Token=" + token + "\n")
        wfile.write("RefreshToken=" + refresh_token + "\n")
        wfile.write("ClientId=" + client_id + "\n")
        wfile.write("TokenTimeEpochSeconds=" + str(token_time) + "\n")
        wfile.write("Service=" + service + "\n")
        wfile.write("IdToken=" + idToken + "\n")
        wfile.close()

def bootstrap_config_values_from_mlflow_rest_if_needed():
    ##########
    #  TODO: a copy exists in 
    #  infinstor-mlflow/plugin/infinstor_mlflow_plugin/login.py 
    #  infinstor-mlflow/processors/singlevm/scripts/rclocal.py
    #  infinstor-jupyterlab/server-extension/jupyterlab_infinstor/__init__.py
    #  infinstor-jupyterlab/server-extension/jupyterlab_infinstor/cognito_utils.py
    #  infinstor-jupyterlab/clientlib/infinstor/bootstrap.py
    #  infinstor-jupyterlab/infinstor_py_bootstrap_project/infinstor_py_bootstrap/infinstor_py_bootstrap.py
    #  Need to see how to share code between two pypi packages to eliminate this duplication
    #  when refactoring this code, also refactor the copies
    ############
    
    # if the configuration values have already been bootstrapped, return
    if getattr(builtins, 'mlflowserver', None): return
    
    # note that this code (server-extension code) runs in the jupyterlab server, where MLFLOW_TRACKING_URI was not set earlier.  Now it needs to be set correctly to the mlflow api hostname: mlflow.infinstor.com.  Note that 'mlflow' in the hostname is not hardcoded.. it can be a different subdomain name
    #
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
        builtins.clientid = resp['cognitoCliClientId']
        builtins.appclientid = resp['cognitoAppClientId']
        builtins.mlflowserver = resp['mlflowDnsName'] + '.' + cognito_domain
        builtins.mlflowuiserver = resp['mlflowuiDnsName'] + '.' + cognito_domain
        builtins.mlflowstaticserver = resp['mlflowstaticDnsName'] + '.' + cognito_domain
        builtins.apiserver = resp['apiDnsName'] + '.' + cognito_domain
        builtins.serviceserver = resp['serviceDnsName'] + '.' + cognito_domain
        builtins.service = cognito_domain
        builtins.region = resp['region']        
    except HTTPError as http_err:
        builtins.log.error(f"Caught Exception: {http_err}: {traceback.format_exc()}" )
        return None
    except Exception as err:
        builtins.log.error(f"Caught Exception: {err}: {traceback.format_exc()}" )
        return None

def renew_token(aws_region:str, tokfile:str, refresh_token:str, client_id:str, service:str):
    payload = "{\n"
    payload += "    \"AuthParameters\" : {\n"
    payload += "        \"REFRESH_TOKEN\" : \"" + refresh_token + "\"\n"
    payload += "    },\n"
    payload += "    \"AuthFlow\" : \"REFRESH_TOKEN_AUTH\",\n"
    payload += "    \"ClientId\" : \"" + client_id + "\"\n"
    payload += "}\n"

    url = 'https://cognito-idp.' + aws_region + '.amazonaws.com:443/'

    headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target' : 'AWSCognitoIdentityProviderService.InitiateAuth'
            }

    if (verbose):
        builtins.log.info(f"Calling renew_token with url={url}; headers={headers}; payload={payload}")

    try:
        response = requests.post(url, data=payload, headers=headers)
    except Exception as err:
        builtins.log.error(f"renew_token: Caught {err}: {traceback.format_exc()}  ")
        raise
    else:
        if (response.status_code != 200):
            builtins.log.error("renew_token: Error. http status_code is " + str(response.status_code)
                    + ", response=" + str(response.text))
        else:
            authres = response.json()['AuthenticationResult']
            token = authres['AccessToken']
            idToken = authres['IdToken']
            token_time = int(time.time())
            write_token_file(tokfile, token_time, token, refresh_token, client_id, service, idToken)

def token_renewer():
    # read and set verbose flag everytime we are called..
    global verbose; verbose = set_verbose_flag()
    
    if (verbose):
        builtins.log.info('token_renewer(): called')
    token, refresh_token, token_time, client_id, service, id_token = read_token_file()
    if (token_time == None):
        if (verbose):
            builtins.log.info('token_renewer: token_time is None. Possibly custom token')
        return
    # example outupt of time.localtime(time_now):  [I 2021-09-22 14:24:10.538 ServerApp] InfinStor token has not expired: token_time=1632300186; time.localtime(token_time)=time.struct_time(tm_year=2021, tm_mon=9, tm_mday=22, tm_hour=14, tm_min=13, tm_sec=6, tm_wday=2, tm_yday=265, tm_isdst=0); time_now=1632300850; time.localtime(time_now)=time.struct_time(tm_year=2021, tm_mon=9, tm_mday=22, tm_hour=14, tm_min=24, tm_sec=10, tm_wday=2, tm_yday=265, tm_isdst=0)
    #
    # when VM's timezone is IST, 'time_now' as computed below is incorrect:  time.localtime(time_now) shows the time to be 5:30 before the actual IST time..
    # time_now = round(datetime.datetime.timestamp(datetime.datetime.utcnow()))
    time_now = int(time.time())
    if ((token_time + (30 * 60)) < time_now):
        if (verbose):
            builtins.log.info('InfinStor token has expired. Calling renew ' + str(token_time)\
                + ', ' + str(time_now))

        # populate builtins.region if needed
        bootstrap_config_values_from_mlflow_rest_if_needed()
        
        renew_token(builtins.region, _get_token_file_name(), refresh_token, client_id, service)
        token, refresh_token, token_time, client_id, service, id_token = read_token_file()
        builtins.accesstoken = token
        builtins.refreshtoken = refresh_token
        builtins.idToken = id_token
    else:
        if (verbose):
            # [I 2021-09-22 14:24:10.538 ServerApp] InfinStor token has not expired: token_time=1632300186; time.localtime(token_time)=time.struct_time(tm_year=2021, tm_mon=9, tm_mday=22, tm_hour=14, tm_min=13, tm_sec=6, tm_wday=2, tm_yday=265, tm_isdst=0); time_now=1632300850; time.localtime(time_now)=time.struct_time(tm_year=2021, tm_mon=9, tm_mday=22, tm_hour=14, tm_min=24, tm_sec=10, tm_wday=2, tm_yday=265, tm_isdst=0)
            builtins.log.info(f"InfinStor token has not expired: token_time={token_time}; time.localtime(token_time)={time.localtime(token_time)}; time_now={time_now}; time.localtime(time_now)={time.localtime(time_now)}")

def perform_infinstor_login(username, password):
    payload = "{\n"
    payload += "    \"AuthParameters\" : {\n"
    payload += "        \"USERNAME\" : \"" + username + "\",\n"
    payload += "        \"PASSWORD\" : \"" + password + "\"\n"
    payload += "    },\n"
    payload += "    \"AuthFlow\" : \"USER_PASSWORD_AUTH\",\n"
    payload += "    \"ClientId\" : \"" + builtins.clientid + "\"\n"
    payload += "}\n"

    # populate builtins.region if needed
    bootstrap_config_values_from_mlflow_rest_if_needed()

    url = 'https://cognito-idp.' + builtins.region + '.amazonaws.com:443/'

    headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target' : 'AWSCognitoIdentityProviderService.InitiateAuth'
            }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        builtins.log.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        builtins.log.error(f'Other error occurred: {err}')
        raise
    else:
        builtins.log.info('Authorization success!')
        challenge = response.json().get('ChallengeName')
        if challenge == "NEW_PASSWORD_REQUIRED":
            return response.json()
        else:
            authres = response.json()['AuthenticationResult']
            builtins.accesstoken = authres['AccessToken']
            builtins.refreshtoken = authres['RefreshToken']
            builtins.idToken = authres['IdToken']
    # Call cognito REST API getUser to get custom:serviceName
    body = dict()
    body['AccessToken'] = authres['AccessToken']
    body_s = json.dumps(body)
    headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target' : 'AWSCognitoIdentityProviderService.GetUser'
            }
    try:
        response = requests.post(url, data=body_s, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        builtins.log.error(f'HTTP error occurred in getUser: {http_err}')
        raise
    except Exception as err:
        builtins.log.error(f'Other error occurred in getUser: {err}')
        raise
    else:
        builtins.log.info('cognito getUser success')
        user = response.json()
        useratt = user['UserAttributes']
        for oneattr in useratt:
            if (oneattr['Name'] == 'custom:serviceName'):
                srvc = oneattr['Value']
                builtins.log.info('Found serviceName ' + srvc + ' in cognito user')
                if (srvc != builtins.service):
                    estr = 'Error. Service mismatch. cognito says service is '\
                            + str(srvc) + ', while user wants ' + str(builtins.service)
                    builtins.log.info(estr)
                    raise Exception('login', estr)
                break
    if (builtins.service == None):
        builtins.log.error('Could not determine service')
        raise Exception('login', 'Could not determine service')

    setup_token_for_mlflow()

    payload = ("ProductCode=" + builtins.prodcode)
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': builtins.accesstoken,
            'Idtoken': builtins.idToken
            }

    url = 'https://' + builtins.apiserver + '/customerinfo'

    try:
        response = requests.post(url, data=payload+'&clientType=browser', headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        builtins.log.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        builtins.log.error(f'Other error occurred: {err}')
        raise
    else:
        builtins.log.info('customerinfo success!')
        return response.json()

def setup_token_for_mlflow():
    home = expanduser("~")
    if (home[len(home) - 1] == '/'):
        dotinfinstor = home + ".infinstor"
    else:
        dotinfinstor = home + separator + ".infinstor"
    builtins.log.info("Setting up token for mlflow in " + dotinfinstor)
    if (not os.path.exists(dotinfinstor)):
        try:
            os.mkdir(dotinfinstor, mode=0o755)
        except Exception as err:
            builtins.log.error('Error creating dir ' + dotinfinstor)
    tokfile = dotinfinstor + separator + "token"
    with open(tokfile, 'w') as wfile:
        wfile.write("Token=" + builtins.accesstoken + "\n")
        wfile.write("RefreshToken=" + builtins.refreshtoken + "\n")
        wfile.write("ClientId=" + builtins.clientid + "\n")
        wfile.write("TokenTimeEpochSeconds=" + str(int(time.time())) + "\n")
        wfile.write("Service=" + builtins.service + "\n")
        wfile.write("IdToken=" + builtins.idToken + "\n")
        wfile.close()

def check_for_custom_token():
    home = expanduser("~")
    if (home[len(home) - 1] == '/'):
        dotinfinstor = home + ".infinstor"
    else:
        dotinfinstor = home + separator + ".infinstor"
    builtins.log.info("Checking for custom token in " + dotinfinstor)
    if (not os.path.exists(dotinfinstor)):
        builtins.log.info('check_for_custom_token: dir ' + str(dotinfinstor)
                + ' does not exist. No custom token')
        return False
    tokfile = dotinfinstor + separator + "token"
    if (not os.path.exists(tokfile)):
        builtins.log.info('check_for_custom_token: file ' + str(tokfile)
                + ' does not exist. No custom token')
        return False
    ftoken, frefresh_token, ftoken_time, fclient_id, fservice, fidtoken = read_token_file(tokfile)
    if (ftoken and ftoken.startswith('Custom ')):
        builtins.accesstoken = ftoken
        builtins.service = fservice
        builtins.idToken = fidtoken
        builtins.log.info('check_for_custom_token: success. found custom token')
        return True
    else:
        return False

def get_customerinfo():
    payload = ("ProductCode=" + builtins.prodcode)
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': builtins.accesstoken,
            'Idtoken': builtins.idToken
            }

    url = 'https://' + builtins.apiserver + '/customerinfo'

    try:
        response = requests.post(url, data=payload+'&clientType=browser', headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        builtins.log.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        builtins.log.error(f'Other error occurred: {err}')
        raise
    else:
        builtins.log.info('customerinfo success!')
        return response.json()

