from datetime import datetime, timezone
from typing import Callable

class DisunityComponent:
    def __init__(
        self,
        name: str,
        coroutine: Callable,
        requires_ack: bool = False,
        requires_ephemeral: bool = False,
        timeout: float = 0.0
    ):
        self.name = name
        self.requires_ack = requires_ack
        self.requires_ephemeral = requires_ephemeral
        self.timeout = timeout if timeout > 0.0 else None
        self.coroutine = coroutine

    async def __call__(self, context):
        if self.timeout is not None:
            if (
                (datetime.now(timezone.utc) - datetime.fromisoformat(context.raw['message']['timestamp'])).total_seconds() > self.timeout
            ):
                if not self.requires_ack:
                    return {"type": 4, "data": {"content": "This component has timed out", "flags": 64}}

        rjson = await self.coroutine(context)
        if type(rjson) == dict:
            return rjson


class DisunityCommand:
    def __init__(
        self, 
        name: str,
        _type: int, 
        coroutine: Callable,
        requires_ack: bool = False,
        requires_ephemeral: bool = False
     ):

        self.name: str = name
        self.type: int = _type
        self.coroutine: Callable = coroutine
        self.requires_ack: bool = requires_ack
        self.requires_ephemeral: bool = requires_ephemeral

    async def __call__(self, context):
        """Invokes the coroutine attached to the command"""
            
        rjson = await self.coroutine(context)
        if type(rjson) == dict:
            return rjson
