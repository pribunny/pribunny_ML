import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from nltk.data import retrieve

from utils.chromaDB_client import get_vectorstore

from prompts.prompt_templates import summary_template, unfair_detect_template
from loaders.html_parser import clean_html

# 환경변수에서 OpenAI API 키 로드
load_dotenv('.env')
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 모델 설정
llm = ChatOpenAI(model="gpt-4o-2024-08-06", api_key=api_key, temperature=0.2,)

vectorstore = get_vectorstore(collection_name="test")

def unfair_dectection(query: str):
    #기본 QA 사용 코드
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type="stuff", # 이것도 알아봐야 함
        chain_type_kwargs={"prompt": unfair_detect_template},
        return_source_documents=True
    )

    response = qa_chain.invoke({"query": query})

    return response

def retriever_test(query: str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs =retriever.invoke(query)

    return docs

query="""
이용자의 개인 정보는 개인정보의 보유기간이 경과된 경우는 종료일로부터 5일 이내에 파기됩니다. 개인정보가 불필요한 것으로 판단되더라도 개인정보의 보유기간이 경과되기 전까지는 개인정보를 파기하지 않습니다.
"""
# response = retriever_test(query)
#
# for i, doc in enumerate(response, 1):
#     print(f"문서 {i} \n {doc.page_content}\n {doc.metadata}\n")

response = unfair_dectection(query)

print(f"Q. {query}")
print(f"A. {response['result']}")
print(f"참고 문서\n")
for doc in response['source_documents']:
    print(doc)