import os
import PyPDF2
import re
import json

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

    def get_file_path(self):

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
                 part_qty_s=re.search(r'Total', line)
                 rate_per_qty_s=re.search(r'Total', line)
                 net_rate_s=re.search(r'Total', line)
                 tax_category_s=re.search(r'TotalAmount', line)
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
                    #print("Gst is: "*20,gst_no)
                 if invoice_date_s:
                     word_list = line.split()
                     invoice_date_format= word_list[word_list.index("MaharashtraDate")+1][1:12]
                     invoice_date_rep=invoice_date_format.replace('-','.')
                     newdate=invoice_date_rep[3:6]
                     #print("new date is"*30,newdate)
                     #new_date=invoice_date.strftime('%m/%d/%y')
                     m = {
                         'jan': '01',
                         'feb': '02',
                         'mar': '03',
                         'apr': '04',
                         'may': '05',
                         'jun': '06',
                         'jul': '07',
                         'aug': '08',
                         'sep': '09',
                         'oct': '10',
                         'nov': '11',
                         'dec': '12'
                     }
                     s = newdate.strip()[:3].lower()

                     try:
                         out = m[s]
                         invoice_date=invoice_date_rep.replace(newdate,out)

                         print("m"*10,out)
                         #return out
                     except:
                         raise ValueError('Not a month')


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
                     #print("HSN NO : ", HSN_no)
                 if invoice_value_s:
                     word_list = line.split()
                     total_amt = word_list[word_list.index("TotalAmount") -1]
                     str_len=len(total_amt)
                     total_alpha=str_len-5
                     invoice_amts=total_amt[0:total_alpha]
                     invoice_amt=invoice_amts.replace(",","")

                     #print("TotalAmount ", invoice_amt)
                 if igst_s:
                     word_list = line.split()
                     igst_rate_act = word_list[word_list.index("TotalAmount") -7][0:2]
                     igst=igst_rate_act.replace("%","")
                     print("%"*50,igst)
                     igst_rate=igst+".00"

                     #print("igst% : ", igst_rate)
                 if igst_amt_s:
                     word_list = line.split()
                     igst_amt_with_len = word_list[word_list.index("TotalAmount") -8]
                     word_len=len(igst_amt_with_len)
                     actual_len=word_len-5
                     igst_amts=igst_amt_with_len[0:actual_len]
                     igst_amt=igst_amts.replace(",","")
                     #print("IGST Amt: ", igst_amt) """
                 if tax_category_s:
                     word_list = line.split()
                     tax_cat=word_list[word_list.index("TotalAmount") -8]
                     my_len=len(tax_cat)
                     init_len=my_len-5
                     #code for differentiate tax categories
                     if tax_cat == "I-GST":
                         print("yes git the tax category"*20)
                         """if igst_s:
                             word_list = line.split()
                             igst_rate = word_list[word_list.index("TotalAmount") - 7][0:2]
                             return igst_rate
                             # print("igst% : ", igst_rate)
                         if igst_amt_s:
                             word_list = line.split()
                             igst_amt_with_len = word_list[word_list.index("TotalAmount") - 8]
                             word_len = len(igst_amt_with_len)
                             actual_len = word_len - 5
                             igst_amt = igst_amt_with_len[0:actual_len]
                             return igst_amt
                     elif tax_cat=="S-GST":
                         print("Not found") """

                     print("tax field is: "*20,tax_cat)
                     print("tax_cat : "*20,tax_cat[init_len:my_len])

                 if invoice_num_s:
                      word_list = line.split()
                      invoice_num_with_len= word_list[word_list.index("Challan") - 2]
                      length_invoice=len(invoice_num_with_len)
                      actual_len=length_invoice-7
                      invoice_num=invoice_num_with_len[12:actual_len]
                      #print("Invoice number: ", invoice_num)
                 try:
                    if part_qty_s:
                        word_list=line.split()
                        part_qty_trimmed = word_list[word_list.index("Total") -3][0:3]
                        max_index=part_qty_trimmed.find('.')
                        part_qty=part_qty_trimmed[0:max_index]
                        #print("part No: "*
                        print(word_list)

                 except:
                     print("part No notfound")

                 try:
                    if rate_per_qty_s:
                         word_list = line.split()
                         part_qty_rate_full = word_list[word_list.index("Total") -3]
                         first_point_pos=part_qty_rate_full.find('.')
                         init_length=first_point_pos+3

                         full_len=len(part_qty_rate_full)
                         first_half = part_qty_rate_full[init_length:full_len]
                         secon_point_pos=first_half.find('.')+3
                         part_qty_rate=first_half[0:secon_point_pos]


                         #print("part_rate is: "*20,part_qty_rate)
                     #print(secon_point_pos)
                         gross_rate_format=float(part_qty)*float(part_qty_rate)
                         gross_rate=format(gross_rate_format,'.2f')
                         print("gross rate: "*20,gross_rate)
                 except:
                     print("rate per qty not found")
                 try:
                    if net_rate_s:
                        word_list = line.split()
                        net_rate= word_list[word_list.index("Total") - 2]
                        #print("net rate is:"*20,net_rate)
                 except:
                     print("net rate not found")

             #print("here is all amount: ",invoice_num,igst_rate,invoice_amt,vendor_code,invoice_date)
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
                 'invoice_num': invoice_num,
                 'part_qty':part_qty,
                 'gross_rate': gross_rate,
                 'net_rate':net_rate,
             }
             data=json.dumps(json_obj)
             print("data is: ",data)
             return data










