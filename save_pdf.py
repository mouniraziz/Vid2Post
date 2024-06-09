from mdpdf.converter import Converter

def md_to_pdf(output_file):
    try:
        converter = Converter(output_file) 
        converter.convert(["./files/generated_text_clean.md"])
        print(f"PDF generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")