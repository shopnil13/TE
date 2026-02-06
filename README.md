# PDF Data Extractor

This tool extracts structured data from PDF files, specifically designed to parse company information (Name, MD, Address, Contact Info) from directory-style PDFs into JSON and Excel formats.

## Prerequisites

Before running the project, ensure you have the following installed:

*   **Git**: To clone the repository.
*   **Python 3.9+** (for local execution).
*   **Docker Desktop** (for containerized execution - Recommended).

## Getting Started

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/shopnil13/TE.git
cd TE
```

---

## How to Run

### Option A: Running with Docker (Recommended)

This is the easiest way to run the application as it handles all dependencies for you.

1.  **Start the container**:
    ```bash
    docker-compose up --build
    ```
    This command will build the image and start the extraction process.

2.  **Process Files**:
    *   Place your target PDF files in the `input/` folder within the project directory. (Don't forget to remove the test.pdf file before running the script).
    *   The script will automatically process them.
    *   Find the results in the `output/` folder (`data.json` and `data.xlsx`).

3.  **Stop**:
    ```bash
    docker-compose down
    ```

### Option B: Running Locally (Python)

If you prefer to run it directly on your machine:

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
