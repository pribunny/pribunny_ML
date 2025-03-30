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
            # 2. 처리하는 개인정보의 항목 : 수집하는 항목을 포함해서 요약하라. 개인정보를 추가로 수집하는 경우에 대한 내용이 있다면, 그것도 포함하라.
            # 3. 개인정보 처리 및 보유 기간 : 각 항목과 보유 기간을 포함해서 요약하라.
            # 4. 개인정보 파기 절차 및 방법에 관한 사항 : 각 항목과 항목에 대한 파기 절차를 포함해서 요악하라.
            # 5. 개인정보의 안전성 확보조치에 관한 사항 : 안전성 확보를 위해 수행하는 것들을 포함해서 요약하라.
            # 6. 정보주체와 법정대리인의 권리 의무 및 행사방법에 관한 사항 : 행사할 수 있는 권리와 방법에 대해 포함해서 요약하라.
            # 7. 개인정보 보호 책임자의 성명 또는 개인정보 업무 담당부서 및 고충사항을 처리하는 부서에 관한 사항 : 책임자와 담당부서에 대한 정보를 포함해서 요약하라.
            # 8. 개인정보 처리방침 변경에 관한 사항 : 시행일자를 포함해서 요약하라.
        #4. '기타' 항목에 있는 내용들은 내용마다 '소제목'을 넣어 구분하고 요약하라.
        #5. Answer 형태는 다음과 같다.

        "You are a helpful assistant. Answer only based on the given Full_clause.\n\n"
        "If the Full_clause does not contain relevant content for any category, then write \"No contents.\" for that category.\n\n"

        "Your task is to perform the following actions:\n"
        "1 - Categorize the following Full_clause into 8 predefined categories. If something doesn’t fit, classify it under '기타'.\n"
        "2 - Summarize the content for each category (except '기타'). Your summary must extract factual, specific details directly from the text. "
        "Include itemized lists, durations, names, or procedures if they are explicitly written. Do not compress these into vague generalizations. "
        "3 - Follow Category-specific instructions :\n"
        "4 - For any part of the Full_clause that does not match the 8 categories, classify it under '기타'. Do not skip or omit these parts. "
        "For each distinct topic under '기타', create a subheading (e.g., \"이메일 수신 동의\") and provide a specific summary. "
        "Format it like this: \"소제목: <subheading>\\n<summary sentence>\".\n\n"
        "5 - Output a JSON list. Each element should contain the following keys : category_name, summarize_content\n\n"

        "Use the following format : \n"
        "Output <list of JSON with category_name and summarize_content>\n\n"
        "Category List : \n"
        "<1.개인정보처리 목적\n"
        "2. 처리하는 개인정보의 항목\n"
        "3. 개인정보 처리 및 보유 기간\n"
        "4. 개인정보 파기 절차 및 방법에 관한 사항\n"
        "5. 개인정보의 안전성 확보조치에 관한 사항 \n"
        "6. 정보주체와 법정대리인의 권리·의무 및 행사방법에 관한 사항 \n"
        "7. 개인정보 보호 책임자의 성명 또는 개인정보 업무 담당부서 및 고충사항을 처리하는 부서에 관한 사항\n"
        "8. 개인정보 처리방침의 변경에 관한 사항 >\n"
        "9. 기타\n\n"
        
        "Category-specific instructions : \n"
        " 처리하는 개인정보의 항목: Summarize the specific data items being collected (e.g., name, email, phone number). If there is any mention of additional data being collected under certain conditions, include that information as well.\n"
        " 개인정보 처리 및 보유 기간: Include each collected item along with its specific retention period if available.\n"
        " 개인정보 파기 절차 및 방법: Describe how and when each item is deleted, including the deletion procedure.\n"
        " 개인정보의 안전성 확보조치: Include the actual technical, administrative, and physical safeguards being applied.\n"
        " 정보주체와 법정대리인의 권리·의무 및 행사방법: Clearly state the rights of the data subject and how those rights can be exercised.\n"
        " 개인정보 보호 책임자 및 담당 부서: Include the name, position, or contact information of the person or department responsible.\n"
        " 개인정보 처리방침 변경: Include the method of notifying changes to the privacy policy. If an effective date is specified, include that as well.\n\n"

        "Example:\n"
        "{{\n"
        " category_name: 개인정보 처리 및 보유 기간,\n"
        "  summarize_content: 이름과 이메일은 회원 탈퇴 후 5일까지 보관되며, 거래기록은 전자상거래법에 따라 5년간 보관됩니다.\n"
        "}}\n"
        "{{\n"
        "  category_name: 기타,\n"
        "  summarize_content: 소제목: 이메일 수신 동의 n회사는 마케팅 정보를 이메일로 수신하는 데 동의할 수 있는 선택 항목을 제공합니다.\n"
        "}}\n\n"
        
        "Full_clause : {full_clause}\n\n"
    )
)

#QA 방식 -> QA가 아닌 방식에선 question을 다른 변수 명(Full_clause)으로 변경해도 됨
unfair_detect_template = PromptTemplate( #독소조항 탐지
    input_variables= ["context", "question"], #참고할 문서, 전체 조항을 받음
    template = (
        #1. context를 기반으로 full_clause와 맞지 않는 부분이 있는 지 확인
        #2. 만약 존재한다면, 그 이유를 제시
        # 이유의 형태 : 맞지 않는 부분 제시 -> 왜 맞지 않는 지 이유 제시, 근거 법 조항 제시
        #3. 만약 존재하지 않는다면, 문제 없는 조항입니다. 출력하기.

        "You are a legal assistant that analyzes whether a clause in a privacy policy contains potentially unfair or abusive content.\n\n"
        "Only use the provided context to evaluate the clause and cite sources if relevant. Do not rely on general knowledge or assumptions or any reasons outside the provided context.\n\n"

        "Full_clause : {question}\n\n"
        "Context : {context}\n\n"

        "Your task is to perform the following actions:\n"
        "1 - Based on the context, determine whether the clause contains any part that violates the legal standard or is unfair to the user.\n"
        "2 - If any issues are found, clearly explain what part of the clause is problematic and why. write your answer in the following format:\n"
        "   - 1)Identify the specific problematic phrase. -  Problematic phrase : <exact problematic text> \n"
        "   - 2)Explain clearly why it is problematic. - Reason : <why it conflicts, based only on the context>\n"
        "   - 3)Cite the relevant law or precedent it violates. - Relevant Law or Precedent : <specific part of the context>\n"
        "3 - If there is no issue, respond with: 'This clause does not contain any legal or fairness issues.'.\n\n"
        
        "Answer : "
    )
)

# 이후에 조항 별로 결과값 출력하는 부분도 작성해보기
# legal_term_template = PromptTemplate( #법률 용어 해석
#     input_variables= [],
#     template = ()
# )
#
# collect_data_template = PromptTemplate( #수집하는 항목 탐지
#     input_variables= ["full_clause"],
#     template = ()
# )
