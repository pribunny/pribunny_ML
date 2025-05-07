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
    docs = vectorstore.as_retriever(search_kwargs={"k": 10}).invoke(query)
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
    law=metadata.get("law", "")
    clause = metadata.get("clause", "")
    law_clause = f"{law} {clause}"

# PromptTemplate에 필요한 모든 필드 전달
    # context: 관련 법량 텍스트 전체(합쳐서 전달), question: 분석 대상 조항
    # 나머지: 프롬프트에서 법 조항 인용에서 사용
    response = chain.invoke({
        "question": query,
        "context": "\n\n".join([doc.page_content for doc in docs]),
        "law": metadata.get("law", ""),
        "chapter": metadata.get("chapter", ""),
        "section": metadata.get("section", ""),
        "clause": metadata.get("clause", ""),
        "law_clause": law_clause
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

개인정보 수집·이용 동의

1. 수집·이용 목적 : 신상품 홍보 및 맞춤형 광고, 타깃 마케팅 제공
2. 수집하는 개인정보의 항목 : 이메일, 휴대전화번호
3. 보유 및 이용기간 : 1년
4. 동의 거부권 및 불이익 : 정보주체는 개인정보 수집·이용에 동의하지 않을 권리가 있으며, 동의를 거부할 경우 신상품 홍보 및 맞춤형 광고, 타깃 마케팅 서비스 이용에 제한을 받을 수 있습니다.

위 개인정보를 수집·이용하는 것에 동의합니다.(선택)
동의함[V]                             동의하지 않음[  ]

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