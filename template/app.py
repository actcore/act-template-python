"""ACT component."""

import json
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
    ToolCall,
    ToolDefinition,
    ToolError,
)

HELLO_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name to greet",
            },
        },
    }
)


class ToolProvider(exports.ToolProvider):
    async def get_metadata_schema(self, metadata):
        return None

    async def list_tools(self, metadata):
        return ListToolsResponse(
            metadata=[],
            tools=[
                ToolDefinition(
                    name="hello",
                    description=LocalizedString_Plain(value="Say hello"),
                    parameters_schema=HELLO_SCHEMA,
                    metadata=[],
                ),
            ],
        )

    async def call_tool(self, call: ToolCall):
        writer, reader = wit_world.types_stream_event_stream()

        async def produce():
            try:
                if call.name != "hello":
                    await writer.write(
                        [
                            StreamEvent_Error(
                                ToolError(
                                    kind="std:not-found",
                                    message=LocalizedString_Plain(
                                        value=f"Unknown tool: {call.name}"
                                    ),
                                    metadata=[],
                                )
                            )
                        ]
                    )
                    return

                args = cbor2.loads(bytes(call.arguments))
                name = args.get("name", "world")

                await writer.write(
                    [
                        StreamEvent_Content(
                            ContentPart(
                                data=f"Hello, {name}!".encode("utf-8"),
                                mime_type="text/plain",
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
