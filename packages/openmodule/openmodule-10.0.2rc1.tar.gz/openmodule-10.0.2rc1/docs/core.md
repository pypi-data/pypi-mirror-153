# OpenModuleCore

The openmodule core provides some utilities.

## RPC Client

The rpc client can be used to call other service's procedures. Please
see [the rpc clients documentation](rpc.md#rpc-client). The client has a dedicated thread and can be used concurrently
and thus there is no need to ever instantiate a rpc client manually.

```python
core.rpc_client.rpc(...)
```

## Message Handler

Since almost any service will listen to some messages, a message handler is provided which can be used for the service.

```python
core.messages.register_handler(b"io", ZMQMessage, handler=io_init_event)
```

By default the message handlers are executed single threaded. If you absolutely have to run your message handlers
multithreaded there is an option to increase the openmodule core's executor threads.

```python
init_openmodule(config, dispatcher_max_threads=5)
```