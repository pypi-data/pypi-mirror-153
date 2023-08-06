# coding=utf8
# Copyright 2020 Cognicept Systems
# Author: Swarooph Seshadri (swarooph@cognicept.systems)
# --> Pusher class handles pushing stuff to the Cognicept cloud

import os
import sys
import time
import glob
import requests
import datetime
import threading
import ntpath
import boto3
from boto3.s3.transfer import TransferConfig
from cogniceptshell.common import bcolors


class ProgressPercentage(object):
    """
    A class to track upload progress for chunks uploaded to S3
    ...

    Parameters
    ----------
    _filename (str): Name of the file that is being uploaded
    _size (float): Size of the file being uploaded
    _seen_so_far (float): Size of the file already uploaded
    _lock (threading.lock): Thread lock object for upload context

    Methods
    -------
    __init__(filename):
        Constructor for ProgressPercentage class that initializes all the parameters.
    __call__(bytes_amount):
        Main method to print progress percentage of file being uploaded.
    """

    def __init__(self, filename):
        """
        Constructor for ProgressPercentage class that initializes all the parameters.

                Parameters:
                        filename: Name of the file that is being uploaded
        """
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """
        Main method to print progress percentage of file being uploaded.

                Parameters:
                        bytes_amount: Size of the file already uploaded
        """
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class Pusher:
    """
    A class to manage Cognicept's file pushes to the Cognicept cloud
    ...

    Parameters
    ----------
    bucket_name (str): Name of the S3 bucket to upload to

    Methods
    -------
    __init__():
        Constructor for Pusher class that initializes all the parameters.
    push(args):
        Main entry point for the push operation.
        Checks arguments and if valid, calls other methods to construct client and push the file.
    construct_client(config_obj):
        Creates an S3 client for temporary credentials fetched by key rotate operation.
        Uses an instance of Configuration class.
    push_bag(args):
        Pushes bag to S3 and posts bag metadata to Cognicept cloud.
    get_latest_bag(args):
        Utility method to get the latest '.bag' file.
    check_bag_exists(bag_file_path):
        Utility method to check if specified bag file exists.
    upload_s3(bag_file_path, config_obj):
        Uploads specified bag file to configured S3 bucket.
        Has built in retry mechanism  in case upload fails.
    post_bag_metadata(bag_file_path):
        Posts bag metadata to the Cognicept Cloud using Cognicept API.
    """
    def __init__(self):
        """
        Constructor for Pusher class that initializes all the parameters.

                Parameters:
                        bucket_name: Name of the S3 bucket to upload to
        """
        self.bucket_name = 'cognicept-bagfiles'

    def push(self, args):
        """
        Main entry point for the push operation.
        Checks arguments and if valid, calls other methods to construct client and push the file.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        if args.bag:
            # Construct client
            self.construct_client(args.config)
            # Push bag
            self.push_bag(args)
        else:
            # start or stop must be provided
            print(
                bcolors.FAIL + "Required command is missing." + bcolors.ENDC)

    def construct_client(self, config_obj):
        """
        Creates an S3 client for temporary credentials fetched by key rotate operation.

                Parameters:
                        config_obj: An instance of Configuration class.
        """
        rotate_status = config_obj.cognicept_key_rotate(None)

        if rotate_status:
            local_cfg = config_obj.config
            self.s3_client = boto3.client(
                's3', region_name='ap-southeast-1',
                aws_access_key_id=local_cfg['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=local_cfg['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=local_cfg['AWS_SESSION_TOKEN'])
        else:
            raise(SystemExit)

    def push_bag(self, args):
        """
        Pushes bag to S3 and posts bag metadata to Cognicept cloud.
        If `args.bag` is set to `latest`, automatically finds the latest file to upload.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        upload_status = False
        if args.bag == 'latest':
            bag_file_path = self.get_latest_bag(args)
            print(
                bcolors.OKBLUE +
                "Uploading latest bag file to S3: " +
                bcolors.ENDC + bag_file_path)
            upload_status = self.upload_s3(bag_file_path, args.config)
        elif args.bag.endswith('.bag'):
            bag_file_path = os.path.expanduser(args.path+"bags/"+args.bag)
            if(self.check_bag_exists(bag_file_path)):
                print(
                    bcolors.OKBLUE +
                    "Uploading bag file to S3: " +
                    bcolors.ENDC + bag_file_path)
                upload_status = self.upload_s3(bag_file_path, args.config)
            else:
                print(
                    bcolors.FAIL +
                    "Specified bag file not found in expected location: " +
                    bcolors.ENDC + bag_file_path)
        else:
            print(
                bcolors.FAIL + "Only .bag files can be uploaded." + bcolors.ENDC)

        if upload_status:
            print(bcolors.OKGREEN + "\nBag file uploaded." + bcolors.ENDC)
            self.post_bag_metadata(args, bag_file_path)
        else:
            pass

    def get_latest_bag(self, args):
        """
        Utility method to get the latest '.bag' file. 
        If no file is found, exits program.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        latest_file (string): Full path of the latest bag file
        """
        bag_path = os.path.expanduser(args.path+"bags")
        bag_list = glob.glob(bag_path+"/*.bag")
        if bag_list:
            latest_file = max(bag_list, key=os.path.getctime)
            return latest_file
        else:
            print(
                bcolors.FAIL + "No bags found in the expected path." + bcolors.ENDC)
            raise(SystemExit)

    def check_bag_exists(self, bag_file_path):
        """
        Utility method to check if specified bag file exists.

                Parameters:
                        bag_file_path: Full path of the bag file to check
                Returns:
                        exist_status (boolean): True if specified bag file exists
        """
        if (os.path.exists(bag_file_path)):
            return True
        else:
            return False

    def upload_s3(self, bag_file_path, config_obj):
        """
        Uploads specified bag file to configured S3 bucket.
        Has built in retry mechanism  in case upload fails.

                Parameters:
                        bag_file_path: Full path of the bag file to upload
                        config_obj: An instance of Configuration class
                Returns:
                        upload_status (boolean): True if bag file is uploaded successfully
        """
        # Multipart threaded approach for larger files
        config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10,
                                multipart_chunksize=1024*25, use_threads=True)
        num_retries = 3

        for trial in range(num_retries):
            try:
                # Upload file
                file_name = ntpath.basename(bag_file_path)
                self.s3_client.upload_file(bag_file_path, self.bucket_name, file_name,
                                           Config=config, Callback=ProgressPercentage(bag_file_path))
                # Return true for successful upload
                return True
            except boto3.exceptions.S3UploadFailedError:
                # On failure, retry
                print('Attempt #' + str(trial+1) + bcolors.FAIL +
                      " FAILED" + bcolors.ENDC + "\033[K")
                # Wait for 1 second before retrying
                time.sleep(1.0)
        # If the loop is completed, upload failed, so return false
        return False

    def post_bag_metadata(self, args, bag_file_path):
        """
        Posts bag metadata to the Cognicept Cloud using Cognicept API.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                        bag_file_path: Full path of the bag file to upload
                Returns:
                        resp_status (boolean): True if metadata posted successfully
        """
        payload = {
            "robot_id": args.config.get_field("ROBOT_CODE"),
            "bagfile_name": ntpath.basename(bag_file_path),
            "bagfile_url": ntpath.basename(bag_file_path),
            "bagfile_size": str(os.path.getsize(bag_file_path)),
            "uploaded_at": datetime.datetime.now().isoformat()
        }

        # retrieve cognicept access key
        try:
            token = args.config.get_field("COGNICEPT_ACCESS_KEY")
        except KeyError:
            print(bcolors.FAIL +
                  'COGNICEPT_ACCESS_KEY variable undefined in configuration. Could not update Cognicept cloud with bag metadata.' +
                  bcolors.ENDC)
            raise(SystemExit)

        headers = {"Authorization": "Basic " + token}

        try:
            resp = requests.post(args.config.get_cognicept_api_uri(
            ) + "bagfile", headers=headers, json=payload, timeout=5)

            if resp.status_code != 200:
                print(
                    'Cognicept REST API error: ' +
                    args.config.get_cognicept_api_uri() +
                    ' responded with ' + str(resp.status_code) +
                    '\n' + resp.json()['Message'])
                return False
            else:
                print(
                    bcolors.OKGREEN +
                    "Metadata posted to Cognicept Cloud." +
                    bcolors.ENDC)
                return True
        except requests.exceptions.Timeout:
            print("Cognicept REST API error: time out.")
            return False
        except requests.exceptions.TooManyRedirects:
            print("Cognicept REST API error: Wrong endpoint.")
            return False
        except Exception as ex:
            print("Cognicept REST API error, " + str(ex))
            return False
