import functools
import json
import os
from textwrap import dedent
from typing import Callable, Any

from openmodule.config import settings


def active(f):
    def wrapper(*args, **kwargs):
        if settings.TESTING:
            return f(*args, **kwargs)
        return None

    return wrapper


class RPCSchema:
    def __init__(self, channel, typ, request, response, handler: Callable[[Any], Any]):
        self.channel = channel if isinstance(channel, str) else channel.decode()
        self.type = str(typ)
        self.request = request.__name__
        self.response = response.__name__
        self.description = dedent(handler.__doc__.strip()) if handler.__doc__ else ""

    def render(self):
        return dict(post=dict(summary=self.description, tags=["RPCs"],
                              requestBody=dict(description=self.request, content={
                                  "application/json": dict(schema={"$ref": f"#/components/schemas/{self.request}"})}),
                              responses={"200": dict(description=self.response, content={
                                  "application/json": dict(
                                      schema={"$ref": f"#/components/schemas/{self.response}"})})}))

    @property
    def key(self):
        return f"/{self.channel}/{self.type}"


class MessageSchema:
    def __init__(self, topic, message_class, handler: Callable[[Any], Any], filter):
        self.topic = topic if isinstance(topic, str) else topic.decode()
        self.message_class = message_class.__name__
        self.filter = filter
        self.handler = handler.__name__
        self.description = dedent(handler.__doc__.strip()) if handler.__doc__ else ""

    def render(self):
        res = dict(put=dict(summary=self.description, tags=["Messages"],
                            requestBody=dict(description=self.message_class, content={
                                "application/json": dict(
                                    schema={"$ref": f"#/components/schemas/{self.message_class}"})})))
        return res

    @property
    def key(self):
        return f"/{self.topic}/{self.handler}"

    def check_new(self, message_list):
        for message in message_list:
            if self.topic == message.topic and self.handler == message.handler and self.filter == message.filter:
                return False
        return True


class SchemaClass:
    """
    Renders a valid OpenApi JSON Schema of rpcs and pydantic models that can be displayed  with Swagger
    """
    rpcs: dict
    models: set
    messages: dict

    def __init__(self):
        self.rpcs = dict()
        self.models = set()
        self.messages = dict()

    @classmethod
    def get_correct_handler(cls, handler, validate) -> Callable[[Any], Any]:
        if isinstance(handler, functools.partial):
            func = handler.func
        else:
            func = handler

        if validate:
            assert func.__doc__, f"You need to describe the message handler {func} with a doc string"
        return func

    @active
    def save_rpc(self, channel, typ, request, response, handler, validate=True):
        self.save_model(request)
        self.save_model(response)

        func = self.get_correct_handler(handler, validate)
        if func:
            schema = RPCSchema(channel, typ, request, response, func)
            self.rpcs[schema.key] = schema

    @active
    def save_model(self, model):
        self.models.add(model)

    @active
    def save_message(self, topic, message_class, handler, filter=None, validate=True):
        self.save_model(message_class)
        func = self.get_correct_handler(handler, validate)
        if func:
            schema = MessageSchema(topic, message_class, func, filter)
            if self.messages.get(schema.key):
                if schema.check_new(self.messages[schema.key]):
                    self.messages[schema.key].append(schema)
            else:
                self.messages[schema.key] = [schema]

    def __str__(self):
        return json.dumps(self.render_schema())

    def clear(self):
        self.rpcs.clear()
        self.models.clear()
        self.messages.clear()

    def render_schema(self):
        res = dict(openapi="3.0.0", info=dict(title="RPC & Message API", version="1.0.0"))
        paths = self.render_rpcs()
        paths.update(self.render_messages())
        if paths:
            res["paths"] = paths
        models = self.render_models()
        if models:
            res["components"] = dict(schemas=models)
        return res

    def render_rpcs(self):
        result = dict()
        for key, value in self.rpcs.items():
            result[key] = value.render()
        return result

    def render_messages(self):
        result = dict()
        for key, messages in self.messages.items():
            if len(messages) > 1:
                for cnt, message in enumerate(messages):
                    result[f"{key} - {cnt + 1}"] = message.render()
            else:
                result[key] = messages[0].render()
        return result

    def render_models(self):
        result = dict()
        for model in self.models:
            model_schema = model.schema().copy()
            definitions = model_schema.pop("definitions", {})
            result[model.__name__] = model_schema
            for key, value in definitions.items():
                result[key] = value
        result = json.loads(json.dumps(result).replace("#/definitions/", "#/components/schemas/"))
        return result

    @active
    def to_file(self, file_name=None):
        if self.models:
            file_name = file_name or os.environ.get("SCHEMA_FILE", "../schemas.json")
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    schema = json.loads(file.read())
                    new_schema = self.render_schema()
                    if schema.get("paths"):
                        schema["paths"].update(new_schema.get("paths", {}))
                    else:
                        schema["paths"] = new_schema.get("paths")
                    if schema.get("components"):
                        schema["components"]["schemas"].update(new_schema.get("components", {}).get("schemas", {}))
                    else:
                        schema["components"] = dict(schemas=new_schema.get("components", {}).get("schemas", {}))

                    schema["components"]["schemas"] = {k: v for k, v in sorted(schema["components"]["schemas"].items(),
                                                                               key=lambda item: item[0])}
                    data = json.dumps(schema)
            else:
                data = str(self)
            with open(file_name, "w") as file:
                file.write(data)


Schema = SchemaClass()
