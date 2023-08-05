# Helios OpenTelemetry SDK

This page describes the Helios OpenTelemetry SDK implementation.

### Requirements
Unless otherwise noted, all published artifacts support Python 3.6 or higher.

### Getting started

#### Installing
The SDK package is available on the Python Package Index (PyPI). You can install it via pip with the following commands:

`pip install helios-opentelemetry-sdk`

### Setting the environment

1. Make sure all the required packages are installed in the environment
2. Set the `HS_ACCESS_TOKEN` env variable with your Helios access token (another option is to provide it within the code when calling to the `initialize` function)
3. If you wish to disable the instrumentation set the `HS_DISABLED` env var to `true`

### Manually instrument your code

To fully instrument your code, just import the `initialize` function from the SDK and run it in the beginning of your code

Here is an example of instrumenting a flask server:

```python
import flask
from helios import initialize

hs = initialize(service_name='my_service_name')

app = flask.Flask('my_app')

@app.route('/', methods=['GET'])
def home():
    return "OK"


app.run()
```

The Helios SDK will automatically check all the supported packages, and instrument every package that is installed on the environment

In our example, assuming the `flask` module is installed in the env, it will be instrumented, together with every other supported module that is installed in the env

### Running instrumented test
Once the `helios-opentelemetry-sdk` package is installed, the `hstest` plugin for `pytest` is installed by default.
This plugin is responsible of automatically instrumenting your tests. In order to enable it,
you should first set `HS_ACCESS_TOKEN` env var with your access token, and the `HS_TEST_ENABLED` env var to `true`.


```bash
HS_ACCESS_TOKEN=<YOUR_ACCESS_TOKEN>
HS_TEST_ENABLED=true

# then run pytest as usual
pytest ./tests
```

This command will run all the tests in `./tests` directory using `pytest`, instrumenting all the supported packages that are installed in the environment
____________
## Developing
### Dev Requirements
#### Python and Pip
Make sure you have python version 3 installed, along with pip (under macos, the default python is version 2).
To install Python 3 separately using brew: `brew install python3 pip3`.
#### Dependencies
Install relevant dev dependencies with pip: `pip3 install -r requirements.txt` and `pip3 install -r dev-requirements.txt`

### Working with local SDK
#### Build
To build a local checkout of the SDK: `python3 setup.py sdist bdist_wheel`
#### Install
To install a local build of the SDK: `pip3 install <<FULL_PATH_TO_YOUR_LOCAL_SDK_CHECKOUT>>/dist/helios_opentelemetry_sdk-<<VERSION>>-py3-none-any.whl`
#### Verify
Run `pip3 freeze > my_requirements.txt` to check it was installed correctly and from the local build (would show something like):
```
helios-opentelemetry-sdk @ file:///<<PATH>>/python-sdk/dist/helios_opentelemetry_sdk-<<VERSION>>-py3-none-any.whl
```

### Testing

- install `nox`:

`pip install nox`

- run all tests using the command `nox` from the main directory
- you can list all available tests by running: `nox --list`
- you can run a single test by runnong: `nox --sessions <TEST_NAME>`

Note that if you are using python3.10 you should upgrade `pytest` to `pytest==6.2.5`.

## Releasing
Follow the [releasing instructions](https://github.com/helios/python-sdk/blob/main/RELEASING.md)






