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
    st.header("Remove Table of Content")

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        st.write("Extracting Table of Contents...")

        # Save uploaded file temporarily
        with open("temp_pdf.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract TOC
        toc_entries, toc_pages = extract_toc("temp_pdf.pdf", max_pages=10)

        if toc_entries:
            st.write("Table of Contents Entries:")
            for entry, page in zip(toc_entries, toc_pages):
                content+=entry
                # st.markdown(f'''{entry}, Page: {page}''')
            st.markdown(f'''{content}''')
            st.toast('Removed ', icon='😍')
            st.markdown('''_Page numbers where TOC entries are extracted_:''')
            st.write(list(set(toc_pages)))

            # Create PDF without TOC pages
            get_contentless_pdf("temp_pdf.pdf", list(set(toc_pages)))

        else:
            st.write("No Table of Contents found in the PDF.")

if __name__ == "__main__":
    main()
