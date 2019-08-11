import csv

csv_headers = ['PoNumber', 'PO Item No', 'Quantity', 'Vendor Challan No', 'Challan Date', 'Gross Rate', 'Net PO Rate',
               'Basic value', 'Taxable value', 'SGST VALUE', 'CGST VALUE', 'IGST VALUE', 'SGST RATE', 'CGST RATE',
               'IGST RATE', 'Packing Amount', 'Freight Amount', 'Others Amount', 'INVOICE VALUE', 'Currency',
               'ROAD PERMIT NO', '57F4 NUMBER', '57F4 NO DATE', 'GSTIN Number', 'Vehicle Number', 'DRG REV Level',
               'COP Certificate', 'Certificate Date', 'TML GSTIN']


class ASNGenerator:
    @staticmethod
    def generate_asn_file(file_path, csv_row):
        csv_data = []
        csv_data.append(csv_headers)
        csv_data.append(csv_row)

        with open(file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)
        csv_file.close()
