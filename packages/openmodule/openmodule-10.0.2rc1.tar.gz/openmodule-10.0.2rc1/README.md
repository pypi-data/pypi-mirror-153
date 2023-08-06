# OpenModule V2

Some additional documentation:

* [Openmodule Core](docs/core.md)
* [RPC Server / Client](docs/rpc.md)

## Changes

Breaking changes are annotated [here](docs/migrations.md).

To quickly check if your service is susceptible to a known issue have a look [here](docs/migrations.md).

## Coding Standard

For ARIVO developers we have defined a simple coding standard [here](docs/coding_standard.md)

## Features

The openmodule package provides a lot of features:

### Settings

The openmodule package uses a global lazy configuration `openmodule.config.settings`. This setting includes some
standard parameters defined in `openmodule.config.GlobalSettings` and parameters from a customizable module. To specify
the module you can call `settings.configure(module)` or you can set the environment variable `SETTINGS_MODULE`. Per
default settings looks for the `config` module (it also looks for the `tests/config` module first for test cases)

#### Models

Inherit from `OpenModuleModel` or in case of ZMQ messages from `ZMQMessage`. Models use
pydantic ([docs](https://pydantic-docs.helpmanual.io/usage/types/)), check openmodule.models.* for some examples (e.g.
PresenceBaseMessage for alias)

### Core

The base of the new openmodule, every package should have exactly one. The core handles various things:

* sentry
* logging
* dsvgo
* messaging
* health
* alerting
* database

``` python
core = init_openmodule(config, **kwargs)
shutdown_openmodule()
```

#### Messaging

##### Receiving messages

The core handles message distribution with a dispatcher. You only need to register your callback.

* **register_schema**: Automatically create a schema for your message handler and its models -> Beware that you need to
  document your handler method

```python
core.messages.register_handler(b"topic", MessageClass, callback, filter={type = "demo"}, register_schema = True)
```

It may also be used together with an event listener to provide further functionality

```python
event_listener = EventListener(log=logger)
core.messages.register_handler(b"topic", MessageClass, event_listener, filter={type = "demo"})
...
event_listener.append(some_function)
```

#### Sending messages

It is even easier to send messages

```python
message = ZMQMessage(name=core.config.NAME, type="demo")
core.publish(message, b"topic")
```

#### Health

Due to the new convention, the health message should only represent if the service is still alive. This is done
automatically by the core. If you need to specify some meta data or errors you can pass your handler to the core or set
it later

```python
def healthy() -> HealthResult:
    if error:
        return health_error("we have an error", meta=dict(error="error"))
    return health_ok(meta=dict(this="is_easy"))


core = init_openmodule(config, health_handler=healthy)
# or
core.health.health_hanlder = healthy
```

#### Alerting

The new core also includes an alert handler.

```python
core.alerts.send(...)
alert_id = core.alerts.get_or_add_alert_id(...)
core.alerts.send_with_alert_id(alert_id, ...)
```

#### Database

The openmodule package now also feature a simple database which can be also specified during the template creation. If
you missed it there, just copy the directory src/database from the template. For more infos see [here](docs/database.md)

### RPCs

A new RPC server/client was implemented. It works like before and also includes better filtering:

* if a channel is provided for a filter, only rpcs of that channel will be subject to that filter
* if a type is provided for a filter, only rpcs of that type will be subject to that filter
* **register_schema**: Automatically create a schema for your rpc and its models -> Beware that you need to document
  your handler method

```python
def handler(request: AccessRequest):
    """
    awesome description
    """


rpc = RPCServer(config=core.config, context=core.context)
rpc_server.add_filter(self._backend_filter, "backend", "auth")
rpc_server.register_handler("backend", "auth", request_class=AccessRequest,
                            response_class=AccessResponse, handler=handler, register_schema=True)
rpc.run()
```

### Utils

#### Api (**DEPRECATED**)



We implemented a very basic Api class you can use for http request and that handles errors and authentication. Either
inherit it or create a class.

```python
api = Api(**kwargs)
try:
    res = api.post("some_url", payload=stuff)
except ApiException as e:
    if e.retry:  # <- makes sense to try again - timeouts or server not available ...
        ...
```

#### Backend

There is also a basic implementation of a backend that provides registration and message passing.

```python
class MyBackend(Backend):
    def check_access(self, request: AccessRequest) -> List[Access]:
        ...

    def check_in(self, message: CountMessage):
        ...

    def check_out(self, message: CountMessage):
        ...
```

#### Charset

Useful functions for character manipulation

#### Connection Status

Helper class that checks the connection status of ogclient to our server:

```python
connection_status = ConnectionStatusListener(core.messages)
connection_status.on_connect.append(some_function)
connection_status.on_disconnect.append(some_function)
```

#### Matching

Useful functions for license plate matching

#### Presence

Helper class for listening to presence messages.

```python
presence_listener = PresenceListener(core.messages)
presence_listener.on_enter.append(some_function)
```

#### Package Reader

Helper class to read settings (env, yml) of specified services. The services are only considered valid and parsed if a revision file for the service exists.
Functions: 
* **installed_services:** Returns a list of installed services, based on prefix
* **load_setting:** Loads the setting of a single service
* **load_with_service_prefix:** Loads the setting of all services starting with the prefix (no or empty prefix means no filter)
* **load_with_hardware_type_prefix:** Load the setting of all services with the given hardware type (i.e. `cam-ip`)
* **load_with_parent_type_prefix:**  Load the setting of all services with the given parent type (i.e. `cam-ip`)

##### Config
* The package reader needs to know the dist folder, where all services are installed. The standard dist folder is `/opt/openmodule/dist2`, but you can:
     * pass different folders to the package reader on creation (highest prio, overwrites other options)
     * overwrite the env variable `DIST_FOLDER`
     * override the settings or context for `DIST_FOLDER`, i.e. override_settings(DIST_FOLDER="/tmp/)
* You need to mount said package folder in `the docker-compose.yml` file so the container using the package reader has access to it 

##### Example
A service wants to sound a confirmation beep whenever a QR code is read. The sound is made by installed commend devices.
To detect all installed commend devices we use the package reader.
```python
reader = PackageReader()
device_by_gate = {x.env.get["GATE"]: x for x in reader.load_with_service_prefix("hw-commend-generic")}
```

##### Local development & testing

For local development and testing you can use the `FakePackageCreator` class to create you project structure. It is able to:
* **Create basic packages**: Define name, env (str=None), yml (str=None)
    * If any value equals `None`, the file will not be created (for test purposes)
* **Create openmodule packages**: Define name, env_kwargs (dict), yml(str=""")
    * NAME variable automatically added
* **Create hardware packages**: Define name, env_kwargs (dict), ip (str), additional_yml_kwargs (dict) and revision (int=1)
    * Network config in yml automatically generated based on ip, can be overwritten by additional_yml_kwargs

##### Example for testing
```python
class SomeTest(TestCase)
    def setUp(self)
        super().setUp()
        self.creator = FakePackageCreator()
        self.creator.clean_dist_folder()
        self.creator.create_service("om_service_test_1", env="NAME=asdf", yml="", revision=2)
        self.creator.create_om_service("om_service_test_1", env="NAME=asdf")
        self.creator.create_hw_service("hw_service_test_1", "NAME=asdf", "1.2.3.4")
```

##### Example for local development

The default location for the dist folder for local development is `dist2`

The structure looks like this:

* project root
    * dist2
        * om-package-test_1
            * revision  
            * env
            * yml
        * hw-package-test_2
            * revision
            * env 
            * yml
            
* The packages only have a single underscore before the instance number
* The revision file needs to be present, but can be empty
* The env file holds env variables in the format `KEY=<value>`, keys should be upper case
* The yml file is simply a yml file. The yml file of hardware services needs to include a standard network config         

You can also create this structure with the help of the `FakePackageCreator`. The best practice is to create a script in a tools directory where you create the necessary packages

```python 
# tools/create_packages.py
try:
    creator = FakePackageCreator()
    creator.create_service("om_service_test_1", env="NAME=asdf", yml="", revision=2)
# already existing packages throw exception
except Exception:
    pass
```


#### Bridged Slave Detection

Some services should behave differently if they are started on a bridged slave device (i.e. prevent double rpc-responses, prevent double code execution).
The function `is_bridged_slave()` is a helper function to detect this. To use this function on the device, you need to mount the dist folder (/opt/openmodule/dist2).
The function returns:
* None: No dist directory, no bridge service installed, multiple bridges installed
* True: `BRIDGED_SLAVE=True` env variable set or a bridge service is installed and it is configured to be a slave bridge.
* False: `BRIDGED_SLAVE=False` env variable set or a bridge service is installed and it is configured to be a master bridge.

##### Config
* The `BRIDGED_SLAVE` slave env variable takes priority. You can set it either with the env variable directly or override it for test cases (@override_settings(BRIDGED_SLAVE=True))
* The slave detection uses the package reader in the background. You can pass the dist folder to the function to alter the PackageReader config (see above)

##### Example 
The DSGVO container takes care of the anonymization. For this it saves links between vehicle_ids and session_ids and forwards requests to anonymize session_ids with the appropriate vehicle_ids.
If we have a bridged installation only the master DSGVO container should perform these tasks. The DSGVO container on slave devices should only anonymize data on its device.
* RPC for anonymization and linking session to vehicle only registered `if is_bridged_slave() is False`

### Anonymization

The openmodule framework uses rpc requests and messages to trigger the anonymization of data.
* **Message:** You can send a AnonymizeMessage (topic: `privacy`). The message includes a session_id and vehicle_ids to delete. 
* **RPC Request:** You can send an AnonymizeRequest with channel=`privacy`, type=`anonymize` to the DSGVO container. This request only includes session_ids.
The DSGVO container will then match vehicle_ids to the session_ids and redistribute the request with the prior mentioned message.

A container with sensible data then needs to implement the message listener for the privacy messages (see example)

##### Example 1
The controller checked that a parking session was finished an fully paid. After a specified time, the DSGVO relevant data has to be anonymized. The controller then triggers the anonymization
```python
request = AnonymizeRequest(session_ids=[session_id])
result = core.rpc_client.rpc("privacy", "anonymize", request)
if result.response.status == "ok":
    self.log.info(f"Anonymized session {session_id}")
```

##### Example 2
The controller checked that a parking session was finished an fully paid. After a specified time, the DSGVO relevant data has to be anonymized. The controller then triggers the anonymization
```python
msg = AnonymizeMessage(vehicle_ids=[vid1, vid2])
self.core.publish(msg, "privacy")
```

The DSGVO container receives the request, matches session_ids with vehicle_ids and publishes the anonymization message. 
It also listens on said messages an deletes vehicle images based on the vehicle_ids in the message.

```python
core.messages.register("privacy", AnonymizeMessage, anonymize_data)

def anonymize_data(message: AnonymizeMessage):
    for vid in message.vehicle_ids:
        delete_vehicle_image_by_vehicle_id(vid)
```


**IMPORTANT** You still have to take care of data retention in each service separately, meaning you have to delete data independently of these anonymization messages.
i.e. the DSGVO service deletes data if we need disk space or the eventlog deletes events after 30 days by default 

## Documentation

Openmodule >= 3.0.5 features automatic generation of Rpc and Message Schemas including their models. The generation uses
data that is generated during the test runs to create an OpenApi Schema. Your RPCs and Message handlers are
automatically documented if:

* You use the message dispatcher of the core (OpenModuleCoreTestMixin)
* You use the RPCServer of Openmodule

You can also register models yourself if you want them documented, but you may need to save the Schema in this case:

```python
from openmodule.utils.schema import Schema

Schema.save_model(Model)
Schema.save_rpc(channel, type, request, reqponse, handler)
Schema.save_message(topic, message_class, handler, filter)

Schema.to_file()
```

With default parameters, you need to document your handler functions with a doc string, that is then included as a
description.

## Testing

A separate package for testing openmodule packages exists within openmodule - openmodule-test. For more infos
see [here](docs/testing.md)
