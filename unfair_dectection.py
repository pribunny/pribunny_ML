import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from nltk.data import retrieve


from utils.chromaDB_client import get_vectorstore

from prompts.prompt_templates import summary_template, unfair_detect_template
from loaders.html_parser import clean_html
from retriever.priority_retriever import PrioritizedLawRetriever


# 환경변수에서 OpenAI API 키 로드
load_dotenv('.env')
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 모델 설정
llm = ChatOpenAI(model="gpt-4o-2024-08-06", api_key=api_key, temperature=0.2,)

vectorstore = get_vectorstore(collection_name="test")

# def unfair_dectection(query: str):
#     #기본 QA 사용 코드
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
#         chain_type="stuff", # 이것도 알아봐야 함
#         chain_type_kwargs={"prompt": unfair_detect_template},
#         return_source_documents=True
#     )

#     response = qa_chain.invoke({"query": query})

#     return response

# # 상위법 우선 순위
# law_priority = [
#     "개인정보보호법",
#     "개인정보보호법 시행령",
#     "표준 개인정보 보호지침",
#     "개인정보보호위원회 개인정보보호지침",
#     "개인정보의 안전성 확보조치 기준"
# ]
#
# # 리트리버 초기화
# #priority_retriever = PrioritizedLawRetriever(vectorstore, law_priority=law_priority)
# # ✅ 올바른 방식
# priority_retriever = PrioritizedLawRetriever(
#     vectorstore,
#     law_priority=law_priority,
#     top_k_per_law=5,
#     final_top_k=5
# )

# query : 독소조항 탐지하고 싶은 내용
def unfair_dectection(query: str):
    # 관련 법령 문서 검색
    # 벡터 검색으로 query와 관련된 상위의 5개 법령 문서 가져옴
    # 가장 연관 높은 문서 1개에서 law, clause, chapter, section 정보 추출 (프롬프트에 삽입)
    docs = vectorstore.as_retriever(search_kwargs={"k": 5}).invoke(query)
    metadata = docs[0].metadata
    chain = unfair_detect_template | llm

    # # ✅ 우선순위 리트리버로 관련 법령 문서 검색
    # #docs = priority_retriever.retrieve(query)
    # docs = priority_retriever.retrieve(query)
    # metadata = docs[0].metadata  # 가장 연관 높은 문서 기준으로 메타데이터 추출
    # chain = unfair_detect_template | llm

    # # 🔁 점수까지 함께 받기
    # results_with_scores = priority_retriever.retrieve_with_scores(query)
    # docs = [doc for doc, _ in results_with_scores]
    # metadata = docs[0].metadata
    # chain = unfair_detect_template | llm

# PromptTemplate에 필요한 모든 필드 전달
    # context: 관련 법량 텍스트 전체(합쳐서 전달), question: 분석 대상 조항
    # 나머지: 프롬프트에서 법 조항 인용에서 사용
    response = chain.invoke({
        "question": query,
        "context": "\n\n".join([doc.page_content for doc in docs]),
        "law": metadata.get("law", ""),
        "chapter": metadata.get("chapter", ""),
        "section": metadata.get("section", ""),
        "clause": metadata.get("clause", "")
    })

# 결과 처리
    # response.content: LLM이 생성한 실제 답변
    # docs: 어떤 법 조항 사용되었는지 출처를 위해 같이 반환
    return {
        "result": response.content,
        "source_documents": docs
        #"source_documents": results_with_scores  # 🔁 점수 포함해 전달
    }

def retriever_test(query: str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs =retriever.invoke(query)

    return docs

query="""
개인정보의 제3자 제공
1. <개인정보처리자명>은 정보주체의 개인정보를 개인정보의 처리 목적에서 명시한 범위 내에서만 처리하며, 정보주체의 동의, 법률의 특별한 규정 등 개인정보 보호법 제17조 및 제18조에 해당하는 경우에만 개인정보를 제3자에게 제공하고 이 외에는 정보주체의 개인정보를 제3자에게 제공하지 않습니다.
2. <개인정보처리자명>은 원활한 서비스 제공을 위해 다음의 경우 정보주체의 동의를 얻어 필요 최소한의 범위로만 제공합니다.
- 제공받는 자: OO업체, 제공 목적: 부가 서비스 제공, 제공항목: 이름, 휴대폰 번호, 생년월일
- 제공받는자 : 상품 판매업체, 제공 목적: 추가 상품 안내, 제공항목 : 이름, 휴대폰 번호

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