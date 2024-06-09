import base64
def open_pdf_as_bytes(pdf_file_path):
    # Open the PDF file in binary mode
    with open(pdf_file_path, 'rb') as pdf_file:
        # Read the PDF file as bytes
        pdf_bytes = pdf_file.read()
    pdf_file.close()
    return pdf_bytes

# Create download link
def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
