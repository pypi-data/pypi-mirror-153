# Project description
Package Version Python Versions License

bc_time is the Binary City (BC) Time Application Programming Interface (API) Software Development Kit (SDK) for Python, that allows Python developers to develop integration with [BC Time](https://time.bcity.me).

bc_time is maintained and published by [Binary City](https://bcity.me).

# Getting started
Assuming that you have a supported version of Python installed, you can first set up your environment with:

$ python venv .venv
...
$ . .venv/bin/activate
Then, you can install bc_time from PyPI with:

$ python pip install bc_time
or install from source with:
~~~
$ git clone git@bitbucket.org:dburger/bc_time_api_sdk.git
$ cd bc_time_api_sdk
$ python pip install -r requirements.txt
$ python pip install -e .
~~~

# Using bc_time
After installing bc_time

Next, set up credentials at:\
$HOME/.bc_time/credentials

~~~
[default]
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
crypt_key = YOUR_CRYPT_KEY
~~~

Then, from a Python interpreter:
~~~
>>> import bc_time
>>> visitors = bc_time.Visitors()
>>> response_data = visitors.get_all_using_pagination(filters={'filter_status' : bc_time.Status.active})
>>> if response_data['status'] == bc_time.RequestStatus.success:
                for visitor in response_data['data']:
                        print(visitor)
~~~

# Available methods

## For objects
* create
* create_many
* update
* update_many
* get_all_using_pagination
* get_one
* get_many

## For membership/group objects
Please note that group objects also has access the the methods as defined for Objects.

* add_visitor_to_group
* remove_visitor_from_group
* get_all_members_using_pagination

All methods will return a Dictionary that - depending on the response - may contain the following keys:
* status
* data

Status IDs can be referenced using the enumerator bc_time.RequestStatus.


# Documentation

Please consult our [BC Time API documentation](https://docs.google.com/document/d/1sI0mUy8-65NuDfVKKBxzJSyY9olkjWp3xmtRnR58Lkg/) for more information.