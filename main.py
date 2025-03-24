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
from nltk.corpus.reader import documents

from loaders.pdf_parser import pdf_to_document

from prompts.prompt_templates import test_prompt

# 환경변수에서 OpenAI API 키 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 모델 설정
llm = OpenAI(model="gpt-3.5-turbo", api_key=api_key)

# LlamaIndex에 LLM 설정 적용
Settings.llm = llm

# LlamaIndex의 Document 객체로 변환
documents = pdf_to_document()

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
query = "개인정보 유출이 발생한 경우 정보 주체에게 알려야 하는 시간을 알려줘."
response = query_engine.query(query)

print("응답 결과:", str(response))

for i, node in enumerate(response.source_nodes):
    print(f"\n--- Source {i+1} ---")
    print(node.node.text[:1000])  # 너무 길면 잘라서 출력
    print(f"[메타데이터] {node.node.text}")

query = "보호법 제30조에 대해 요약해줘."
response = query_engine.query(query)

print("응답 결과", str(response))

for i, node in enumerate(response.source_nodes):
    print(f"\n--- Source {i+1} ---")
    print(node.node.text[:1000])  # 너무 길면 잘라서 출력
    print(f"[메타데이터] {node.node.metadata}")
