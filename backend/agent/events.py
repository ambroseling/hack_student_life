from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context,
)
from llama_index.core.tools import ToolSelection, ToolOutput
from llama_index.core.workflow import draw_all_possible_flows
from llama_index.utils.workflow import draw_most_recent_execution
from llama_index.llms.openai import OpenAI
from types import CampusEvent

class FailedEvent(Event):
    error: str

class QueryEvent(Event):
    query: str

class AnswerEvent(Event):
    answer: str

class WriteEvent(Event):
    data: CampusEvent

class ReadEvent(Event):
    data: CampusEvent

class ToolCallEvent(Event):
    tool_calls: list[ToolSelection]

class FunctionOutputEvent(Event):
    function_outputs: list[ToolOutput]

class PrepEvent(Event):
    pass
