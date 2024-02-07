
# Table of Content (TOC) Removal

This Python script removes the Table of Contents (TOC) pages from a PDF file based on the user's input. It identifies TOC pages by analyzing the content and page structure of the PDF file.

## Usage

### Prerequisites

- Python 3.x
- Required Python packages: `PyPDF2`,fitz,streamlit (for PDF manipulation)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:
   ```bash
   cd your-repository
   ```

3. Install required packages:
   ```bash
   pip install PyPDF2
   ```

### Running the Script

1. Ensure you have a PDF file from which you want to remove TOC pages.

2. Run the script:
   ```bash
   streamlit run toc.py
   ```

3. Follow the on-screen instructions:
   - Input the path to the PDF file.
   - The script will analyze the PDF file and display the number of pages where TOC entries are found.
   - You can choose to remove the TOC pages from the PDF file.

### Example

```
$ python toc.py
Enter the path to the PDF file: sample.pdf

Number of TOC pages found: 5

Do you want to remove these pages? (yes/no): yes
TOC pages removed successfully.

```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the code.

