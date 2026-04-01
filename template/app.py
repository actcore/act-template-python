"""ACT component."""

import traceback

import cbor2
import componentize_py_async_support
import wit_world
from wit_world import exports
from wit_world.imports.types import (
    ContentPart,
    ListToolsResponse,
    LocalizedString_Plain,
    StreamEvent_Content,
    StreamEvent_Error,
    ToolDefinition,
    ToolError,
)

from act_sdk import component, tool
from act_sdk.provider import dispatch_tool, get_tool_definitions


# ── Component ──


@component
class Component:
    @tool(description="Say hello", read_only=True)
    async def hello(self, name: str = "world") -> str:
        return f"Hello, {name}!"


# ── WIT bridge (componentize-py entry point) ──


class ToolProvider(exports.ToolProvider):
    async def get_metadata_schema(self, metadata):
        return None

    async def list_tools(self, metadata):
        defs = get_tool_definitions()
        return ListToolsResponse(
            metadata=[],
            tools=[
                ToolDefinition(
                    name=name,
                    description=LocalizedString_Plain(value=desc),
                    parameters_schema=schema,
                    metadata=meta,
                )
                for name, desc, schema, meta in defs
            ],
        )

    async def call_tool(self, call):
        writer, reader = wit_world.types_stream_event_stream()

        async def produce():
            try:
                result = await dispatch_tool(call.name, bytes(call.arguments))

                if len(result) == 3 and result[2] == "error":
                    kind, message, _ = result
                    await writer.write(
                        [
                            StreamEvent_Error(
                                ToolError(
                                    kind=kind,
                                    message=LocalizedString_Plain(value=message),
                                    metadata=[],
                                )
                            )
                        ]
                    )
                else:
                    data, mime = result
                    await writer.write(
                        [
                            StreamEvent_Content(
                                ContentPart(
                                    data=data,
                                    mime_type=mime,
                                    metadata=[],
                                )
                            )
                        ]
                    )
            except Exception:
                await writer.write(
                    [
                        StreamEvent_Error(
                            ToolError(
                                kind="std:internal",
                                message=LocalizedString_Plain(
                                    value=traceback.format_exc()
                                ),
                                metadata=[],
                            )
                        )
                    ]
                )

        componentize_py_async_support.spawn(produce())
        return reader
