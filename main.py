'''
실행 스크립트
'''

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from utils.chromaDB_client import get_vectorstore

from prompts.prompt_templates import summary_template, unfair_detect_template
from loaders.html_parser import clean_html

# 환경변수에서 OpenAI API 키 로드
load_dotenv('.env')
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 모델 설정
llm = ChatOpenAI(model="gpt-4o-2024-08-06", api_key=api_key, temperature=0.2,)

vectorstore = get_vectorstore(collection_name="test")

'''
# summary_template에 HTML 원문 바로 전달
clean_text = clean_html(html_data)
prompt_input = summary_template.format(full_clause=clean_text)

# 모델 실행
response = llm.invoke(prompt_input)

# 결과 출력
print("📌 요약 결과:")
print(response)
'''


#기본 QA 사용 코드
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    chain_type="stuff", # 이것도 알아봐야 함
    chain_type_kwargs={"prompt": unfair_detect_template},
    return_source_documents=True
)

# query = html_data
response = qa_chain.invoke({"query": query})
# 응답 출력
print("답변:\n", response["result"])

# 참조 문서 출력
print("\n📄 참조 문서:")
for i, doc in enumerate(response["source_documents"], 1):
    print(f"\n[{i}] {doc.metadata}")
    print(doc.page_content)  # 길면 앞부분만 보여줘도 됨