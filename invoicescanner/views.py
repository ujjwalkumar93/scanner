# import datetime
from datetime import datetime

import pyqrcode
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from tabula import *

from invoicescanner.arn_csv_generator import ARNGenerator
from invoicescanner.hindustan_brush import *
from invoicescanner.nelson_pdf_to_text import *
from invoicescanner.pdf_to_text import *
from invoicescanner.perfectpackingPdf_to_text import *

file_path = ""


def upload(request):
    context = {}
    content = ""

    if request.method == 'POST':
        global uploaded_file
        uploaded_file = request.FILES['doccument']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        global file_path
        # code for identify file extension name
        if name.endswith('.xlsx'):
            file_location = os.path.join(os.getcwd(), 'media', 'text')
            text_file = open(file_location, 'w')
            text_file.write("Excel file")
            print("Excell sheet found - ", name)
        else:
            print("PDF found " * 10, name)
            file_path = os.path.join(os.getcwd(), 'media', name)
            file_obj = open(file_path, 'rb')
            pdf_reader = PyPDF2.PdfFileReader(file_obj)
            total_pages = pdf_reader.numPages
            # print("Total number of pages: ",total_pages)
            page_obj = pdf_reader.getPage(0)
            content = page_obj.extractText()
            file_location = os.path.join(os.getcwd(), 'media', 'text')
            text_file = open(file_location, 'w')
            write_content = text_file.write(str(content.encode('utf-8')))
            tabula_text_file_location = os.path.join(os.getcwd(), 'media', 'tabula_text')
            tabula_text_file = open(tabula_text_file_location, 'w+', encoding='ascii', errors='ignore')
            df = read_pdf(file_path, pages="1")
            # tabula_text_file.truncate(0)
            df.to_csv(tabula_text_file, sep='\t')
        if uploaded_file.name != "doccument":
            return HttpResponseRedirect('fields')
    return render(request, 'index.html')


def fields(request):
    template = loader.get_template('fields.html')
    # creating object of pdf_to_text.py file so we can get json data returned by field_data from Text_converter class
    data = " "
    file_location = os.path.join(os.getcwd(), 'media', 'text')
    if 'Nelson' in open(file_location).read():
        obj = Text_Converter_nel(file_path)
        data = obj.fields_data_nel()
        print("nelson found " * 3, data)

        # return HttpResponse(template.render(data))

    elif 'HINDUSTAN' in open(file_location).read():
        obj = Text_Converter_hindustan(file_path)
        data = obj.fields_data_hindustan()
        print("Hindustan Found " * 3)



    else:
        obj = Text_Converter(file_path)
        data = obj.fields_data()
        print("bagwati found " * 3)
        print(data)

    print("#" * 20, data)
    json_data = json.loads(data)
    rendata = {
        'Po_No': json_data["po_no"],
        'invoice_no': json_data['invoice_num'],
        'invoice_date': json_data['invoice_date'],
        'vendor_code': json_data['vendor_code'],
        'gst_no': json_data['gst_no'],
        'part_no': json_data['part_no'],
        'igst_amt': json_data['igst_amt'],
        'igst_rate': json_data['igst_rate'],
        'total_inv_val': json_data['invoice_val'],
        'hsn_no': json_data['hsn_no'],
        'ord_item_no': json_data['po_order_item_no'],
        'part_qty': json_data['part_qty'],
        'gross_rate': json_data['gross_rate'],
        'net_rate': json_data['net_rate'],
        'sgst_rate': json_data['sgst_rate'],
        'cgst_rate': json_data['cgst_rate'],
        'sgst_amt': json_data['sgst_amt'],
        'cgst_amt': json_data['cgst_amt'],
        'ugst_rate': '0.00',
        'ugst_value': '0.00',
        'cess': '0.00'

    }

    return HttpResponse(template.render(rendata))


@csrf_exempt
def qr_generator(request):
    po_no = request.POST.get('po', None)
    gst_no = request.POST.get('gst_no', None)
    item_no = request.POST.get('item_no', None)
    part_qty = request.POST.get('part_qty', None)
    gross_rate = request.POST.get('gross_rate', None)
    net_rate = request.POST.get('net_rate', None)
    cgst_value = request.POST.get('cgst_value', None)
    sgst_value = request.POST.get('sgst_value', None)
    ugst_value = request.POST.get('ugst_value', None)
    cgst_rate = request.POST.get('cgst_rate', None)
    sgst_rate = request.POST.get('sgst_rate', None)
    ugst_rate = request.POST.get('ugst_rate', None)
    cess = request.POST.get('cess', None)
    inv_no = request.POST.get('inv_no', None)
    inv_date = request.POST.get('inv_date', None)
    vendor_code = request.POST.get('vendor_code', None)
    part_no = request.POST.get('part_no', None)
    igst_value = request.POST.get('igst_value', None)
    igst_rate = request.POST.get('igst_rate', None)
    invoice_value = request.POST.get('invoice_value', None)
    HSN_code = request.POST.get('HSN_code', None)

    datalist = [po_no, item_no, part_qty, inv_no, inv_date, gross_rate, net_rate, vendor_code, part_no, cgst_value,
                sgst_value, igst_value, ugst_value, cgst_rate, sgst_rate, igst_rate, ugst_rate, cess, invoice_value,
                HSN_code]
    # adding 0.00 as default value for blank fields
    for n, i in enumerate(datalist):
        if i == "":
            datalist[n] = "0.00"
    data = ",".join(datalist)
    print("data for qr code is: ", data)
    file_location = os.path.join(os.getcwd(), 'media', 'text')
    base_name = uploaded_file.name.strip('.pdf') + '_' if uploaded_file and uploaded_file.name else ''
    res_file_name = base_name

    if 'Nelson' in open(file_location).read():
        qr = pyqrcode.create(data)
        qr.svg("qrcode", scale=1.1)
        # writing code to get location on QRCode
        qrcode_path = os.path.join(os.getcwd(), 'qrcode')
        drawing = svg2rlg(qrcode_path)
        scaleFactor = 1
        drawing.width *= scaleFactor
        drawing.height *= scaleFactor
        drawing.scale(scaleFactor, scaleFactor)
        drawing.shift(410, -655)
        # creating qrcode on blank pdf so later we can merge as watermark on origional pdf
        renderPDF.drawToFile(drawing, "qrpdf.pdf", autoSize=0)
        blank_pdf_qr = os.path.join(os.getcwd(), 'qrpdf.pdf')
        watermarkFile = open(blank_pdf_qr, 'rb')
        pdfWatermarkReader = PyPDF2.PdfFileReader(watermarkFile)
        minutesFile = open(file_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(minutesFile)
        pdfWriter = PyPDF2.PdfFileWriter()
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pageObj.mergePage(pdfWatermarkReader.getPage(0))
            pdfWriter.addPage(pageObj)

        base_name = "Nelson_invoice_" if not base_name else base_name
        now = datetime.now()
        time = now.strftime("%H_%M_%S")
        now_time = "".join(time)
        res_file_name = base_name + now_time
        base_name = os.path.join(os.getcwd(), 'media', 'result', res_file_name)
        resultPdfFile = open(base_name, 'wb')
        pdfWriter.write(resultPdfFile)
        watermarkFile.close()
        minutesFile.close()
        resultPdfFile.close()

        # code printing qrcode on invoice

    elif 'HINDUSTAN' in open(file_location).read():
        qr = pyqrcode.create(data)
        qr.svg("qrcode", scale=1.1)
        # writing code to get location on QRCode
        qrcode_path = os.path.join(os.getcwd(), 'qrcode')
        drawing = svg2rlg(qrcode_path)
        scaleFactor = 1
        drawing.width *= scaleFactor
        drawing.height *= scaleFactor
        drawing.scale(scaleFactor, scaleFactor)
        drawing.shift(70, -470)
        # creating qrcode on blank pdf so later we can merge as watermark on origional pdf
        renderPDF.drawToFile(drawing, "qrpdf.pdf", autoSize=0)
        blank_pdf_qr = os.path.join(os.getcwd(), 'qrpdf.pdf')
        watermarkFile = open(blank_pdf_qr, 'rb')
        pdfWatermarkReader = PyPDF2.PdfFileReader(watermarkFile)
        minutesFile = open(file_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(minutesFile)
        pdfWriter = PyPDF2.PdfFileWriter()
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pageObj.mergePage(pdfWatermarkReader.getPage(0))
            pdfWriter.addPage(pageObj)

        base_name = "Hindustan" if not base_name else base_name
        now = datetime.now()
        time = now.strftime("%H_%M_%S")
        now_time = "".join(time)
        res_file_name = base_name + now_time
        base_name = os.path.join(os.getcwd(), 'media', 'result', res_file_name)
        resultPdfFile = open(base_name, 'wb')
        pdfWriter.write(resultPdfFile)
        watermarkFile.close()
        minutesFile.close()
        resultPdfFile.close()

    else:
        qr = pyqrcode.create(data)
        qr.svg("qrcode", scale=1.1)
        # writing code to get location on QRCode
        qrcode_path = os.path.join(os.getcwd(), 'qrcode')
        drawing = svg2rlg(qrcode_path)
        scaleFactor = 1
        drawing.width *= scaleFactor
        drawing.height *= scaleFactor
        drawing.scale(scaleFactor, scaleFactor)
        drawing.shift(200, -605)
        # creating qrcode on blank pdf so later we can merge as watermark on origional pdf
        renderPDF.drawToFile(drawing, "qrpdf.pdf", autoSize=0)
        blank_pdf_qr = os.path.join(os.getcwd(), 'qrpdf.pdf')
        watermarkFile = open(blank_pdf_qr, 'rb')
        pdfWatermarkReader = PyPDF2.PdfFileReader(watermarkFile)
        minutesFile = open(file_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(minutesFile)

        pdfWriter = PyPDF2.PdfFileWriter()
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pageObj.mergePage(pdfWatermarkReader.getPage(0))
            pdfWriter.addPage(pageObj)

        base_name = "bhagwati_invoice_" if not base_name else base_name
        now = datetime.now()
        time = now.strftime("%H_%M_%S")
        now_time = "".join(time)
        res_file_name = base_name + now_time
        base_name = os.path.join(os.getcwd(), 'media', 'result', res_file_name)

        resultPdfFile = open(base_name, 'wb')
        pdfWriter.write(resultPdfFile)
        watermarkFile.close()
        minutesFile.close()
        resultPdfFile.close()

    csv_file_name = os.path.join(os.getcwd(), 'media', 'result', (res_file_name + '.csv'))
    basic_taxable_cost = format(float(part_qty) * float(net_rate), '.2f').replace(",", "")
    csv_row = [po_no, item_no, part_qty, inv_no, inv_date, gross_rate, net_rate, basic_taxable_cost, basic_taxable_cost,
               sgst_value, cgst_value,
               igst_value, sgst_rate, cgst_rate, igst_rate, '0', '0', '0', invoice_value, 'INR', '', '', '', gst_no, '',
               '',
               '', '', '27AAACT2727Q1ZW']
    ARNGenerator.generate_arn_file(csv_file_name, csv_row)
    template = loader.get_template("fields.html")
    link = 'http://{}/{}'.format(request.get_host(), base_name)
    data = {
        'pdf_name': res_file_name,
    }

    return HttpResponse(template.render(data))
