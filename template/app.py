"""ACT component."""

from act_sdk import component, tool
from act_sdk.wit_entry import ToolProvider  # noqa: F401 — componentize-py export


@component
class Component:
    @tool(description="Say hello", read_only=True)
    async def hello(self, name: str = "world") -> str:
        return f"Hello, {name}!"
