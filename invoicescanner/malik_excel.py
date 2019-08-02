import json
import xlsxwriter
from xlrd import open_workbook
import os
#from win32com import client
class Data_parser:
    def __init__(self,excel_sheet_name_and_location):
        self.excel_sheet_name_and_location=excel_sheet_name_and_location

    def field_data_malik(self):
        book=open_workbook(self.excel_sheet_name_and_location)
        #book = open_workbook('/home/ujjwal/Downloads/tatabillformate.xlsx')
        #print("Found the data")
        sheet=book.sheet_by_index(0)
        key_col=1
        value_col=2
        keys={
            'invoice_num':   'Tax Invoice No ',
            'invoice_date':  'Date of Invoice',
            'vendor_code':   'Vendor code',
            'hsn_code':      'SAC Code ',
            'igst_rate':     'IGST @ 12%',
            'total_invoice_value': 'Total Invoice Value in Rs',
            'net_rate' :     'Basic price of service',
            'part_qty' :     'Nos. of Units',
        }
        #print("runing outside of for block")

        for row in range(sheet.nrows):
            #print("inside for loop")
            if sheet.cell(row, key_col).value == keys['invoice_num']:
                invoice_num = sheet.cell_value(rowx=row, colx=value_col)
                print("Invoice number is found: "*5,invoice_num)
                #return invoice_num

            if sheet.cell(row, key_col).value == keys['invoice_date']:
                invoice_date = sheet.cell_value(rowx=row, colx=value_col)
                print("Invoice date found: "*5,invoice_date)

            if sheet.cell(row, key_col).value == keys['vendor_code']:
                vendor_code = sheet.cell_value(rowx=row, colx=value_col)
                print("Vendor code is found: "*5,vendor_code)

            if sheet.cell(row, key_col).value == keys['hsn_code']:
                hsn_code = sheet.cell_value(rowx=row, colx=value_col)
                print("hsn code found: "*5,hsn_code)

            if sheet.cell(row, key_col).value == keys['igst_rate']:
                igst_value = sheet.cell_value(rowx=row, colx=value_col+8)
                print("IGST value found: "*5,igst_value)

            if sheet.cell(row,key_col).value ==keys['total_invoice_value']:
                total_invoice_value=sheet.cell_value(rowx=row,colx=value_col+8) #we get total ammount in 10th column of the excell sheet so 2+8 where value_col is 2
                print("Total Invoice value: "*5,total_invoice_value)
            if sheet.cell(row,key_col).value ==keys['net_rate']:
                net_rate=sheet.cell_value(rowx=row,colx=value_col)
                gross_rate=net_rate
                print("Gross rate found: "*5,gross_rate)


            if sheet.cell(row,key_col+4).value ==keys['part_qty']:
                part_qty=sheet.cell_value(rowx=row+1,colx=key_col+4)
                print("part qty found: "*5,part_qty)

        try:
                json_obj = {
                    'po_no': "No",
                    'gst_no': "Not found",
                    'invoice_date': invoice_date,
                    'vendor_code': vendor_code,
                    'part_no': "No",
                    'hsn_no': hsn_code,
                    'invoice_val': total_invoice_value,
                    'igst_rate': '12.00',
                    'igst_amt': igst_value,
                    'invoice_num': invoice_num,
                    'part_qty': part_qty,
                    'gross_rate': net_rate,
                    'net_rate': net_rate,
                    'sgst_rate': "0.00",
                    'cgst_rate': "0.00",
                    'sgst_amt': "0.00",
                    'cgst_amt': "0.00",
                    'po_order_item_no': "No"
                }
                print(json_obj)
        except Exception as e:
            print("exception handeled: ", e)
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
                    'po_order_item_no': 10
                }
            #print("data before dumped into json: ",js)
        data = json.dumps(json_obj)
        print("Returned data is: "*10,data)
        return data

    def convert_to_pdf(self):
        print("This method is responsible for converting excel to pdf")



    def paste_qrcode_on_excel(self):
        print("this method is for pasting qrcode on excell sheet")
        workbook = xlsxwriter.Workbook(self.excel_sheet_name_and_location)
        worksheet = workbook.add_worksheet()

        # Widen the first column to make the text clearer.
        #worksheet.set_column('A:A', 30)

        # Insert an image.
        #worksheet.write('A2', 'Insert an image in a cell:')
        qrcode_img=os.path.join(os.getcwd(), 'qrcode')
        worksheet.insert_image('B56', qrcode_img)
        print("QR code pasted on excell sheet \n file name is:",self.excel_sheet_name_and_location)



