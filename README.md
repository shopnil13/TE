# PDF Data Extractor

This tool extracts structured data from PDF files, specifically designed to parse company information (Name, MD, Address, Contact Info) from directory-style PDFs into JSON and Excel formats.

## Prerequisites

To run this project, you need the following installed on your local machine:

*   **Git**: Version control tool to clone the repository.
*   **Python**: Version 3.9 or higher.
*   **PIP**: Python package installer (usually included with Python).

### Required Libraries
The following Python libraries are used (installed via `requirements.txt`):
*   `pdfplumber`: For extracting text from PDF files.
*   `pandas`: For data structuring and Excel export.
*   `openpyxl`: For saving Excel (`.xlsx`) files.
*   `reportlab`: For creating dummy PDFs (if testing).

## Getting Started

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/shopnil13/TE.git
cd TE
```

---

## How to Run

### Running Locally (Python)

1.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the script**:
    ```bash
    python extract_pdf.py
    ```

## Output

The script generates two files in the `output/` directory:

1.  **data.json**: Structured JSON data containing all extracted records.
2.  **data.xlsx**: An Excel spreadsheet with the same data for easy viewing and filtering.
