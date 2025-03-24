#pip install pymupdf4llm 필요
import os
import pymupdf4llm


def change_pdf_to_md(file_name):

    #1. data/pdf 폴더에서 .pdf 파일 목록 불러오기
    folder_path = "./data/pdf"
    data_path = os.path.join(folder_path, file_name)

    #folder에 존재하는 file이 없을 때까지 진행
    try :

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"파일이 존재하지 않습니다: {data_path}")

        md_pages = pymupdf4llm.to_markdown(doc=data_path, page_chunks=True)
        print(f"[✓] {file_name} 파일 변환 완료")
        return md_pages

    except Exception as e:
        print('Error!(Pdf 변환 과정)', e)
        return None