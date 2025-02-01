from typing import Union, List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser


load_dotenv()



@tool
def get_text_length(text: str) -> int:
    """텍스트의 문자 길이를 반환하는 도구"""
    print(f"get_text_length enter with {text=}")  # 디버깅용 로그
    text = text.strip("'\n").strip('"')  # 따옴표와 줄바꿈 제거
    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    """도구 이름으로 도구 객체를 찾는 헬퍼 함수"""
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")

if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    
    # 1. 도구 설정: AI가 사용할 수 있는 도구들을 정의
    tools = [get_text_length]

    # 2. ReAct 프롬프트 템플릿 정의
    # - AI에게 도구 사용법과 응답 형식을 알려주는 지침서
    # - {tools}: 사용 가능한 도구들의 설명
    # - {tool_names}: 도구들의 이름 목록
    # - {input}: 사용자의 실제 질문이 들어갈 자리
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought:
    """

    # 3. 프롬프트 템플릿 초기화 및 도구 정보 주입
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),  # 도구 설명을 텍스트로 변환
        tool_names=", ".join([t.name for t in tools]),  # 도구 이름들을 문자열로 변환
    )

    # 4. LLM(Language Model) 초기화
    # - temperature=0: 일관된 응답을 위해 무작위성 제거
    # - stop: 이 텍스트가 나오면 응답 생성 중단
    llm = ChatOpenAI(
        temperature=0, 
        stop = ["\nObservation", "Observation"]
    )
    
    # 5. 에이전트 파이프라인 구성
    # - {"input": lambda x: x["input"]}: 입력 데이터 전처리
    # - prompt: 프롬프트 템플릿 적용
    # - llm: AI 모델로 응답 생성
    # - ReActSingleInputOutputParser(): AI 응답을 구조화된 형식으로 파싱
    agent = (
        {"input": lambda x: x["input"]} 
        | prompt 
        | llm 
        | ReActSingleInputOutputParser()
    )

    # 6. 에이전트 실행 및 결과 처리
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {"input": "What is the length of the text 'DOG' in characters?"}
    )
    
    # 7. 도구 실행 결과 처리
    if(isinstance(agent_step, AgentAction)):
        tool_name = agent_step.tool  # 사용할 도구 이름
        tool_to_use = find_tool_by_name(tools, tool_name)  # 도구 객체 찾기
        tool_input = agent_step.tool_input  # 도구에 전달할 입력값
        observation = tool_to_use.func(str(tool_input))  # 도구 실행
        print(f"Observation: {observation}")  # 결과 출력

    # elif(isinstance(agent_step, AgentFinish)):
    #     print(f"Final Answer: {agent_step.return_values['output']}")

    
