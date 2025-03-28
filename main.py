'''
실행 스크립트
'''

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from prompts.prompt_templates import prompt_template
from utils.chromaDB_client import get_chroma_client

# 환경변수에서 OpenAI API 키 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 모델 설정
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key, temperature=0.2,)

vectorstore = get_chroma_client(collection_name="test")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    chain_type="stuff", # 이것도 알아봐야 함
    chain_type_kwargs={"prompt": prompt_template},
    return_source_documents=True
)

query = "개인정보보호법 제30조, 개인정보 처리방침의 수립 및 공개에 대해서 요약, 쉬운 설명 부탁해."
response = qa_chain.invoke({"query": query})


# 응답 출력
print("답변:\n", response["result"])

# 참조 문서 출력
print("\n📄 참조 문서:")
for i, doc in enumerate(response["source_documents"], 1):
    print(f"\n[{i}] {doc.metadata}")
    print(doc.page_content[:500])  # 길면 앞부분만 보여줘도 됨