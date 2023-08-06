import json
import os
import random
import socket
from typing import Union, Any, List
from dotenv import load_dotenv, find_dotenv

import boto3
from botocore.exceptions import ClientError


class Config:
    def __init__(self,
                 profile_name: str = None,
                 secret_name: str = None,
                 aws_cache: bool = True,
                 aws_secrets: bool = False,
                 region_name: str = 'us-east-1',
                 test_mode: bool = False
                 ):
        """
        Init Function.

        Args:
            region_name: Region where secrets are stored.
            test_mode: If set to true, config service will return mockup values instead of env variables.
        """
        self.profile_name = profile_name
        self.secret_name = secret_name
        self.aws_cache = aws_cache
        self.aws_secrets = aws_secrets
        self.region_name = region_name
        self._test_mode = test_mode
        self.secrets_cache = dict()

        if self.aws_cache:
            self.get_all_secrets()

    def get_secret(self, key_name, error_flag=None, test_response=None, default_value=None, data_type_convert=None, legacy_key_name=None):
        if not self.aws_secrets:
            return self.get_env(key_name, error_flag, test_response, default_value, data_type_convert, legacy_key_name)
        else:
            return self.get_aws_secret(key_name, error_flag, test_response, default_value, data_type_convert,
                                       legacy_key_name)

    def get_aws_secret(self,
                       key_name: str = None,
                       error_flag: bool = None,
                       test_response: Any = None,
                       default_value: Any = None,
                       data_type_convert: Union[str, None] = None,
                       legacy_key_name: str = None) -> Union[None, str, int, list]:
        """
        Checks if an env value is set for the key. Optionally raises an error if value is not set.

        Args:
            key_name: The name of the key within AWS Secrets Manager.

            error_flag: If set to True and the following conditions exist, an error will be raised.
                       Conditions: 1.) The env value was not set, 2.) and the assigned_value is not set.

            test_response: Value to return if in test mode. When test mode is turned on, the value provided will be
                           returned regardless of the value or existence of an env value.  Test mode is set by either
                           passing in `test_mode=True` when instantiating the Config class, or by setting the class
                           parameter `test_mode` to `True`.

            default_value: A value to return if no other values are set. Error flag must be set to False or an error
                           will be raised.

            data_type_convert: Will convert the returned value to either a float, or int type. Allowed values are
                              None (default), 'int', 'float', 'bool', or 'list' (assumes CSV).

            legacy_key_name: Supports a second legacy key. A warning about the legacy key will be given asking the user
                             to update to the new key.

        Returns:
            The value or None if the value is empty.

        """
        # If in test mode, return the test response. A default value will override this.
        if self._test_mode and not default_value:
            return self._convert_value(test_response, data_type_convert)

        # create logic to determine if cache has been set or reach out to AWS
        if self.aws_cache:
            env_value = self.secrets_cache.get(key_name)
        else:
            # Connect to AWS secrets manager through boto3.session.
            session = boto3.session.Session(profile_name=self.profile_name)
            client = session.client(
                service_name='secretsmanager',
                region_name=self.region_name
            )

            # Pick which secret to use. If secret_name not set during init, then look for env file path.
            secret_name = self.secret_name if self.secret_name is not None else self.get_env('SECRET_NAME',
                                                                                             error_flag=True)

            try:
                get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            except ClientError as e:
                raise e

            # Pull specific value for a given key_name.
            env_value = json.loads(get_secret_value_response['SecretString'])[key_name]

        if env_value:
            # If the value is set, simply return it.
            return self._convert_value(env_value, data_type_convert)

        elif default_value:
            if error_flag:
                raise ErrorFlagTrue('The error flag must be set to false if a default value is set.')
            return self._convert_value(default_value, data_type_convert)

        elif error_flag:
            # If the value is not set and error_msg is not None, raise error.
            raise MissingEnviron(key_name)

        # If no error was set, and the value isn't set, return None.
        return None

    def get_all_secrets(self):
        """
        Checks if an env value is set for the key. Optionally raises an error if value is not set.

        Args:
            self.secret_name: The name of the secret within AWS Secrets Manager.

        Returns:
            The value or None if the value is empty.

        """
        # Connect to AWS secrets manager through boto3.session.
        session = boto3.session.Session(profile_name=self.profile_name)
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )

        # Pick which secret to use
        if isinstance(self.secret_name, list):
            for i in self.secret_name:
                try:
                    get_secret_value_response = client.get_secret_value(SecretId=i)
                except ClientError as e:
                    raise e
                # Pull specific value for a given key_name.
                env_values = json.loads(get_secret_value_response['SecretString'])
                self.secrets_cache.update(env_values)
        else:
            try:
                get_secret_value_response = client.get_secret_value(SecretId=self.secret_name)
            except ClientError as e:
                raise e

            # Pull specific value for a given key_name.
            env_values = json.loads(get_secret_value_response['SecretString'])
            self.secrets_cache = env_values

    def get_env(self,
                key_name: str,
                error_flag: bool = None,
                test_response: Any = None,
                default_value: Any = None,
                data_type_convert: Union[str, None] = None,
                legacy_key_name: str = None) -> Union[None, str, int, list]:
        """
        Checks if an env value is set for the key. Optionally raises an error if value is not set.

        Args:
            key_name: The name of the environment variable.

            error_flag: If set to True and the following conditions exist, an error will be raised.
                       Conditions: 1.) The env value was not set, 2.) and the assigned_value is not set.

            test_response: Value to return if in test mode. When test mode is turned on, the value provided will be
                           returned regardless of the value or existence of an env value.  Test mode is set by either
                           passing in `test_mode=True` when instantiating the Config class, or by setting the class
                           parameter `test_mode` to `True`.

            default_value: A value to return if no other values are set. Error flag must be set to False or an error
                           will be raised.

            data_type_convert: Will convert the returned value to either a float, or int type. Allowed values are
                              None (default), 'int', 'float', 'bool', or 'list' (assumes CSV).

            legacy_key_name: Supports a second legacy key. A warning about the legacy key will be given asking the user
                             to update to the new key.

        Returns:
            The value or None if the value is empty.

        """
        load_dotenv(find_dotenv())
        # If in test mode, return the test response. A default value will override this.
        if self._test_mode and not default_value:
            return self._convert_value(test_response, data_type_convert)

        env_value = os.environ.get(key_name)
        if legacy_key_name:
            legacy_env_value = os.environ.get(legacy_key_name)
        else:
            legacy_env_value = None

        if env_value:
            # If the value is set, simply return it.
            return self._convert_value(env_value, data_type_convert)

        elif legacy_env_value:
            print(f'{legacy_key_name} has been deprecated. Please update your env file to use {key_name}')
            return self._convert_value(legacy_env_value, data_type_convert)

        elif default_value:
            if error_flag:
                raise ErrorFlagTrue('The error flag must be set to false if a default value is set.')
            return self._convert_value(default_value, data_type_convert)

        elif error_flag:
            # If the value is not set and error_msg is not None, raise error.
            raise MissingEnviron(key_name)

        # If no error was set, and the value isn't set, return None.
        return None

    @staticmethod
    def _convert_value(value: Any, conversion: Union[str, None]) -> Union[str, int, float, list, None]:
        """
        Converts a value to int or float if specified, otherwise, returns as is.

        Args:
            value: The env variable value.
            conversion: A string specifying the type of conversion. Options are 'int', 'float', or 'list'

        Returns:
            The value either as original, or converted.
        """
        if conversion:
            if conversion == 'int':
                value = int(value)
            elif conversion == 'float':
                value = float(value)
            elif conversion == 'bool':
                if value.lower() == 'true' or value == '1':
                    return True
                elif value.lower() == 'false' or value == '0':
                    return False
            elif conversion == 'list' or conversion == 'list_int' or conversion == 'list_float':
                value = value.split(',')

                if conversion == 'list_int':
                    value = [int(x) for x in value]

                elif conversion == 'list_float':
                    value = [float(x) for x in value]

        return value

    @property
    def ssh_local_bind_port(self) -> int:
        """
        Sets a local bind port.
        In certain circumstances such as multi-processing, multiple SSH connections will need to be made at one time.
        If the LOCAL_BIND_PORT value is set to random a random port number will be selected and validated as not in use.
        Returns:
            An integer to use as the SSH local bind port.
        """
        if self._ssh_local_bind_port is not None:
            return self._ssh_local_bind_port

        port = os.environ.get('LOCAL_BIND_PORT')
        if port == 'random':
            while 1 == 1:
                rand_port = random.randint(5000, 50000)
                if not self.is_port_in_use(rand_port):
                    return rand_port
        elif port:
            return int(port)
        return 5400

    @staticmethod
    def is_port_in_use(port: int):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0


class MissingEnviron(Exception):
    """Raised when a required environment variable is missing"""

    def __init__(self, env_var_name):
        self.env_var_name = env_var_name
        self.message = f'The required environment variable {self.env_var_name} is missing'
        super().__init__(self.message)


class ErrorFlagTrue(Exception):
    pass
