from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate( #기본 형태
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant. Only use the following context to answer the question.\n"
        "Only use the provided context and cite sources if relevant.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    ))

summary_template = PromptTemplate( #문서 내용 요약 - 참고 문서 없는 버전
    input_variables= ["full_clause"], #참고할 문서는 필요X, 요약이 필요한 내용을 받음
    template = (
        #1. 받은 내용 내에서 답을 작성해라.
        #2. 받은 내용을 8개의 범주에 넣어라, 만약 해당되지 않는다면 '기타' 항목에 넣어라.
        #3. 각 범주마다 내용을 요약하라.
        #4. '기타' 항목에 있는 내용들은 내용마다 '소제목'을 넣어 구분하고 요약하라.
        #5. Answer 형태는 다음과 같다.

        "You are a helpful assistant. Answer only based on the given Full_clause.\n\n"
        "If the Full_clause does not contain relevant content for any category, then write \"No contents.\" for that category.\n\n"

        "Your task is to perform the following actions:\n"
        "1 - Categorize the following Full_clause into 8 predefined categories. If something doesn’t fit, put it under '기타(Others)'.\n"
        "2 - Summarize the content for each category (except '기타').\n"
        "3 - For items under '기타', add a subheading for each item and summarize it separately.\n"
        "4 - Output a JSON list. Each element should contain the following keys : category_name, summarize_content\n\n"

        "Use the following format : \n"
        "Output <list of JSON with category_name and summarize_content>\n\n"
        "Category List : \n"
        "<1.개인정보처리 목적\n"
        "2. 처리하는 개인정보의 항목\n"
        "3. 개인정보 처리 및 보유 기간\n"
        "4. 개인정보 파기 절차 및 방법에 관한 사항\n"
        "5. 개인정보의 안전성 확보조치에 관한 사항 \n"
        "6.정보주체와 법정대리인의 권리·의무 및 행사방법에 관한 사항 \n"
        "7. 개인정보 보호 책임자의 성명 또는 개인정보 업무 담당부서 및 고충사항을 처리하는 부서에 관한 사항\n"
        "8. 개인정보 처리방침의 변경에 관한 사항 >\n\n"

        "Full_clause : {full_clause}\n\n"
    )
)

# unfair_detect_template = PromptTemplate( #독소조항 탐지
#     input_variables= ["full_clause", "context"], #참고할 문서, 전체 조항을 받음
#     template = (
#     )
# )
#
# legal_term_template = PromptTemplate( #법률 용어 해석
#     input_variables= [],
#     template = ()
# )
#
# collect_data_template = PromptTemplate( #수집하는 항목 탐지
#     input_variables= ["full_clause"],
#     template = ()
# )
