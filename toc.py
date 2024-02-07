import streamlit as st
import fitz
import PyPDF2

# Function to extract TOC from PDF
def extract_toc(pdf_path, max_pages=10):
    toc_entries = []
    toc_pages = []
    doc = fitz.open(pdf_path)
    for page_num in range(min(max_pages, len(doc))):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        # Split text into lines
        lines = text.split("\n")
        # Look for patterns indicative of TOC entries
        for line in lines:
            # Check if the line starts with text, has more than 20 spaces, or dots, and ends with a numeric number.
            if line.strip() and line[0].isalpha() and (line.count(" ") > 20 or line.count(".") > 20) and line.rstrip()[-1].isdigit():
                # Check if the line ends with a numeric character and the total character length in a line is > 20
                if line.strip()[-1].isdigit() and len(line) > 20:
                    toc_entries.append(line)  # Store the TOC entry text without stripping
                    toc_pages.append(page_num)  # Store the current page number
    doc.close()
    return toc_entries, toc_pages

# Function to create a PDF without TOC pages
def get_contentless_pdf(pdf_file, exclude_pages):
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

# Streamlit app
def main():
    st.title("PDF Table of Contents Extractor")

    # File uploader for PDF
    uploaded_pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # File uploader for static files
    uploaded_static_files = st.file_uploader("Upload static files", type=["css", "js", "png", "jpg"], accept_multiple_files=True)

    if uploaded_pdf_file is not None:
        st.write("Extracting Table of Contents...")
        # Save uploaded PDF file temporarily
        with open("temp_pdf.pdf", "wb") as f:
            f.write(uploaded_pdf_file.getbuffer())
        
        # Extract TOC
        toc_entries, toc_pages = extract_toc("temp_pdf.pdf", max_pages=10)
        
        # Process static files
        static_files_paths = []
        for static_file in uploaded_static_files:
            file_path = f"static/{static_file.name}"
            with open(file_path, "wb") as f:
                f.write(static_file.getbuffer())
            static_files_paths.append(file_path)
        
        # Include static files in PDF processing logic if uploaded
        if static_files_paths:
            # Process PDF with static files
            # You may need to modify this part to include static files in PDF processing
            pass
        
        # Display extracted TOC
        if toc_entries:
            st.write("Table of Contents Entries:")
            for entry, page in zip(toc_entries, toc_pages):
                st.write(f"Entry: {entry}, Page: {page}")
            st.write("Page numbers where TOC entries are extracted:")
            st.write(list(set(toc_pages)))
        else:
            st.write("No Table of Contents found in the PDF.")

if __name__ == "__main__":
    main()
