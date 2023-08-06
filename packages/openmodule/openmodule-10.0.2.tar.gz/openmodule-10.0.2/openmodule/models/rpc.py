from typing import Optional, Dict, Any
from uuid import UUID

from openmodule.models.base import ZMQMessage, OpenModuleModel


class RPCRequest(ZMQMessage):
    rpc_id: UUID
    resource: Optional[str]
    request: Optional[Dict]


class RPCResponse(ZMQMessage):
    rpc_id: Optional[UUID]
    response: Any


class RPCResult(OpenModuleModel):
    rpc_id: UUID
    status: str = "error"
    error: Optional[str]
    response: Any
