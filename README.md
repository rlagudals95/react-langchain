
## **Agent 동작원리**  
![image](https://github.com/user-attachments/assets/25fe53a3-33de-4ffa-b438-7a64b6d14601)  


[사용자 질문] → [에이전트 루프 시작]
         ↑          ↓
         |     1. 생각(Thought)
         |          ↓
         |     2. 행동 선택(Action)
         |          ↓
[최종 답변] ← 3. 도구 실행(Tool Execution)
         ↑          ↓
         |     4. 관찰(Observation)
         |          ↓
         └── 5. 결과 충분? (No → 1로 돌아가기)
                        (Yes → 최종 답변 반환)  


LangChain의 **"Agent"**(에이전트)는 주어진 목표를 달성하기 위해 도구(예: 검색, 계산, API 호출 등)를 활용하여 동적으로 의사결정을 내리는 시스템입니다.

### 🔹 **Agent의 핵심 개념**

1. **Action(행동)**: 입력을 분석한 후, 어떤 도구를 사용할지 결정
2. **Tool(도구)**: 외부 API, DB, 계산기 등 실제 작업을 수행하는 기능
3. **LLM(언어 모델)**: 주어진 문제를 이해하고 적절한 Action을 선택
4. **Prompting(프롬프트)**: LLM이 올바른 결정을 내리도록 가이드

### 🔹 **Agent의 작동 방식**

1. 사용자의 질문을 입력받음
2. LLM이 질문을 분석하고 적절한 도구를 선택
3. 도구를 사용하여 필요한 정보를 얻음
4. 결과를 종합하여 최종 응답을 반환

### 🔹 **Agent의 종류**

- **ReAct (Reason + Act)**: 한 번에 한 단계씩 생각하면서 행동 (반복 루프 가능)
- **Zero-shot ReAct**: 한 번의 프롬프트로 결정
- **Self-ask with Search**: 필요한 경우 검색을 통해 추가 정보를 얻음