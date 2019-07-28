from __future__ import division
import os
import re
import json
class Text_Converter_perfect_packing:
    def __init__(self,file_url):
        self.file_url=file_url
        #print("file url is: ",self.file_url)
    def fields_data_perfect_packing(self):
         file_location=os.path.join(os.getcwd(),'media','tabula_text')
         with open(file_location,'r+') as fl:
             i=0
             for line in fl:
                 po_s = re.search(r'Order No.|Order No. (\S+)', line,re.IGNORECASE)
                 invoice_num_s = re.search(r'Inv. No.|Inv. No. (\S+)', line, re.IGNORECASE)
                 invoice_date_s = re.search(r'Inv. No.|Inv. No. (\S+)', line,re.IGNORECASE)
                 order_item_num_s = re.search(r'ITEM|ITEM (\S+)', line,re.IGNORECASE)
                 part_no_s = re.search(r'MATERIAL|MATERIAL CODE:|ITEM CODE(\S+)', line,re.IGNORECASE)
                 total_invoice_value_s=re.search(r'Gross Amount|Gross Amount (\S+)', line,re.IGNORECASE)
                 igst_s=re.search(r"IGST|IGST (\S+)",line,re.IGNORECASE)
                 cgst_s=re.search(r"CGST|CGST (\S+)",line,re.IGNORECASE)
                 sgst_s = re.search(r"SGST|SGST (\S+)", line, re.IGNORECASE)
                 hsn_code_s = re.search(r"15|15 (\S+)", line, re.IGNORECASE)
                 #print("Po_s is "*5,po_s)
                 try:
                    if po_s:
                        word_list=line.split()
                        #print(word_list)
                        po_no=word_list[word_list.index("No.")+2]
                        #print("Po number is: "*5,po_no)
                 except:
                    po_no="NA"
                    #print("Po Number Not Found ")
                 try:
                     if invoice_num_s:
                         word_list=line.split()
                         invoice_num=word_list[word_list.index("No.")+2]
                         #print("Invoice Num "*5,invoice_num)
                 except:
                     invoice_num="Not Found"

                 try:
                    if invoice_date_s:
                        word_list = line.split()
                        #print("word list is: "*5,word_list)
                        invoice_date= word_list[word_list.index("No.")+5].replace('/','.')
                        #print("invoice date is: "*5,invoice_date)
                 except:
                     invoice_date="NA"
                     print("invoice date not found")
                # print("order_item_num_s is "*3,order_item_num_s)
                 try:
                     if order_item_num_s:
                         word_list=line.split()
                         #print("word list for order item number: ",word_list)
                         order_item_no=word_list[word_list.index("ITEM")+2]
                         #print("order item number is: ",order_item_no)
                 except:
                     order_item_no="Not found"
                     print("Exception handeled")
                 print("Part_no_s found"*10,part_no_s)
                 try:
                     if part_no_s:
                         word_list = line.split()
                         #print("word list for part_number is: "*5,word_list)
                         part_no = word_list[word_list.index("CODE:") + 1]
                         #print("Part no. is: " * 5, part_no)
                 except:
                     part_no="Not found"
                     print("part no not found")
                 print("Total_Invoice_Value "*5,total_invoice_value_s)
                 try:
                     if total_invoice_value_s:
                         word_list=line.split()
                         #print("word list is: ",word_list)
                         total_invoice_value=word_list[word_list.index("Amount")+1]
                         print("Total invoice value is: ",total_invoice_value)
                 except:
                     total_invoice_value="Not found"
                     print("Total invoice value is not found:")

                 try:
                     if igst_s:
                         word_list=line.split()
                         igst_rate=word_list[word_list.index("IGST")+2]+".00"
                         #print("IGST rate is: "*10,igst_rate)
                         igst_amt=word_list[word_list.index("IGST")+7]
                         #print("Igst amt is: "*10,igst_amt)
                         sgst_rate="0.00"
                         sgst_amt="0.00"
                         cgst_rate="0.00"
                         cgst_amt="0.00"
                 except:
                     igst_rate="Not Found"
                     igst_amt="Not found"
                     print("IGST Exception handeled")
                 try:
                     if sgst_s:
                         word_list=line.split()
                         sgst_rate=word_list[word_list.index("SGST")+2]+".00"
                         sgst_amt=word_list[word_list.index("SGST")+7]

                 except:
                     sgst_rate="Not found"
                     sgst_amt="Not Found"

                 try:
                     if cgst_s:
                         word_list = line.split()
                         cgst_rate = word_list[word_list.index("CGST") + 2] + ".00"
                         cgst_amt = word_list[word_list.index("CGST") + 7]
                         igst_rate="0.00"
                         igst_amt="0.00"

                 except:
                     cgst_rate = "Not found"
                     cgst_amt = "Not Found"

                 try:
                     print("HSN code_s : ", hsn_code_s)
                     if hsn_code_s:
                         word_list = line.split()
                         #print("word list for HSN Code" * 5, word_list)
                         list_lenth = len(word_list) - 6
                         hsn_code_predict = word_list[word_list.index("15") + list_lenth]
                         if hsn_code_predict.find('.') == 1:
                             print("inside if block "*20)
                             hsn_code=word_list[word_list.index("15")+(list_lenth-1)]
                         else:
                             print("inside else block " * 20)
                             hsn_code=word_list[word_list.index("15")+(list_lenth)]

                         print("decimal"*10,hsn_code.find('.'))
                         print("HSN Code is:", hsn_code)
                 except:
                     hsn_code = "Not Found"

         file_location = os.path.join(os.getcwd(), 'media','text')
         with open(file_location, 'r+') as fl:
             i=0
             for line in fl:
                 part_qty_s=re.search(r"sales@perfectpacking.in|sales@perfectpacking.in ",line,re.IGNORECASE)

                 net_rate_s=re.search(r"sales@perfectpacking.in|sales@perfectpacking.in (\S+)",line,re.IGNORECASE)
                 #print("Part_Qty_s Found: "*5,part_qty_s)
                 try:
                    if part_qty_s:
                        word_list = line.split()
                        #print("word_list for part qty: "*5,word_list)
                        part_qty = word_list[word_list.index("sales@perfectpacking.in") + 1]
                        print("part qty "*5, part_qty)
                 except:
                     part_qty="Not Found"
                     print("part qty not found")


                 try:
                     if net_rate_s:
                         word_list=line.split()
                         #print("Word list for net rate is: ",word_list)
                         net_rate_with_extra_char=word_list[word_list.index("sales@perfectpacking.in")+2]
                         last_index=net_rate_with_extra_char.index(".")+3
                         net_rate=net_rate_with_extra_char[0:last_index]
                         print("Last Index is: "*10,last_index)
                 except:
                     net_rate="Not found"
         try:
            json_obj={
             'po_no': po_no,
             'gst_no' : "Not found",
             'invoice_date' : invoice_date,
             'vendor_code':'P66090',
             'part_no': part_no,
             'hsn_no': hsn_code,
             'invoice_val': total_invoice_value,
             'igst_rate': igst_rate,
             'igst_amt': igst_amt,
             'invoice_num': invoice_num,
             'part_qty':part_qty,
             'gross_rate':net_rate,
             'net_rate': net_rate,
             'sgst_rate':sgst_rate,
             'cgst_rate':cgst_rate,
             'sgst_amt': sgst_amt,
             'cgst_amt': cgst_amt,
             'po_order_item_no':order_item_no
            }
            print(json_obj)
         except Exception as e:
             print("exception handeled: ",e)
             json_obj = {
                 'po_no': "NAA",
                 'gst_no': "NAA",
                 'invoice_date': "NA",
                 'vendor_code': "P66090",
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

