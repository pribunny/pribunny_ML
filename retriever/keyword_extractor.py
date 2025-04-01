import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from retriever.custom_retriever import MetadataFilteredRetriever

from langchain_openai import ChatOpenAI
from utils.chromaDB_client import get_vectorstore

# 환경변수에서 OpenAI API 키 로드
load_dotenv('../.env')
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)

# 입력할 개인정보처리방침
query="""
서비스 이용 과정에서 IP 주소, 쿠키, 서비스 이용 기록, 기기정보, 위치정보가 생성되어 수집될 수 있습니다.
또한 이미지 및 음성을 이용한 검색 서비스 등에서 이미지나 음성이 수집될 수 있습니다.

구체적으로 1) 서비스 이용 과정에서 이용자에 관한 정보를 자동화된 방법으로 생성하거나 이용자가 입력한 정보를 저장(수집)하거나, 2) 이용자 기기의 고유한 정보를 원래의 값을 확인하지 못 하도록 안전하게 변환하여 수집합니다. 서비스 이용 과정에서 위치정보가 수집될 수 있으며, 네이버에서 제공하는 위치기반 서비스에 대해서는 '네이버 위치기반서비스 이용약관'에서 자세하게 규정하고 있습니다.
이와 같이 수집된 정보는 개인정보와의 연계 여부 등에 따라 개인정보에 해당할 수 있고, 개인정보에 해당하지 않을 수도 있습니다.
"""

# OpenAI 모델 설정
llm = ChatOpenAI(model="gpt-4o-2024-08-06", api_key=api_key, temperature=0.2,)

# vectorstor
vectorstore = get_vectorstore(collection_name="test")


# 단락에서 keyword 뽑기, 모델은 동일 모델 이용
summary_prompt = PromptTemplate.from_template("""
너는 개인정보 처리방침 문서를 분석하는 법률 전문가야.
아래의 단락에서 핵심 주제를 한 문장으로 요약하고, 
그 문장을 기반으로 법률적으로 의미 있는 대표 키워드 5개를 뽑아줘.
요약한 내용은 출력하지 않아도 돼. 아래 답변 형식에 맞춰서 키워드만 출력해줘.

[답변 형식]
keyword1 keyword2
- 위와 같이 키워드는 공백으로 구분

[단락]
{query}
""")

def extract_keywords(llm, query: str) -> list[str]:
    chain = summary_prompt | llm
    result = chain.invoke({"query": query})
    for line in result.content.splitlines():
        if line.lower().startswith("키워드"):
            return line.split(":", 1)[-1].strip().split()
    return []

def build_metadata_filter(keywords: list[str]) -> dict:
    fields = ["clause", "chapter", "section", "clause_name"]
    return {
        "$or": [{field: {"$in": keywords}} for field in fields]
    }

# 최신 LangChain 방식: prompt | llm
summary_chain = summary_prompt | llm

result = summary_chain.invoke({"query": query})
keywords = result.content.split(":", 1)[-1].strip() # 공백으로 구분해서 키워드 파싱
keywords = keywords.split(' ')
print(keywords)

filter_query = build_metadata_filter(keywords)

retriever = MetadataFilteredRetriever(vectorstore=vectorstore, metadata_filter=filter_query, k=5)
docs = retriever.get_relevant_documents(query)
# 5. 결과 출력
print(f"\n🔍 관련 조항 {len(docs)}개 찾음:")
for i, doc in enumerate(docs, 1):
    print(f"[{i}] {doc.metadata.get('clause_name')}")
    print(doc.page_content[:300])
    print("-" * 40)
