# Breaking Version Changes

## 11.0.0

* `prep_upgrade()` was removed.

## 10.0.1

Deprecation warning: `prep_upgrade()` is deprecated and will be removed in 11.0.0.

## 10.0.0

### Testcases:

* The `MockEvent.wait_for_call` method now requires arguments to be named explicitly
* The `openmodule_test.io` module was renamed to `openmodule_test.io_simulator`

### Presence Listener:

Event constraints (changed slightly to previous versions):

* For every enter a leave is sent. The vehicle_id of enter and leave always matches!
* There is never a vehicle is present on enter and backward (ensured by faking leave in case there is a lingering
  vehicle)

There are no further constraints, especially there might be no forward/backward for a vehicle!  
Therefore you must not rely on forward/backward to free up memory, instead use leave for cleanup! If you need some data
until forward/backward, you have to cleanup this data even if no forward/backward occurs. Also keep in mind that another
enter and even leave events might happen before the forward/backward of the last vehicle.

### Privacy

* session_id in AnonymizeMessage is now optional

## 9.0.0

This version refactored the RPC client, especially asynchronous retrieval of rpc results. See
the [RPC Documentation](./rpc.md) for more information about asynchronous rpc calls and the RPC Client. Critically the
common issue of "cannot do RPC's while inside an RPC handler" has been solved by creating a dedicated thread for the rpc
client and some future openmodule core internals which should not be blocked by badly behaving user code anyways.

* the `RPCClient.check_results()` function was removed, and is replaced by a `.result()`.
* The RPCClient together with the HealthHandler how has a dedicated thread in the open module core. It is discouraged to
  create an rpc client of your own. Please use the rpc client of openmodule core. A deprecation warning hints this also.

Also some things have been deprecated and will be removed

* the RPC Server no longer requires a config object to be passed. It takes the global openmodule settings instead.
* the RPC Client now warns if a `OpenModuleCore` is passed to it's constructor
* the RPC Client now warns if a dictionary is used for RPC requests
* MockEvent's `reset_call_count()` and `reset_all_call_counts()` was replaced by analog `reset_mock()`
  and `reset_all_mocks()`

Furthermore, fields were renamed in python (with aliases, so the serialized version stays the same):

* `Backend -> AccessRequest: id -> medium_id`
* `Backend -> MediumAccesses: id -> medium_id, type -> medium_type`
* `Backend -> CountMessage: id -> medium_id`
* `Backend -> CountMessage: previous_id ->  previous_medium_id`

In the backend test utils the `create_access_request()` method was removed.

The default value for `match_type` in `MessageDispatcher.register_handler` is now `True`.

The `api` class, aswell as the test utils were removed from the framework. You can still find it
in [docs/deprecated_code/api](./deprecated_code/README.md) if you used it in your service.

## 8.1.1

This version includes breaking changes for testcases only.

* The main test mixin was refactored and `exception_in_function` was removed.

## 8.0.0

* Drops support for python 3.7

## 7.0.0

* Removed all support for direct config changes in all test classes. Now everything is controlled by the lazy settings.

## 6.1.6

* Removed redis_kv from Version 6.1.5

## 6.1.2

* Please add the following snippet to your `tox.ini`, before `[testenv:clean]`.
  ```
  [testenv:openmodule_test]
  deps =
  skip_install = true
  changedir = {toxinidir}/src
  whitelist_externals = bash
  commands = bash -c 'if grep -ri "openmodule_test" . ; then echo ; echo "You must not import openmodule_test inside the openmodule project!" ; echo ; exit 1; else exit 0 ; fi'
  ```
* SETTINGS_MODULE now needs a module instead of a path

## 6.1.0

* The new lazy settings need a `src/config.py` file or you need to set the `SETTINGS_MODULE` environment variable to a
  module

## 6.0.0

* All `OpenModuleModel` fields of type `datetime` require a timezone validator which is checked during testing /
  debugging. After this version **all datetime objects should be timezone naive**.
* All sqlalchemy database models disallow the use of `DateTime` and require the use of `TZDateTime`. This preemptively
  avoids bugs, because sqlalchemy with sqlite looses timezone information.
* `models.backend.Access` now uses timezone naive datetimes instead of timezone aware datetimes. The `is_valid` method
  still accepts both.
* in MessageDispatcher `raise_validation_errors` and `raise_handler_errors` are now required to be named arguments
* `MockEvent.wait_for_call()` now raises a Timeout error instead of an assertion error

## 5.0.0

* AlertHandler.send() and get_or_add_alert_id() were refactored:
    * `source` is now a keyword argument, with default value `""`
    * most arguments are forced to keyword arguments

## 4.0.0

* the Category Enum was renamed to AccessCategory
* all member variables of Category/AccessCategory are lowercased
* the Medium Enum was renamed to MediumType
* all member variables of Medium/MediumType are lowercased
* the default database folder changed to a mounted volume

## 3.0.0

* the registration of bases for the database changed from `register_bases([...])` to `run_env_py([...])`

## 2.0.0

* Pydantic models are now defined in a model folder
