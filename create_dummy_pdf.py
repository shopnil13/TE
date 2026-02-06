from reportlab.pdfgen import canvas
import os

def create_dummy_pdf(filename="input/test.pdf"):
    # Ensure input directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Hello, this is a test PDF.")
    c.drawString(100, 730, "It contains some sample text to extract.")
    c.showPage()
    c.drawString(100, 750, "This is the second page.")
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_dummy_pdf()
