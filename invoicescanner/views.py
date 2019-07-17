import datetime
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import pyqrcode
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from invoicescanner.nelson_pdf_to_text import *
from invoicescanner.pdf_to_text import *
from django.template import loader
import os
from django.core.files.storage import FileSystemStorage
import json
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
file_path=""


def upload(request):

    context = {}
    content = ""

    if request.method=='POST':
        global uploaded_file
        uploaded_file=request.FILES['doccument']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        global file_path
        file_path = os.path.join(os.getcwd(),'media',name)
        """obj=Text_Converter(file_path)
        obj.convert_pdf_to_text()
        #obj.pdf_to_string()
        obj.fields_data()
        obj.convert_pdf_to_text()"""
        file_location = os.path.join(os.getcwd(), 'media', 'text')
        if 'Nelson' in open(file_location).read():
            obj=Text_Converter_nel(file_path)
            obj.convert_pdf_to_text_nel()
            obj.fields_data_nel()
            # print("nelson found"*20)
        else:
            obj=Text_Converter(file_path)
            obj.convert_pdf_to_text()
            obj.fields_data()
            # print("bagwati found"*20)
        if uploaded_file.name!="doccument":
             return HttpResponseRedirect('fields')
    return render(request,'index.html')


def fields(request):
    template = loader.get_template('fields.html')
    #creating object of pdf_to_text.py file so we can get json data returned by field_data from Text_converter class
    data=" "
    file_location = os.path.join(os.getcwd(), 'media', 'text')
    if 'Nelson' in open(file_location).read():
        obj = Text_Converter_nel(file_path)
        #obj.convert_pdf_to_text_nel()
        data=obj.fields_data_nel()
        print("nelson found " * 20)
        # return HttpResponse(template.render(data))
    else:
        obj = Text_Converter(file_path)
        #obj.convert_pdf_to_text()
        data=obj.fields_data()
        print("bagwati found " * 20)
        print(data)
        # return HttpResponse(template.render(data))
    # obj=Text_Converter(file_path)
    # data=obj.fields_data()

    # data=filter()
    print("#"*20,data)
    json_data=json.loads(data)
    rendata={
        'Po_No':json_data["po_no"],
        'invoice_no': json_data['invoice_num'],
        'invoice_date': json_data['invoice_date'],
        'vendor_code': json_data['vendor_code'],

        'part_no': json_data['part_no'],
        'igst_amt':json_data['igst_amt'],
        'igst_rate':json_data['igst_rate'],
        'total_inv_val': json_data['invoice_val'],
        'hsn_no':json_data['hsn_no'],
        'ord_item_no': "10",
        'part_qty': json_data['part_qty'],
        'gross_rate': json_data['gross_rate'],
        'net_rate':json_data['net_rate'],
        'sgst_rate':json_data['sgst_rate'],
        'cgst_rate':json_data['cgst_rate'],
        'sgst_amt':json_data['sgst_amt'],
        'cgst_amt': json_data['cgst_amt'],
        'ugst_rate':'0.00',
        'ugst_value':'0.00',
        'cess':'0.00'


    }

    return HttpResponse(template.render(rendata))
@csrf_exempt
def qr_generator(request):

    po_no=request.POST.get('po', None)
    item_no=request.POST.get('item_no',None)
    part_qty=request.POST.get('part_qty',None)
    gross_rate=request.POST.get('gross_rate',None)
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
    #print("data from qr: ",po_no)
    datalist = [po_no, item_no,part_qty,inv_no,inv_date,gross_rate,net_rate,vendor_code,part_no,cgst_value,sgst_value,igst_value,ugst_value,cgst_rate,sgst_rate,igst_rate,ugst_rate,cess,invoice_value,HSN_code]
    # adding 0.00 as default value for blank fields
    for n, i in enumerate(datalist):
        if i=="":
            datalist[n] ="0.00"
    data=",".join(datalist)
    print("data for qr code is: ",data)

    file_location = os.path.join(os.getcwd(), 'media', 'text')
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
            base_name = "Nelson_invoice_"
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
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
            base_name = "bhagwati_invoice_"
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            now_time = "".join(time)
            res_file_name = base_name + now_time
            base_name = os.path.join(os.getcwd(), 'media', 'result', res_file_name)
        resultPdfFile = open(base_name, 'wb')
        pdfWriter.write(resultPdfFile)
        watermarkFile.close()
        minutesFile.close()
        resultPdfFile.close()



    template=loader.get_template("fields.html")
    link = 'http://{}/{}'.format(request.get_host(), base_name)
    data={
         'pdf_name':res_file_name,
      }

    #extra code added

    #code ends here

    return HttpResponse(template.render(data))

# code for downloading result pdf file
"""def pdf_view(request):
    fs = FileSystemStorage()
    filename = 'bhagwati_invoice.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')"""