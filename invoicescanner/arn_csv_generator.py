import csv

csv_headers = ['PoNumber', 'PO Item No', 'Quantity', 'Vendor Challan No', 'Challan Date', 'Gross Rate', 'Net PO Rate',
               'Basic value', 'Taxable value', 'SGST VALUE', 'CGST VALUE', 'IGST VALUE', 'SGST RATE', 'CGST RATE',
               'IGST RATE', 'Packing Amount', 'Freight Amount', 'Others Amount', 'INVOICE VALUE', 'Currency',
               'ROAD PERMIT NO', '57F4 NUMBER', '57F4 NO DATE', 'GSTIN Number', 'Vehicle Number', 'DRG REV Level',
               'COP Certificate', 'Certificate Date', 'TML GSTIN']


class ARNGenerator:
    @staticmethod
    def generate_arn_file(file_path, csv_row):
        print ()
        print ()
        print (csv_row)
        print ()
        print ()
        print (csv_headers)
        print ()
        print ()
        csv_data = []
        csv_data.append(csv_headers)
        csv_data.append(csv_row)

        print (file_path)
        print ()
        print (csv_data)
        print ()
        print ()

        with open(file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)
        csv_file.close()


# ARNGenerator.generate_arn_file('temp.csv', ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','1','2','3','4','5','6','7','8','9','10','11','12'])