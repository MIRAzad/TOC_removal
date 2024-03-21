import fitz
import PyPDF2
from typing import List, Tuple

def extract_toc(pdf_path: str, max_pages: int = 10) -> Tuple[List[str], List[int]]:
    toc_entries = []
    toc_pages = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(min(max_pages, len(doc))):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            lines = text.split("\n")
            for line in lines:
                if line.strip() and line[0].isalpha() and (line.count(" ") > 20 or line.count(".") > 20) and line.rstrip()[-1].isdigit():
                    if line.strip()[-1].isdigit() and len(line) > 20:
                        toc_entries.append(line)
                        toc_pages.append(page_num)
        doc.close()
    except Exception as e:
        print(f"Error extracting Table of Contents: {e}")
    return toc_entries, toc_pages

def get_contentless_pdf(pdf_file: str, exclude_pages: List[int]) -> None:
    try:
        pdf_writer = PyPDF2.PdfWriter()
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                if page_num in exclude_pages:
                    continue
                pdf_writer.add_page(page)
        with open("modified_pdf_except_toc.pdf", 'wb') as output_file:
            pdf_writer.write(output_file)
        print("PDF saved without TOC pages")
    except Exception as e:
        print(f"Error creating PDF without TOC pages: {e}")

def main() -> None:
    pdf_file = "file.pdf"

    try:
        print("Extracting Table of Contents...")
        toc_entries, toc_pages = extract_toc(pdf_file, max_pages=10)

        if toc_entries:
            print("Table of Contents Entries:")
            for entry, page in zip(toc_entries, toc_pages):
                print(f"Entry: {entry}, Page: {page}")
            print("Page numbers where TOC entries are extracted:")
            print(list(set(toc_pages)))
            get_contentless_pdf(pdf_file, list(set(toc_pages)))
        else:
            print("No Table of Contents found in the PDF.")
    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    main()
