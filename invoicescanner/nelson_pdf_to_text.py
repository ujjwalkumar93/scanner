from __future__ import division

import PyPDF2
import json
import os
import re


class Text_Converter_nel:

    def __init__(self, file_url):
        self.file_url = file_url
        # print("file url is: ",self.file_url)

    def fields_data_nel(self):
        file_location = os.path.join(os.getcwd(), 'media', 'text')
        with open(file_location, 'r+') as fl:
            i = 0
            for line in fl:
                po_s = re.search(r'PURCHASE|PURCHASE (\S+)', line, re.IGNORECASE)
                gst_s = re.search(r'www.nelsonglobalproducts.comGSTIN|www.nelsonglobalproducts.comGSTIN (\S+)', line,
                                  re.IGNORECASE)
                invoice_date_s = re.search(r'NO.:|NO.: (\S+)', line, re.IGNORECASE)
                part_no_s = re.search(r'MEASUREQTYRATE|MEASUREQTYRATE (\S+)', line, re.IGNORECASE)
                HSN_s = re.search(r'VALUE|VALUE (\S+)', line, re.IGNORECASE)
                invoice_value_s = re.search(r'REMOVAL`TOTAL|REMOVAL`TOTAL (\S+)', line, re.IGNORECASE)
                invoice_num_s = re.search(r'Page|Page (\S+)', line, re.IGNORECASE)
                sgst_amt_s = re.search(r'PACKING|PACKING ', line, re.IGNORECASE)

                # print("Vendor code "*2,vendor_code_s)

                try:
                    if po_s:
                        word_list = line.split()
                        # print(word_list)
                        po_no_s = word_list[word_list.index("PURCHASE") + 4]
                        po_len = len(po_no_s) - 4
                        po_no = po_no_s[0:po_len]
                        print("Po number is: " * 3, po_no)

                except:
                    po_no = "Not found"
                    print("Po Number Not Found")

                try:
                    if gst_s:
                        # print("Gst line is: ",gst_s)
                        word_list = line.split()
                        gst_no = word_list[word_list.index("www.nelsonglobalproducts.comGSTIN") + 2]
                        # print("Gst is: "*20,gst_no)
                        # print(word_list)
                except:
                    gst_no = "Not found"
                    print("GST Number not found")

                try:
                    if invoice_date_s:
                        word_list = line.split()
                        invoice_date_format = word_list[word_list.index("NO.:") + 3][0:11]
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
                    invoice_date = "Not found"
                    print("Exception handeled")

                try:
                    if part_no_s:
                        word_list = line.split()
                        part_no_line = word_list[word_list.index("MEASUREQTYRATE") + 3]
                        second_half = part_no_line[30:len(part_no_line)]
                        init_index = second_half.find('(') + 1
                        last_index = second_half.find(')')
                        part_no = second_half[init_index:last_index]

                except:
                    part_no = "Not found"
                    print("part number not found")

                try:
                    if HSN_s:
                        word_list = line.split()
                        HSN_no = word_list[word_list.index("VALUE") + 1][54:62]
                except:
                    HSN_no = "Not found"
                    print("HSN Number not found")

                try:
                    if invoice_value_s:
                        word_list = line.split()
                        total_amt = word_list[(word_list.index("REMOVAL`TOTAL")) + 1]
                        str_len = len(total_amt)
                        last_index = str_len - 9
                        invoice_amts = total_amt[11:last_index]
                        # print("TotalAmount "*30, invoice_amts)
                except:
                    invoice_amts = "Not found"
                    print("Invoice value not found")

                try:
                    if invoice_num_s:
                        print("yes")
                        word_list = line.split()
                        invoice_num_with_len = word_list[word_list.index("DATE:") - 1]
                        length_invoice = len(invoice_num_with_len) - 7
                        invoice_num = invoice_num_with_len[0:length_invoice]
                        print("Invoice number: " * 23, invoice_num)

                except:
                    invoice_num = "Not found"
                    print("Invoice number not found")
        # code for getting complex data
        file_location = os.path.join(os.getcwd(), 'media', 'tabula_text')
        with open(file_location, 'r+') as fl:
            i = 0
            for line in fl:
                part_qty_s = re.search(r'Page Total', line)
                multiple_data_s = re.search(r'Ea (\S)', line)
                vendor_code_s = re.search(r'Vendor Code|Vendor Code |Vendor Code:(\S+)', line, re.IGNORECASE)

                try:
                    if vendor_code_s:
                        word_list = line.split()
                        print("Vendor code wordlist is: " * 5, word_list)
                        vendor_code = word_list[word_list.index("MOTORS") + 3].replace(")", '')
                        print("vendor code is: " * 5, vendor_code)
                    else:
                        vendor_code = "C66270"
                except:
                    vendor_code = "C66270"
                    print("vendor code not found...")

                try:
                    if part_qty_s:
                        # print("Yes found")
                        word_list = line.split()
                        # print("word list is: ",word_list)
                        part_qty = word_list[word_list.index("Total") + 1] + ".000"
                        # print("qty is: "*15,part_qty)
                except:
                    part_qty = "Not found"
                    print("Part qty not found")
                try:
                    if multiple_data_s:
                        word_list = line.split()
                        print("first line is: ", word_list)
                        # print('printing next line: ',next(line))
                        net_rate = gross_rate = word_list[word_list.index('Ea') + 2]
                        print("net rate = gross rate =" * 5, gross_rate)
                        cgst_rate = word_list[word_list.index('Ea') + 4] + ".00"
                        cgst_amt = word_list[word_list.index('Ea') + 5]
                        sgst_rate = word_list[word_list.index('Ea') + 6] + ".00"
                        sgst_amt = word_list[word_list.index('Ea') + 7]
                        datalist = [cgst_rate, cgst_amt, sgst_rate, sgst_amt]
                        print("type" * 5, type(cgst_amt))
                        print("datalist " * 5, datalist)
                        if cgst_rate == "0.00" and cgst_amt == "0.00" and sgst_rate == "0.00" and sgst_amt == "0.00":
                            print("yes came inside if block" * 5)
                            igst_rate = word_list[word_list.index('Ea') + 8] + ".00"
                            igst_amt = word_list[word_list.index('Ea') + 9]
                            cgst_amt = "0.00"
                            cgst_rate = "0.00"
                            sgst_rate = "0.00"
                            sgst_amt = "0.00"
                        else:
                            print("came in outer block" * 5)
                            cgst_rate = cgst_rate
                            cgst_amt = cgst_amt
                            sgst_rate = sgst_rate
                            sgst_amt = sgst_amt
                            igst_rate = "0.00"
                            igst_amt = "0.00"

                        # d=[net_rate,cgst_rate,cgst_amt,sgst_amt,sgst_rate,po_no,gst_no,invoice_date,part_no,HSN_no,invoice_amts]
                        # print("all data is: ",d)

                except:
                    # net_rate, cgst_rate, cgst_amt, sgst_amt, sgst_rate, po_no, gst_no, invoice_date, part_no, HSN_no, invoice_amts="NA"

                    print("multiple data exception handeled " * 3)

        try:
            json_obj = {
                'po_no': po_no,
                'gst_no': gst_no,
                'invoice_date': invoice_date,
                'vendor_code': vendor_code,
                'part_no': part_no,
                'hsn_no': HSN_no,
                'invoice_val': invoice_amts,
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
                'po_order_item_no': 10

            }
            print(json_obj)
        except Exception as e:
            print("exception handeled: ", e)
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
                'po_order_item_no': 10
            }
            # print(json_obj)
        data = json.dumps(json_obj)
        # print("data is: ",data)
        return data
