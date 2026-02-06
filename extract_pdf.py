import pdfplumber
import pandas as pd
import json
import os
import re
from glob import glob

def extract_text_from_pdfs(input_dir="input", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return

    records = []

    print(f"Found {len(pdf_files)} PDF files. Starting extraction...")

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"Processing: {filename}")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for i, page in enumerate(pdf.pages):
                    width = page.width
                    height = page.height
                    
                    # Split page into left and right columns
                    left_bbox = (0, 0, width / 2, height)
                    right_bbox = (width / 2, 0, width, height)
                    
                    left_crop = page.crop(bbox=left_bbox)
                    right_crop = page.crop(bbox=right_bbox)
                    
                    left_text = left_crop.extract_text() or ""
                    right_text = right_crop.extract_text() or ""
                    
                    full_text += left_text + "\n" + right_text + "\n"
                
                # Parse the accumulated text
                parsed_records = parse_records(full_text)
                records.extend(parsed_records)
                
        except Exception as e:
            print(f"  Error processing {filename}: {e}")

    if not records:
        print("No records extracted.")
        return

    # Sort records by index
    records.sort(key=lambda x: x['record_index'])

    # Prepare output structure
    output_data = {
        "schema": [
            "record_index",
            "company_name",
            "registration_number",
            "managing_director_name",
            "managing_director_title",
            "address",
            "telephone_office",
            "fax_office",
            "email",
            "website",
            "product"
        ],
        "records": records
    }

    # Export to JSON
    json_path = os.path.join(output_dir, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"Saved JSON to: {json_path}")

    # Export to Excel
    excel_path = os.path.join(output_dir, "data.xlsx")
    df = pd.DataFrame(records)
    # Reorder columns to match schema
    cols = output_data["schema"]
    # Ensure all schema columns exist in df
    for col in cols:
        if col not in df.columns:
            df[col] = ""
    df = df[cols]
    
    df.to_excel(excel_path, index=False)
    print(f"Saved Excel to: {excel_path}")
    print("Extraction complete.")

def parse_records(text):
    records = []
    text = text.replace('\r\n', '\n')
    
    # Regex to find records: (Index) Name (Reg.#)
    # Use re.DOTALL to let . match newlines in the content part
    # Improved regex:
    # 1. Match start index: `(?:^|\n)\(\d+\)`
    # 2. Match Name: `.+?` (non-greedy until Reg.#)
    # 3. Match Reg: `\(Reg\.#\s*\d+\)`
    # 4. Match Body: `.*?` (non-greedy until next index or end)
    # Lookahead for next index must handle newlines
    
    pattern = re.compile(r'(?:^|\n)\((\d+)\)\s+(.+?)\s+\(Reg\.#\s*(\d+)\)(.*?)(?=(?:^|\n)\(\d+\)\s+|$)', re.DOTALL)
    
    matches = pattern.finditer(text)
    
    for match in matches:
        record_index = int(match.group(1))
        company_name = match.group(2).strip()
        reg_number = match.group(3).strip()
        body = match.group(4).strip()
        
        parsed_fields = parse_fields(body)
        
        record_data = {
            "record_index": record_index,
            "company_name": company_name,
            "registration_number": reg_number,
            **parsed_fields
        }
        records.append(record_data)
        
    return records

def parse_fields(text):
    data = {
        "managing_director_name": "",
        "managing_director_title": "",
        "address": "",
        "telephone_office": "",
        "fax_office": "",
        "email": "",
        "website": "",
        "product": ""
    }
    
    # helper for regex extraction
    def extract(pattern, content):
        m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else ""

    # Extract Contact Info first to clean them from address search
    # Note: Fields are often 'Label : Value'
    # We look for value until newline or next label
    
    labels = ["Tel \(Off\)", "Fax \(Off\)", "Email", "Website", "Product"]
    labels_pattern = "|".join(labels)
    
    # Tel
    data["telephone_office"] = extract(r'Tel \(Off\)\s*:\s*(.*?)(?:' + labels_pattern + r'|$)', text)
    # Fax
    data["fax_office"] = extract(r'Fax \(Off\)\s*:\s*(.*?)(?:' + labels_pattern + r'|$)', text)
    # Email
    data["email"] = extract(r'Email\s*:\s*(.*?)(?:' + labels_pattern + r'|$)', text)
    # Website
    data["website"] = extract(r'Website\s*:\s*(.*?)(?:' + labels_pattern + r'|$)', text)
    # Product
    data["product"] = extract(r'Product\s*:\s*(.*?)(?:' + labels_pattern + r'|$)', text)

    # MD and Address
    # Lines before the first contact label are MD + Address
    # Find start of first contact label
    first_label_match = re.search(r'(?:' + labels_pattern + r')\s*:', text)
    if first_label_match:
        top_section = text[:first_label_match.start()].strip()
    else:
        top_section = text.strip()
        
    lines = [l.strip() for l in top_section.split('\n') if l.strip()]
    
    if lines:
        md_line = lines[0]
        # Parse MD
        if ',' in md_line:
            last_comma_idx = md_line.rfind(',')
            name = md_line[:last_comma_idx].strip()
            title = md_line[last_comma_idx+1:].strip()
            # Basic validation: title should be short-ish?
            data["managing_director_name"] = name
            data["managing_director_title"] = title
        else:
            data["managing_director_name"] = md_line
            
        if len(lines) > 1:
            data["address"] = " ".join(lines[1:])

    # Cleanups
    # Remove newlines from fields
    for k in data:
         data[k] = data[k].replace('\n', ', ') # Replace newlines in fields with comma

    return data

if __name__ == "__main__":
    extract_text_from_pdfs()
