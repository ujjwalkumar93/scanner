import PyPDF2
pdf_file = open('/home/ujjwal/Downloads/365.pdf','rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
file=open('/home/ujjwal/Downloads/pdftotext','a')
file.write(page_content)
print(page_content)

# from tabula import read_pdf
# df=read_pdf('/home/ujjwal/Downloads/365.pdf')
# print(df)

# import fitz
# ifile = "C:\\user\\docs\\aPDFfile.pdf"
# doc = fitz.open(ifile)
# page_count = doc.pageCount
# page = 0
# text = ''
# while (page < page_count):
#     p = doc.loadPage(page)
#     page += 1
#     text = text + p.getText()
# print(text)


# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
# from io import BytesIO
# #path="/home/ujjwal/Downloads/365.pdf"
# def pdf_to_text(path):
#     manager = PDFResourceManager()
#     retstr = BytesIO()
#     layout = LAParams(all_texts=True)
#     device = TextConverter(manager, retstr, laparams=layout)
#     filepath = open(path, 'rb')
#     interpreter = PDFPageInterpreter(manager, device)
#
#     for page in PDFPage.get_pages(filepath, check_extractable=True):
#         interpreter.process_page(page)
#
#     text = retstr.getvalue()
#
#     filepath.close()
#     device.close()
#     retstr.close()
#     return text
#
#
# if __name__ == "__main__":
#     #file="result"
#     text = pdf_to_text("/home/ujjwal/Downloads/366.pdf")
#     write_file=open("/home/ujjwal/Downloads/pdftotext",'wb')
#     write_file.write(text)
#     print(text)