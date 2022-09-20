import pdfkit
PATH_WHTMLTOPDF = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'

config = pdfkit.configuration(wkhtmltopdf=PATH_WHTMLTOPDF)

def convert_html_to_pdf(html_path: str, output_pdf_path: str):
    pdfkit.from_file(html_path, output_pdf_path, configuration=config)