from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler  # 여기가 변경됨
from langchain.schema import LLMResult

class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        print(f"***Prompt to LLM was:***\n{prompts[0]}")
        print("**********")
        
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        print(f"***LLM response***\n{response.generations[0][0].text}")
        print("**********")