import PyPDF2
pdf_file = open('/home/ujjwal/Downloads/365.pdf','rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
file=open('/home/ujjwal/Downloads/pdftotext','a')
file.write(page_content)
print(page_content)