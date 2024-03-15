import streamlit as st
import fitz
import PyPDF2
from typing import List, Tuple

def extract_toc(pdf_path: str, max_pages: int = 10) -> Tuple[List[str], List[int]]:
    """Extracts Table of Contents from the given PDF.

    Parameters:
    - pdf_path (str): Path to the PDF file.
    - max_pages (int): Maximum number of pages to scan for TOC. Default is 10.

    Returns:
    - toc_entries (List[str]): List of TOC entries.
    - toc_pages (List[int]): List of page numbers where TOC entries are found.
    """
    toc_entries = []
    toc_pages = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(min(max_pages, len(doc))):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            lines = text.split("\n")
            for line in lines:
                #Checking contineous spaces or dots between text and page no as almost evrey TOC has.
                #Because we may have text foloowed by numeric number and it takes as TOC,so this will handle 
                if line.strip() and line[0].isalpha() and (line.count(" ") > 20 or line.count(".") > 20) and line.rstrip()[-1].isdigit():
                    if line.strip()[-1].isdigit() and len(line) > 20:
                        toc_entries.append(line)
                        toc_pages.append(page_num)
        doc.close()
    except Exception as e:
        st.error(f"Error extracting Table of Contents: {e}")
    return toc_entries, toc_pages

def get_contentless_pdf(pdf_file: str, exclude_pages: List[int]) -> None:
    """Creates a PDF without TOC pages.

    Parameters:
    - pdf_file (str): Path to the PDF file.
    - exclude_pages (List[int]): List of page numbers to exclude.

    Returns:
    - None
    """
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
        st.success("PDF saved without TOC pages")
    except Exception as e:
        st.error(f"Error creating PDF without TOC pages: {e}")

def main() -> None:
    st.title("PDF Table of Contents Extractor")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        try:
            st.write("Extracting Table of Contents...")
            with open("temp_pdf.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            toc_entries, toc_pages = extract_toc("temp_pdf.pdf", max_pages=10)

            if toc_entries:
                st.write("Table of Contents Entries:")
                for entry, page in zip(toc_entries, toc_pages):
                    st.write(f"Entry: {entry}, Page: {page}")
                st.write("Page numbers where TOC entries are extracted:")
                st.write(list(set(toc_pages)))
                get_contentless_pdf("temp_pdf.pdf", list(set(toc_pages)))
            else:
                st.write("No Table of Contents found in the PDF.")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

if __name__ == "__main__":
    main()
