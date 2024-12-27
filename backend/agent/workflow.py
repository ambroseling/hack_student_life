import os
from typing import Any, List
from llama_index.core.agent.react import ReActChatFormatter, ReActOutputParser
from llama_index.core.agent.react.types import (
    ActionReasoningStep,
    ObservationReasoningStep,
)
from llama_index.llms.ollama import Ollama
from llama_index.core.llms.llm import LLM
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools.types import BaseTool
from llama_index.core.workflow import (
    Context,
    Workflow,
    StartEvent,
    StopEvent,
    step,
)

class InstagramAgent(Workflow):
    def __init__(self,tools: list[BaseTool],extra_context:str):
        self.llm = Ollama(model="llama3.2", request_timeout=120.0)
        self.memory = ChatMemoryBuffer.from_defaults(llm=self.llm)
        self.tools = tools
    


