# coding=utf8
# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> Configuration class handles Cognicept configuration

from dotenv import dotenv_values
from pathlib import Path
from Crypto.PublicKey import RSA
import subprocess
import os
import re
import jwt
import requests
import getpass


class Configuration:
    """
    A class to manage agent and Cognicept's configuration
    ...

    Parameters
    ----------
    None

    Methods
    -------    
    load_config(path):
        Loads and parses `runtime.env` file into `object.config` located at `path`.
    configure(args):
        Manages cognicept configuration based on values in `args`.
    save_config():
        Saves configuration into `runtime.env` file.
    get_cognicept_credentials():
        Checks and returns `COGNICEPT_ACCESS_KEY` from configuration.
    get_cognicept_api_uri():
        Checks and returns `COGNICEPT_API_URI` from configuration.
    get_cognicept_user_api_uri():
        Checks and returns `COGNICEPT_USER_APT_URI` from configuration.
    get_field():
        Returns single config value
    configure_ssh():
        Function to setup ssh access for the host machine given user input.
    is_ssh_enabled(args):
        Checks and returns value of `COG_ENABLE_SSH_KEY_AUTH` as bool.
    is_audio_enabled(args):
        Checks and returns value of `COG_ENABLE_AUDIO` as bool
    cognicept_key_rotate:
        Rotates AWS temporary keys retriving them from Cognicept API.
    init_config(args):
        Initiates runtime.env file with values from Cognicept API
    """
    config_path = os.path.expanduser("~/.cognicept/")
    env_path = config_path + "runtime.env"
    _regex_key = r"^([_A-Z0-9]+)$"
    _config_loaded = False

    def load_config(object, path):
        """
        Loads and parses `runtime.env` file into `object.config` located at `path`.

                Parameters:
                        path (str): Cognicept path, e.g. `~/.cognicept/`.                
        """
        object.config_path = os.path.expanduser(path)
        object.env_path = object.config_path + "runtime.env"
        file = Path(object.env_path)

        if ((not file.exists()) or (file.is_dir())):
            print("Configuration file `" + object.env_path + "` does not exist.")
            try:
                with open(object.env_path, 'w') as f:
                    pass
            except:
                print("Failed to initialize the robot: insufficient priviledges to create `/home/username/.cognicept/runtime.env file.")
                return False

        #object.config = dotenv_values(dotenv_path=file.name) if sys.version_info.minor > 5 else dotenv_values(dotenv_path=find_dotenv(), verbose=True)
        object.config = dotenv_values(
            dotenv_path=object.env_path, verbose=True)
        if(len(object.config) == 0):
            print("Configuration file `" + object.env_path +
                  "` is empty or could not be parsed.")
            return False
        object._config_loaded = True
        return True

    def configure(object, args):
        """
        Manages cognicept configuration based on values in `args`:
            * If `args.read` is True, then it prints all configuration,
            * If `args.add` is True, then it will add or modify a single value inputed by user,
            * Otherwise it will iterate through all values and asks for modifications.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`            
        """
        if(args.ssh):
            if object.configure_ssh():
                print(
                    'SSH config done. To apply changes restart agents using `cognicept restart`.')
        elif(args.autocomplete):
            if object.configure_autocomplete():
                print('Autocomplete setup done')
        else:
            if(not object._config_loaded):
                return

            if (not os.access(object.env_path, os.W_OK)):
                print("Error: You don't have writing permissions for `" +
                    object.env_path + "`. Run as `sudo` or change file permissions.")
                return
            if(args.read):
                for key, value in object.config.items():
                    print(key + ': "' + value + '"')
            elif(args.add):
                new_key = ""
                while(new_key == ""):
                    new_key = input("Config name: ")

                    # if empty, exit
                    if(new_key == ""):
                        return
                    # check if matches key specs
                    matches = re.match(object._regex_key, new_key)
                    if matches is None:
                        print(
                            "Error: Key can be uppercase letters, digits, and the '_'. Try again.")
                        new_key = ""

                new_value = ""
                while(new_value == ""):
                    new_value = input("Value: ")
                    if(new_value == ""):
                        return
                    matches = re.match(r"^.*[\"].*$", new_value)
                    if matches is not None:
                        print("Error: Value cannot contain '\"'. Try again.")
                        new_value = ""

                object.config[new_key] = new_value        
            else:
                for key, value in object.config.items():
                    new_value = input(key + "[" + value + "]:")
                    matches = re.match(r"^.*[\"].*$", new_value)
                    if((new_value != "") and (matches == None)):
                        object.config[key] = new_value
            object.save_config()

    def save_config(object):
        """
        Saves configuration into `runtime.env` file

                Parameters:
                    None
        """
        try:
            with open(object.env_path, 'w') as file:
                for key, value in object.config.items():
                    file.write(key + '=' + value + '\n')
        except IOError:
            print("Could not write into `" + object.env_path +
                  "`. Please check write permission or run with `sudo`.")

    def get_cognicept_credentials(object):
        """
        Checks and returns `COGNICEPT_ACCESS_KEY` from configuration.

                Returns:
                    cognicept_access_key (str): value of `COGNICEPT_ACCESS_KEY`
        """
        if "COGNICEPT_ACCESS_KEY" in object.config:
            return object.config["COGNICEPT_ACCESS_KEY"]
        else:
            print('COGNICEPT_ACCESS_KEY missing')

    def get_cognicept_api_uri(object):
        """
        Checks and returns `COGNICEPT_API_URI` from configuration.

                Returns:
                    cognicept_api_uri (str): value of `COGNICEPT_API_URI`, defaults to "https://app.cognicept.systems/api/v1/"
        """
        if "COGNICEPT_API_URI" in object.config:
            return object.config["COGNICEPT_API_URI"]
        else:
            return "https://app.cognicept.systems/api/v1/"

    def get_cognicept_user_api_uri(object):
        """
        Checks and returns `COGNICEPT_USER_API_URI` from configuration.

                Returns:
                    cognicept_user_api_uri (str): value of `COGNICEPT_USER_API_URI`, defaults to "https://app.cognicept.systems/api/v1/"
        """
        if "COGNICEPT_USER_API_URI" in object.config:
            return object.config["COGNICEPT_USER_API_URI"] 
        else:
            return "https://app.cognicept.systems/api/v1/"

    def get_field(object, field_name):
        """
        Returns single config value

                Parameters:
                        field_name (str): name of config field
                Returns:
                        value (str): value
        """
        if field_name in object.config:
            return object.config[field_name]
        else:
            raise KeyError(field_name)

    def _interpret_bool_input(object, input_string):
        """
        Parses user input string bool value 

                Parameters:
                        input_string (str): input value
                Returns:
                        bool_value (bool): True if value is 'Y'
        """
        if(input_string == 'Y'):
            return True
        elif(input_string == 'n'):
            return False
        else:
            return None

    def configure_ssh(object):
        """
        Function to setup ssh access for the host machine given user input

                Parameters:
                        None
                Returns:
                        result (bool): True if some step didn't fail
        """
        print('SSH is used to access the host machine from the isolated docker environment of Cognicept agent.')

        enable_ssh = None
        while(enable_ssh == None):
            enable_ssh = object._interpret_bool_input(
                input("Enable SSH access? (Y/n):"))

        if(not enable_ssh):
            object.config["COG_ENABLE_SSH"] = "False"
            object.config["COG_ENABLE_SSH_KEY_AUTH"] = "False"
            object.config["COG_ENABLE_AUTOMATIC_SSH"] = "False"
            object.save_config()
            return True
        else:
            object.config["COG_ENABLE_SSH"] = "True"

        ssh_authorized_keys_path = os.path.expanduser(
            "~") + "/.ssh/authorized_keys"
        print("\n \nSSH key needs to be used for hosts with disabled password login. "
              "It can also simplify access so you don't need to input the password each time.\n"
              "This process will generate ssh key locally and mount it to the docker container. "
              "The public key is copied to `" + ssh_authorized_keys_path +
              "` to give access.  Root access is needed and you will be prompted for password."
              "The ssh key is neither sent nor stored to the Cognicept server. "
              "If you choose not to, manual password ssh access can be still used.")

        enable_ssh_key = None
        while(enable_ssh_key == None):
            enable_ssh_key = object._interpret_bool_input(
                input("Generate SSH key and give access? (Y/n):"))

        if(not enable_ssh_key):
            object.config["COG_ENABLE_SSH_KEY_AUTH"] = "False"
        else:
            object.config["COG_ENABLE_SSH_KEY_AUTH"] = "True"

        # generate the ssh key and write them in the file
        if object.config["COG_ENABLE_SSH_KEY_AUTH"] == "True":
            cognicet_ssh_directory = object.config_path + "ssh/"
            try:
                if not os.path.exists(cognicet_ssh_directory):
                    os.makedirs(cognicet_ssh_directory)
            except:
                print(
                    "Failed. Don't have privileges to create files/directories within the ssh directory.")
                return False

            # generate the keys
            ssh_key = RSA.generate(2048)
            private_key_path = cognicet_ssh_directory + "id_rsa"
            public_key_path = cognicet_ssh_directory + "id_rsa.pub"
            config_file_path = cognicet_ssh_directory + "config"
            with open(private_key_path, 'wb') as content_file:
                os.chmod(private_key_path, 0o600)
                content_file.write(ssh_key.exportKey('PEM'))
            pub_key = ssh_key.publickey().exportKey('OpenSSH')
            with open(public_key_path, 'wb') as content_file:
                content_file.write(pub_key)
            # add new line at the end of the file
            with open(public_key_path, 'a') as content_file:
                content_file.write("\n")

        default_user = getpass.getuser()
        user_exists = False
        ssh_directory_path = ""

        # retrieve the user name
        user_prompt_number = 0
        while not user_exists:
            user_name = input(
                "Name of the user to access ssh(if empty, defaults to `" + default_user + "`): ")
            if(user_name == ""):
                user_name = default_user
            object.config["COG_SSH_DEFAULT_USER"] = user_name
            
            if(user_name == "root"):
                ssh_directory_path = "/root/.ssh/"
            else:                
                ssh_directory_path = "/home/" + user_name + "/.ssh/"
            if os.path.exists(ssh_directory_path):
                user_exists = True
            else:
                print("User " + user_name +
                      " doesn't seem to exist or openssh server is not installed.")
                user_prompt_number = user_prompt_number + 1
                if(user_prompt_number > 2):
                    print("Failed to find user's openssh configuration directory.")
                    return False

        # copy the keys to authorized_keys file if automatic authentication was enabled
        if object.config["COG_ENABLE_SSH_KEY_AUTH"] == "True":
            authorized_keys_path = ssh_directory_path + "authorized_keys"
            try:
                print('Root access is needed to modify `' +
                      authorized_keys_path + '` and you will be prompted for password.')
                proc = subprocess.call(
                    ['sudo', 'sh', '-c', 'cat ' + public_key_path + ' >> ' + authorized_keys_path])
            except:
                print("Failed! Don't have access to " + authorized_keys_path)
                return

        enable_automatic_ssh = None
        while(enable_automatic_ssh == None):
            enable_automatic_ssh = object._interpret_bool_input(
                input("Enable automatic ssh access? (Y/n):"))

        if(not enable_automatic_ssh):
            object.config["COG_ENABLE_AUTOMATIC_SSH"] = "False"
        else:
            object.config["COG_ENABLE_AUTOMATIC_SSH"] = "True"

        object.save_config()
        return True

    def is_ssh_enabled(object):
        """
        Checks and returns value of `COG_ENABLE_SSH_KEY_AUTH` as bool

                Parameters:
                        None
                Returns:
                        ssh_enabled (bool): True if ssh is enabled
        """
        if(not "COG_ENABLE_SSH_KEY_AUTH" in object.config):
            return False

        return object.config["COG_ENABLE_SSH_KEY_AUTH"]

    def is_audio_enabled(object):
        """
        Checks and returns value of `COG_ENABLE_AUDIO` as bool

                Parameters:
                        None
                Returns:
                        sound enabled (bool): True if sound is enabled
        """
        if(not "COG_ENABLE_AUDIO" in object.config):
            return False

        return object.config["COG_ENABLE_AUDIO"]
    

    def fetch_aws_keys(object):
        """
        Fetch AWS temporary keys retriving them from Cognicept API.

                Parameters:
                        
                Returns:
                        result (json): AWS temporary credentials returned from Cognicept API
        """
        try:
            headers = {
                'Authorization': 'Basic ' + object.get_cognicept_credentials()
            }
            resp = requests.get(object.get_cognicept_api_uri(
            ) + 'aws/assume_role', headers=headers, timeout=5)
            if resp.status_code != 200:
                print('Login error: wrong credentials.')
                return False
            return resp.json()            
        except requests.exceptions.Timeout:
            print("Cognicept REST API error: time out.")
            return False
        except requests.exceptions.TooManyRedirects:
            print("Cognicept REST API error: Wrong endpoint.")
            return False
        except Exception as e:
            print("Cognicept REST API error" + str(e))
            return False
        object.save_config()

        return True

    def cognicept_key_rotate(object, args):
        """
        Rotates AWS temporary keys retriving them from Cognicept API.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        print("Updating cloud credentials.")
        try:
            response = object.fetch_aws_keys()
            if response==False:
                print("Error connecting Cognicept API. Please contact support@cognicept.systems")
                return False
            object.config["AWS_ACCESS_KEY_ID"] = response[
                "AccessKeyId"]
            object.config["AWS_SECRET_ACCESS_KEY"] = response[
                "SecretAccessKey"]
            object.config["AWS_SESSION_TOKEN"] = response[
                "SessionToken"]
            object.config["AWS_TOKEN_EXPIRATION"] = response[
                "Expiration"]
            print("Cloud access keys rotated successfully!")
        except requests.exceptions.Timeout:
            print("Cognicept REST API error: time out.")
            return False
        except requests.exceptions.TooManyRedirects:
            print("Cognicept REST API error: Wrong endpoint.")
            return False
        except Exception as e:
            print("Cognicept REST API error" + str(e))
            raise SystemExit()
        object.save_config()

        return True

    
    def init_config(object, args):
        """
        Initiates runtime.env file with values from Cognicept API.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        result (bool): True if succeeded
        """
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        api_uri = object.get_cognicept_user_api_uri()
        try:
            x = requests.post(api_uri + 'user/login', json={'username': username, 'password': password})
            if 'access_token' not in x.json():
                print('Failed to initialize the robot: Wrong credentials') 
            else:
                auth_key = x.json()["access_token"]
                # check whether whether user activate the 2FA
                decode_json = jwt.decode(auth_key, verify=False, algorithms=["HS256"])

                # False means 2FA Verification is activated by the user
                if decode_json['user_claims']['authorized'] == False:
                    new_key = object.mfa_verfication(api_uri,auth_key)
                    if new_key == auth_key:    
                        print("Failed to initialized robot: Invalid OTP entered 3 times")
                        return False
                    else:
                        auth_key=new_key

                r = requests.get(api_uri + 'spinup/config/' + args.org_id + '/' + args.robot_id, headers={'Authorization': 'Bearer {}'.format(auth_key)})
                j = r.json()
                if j is not None:
                    for key in j:
                        object.config[key] = j[key]
                    object.save_config()
                    print("Successfully initialized configuration for the robot `" + args.robot_id + "`. To start agents run `cognicept start`")
                    return True
                else:
                    print("Failed to initialize the robot: ID `" + args.robot_id + "` in organization `" + args.org_id + "` not found")
                    return False
        except requests.exceptions.Timeout:
            print("Cognicept REST API error: time out.")
            return False
        except requests.exceptions.TooManyRedirects:
            print("Cognicept REST API error: Wrong endpoint.")
            return False
        except Exception as e:
            print("Cognicept REST API error" + str(e))
            raise SystemExit()

    def mfa_verfication(object,api_uri,auth_key):
        otp_trial = 3
        loop = True
        while loop:
            if otp_trial == 0:
                key = auth_key
                loop = False
            else:
                otp = getpass.getpass('OTP from Authenticator: ')
                x = requests.post(api_uri + 'user/mfa/verify', headers={'Authorization': 'Bearer {}'.format(auth_key)}, json={'otp': otp})
                if 'access_token' not in x.json():
                    print('Invalid OTP! Please try again...')
                else:
                    key = x.json()["access_token"]
                    loop = False
            otp_trial -= 1
        return key
             
    def configure_autocomplete(object):
        """

        Function to setup autcomplate functionality
                Parameters:
                        None
                Returns:
                        result (bool): True if some step didn't fail

        """

        enable_autocomplete = None
        while(enable_autocomplete == None):
            enable_autocomplete = object._interpret_bool_input(
                input("Enable Autocomplete? (Y/n):"))
        
        if (not enable_autocomplete):
            print("Autocomplete was not configured")
            return True

        bash_complete_path = "/etc/bash_completion.d/"
        tmp_path = os.path.expanduser("~") + "/.cognicept/"
        
        print("Root access is needed to place bash completition script at `" + bash_complete_path +
              "' you will be prompted for password.")

        allow_root_access = None
        while(allow_root_access == None):
            allow_root_access = object._interpret_bool_input(
            input("Generate script and give access? (Y/n):"))
        subprocess.call(['bash', '-c', 'activate-global-python-argcomplete --dest ' + tmp_path])
        subprocess.call(['sudo', 'bash', '-c', 'mv ' + tmp_path + "python-argcomplete" + " /etc/bash_completion.d/"])
        print("Please restart the terminal.....")
        return True
