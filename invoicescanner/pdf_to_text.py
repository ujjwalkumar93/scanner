import os
import pandas as pd
import tabula
import PyPDF2
import re
import json
import xlwt
from xlwt import Workbook
class Text_Converter:

    def __init__(self,file_url):
        self.file_url=file_url
        print("file url is: ",self.file_url)

    def convert_pdf_to_text(self):
        file_path=self.file_url
        file_obj=open(file_path,'rb')
        pdf_reader=PyPDF2.PdfFileReader(file_obj)
        total_pages=pdf_reader.numPages
        #print("Total number of pages: ",total_pages)
        page_obj=pdf_reader.getPage(0 )
        content=page_obj.extractText()
        #print(content)

        file_location=os.path.join(os.getcwd(),'media','text')
        text_file=open(file_location,'w')
        write_content=text_file.write(content)
        #print("53"*50,file_path)
        #return file_path
        # list=[content]
        # print(list)
        #print("content coppied")
    def get_file_path(self):
        #file_path=self.file_url
         #print("File url from get_file_path is : ",file_path)
        #print("%%%%%%%%%%%%%%%%%%%%%%%%%%",self.file_url)
        return self.file_url
    def fields_data(self):

         file_location=os.path.join(os.getcwd(),'media','text')
         with open(file_location,'r+') as fl:
             i=0
             for line in fl:
                 po_s = re.search(r'Terms (\S+)', line)
                 gst_s = re.search(r'MaharashtraDate (\S+)', line)
                 invoice_date_s = re.search(r'MaharashtraDate (\S+)', line)
                 vendor_code_s = re.search(r':Reg.Type (\S+)', line)
                 part_no_s = re.search(r':Reg.Type (\S+)', line)
                 HSN_s = re.search(r'Total(\S+)', line)
                 invoice_value_s = re.search(r'TotalAmount (\S+)', line)
                 igst_s=re.search(r'TotalAmount', line)
                 igst_amt_s = re.search(r'TotalAmount', line)
                 invoice_num_s = re.search(r'Challan', line)
                 #print(po_s.group(0))
                 if po_s:
                     word_list=line.split()

                     po_no_s=word_list[word_list.index("Terms")+2]
                     #po_no=po_no_s[0:10]
                     po_num=po_no_s[1:11]
                     #return po_num
                     #print("Po number is: ",po_num)
                 if gst_s:
                    #print("Gst line is: ",gst_s)
                    word_list=line.split()
                    gst_no=word_list[word_list.index("MaharashtraDate")-6][21:36]
                    #print("Gst is: ",gst_no)
                 if invoice_date_s:
                     word_list = line.split()
                     invoice_date = word_list[word_list.index("MaharashtraDate")+1][1:12]
                     #print("Invoice date: ",invoice_date)
                 if vendor_code_s:
                     word_list = line.split()
                     vendor_code = word_list[word_list.index(":Reg.Type") + 4][0:6]
                     #print("vendor code: ", vendor_code)
                 if part_no_s:
                     word_list = line.split()
                     part_no = word_list[word_list.index(":Reg.Type") + 7][0:11]
                    # print("part no: : ", part_no)
                 if HSN_s:
                     word_list = line.split()
                     HSN_no_len = word_list[word_list.index("Total") -3]
                     length_hsn=len(HSN_no_len)
                     init_len=length_hsn-8
                     HSN_no=HSN_no_len[init_len:length_hsn]
                     print("HSN NO : ", HSN_no)
                 if invoice_value_s:
                     word_list = line.split()
                     total_amt = word_list[word_list.index("TotalAmount") -1]
                     str_len=len(total_amt)
                     total_alpha=str_len-5
                     invoice_amt=total_amt[0:total_alpha]
                     #print("TotalAmount ", invoice_amt)
                 if igst_s:
                     word_list = line.split()
                     #print(word_list)
                     #print(word_list)
                     igst_rate = word_list[word_list.index("TotalAmount") -7]
                     #print("igst% : ", igst_rate)
                 if igst_amt_s:
                     word_list = line.split()
                     igst_amt_with_len = word_list[word_list.index("TotalAmount") -8]
                     word_len=len(igst_amt_with_len)
                     actual_len=word_len-5
                     igst_amt=igst_amt_with_len[0:actual_len]
                     #print("IGST Amt: ", igst_amt)
                 if invoice_num_s:
                      word_list = line.split()
                      invoice_num_with_len= word_list[word_list.index("Challan") - 2]
                      length_invoice=len(invoice_num_with_len)
                      actual_len=length_invoice-7
                      invoice_num=invoice_num_with_len[11:actual_len]
                      #print("Invoice number: ", invoice_num)

             print("here is all amount: ",invoice_num,igst_rate,invoice_amt,vendor_code,invoice_date)
             json_obj={
                 'po_no': po_num,
                 'gst_no' : gst_no,
                 'invoice_date': invoice_date,
                 'vendor_code': vendor_code,
                 'part_no': part_no,
                 'hsn_no': HSN_no,
                 'invoice_val': invoice_amt,
                 'igst_rate': igst_rate,
                 'igst_amt': igst_amt,
                 'invoice_num': invoice_num
             }
             data=json.dumps(json_obj)
             return data










