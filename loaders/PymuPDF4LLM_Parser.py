#pip install pymupdf4llm 필요
import os
import pymupdf4llm

def change_pdf_to_md():

    #1. data/pdf 폴더에서 .pdf 파일 목록 불러오기
    folder_path = "../data/pdf"
    markdown_data = []

    #folder에 존재하는 file이 없을 때까지 진행
    try :
        for i in os.listdir(folder_path):
            #2. 불러온 데이터를 markdown으로 변환,저장하기
            data_path = f"../data/pdf/{i}"
            # print(f"{i}파일 변환 중")

            md_text = pymupdf4llm.to_markdown(data_path)
            markdown_data.append(md_text)
            print(f"[✓] {i} 파일 변환 완료")

    except Exception as e:
        print('Error!(Pdf 변환 과정)', e)

    print('모든 파일 변환 완료!!')
    return markdown_data