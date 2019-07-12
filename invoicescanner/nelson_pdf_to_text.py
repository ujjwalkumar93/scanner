from __future__ import division
import os
import PyPDF2
import re
import json

class Text_Converter:

    def __init__(self,file_url):
        self.file_url=file_url
        #print("file url is: ",self.file_url)

    def convert_pdf_to_text(self):
        file_path=self.file_url
        file_obj=open(file_path,'rb')
        pdf_reader=PyPDF2.PdfFileReader(file_obj)
        total_pages=pdf_reader.numPages
        file_location = os.path.join(os.getcwd(), 'media', 'text')
        text_file = open(file_location, 'a')
        text_file.truncate(0)
        for page in range(total_pages):
            page_obj=pdf_reader.getPage(page)
            content=page_obj.extractText()
            write_content = text_file.write(content)

    def get_file_path(self):

        return self.file_url
    def fields_data(self):

         file_location=os.path.join(os.getcwd(),'media','text')
         with open(file_location,'r+') as fl:
             i=0
             for line in fl:
                 po_s = re.search(r'PURCHASE (\S+)', line)
                 gst_s = re.search(r'www.nelsonglobalproducts.comGSTIN (\S+)', line)
                 invoice_date_s = re.search(r'NO.: (\S+)', line)
                 #vendor_code= directly assign the constant value
                 part_no_s = re.search(r'MEASUREQTYRATE (\S+)', line)
                 HSN_s = re.search(r'VALUE (\S+)', line)
                 invoice_value_s = re.search(r'REMOVAL`TOTAL (\S+)', line)
                 #igst_s=re.search(r'TotalAmount', line)
                 #igst_amt_s = re.search(r'TotalAmount', line)
                 invoice_num_s = re.search(r'Page (\s+)', line)
                 part_qty_s=re.search(r'Total', line)
                 """rate_per_qty_s=re.search(r'Total', line)
                 net_rate_s=re.search(r'Total', line)
                 tax_category_s=re.search(r'TotalAmount', line)
                 word_list = line.split()
                 temp_cat = word_list[word_list.index("TotalAmount") - 8]
                 offset = 0

                 if 'gst' not in temp_cat.lower():
                     offset = 1
                 #print(po_s.group(0))"""
                 try:
                    if po_s:
                        word_list=line.split()
                        print(word_list)
                        po_no_s=word_list[word_list.index("PURCHASE")+4]
                        po_len=len(po_no_s)-4
                        po_no=po_no_s[0:po_len]
                        print("Po number is: "*20,po_no)
                    else:
                        print("Not found"*30)


                 except:
                    print("Po Number Not Found")
                 try:
                    if gst_s:
                        #print("Gst line is: ",gst_s)
                        word_list=line.split()
                        gst_no=word_list[word_list.index("www.nelsonglobalproducts.comGSTIN")+2]
                        print("Gst is: "*20,gst_no)
                        #print(word_list)
                 except:
                     print("GST Number not found")
                 try:
                    if invoice_date_s:
                        word_list = line.split()
                        invoice_date_format= word_list[word_list.index("NO.:")+3][0:11]
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
                 # except:
                 #     print("Invoice date not found")
                        out = m[s]
                        invoice_date=invoice_date_rep.replace(newdate,out)

                        #print("m"*10,invoice_date)
                 except:
                     print("Exception handeled")


                 try:
                    if part_no_s:
                        word_list = line.split()
                        part_no_line = word_list[word_list.index("MEASUREQTYRATE") + 3]
                        second_half=part_no_line[30:len(part_no_line)]
                        init_index=second_half.find('(')+1
                        last_index=second_half.find(')')
                        #a = "samesame"
                        #init_index=[i for i, n in enumerate(part_no_line) if n == '('][1]
                        part_no=second_half[init_index:last_index]
                        print("part no: : "*20, part_no)
                    else:
                        print("Not found "*20)
                 except:
                     print("part number not found")
                 try:
                    if HSN_s:
                        word_list = line.split()
                        HSN_no = word_list[word_list.index("VALUE") +1][54:62]

                        #print("HSN NO : "*50, HSN_no)
                 except:
                     print("HSN Number not found")
                 try:
                    if invoice_value_s:
                        word_list = line.split()
                        total_amt = word_list[( word_list.index("REMOVAL`TOTAL") ) +1]
                        str_len=len(total_amt)
                        last_index=str_len-9
                        invoice_amts=total_amt[11:last_index]
                        #invoice_amt=invoice_amts.replace(",","")

                        print("TotalAmount "*30, invoice_amts)

                 except:
                     print("Invoice value not found")
                 """try:
                    if tax_category_s:
                        word_list = line.split()
                        tax_cat=word_list[( word_list.index("TotalAmount") - offset ) - 8]

                        if 'gst' not in tax_cat.lower():
                            tax_cat = word_list[( word_list.index("TotalAmount") - offset ) - 9]

                        my_len=len(tax_cat)
                        init_len=my_len-5
                        #code for differentiate tax categories
                 except Exception as e:
                     print("tax category not found: ", repr(e))
                 try:
                    if igst_s and tax_cat[init_len:my_len]=='I-Gst':
                        word_list = line.split()
                        igst_rate_act = word_list[( word_list.index("TotalAmount") - offset ) -7][0:2]
                        igst=igst_rate_act.replace("%","")
                        #print("%"*50,igst)
                        igst_rate=igst+".00"
                        sgst_rate="0.00"
                        cgst_rate="0.00"
                        sgst_amt="0.00"
                        cgst_amt="0.00"
                    elif igst_s and tax_cat[init_len:my_len]=='S-Gst':
                        word_list = line.split()
                        sgst_rate_act = word_list[( word_list.index("TotalAmount") - offset ) - 7][0:2]
                        sgst = sgst_rate_act.replace("%", "")
                        sgst_rate = sgst + ".00"
                        #print("%" * 50, sgst_rate)

                        cgst_rate_act=word_list[( word_list.index("TotalAmount") - offset ) - 13]
                        #print("#"*20,cgst_rate_act)
                        cgst=cgst_rate_act.replace('%','')
                        cgst_rate=cgst+".00"
                        #print("@"*30,cgst_rate)

                        #code for sgst amt
                        sgst_amt_act = word_list[( word_list.index("TotalAmount") - offset ) - 8]
                        total_len=len(sgst_amt_act)-5
                        sgst_amt=sgst_amt_act[0:total_len]
                        #print("+"*20,sgst_amt)

                        #code for cgst amt
                        cgst_amt_act = word_list[( word_list.index("TotalAmount") - offset ) - 14]
                        total_len = len(cgst_amt_act) - 5
                        cgst_amt = cgst_amt_act[0:total_len]
                        #print("o" * 20, cgst_amt)

                        igst_rate = "0.00"
                        igst_amt='0.00'
                 except:
                     print("Exception handeled")



                 # else:
                 #     igst_rate="0.00"
                 #     cgst_rate="0.00"
                 #     sgst_rate="0.00"

                     #print("igst% : ", igst_rate)
                 try:
                    if igst_amt_s and tax_cat[init_len:my_len]=='I-Gst':
                        word_list = line.split()
                        igst_amt_with_len = word_list[( word_list.index("TotalAmount") - offset ) -8]
                        word_len=len(igst_amt_with_len)
                        actual_len=word_len-5
                        igst_amts=igst_amt_with_len[0:actual_len]
                        igst_amt=igst_amts.replace(",","")
                        #print("IGST Amt: ", igst_amt)
                 except:
                     print("Exception regarding igst handeled")"""



                 try:
                    if invoice_num_s:
                        print("yes")
                        word_list = line.split()
                        invoice_num_with_len= word_list[word_list.index("DATE:") -1]
                        length_invoice=len(invoice_num_with_len)-7
                        # actual_len=length_invoice-7
                        invoice_num=invoice_num_with_len[0:length_invoice]
                        print("Invoice number: "*23, invoice_num)
                    else:
                        print("No")
                 except:
                     print("Invoice number not found")

             """
             try:
                if part_qty_s:
                    word_list=line.split()
                    part_qty_trimmed = word_list[word_list.index("Total") -3][0:3]
                    max_index=part_qty_trimmed.find('.')
                    part_qty=part_qty_trimmed[0:max_index]
                    #print("part No: "*
                    #print('::'*20,part_qty)

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
                     #gross_rate_format=part_qty_rate
                     gross_rate=part_qty_rate
                     #print("gross rate: "*20,gross_rate)
             except:
                 print("rate per qty not found")
             try:
                if net_rate_s:
                    word_list = line.split()
                    total_price= word_list[word_list.index("Total") - 2]
                    #print("Total price"*20,float(total_price))
                    round=total_price.replace(',','')
                    #print("round"*20,round)
                    price=float(round)
                    qty=float(part_qty)
                    net=price/qty
                    net_rate=format(net,'.2f')
                    #print("conversion successfull"*30,net_rate)
             except:
                 print("net rate not found")

         #print("here is all amount: ",invoice_num,igst_rate,invoice_amt,vendor_code,invoice_date)
         try:
            json_obj={
             'po_no': po_num,
             'gst_no' : gst_no,
             'invoice_date': invoice_date,
             'vendor_code':'N72071',
             'part_no': part_no,
             'hsn_no': HSN_no,
             'invoice_val': invoice_amt,
             'igst_rate': igst_rate,
             'igst_amt': igst_amt,
             'invoice_num': invoice_num,
             'part_qty':part_qty,
             'gross_rate': gross_rate,
             'net_rate':net_rate,
             'sgst_rate':sgst_rate,
             'cgst_rate':cgst_rate,
             'sgst_amt': sgst_amt,
             'cgst_amt': cgst_amt
            }
         except Exception as e:
             print(e)
             json_obj = {
                 'po_no': "NA",
                 'gst_no': "NA",
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
                 'cgst_amt': "NA"
             }
         data=json.dumps(json_obj)
         print("data is: ",data)
         return data"""










