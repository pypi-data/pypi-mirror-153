# Configuration Service Core

The configuration service core provides a lightweight function to assist in the loading of environmental variables. 

## Methods 

The configuration service core has only one public method, `get_env`


Args:

`key_name` - The name of the environment variable.

`error_flag` - If set to True and the env variable was not set, an error will be raised. 

`test_response` - Value to return if in test mode.

`default_value` - A value to return if no other values are set. Error flag must be set to False or an error will be raised.

`data_type_convert` - Will convert the returned value to either a float, or int type. Allowed values are: 
* None (default)
* `int` - Convert response to integer 
* `float` - Converts response to float. 
* `bool`
* `list` (assumes CSV). List can optionally have `list_int` to convert the list elements to int, or `list_float` to convert list elements to float. 
 
`legacy_key_name` - Allows for an alternative env variable name to be set. For example, the main env variable might be set to 
`DB_HOST_NAME`. At some point in the past some systems used `DBHOSTNAME`. This second value can be included under `legacy_key_name`. 
A warning will be printed to the std output indicating that the user should update their `.env` file.

## Examples

### Usage as a parent class

In this method of implementation, the configuration service is inherited as a class. Env variables 
are setup a properties of the class.

    from configservice import Config

   
    class ConfigService(Config):

        def __init__(self, test_mode=False):
            super().__init__(test_mode)

        @property 
        def api_key(self):
            return self.get_env('API_KEY')

### Direct usage 

The package can be used directly to set a variable as well. 

    from configservice import Config

    c = Config()
    api_key = c.get_env('API_KEY')


### Options 

#### Simple get of an environmental variable

The most straight forward implementation simply requires the name of an environmental variable. If no error 
flags are set, and the environmental variable does not exist, the method will return None. 

     api_key = get_env('API_KEY')

#### Raise an error if env is missing. 

By default, if no env value is found for the requested key, the method will return `None`. If 
you would rather raise an error, the `error_flag` parameter can be set to true. If the env variable 
is not set a `MissingEnviron` error will be raised.

    api_key = get_env('API_KEY', error_flag=True)

#### Set a default value 

A default value can be set as a fallback if the requested env variable is not set. 
    
    db_port = get_env('DB_PORT', default_value=5432, data_type_convert='int')

#### Convert the return data type. 

By default, all environmental variables will return as strings. By setting the `data_type_convert` 
parameter you can have the value return as an int, float, bool, or list. List has further options of `list_int` 
and `list_float`.

    db_port = get_env('DB_PORT', data_type_convert='int')

Lists support CSV. For example if the env `STORE_IDS` was `5,2,1,4,5,3` and the option `list_int` is used, the 
system will return [5, 2, 1, 4, 5, 3]

    store_ids = get_env('STORE_IDS', data_type_convert='list_int')

#### Test mode response. 

Test mode can be set by either passing in `test_mode` when instantiating the class, or by setting the class 
parameter `test_mode=True`. Then the `test_response` parameter can be passed in to override any env variable. For 
example:

    from configservice import Config

    c = Config(test_mode=True)
    api_key = c.get_env('API_KEY', test_response='ABC123')

This will return 'ABC123' regardless of if an env variable named `API_KEY` is set. This can be handy for unit 
testing.
    