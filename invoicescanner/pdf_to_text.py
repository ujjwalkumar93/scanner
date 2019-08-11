from __future__ import division

import json
import os
import re


class Text_Converter:

    def __init__(self, file_url):
        self.file_url = file_url
        # print("file url is: ",self.file_url)

    def fields_data(self):
        file_location = os.path.join(os.getcwd(), 'media', 'text')
        with open(file_location, 'r+') as fl:
            i = 0
            for line in fl:
                try:
                    po_s = re.search(r'Terms|Terms (\S+)', line, re.IGNORECASE)
                    gst_s = re.search(r'GSTIN (\S+)', line)
                    invoice_date_s = re.search(r'MaharashtraDate (\S+)', line)
                    vendor_code_s = re.search(r':Reg.Type (\S+)', line)
                    part_no_s = re.search(r':Reg.Type (\S+)', line)
                    HSN_s = re.search(r'Total(\S+)', line)
                    invoice_value_s = re.search(r'TotalAmount|TotalAmount (\S+)', line, re.IGNORECASE)
                    # igst_s=re.search(r'TotalAmount|TotalAmount (\S+)', line,re.IGNORECASE)
                    # igst_amt_s = re.search(r'TotalAmount|TotalAmount (\S+)', line,re.IGNORECASE)
                    invoice_num_s = re.search(r'Challan', line)
                    part_qty_s = re.search(r'Total', line)
                    rate_per_qty_s = re.search(r'Total', line)
                    net_rate_s = re.search(r'Total', line)
                    tax_category_s = re.search(r'TotalAmount', line)
                    po_order_item_no_s = re.search(r'NO: (\S+)', line)
                    word_list = line.split()
                    temp_cat = word_list[word_list.index("TotalAmount") - 8]
                    offset = 0
                except:
                    print("exception handeled")
                try:
                    if 'gst' not in temp_cat.lower():
                        offset = 1
                except:
                    print("Exception handeled")
                # print(po_s.group(0))
                print("Po_s is " * 5, po_s)

                try:
                    if po_s:
                        word_list = line.split()
                        po_num = word_list[word_list.index("Terms") + 2][1:11]
                        # po_num=po_s.group(1)
                        print("po num is: ", po_num)

                except:
                    po_num = "NA"
                    print("Po Number Not Found")
                try:
                    if gst_s:
                        word_list = line.split()
                        gst_no = word_list[word_list.index("MaharashtraDate") - 6][21:36]
                except:
                    gst_no = "NA"
                    print("GST Number not found")
                try:
                    if invoice_date_s:
                        word_list = line.split()
                        invoice_date_format = word_list[word_list.index("MaharashtraDate") + 1][1:12]
                        invoice_date_rep = invoice_date_format.replace('-', '.')
                        newdate = invoice_date_rep[3:6]
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
                        out = m[s]
                        invoice_date = invoice_date_rep.replace(newdate, out)
                except:
                    invoice_date = "NA"
                    print("Exception handeled")

                try:
                    if vendor_code_s:
                        word_list = line.split()
                        vendor_code = word_list[word_list.index(":Reg.Type") + 4][0:6]
                        # print("vendor code: ", vendor_code)
                except:
                    vendor_code = "B64030"
                    print("vendor code not found")
                try:
                    if part_no_s:
                        word_list = line.split()
                        part_no = word_list[word_list.index(":Reg.Type") + 7][0:11]
                        # print("part no: : ", part_no)
                except:
                    part_no = "NA"
                    print("part number not found")
                try:
                    if HSN_s:
                        word_list = line.split()
                        HSN_no_len = word_list[word_list.index("Total") - 3]
                        length_hsn = len(HSN_no_len)
                        init_len = length_hsn - 8
                        HSN_no = HSN_no_len[init_len:length_hsn]
                        # print("HSN NO : ", HSN_no)
                except:
                    HSN_no = "NA"
                    print("HSN Number not found")
                try:
                    if invoice_value_s:
                        word_list = line.split()
                        total_amt = word_list[(word_list.index("TotalAmount")) - 1]
                        str_len = len(total_amt)
                        total_alpha = str_len - 5
                        invoice_amts = total_amt[0:total_alpha]
                        invoice_amt = invoice_amts.replace(",", "")
                except:
                    invoice_amt = "NA"
                    print("Invoice value not found")
                print("tax cat_s " * 10, tax_category_s)
                """try:
                   if tax_category_s:
                       word_list = line.split()
                       print("Print word lis is : ",word_list)
                       tax_cat=word_list[( word_list.index("TotalAmount") - offset ) - 8]

                       if 'gst' not in tax_cat.lower():
                           tax_cat = word_list[( word_list.index("TotalAmount") - offset ) - 9]

                       my_len=len(tax_cat)
                       init_len=my_len-5
                       #code for differentiate tax categories
                except Exception as e:
                    print("tax category not found: ", repr(e))
                print("taxt_cat "*5,tax_cat)
                try:
                   if igst_s and tax_cat[init_len:my_len]=='I-Gst':
                       print("yes found IGST "*20)
                       word_list = line.split()
                       igst_rate_act = word_list[( word_list.index("TotalAmount") - offset ) -7][0:2]
                       igst=igst_rate_act.replace("%","")
                       print("%"*50,igst)
                       igst_rate=igst+".00"
                       sgst_rate="0.00"
                       cgst_rate="0.00"
                       sgst_amt="0.00"
                       cgst_amt="0.00"
                   elif igst_s and tax_cat[init_len:my_len]=='S-Gst':
                       print("yes found SGST " * 20)
                       word_list = line.split()
                       sgst_rate_act = word_list[( word_list.index("TotalAmount") - offset ) - 7][0:2]
                       sgst = sgst_rate_act.replace("%", "")
                       sgst_rate = sgst + ".00"
                       cgst_rate_act=word_list[( word_list.index("TotalAmount") - offset ) - 13]
                       cgst=cgst_rate_act.replace('%','')
                       cgst_rate=cgst+".00"
                       #print("@"*30,cgst_rate)

                       #code for sgst amt
                       sgst_amt_act = word_list[( word_list.index("TotalAmount") - offset ) - 8]
                       total_len=len(sgst_amt_act)-5
                       sgst_amt=sgst_amt_act[0:total_len].replace(',','')
                       #print("+"*20,sgst_amt)

                       #code for cgst amt
                       cgst_amt_act = word_list[( word_list.index("TotalAmount") - offset ) - 14]
                       total_len = len(cgst_amt_act) - 5
                       cgst_amt = cgst_amt_act[0:total_len].replace(',','')
                       #print("o" * 20, cgst_amt)

                       igst_rate = "0.00"
                       igst_amt='0.00'
                except:
                    igst_amt = 'NA'
                    igst_rate = "NA"
                    sgst_rate = "NA"
                    cgst_rate = "NA"
                    sgst_amt = "NA"
                    cgst_amt = "NA"
                    print("Exception handeled")
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
                    igst_amt="NA"
                    print("Exception regarding igst handeled")"""

                try:
                    if invoice_num_s:
                        word_list = line.split()
                        invoice_num_with_len = word_list[word_list.index("Challan") - 2]
                        length_invoice = len(invoice_num_with_len)
                        actual_len = length_invoice - 7
                        invoice_num = invoice_num_with_len[12:actual_len]
                        # print("Invoice number: ", invoice_num)
                except:
                    invoice_num = "NA"
                    print("Invoice number not found")
                try:
                    if part_qty_s:
                        word_list = line.split()
                        part_qty_trimmed = word_list[word_list.index("Total") - 3][0:3]
                        max_index = part_qty_trimmed.find('.')
                        part_qty = part_qty_trimmed[0:max_index] + ".000"

                except:
                    part_qty = "NA"
                    print("part No notfound")
                try:
                    if rate_per_qty_s:
                        word_list = line.split()
                        part_qty_rate_full = word_list[word_list.index("Total") - 3]
                        first_point_pos = part_qty_rate_full.find('.')
                        init_length = first_point_pos + 3
                        full_len = len(part_qty_rate_full)
                        first_half = part_qty_rate_full[init_length:full_len]
                        secon_point_pos = first_half.find('.') + 3
                        part_qty_rate = first_half[0:secon_point_pos]
                        gross_rate = part_qty_rate
                        # print("gross rate: "*20,gross_rate)
                except:
                    gross_rate = "NA"
                    print("rate per qty not found")
                try:
                    if net_rate_s:
                        word_list = line.split()
                        total_price = word_list[word_list.index("Total") - 2]
                        # print("Total price"*20,float(total_price))
                        round = total_price.replace(',', '')
                        # print("round"*20,round)
                        price = float(round)
                        qty = float(part_qty)
                        net = price / qty
                        net_rate = format(net, '.2f').replace(",", "")
                        # print("conversion successfull"*30,net_rate)
                except:
                    print("net rate not found")
                """try:
                    if po_order_item_no_s:
                        word_list=line.split()
                        po_order_item_no=total_price= word_list[word_list.index("NO:") +1]
                        print("po order item no - ", po_order_item_no)
                except:
                    print("Po order not found"*20)
                    po_order_item_no="NA"""
                file_location = os.path.join(os.getcwd(), 'media', 'tabula_text')
                with open(file_location, 'r+') as fl:
                    i = 0
                    for line in fl:
                        po_order_item_no_s = re.search(r'ITEM NO:|ITEM NO :', line, re.IGNORECASE)
                        igst_tax_s = re.search(r'I-Gst|I-Gst ', line, re.IGNORECASE)
                        sgst_tax_s = re.search(r'S-Gst|S-Gst ', line, re.IGNORECASE)
                        cgst_tax_s = re.search(r'C-Gst|C-Gst ', line, re.IGNORECASE)
                        # print("po_order_item_no_s is: "*5,po_order_item_no_s)
                        try:
                            if po_order_item_no_s:
                                print("Yes found" * 10)
                                word_list = line.split()
                                # print("wordlist is "*5,word_list)
                                po_order_item_no = word_list[word_list.index("NO:") + 1]

                                print("Po order item no is - ", po_order_item_no)

                        except:
                            po_order_item_no = "NA"
                            print("Part qty not found")
                        try:
                            if igst_tax_s:
                                word_list = line.split()
                                # print("Word list is: ", word_list)
                                igst_rate = word_list[word_list.index("I-Gst") + 1].replace("%", ".00")
                                igst_amt = word_list[word_list.index("I-Gst") + 6].replace(",", "")
                                cgst_rate = "0.00"
                                sgst_rate = "0.00"
                                cgst_amt = "0.00"
                                sgst_amt = "0.00"
                                print("Igst is - ", igst_amt)
                        except:
                            igst_rate = "NA"
                            igst_amt = "NA"
                            print("Tax exception handeled")
                        try:
                            if sgst_tax_s:
                                word_list = line.split()
                                # print("wordlist " * 5, word_list)
                                sgst_rate = word_list[word_list.index("S-Gst") + 1].replace("%", ".00")
                                sgst_amt = word_list[word_list.index("S-Gst") + 6].replace(",", "")
                                igst_amt = "0.00"
                                igst_rate = "0.00"
                        except:
                            sgst_rate = "NA"
                            sgst_amt = "NA"
                        try:
                            if cgst_tax_s:
                                word_list = line.split()
                                cgst_rate = word_list[word_list.index("C-Gst") + 1].replace("%", ".00")
                                cgst_amt = word_list[word_list.index("C-Gst") + 6].replace(",", "")
                        except:
                            cgst_amt = "NA"
                            cgst_rate = "NA"

            # print("here is all amount: ",invoice_num,igst_rate,invoice_amt,vendor_code,invoice_date)
            try:
                if not vendor_code:
                    vendor_code = "B64030"
                json_obj = {
                    'po_no': po_num,
                    'gst_no': gst_no,
                    'invoice_date': invoice_date,
                    'vendor_code': vendor_code,
                    'part_no': part_no,
                    'hsn_no': HSN_no,
                    'invoice_val': invoice_amt,
                    'igst_rate': igst_rate,
                    'igst_amt': igst_amt,
                    'invoice_num': invoice_num,
                    'part_qty': part_qty,
                    'gross_rate': gross_rate,
                    'net_rate': net_rate,
                    'sgst_rate': sgst_rate,
                    'cgst_rate': cgst_rate,
                    'sgst_amt': sgst_amt,
                    'cgst_amt': cgst_amt,
                    'po_order_item_no': po_order_item_no

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
                    'cgst_amt': "NA",
                    'po_order_item_no': 'NA'

                }
            data = json.dumps(json_obj)
            # print("data is: ", data)
            return data
