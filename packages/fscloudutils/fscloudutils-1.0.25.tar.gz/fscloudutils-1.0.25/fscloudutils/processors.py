import json
import boto3
import logging
import warnings
import os
from fscloudutils.chatbot import SlackMessanger
from fscloudutils.chatbot import EmailMessanger
from fscloudutils.data_validation import InputValidator

from botocore.exceptions import ClientError
from botocore.client import Config


class TaskProcessor:
    def __init__(self, region_name: str, bucket_name: str, service_name: str, queue_name: str, local: str = False) -> None:
        """

        :param region_name:
        :param bucket_name:
        :param service_name:
        :param queue_name:
        :param local:
        """
        self._local = local
        self._session = boto3.session.Session(region_name=region_name)
        self._s3_client = self._session.client('s3', config=Config(signature_version='s3v4'))
        self._s3_resource = self._session.resource('s3')
        self._lambda_client = self._session.client('lambda')
        self._sqs_client = self._session.client('sqs')
        self._ec2_client = self._session.client('ec2')
        self._bucket_name = bucket_name
        self._service_name = service_name
        self._queue_name = queue_name

    def __pull_task__(self, path: str = None) -> dict:
        """

        :param path: path to local metadata.json file
        :return: metadata as python dictionary object
        """
        # pull message from aws queue
        if path is None:
            response = self._sqs_client.receive_message(QueueUrl=self._queue_name,
                                                        AttributeNames=[
                                                            'All'
                                                        ],
                                                        MaxNumberOfMessages=1,
                                                        MessageAttributeNames=[
                                                            'All'
                                                        ],
                                                        VisibilityTimeout=43199,
                                                        WaitTimeSeconds=0
                                                        )
            try:
                message = response['Messages'][0]
                receipt_handle = message['ReceiptHandle']
                data = json.loads(message['Body'])
            except KeyError as ke:
                logging.error('KeyError: no files to pull from queue')
                print('KeyError: no files to pull from queue')
        # pull metadata from local resources
        else:
            with open(path, "r") as js:
                data = json.loads(js.read())
        return data

    def __download_data__(self, data: dict) -> None:
        """
        Download all files recursivley for the given file prefix
        :param data: metadata dictionary object
        :return: None
        """
        print(f"[{self._service_name}] Downloading files from S3...")
        paginator = self._s3_client.get_paginator('list_objects')
        for result in paginator.paginate(Bucket=self._bucket_name, Delimiter='/', Prefix=data["s3 path"]):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    self.__download_data__(data)
            for file in result.get('Contents', []):
                dest_pathname = os.path.join(settings.download_path, file.get('Key'))
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                try:
                    # progress = ProgressPercentage(resource.meta.client, bucket, file.get('Key'))
                    # resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname, Callback=progress)
                    self._s3_resource.meta.client.download_file(self._bucket_name, file.get('Key'), dest_pathname)
                except Exception as e:
                    print(f"[ERROR] file {file.get('key')} failed to download from S3...")

    def __input_validation__(self, data: dict, localpath: str, universal_model_input_requirement: list) -> None:
        """
        Validates input manifest for the given block
        :param data: metadata dictionary object
        :param localpath: path to local directory
        :param universal_model_input_requirement:
        :return:
        """
        validator = InputValidator(data, localpath, universal_model_input_requirement)
        validator.run_validation()

    def __prepare_data__(self) -> None:
        """

        :return:
        """
        pass

    def __execute_task__(self) -> None:
        """

        :return:
        """
        pass

    def __upload_data__(self) -> None:
        """

        :return:
        """
        pass

    def __notify__(self, slack_message: str = None, email_message: str = None) -> None:
        """
        Send message via Email/Slack and push metadata to queue
        :param slack_message:
        :param email_message:
        :return:
        """
        pass

