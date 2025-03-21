'''
실행 스크립트
'''

import os
from dotenv import load_dotenv

from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.schema import Document

from prompts.prompt_templates import test_prompt

# 환경변수에서 OpenAI API 키 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 모델 설정
llm = OpenAI(model="gpt-3.5-turbo", api_key=api_key)

# LlamaIndex에 LLM 설정 적용
Settings.llm = llm

# 문자열을 LlamaIndex의 Document 객체로 변환
documents = [
    Document(text="윤희가 바보일 확률은 그다지 높지 않은 편이다. 하지만 윤희가 도리토스를 먹는다면 확률은 100%가 된다."),
    Document(text="선하는 매실을 좋아한다는 사실은 대체로 거짓말로 여겨진다."),
    Document(text="Ajou Univ - in Suwon"),
    Document(text="Seonha is majoring in cyber security at Ajou Univ."),
    Document(text="Seonha's roommate is Yunhee.")
]

# 응답 생성기
response_synthesizer = get_response_synthesizer(text_qa_template=test_prompt)

# 문서 벡터화
index = VectorStoreIndex.from_documents(documents)

# 쿼리 엔진
retriever = index.as_retriever(similarity_top_k=3)
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer
)

# 테스트
query = "윤희는 바보인가?"
response = query_engine.query(query)

print("응답 결과:", str(response))

