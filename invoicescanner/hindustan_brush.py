from __future__ import division

import os
import re
import json



class Text_Converter_hindustan:

    def __init__(self,file_url):
        self.file_url=file_url
        #print("file url is: ",self.file_url)

    def fields_data_hindustan(self):
         file_location=os.path.join(os.getcwd(),'media','tabula_text')
         with open(file_location,'r+') as fl:
             i=0
             for line in fl:
                 po_s = re.search(r'P.O.|P.O. (\S+)', line)
                 invoice_date_s = re.search(r'Date:|Date: (\S+)', line)
                 part_qty_s = re.search(r'It|It (\S+)', line)
                 net_rate_s = re.search(r'It|It (\S+)', line)
                 HSN_s = re.search(r'It|It (\S+)', line)
                 invoice_value_s = re.search(r'TOTAL|TOTAL (\S+)', line)
                 invoice_num_s = re.search(r'No:|No: (\S+)', line)
                 cgst_rate_s = re.search(r'CGST|CGST (\S+)', line)
                 cgst_amt_s = re.search(r'CGST|CGST (\S+)', line)
                 sgst_rate_s = re.search(r'SGST|SGST (\S+)', line)
                 sgst_amt_s = re.search(r'SGST|SGST (\S+)', line)
                 part_no_s = re.search(r'16|16 (\S+)', line)
                 """sgst_amt_s=re.search(r'PACKING', line)"""
                 print("Po_s is "*5,po_s)
                 try:
                    if po_s:
                        word_list=line.split()
                        #print(word_list)
                        po_no=word_list[word_list.index("P.O.No.:")+1]
                        print("Po number is: "*5,po_no)
                 except:
                    po_no=po_no
                    print("Po Number Not Found ")

                 try:
                    if invoice_date_s:
                        word_list = line.split()
                        invoice_date= word_list[word_list.index("Date:")+1].replace('/','.')
                        print("invoice date is: "*5,invoice_date)
                 except:
                     invoice_date=invoice_date
                     print("invoice date not found")
                 try:
                    if part_qty_s:
                        word_list = line.split()
                        print(word_list)
                        part_qty = word_list[word_list.index("It") + 4]+".000"
                        print("part qty "*5, part_qty)

                 except:

                     print("part qty not found")

                 try:
                     if net_rate_s:
                        word_list = line.split()
                        net_rate = word_list[word_list.index("It") + 5]
                        print("net rate is: " * 5, net_rate)
                 except:
                     print("Net rate not found ")

                 try:
                    if HSN_s:
                        word_list = line.split()
                        HSN_no = word_list[word_list.index("It") +3]
                        print("Hsn no is: "*5,HSN_no)
                 except:

                     print("HSN Number not found")

                 try:
                    if invoice_value_s:
                        word_list = line.split()
                        total_amt = word_list[( word_list.index("TOTAL") ) +1].replace(',','')
                        print("invoice amt is: "*5,total_amt)
                 except:
                     print("Invoice value not found")
                 try:
                    if invoice_num_s:
                        word_list = line.split()
                        invoice_num= word_list[word_list.index("No:") +1]
                        print("invoice num is: "*5,invoice_num)
                 except:
                     print("Invoice number not found...")
                 try:
                     if cgst_rate_s:
                        word_list = line.split()
                        cgst_rate = word_list[word_list.index("CGST") + 1].replace('%',"")+".00"
                        print("cgst rate is: "*5,cgst_rate)
                 except:
                     print("Cgst rate not found")
                 try:
                     if cgst_amt_s:
                        word_list = line.split()
                        cgst_amt = word_list[word_list.index("CGST") + 2].replace(',','')
                        print("cgst amt is: "*5, cgst_amt)
                 except:
                     print("Cgst amt not found")
                 try:
                     if sgst_rate_s:
                        word_list = line.split()
                        sgst_rate = word_list[word_list.index("SGST") + 1].replace('%',"")+".00"
                        print("sgst rate is: "*5,sgst_rate)
                 except:
                     print("Sgst rate not found")

                 try:
                     if sgst_amt_s:
                        word_list = line.split()
                        sgst_amt = word_list[word_list.index("SGST") + 2].replace(',','')
                        print("sgst amt is: "*5,sgst_amt)
                 except:
                     print("Sgst amt not found")

                 try:
                     if part_no_s:
                        word_list = line.split()
                        part_no = word_list[word_list.index("16") + 2]
                        print("Part no. is: "*5,part_no)
                 except:
                     print("part no not found")
         try:
            json_obj={
             'po_no': po_no,
             'gst_no' : "Not found",
             'invoice_date' :invoice_date,
             'vendor_code':'H62040',
             'part_no': part_no,
             'hsn_no': HSN_no,
             'invoice_val': total_amt,
             'igst_rate': "0.00",
             'igst_amt': "0.00",
             'invoice_num': invoice_num,
             'part_qty':part_qty,
             'gross_rate':net_rate,
             'net_rate':net_rate,
             'sgst_rate':sgst_rate,
             'cgst_rate':cgst_rate,
             'sgst_amt': sgst_amt,
             'cgst_amt': cgst_amt,
             'po_order_item_no':10
            }
            print(json_obj)
         except Exception as e:
             print("exception handeled: ",e)
             json_obj = {
                 'po_no': "NAA",
                 'gst_no': "NAA",
                 'invoice_date': "NA",
                 'vendor_code': "NA",
                 'part_no': 'NA',
                 'hsn_no': "NA",
                 'invoice_val': "NA",
                 'igst_rate': "NA",
                 'igst_amt': "NA",
                 'invoice_num': "NA",
                 'part_qty': "NA",
                 'gross_rate': "NA",
                 'net_rate': "NA",
                 'sgst_rate': "NA",
                 'cgst_rate': "NA",
                 'sgst_amt': "NA",
                 'cgst_amt': "NA",
                 'po_order_item_no':10
             }
         data=json.dumps(json_obj)
         #print("data is: ",data)
         return data

