from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import pyqrcode
from django.views.decorators.csrf import csrf_exempt

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
        print("#######################################")
        global file_path
        file_path = os.path.join(os.getcwd(),'media',name)
        print(file_path)
        print("****************************************")
        print(uploaded_file.name)
        print("==========================================")
        obj=Text_Converter(file_path)
        obj.convert_pdf_to_text()
        obj.fields_data()
        obj.convert_pdf_to_text()
        if uploaded_file.name!="doccument":
             return HttpResponseRedirect('fields')
    return render(request,'index.html')
def fields(request):
    template = loader.get_template('fields.html')
    print("code runs well....")
    obj=Text_Converter(file_path)

    #print("object is:"*60,file_path)
    data=obj.fields_data()
    print("code runs well....")
    json_data=json.loads(data)
    print("code runs well....")
    #print("data is :",json_data)
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

    }

    #print("context: ",RequestContext(request))
    return HttpResponse(template.render(rendata))
@csrf_exempt
def qr_generator(request):

    po_no=request.POST.get('po', None)
    item_no=request.POST.get('item_no',None)
    inv_no = request.POST.get('inv_no', None)
    inv_date = request.POST.get('inv_date', None)
    vendor_code = request.POST.get('vendor_code', None)
    part_no = request.POST.get('part_no', None)
    igst_value = request.POST.get('igst_value', None)
    igst_rate = request.POST.get('igst_rate', None)
    invoice_value = request.POST.get('invoice_value', None)
    HSN_code = request.POST.get('HSN_code', None)
    #print("data from qr: ",po_no)

    datalist=[po_no,item_no,inv_no,inv_date,vendor_code,part_no,igst_value,igst_rate,invoice_value,HSN_code]
    data=",".join(datalist)
    print("list is: ",datalist)
    qr=pyqrcode.create(data)
    #qr.png("qrcode")
    qr.svg("qrcode", scale=.8)
    #writing code to get location on QRCode
    qrcode_path=os.path.join(os.getcwd(),'qrcode')
    print("path for qrcode is: ",qrcode_path)
    #convert qrcode in blank pdf with qrcode in footer
    drawing = svg2rlg(qrcode_path)
    scaleFactor = 1
    drawing.width *= scaleFactor
    drawing.height *= scaleFactor
    drawing.scale(scaleFactor, scaleFactor)
    # drawing.shift(200,-675)
    drawing.shift(225, -630)
    renderPDF.drawToFile(drawing, "qrpdf.pdf", autoSize=0)
    blank_pdf_qr=os.path.join(os.getcwd(),'qrpdf.pdf')
    watermarkFile = open(blank_pdf_qr, 'rb')
    pdfWatermarkReader = PyPDF2.PdfFileReader(watermarkFile)
    minutesFile = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(minutesFile)

    pdfWriter = PyPDF2.PdfFileWriter()
    #print("b"*60)
    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pageObj.mergePage(pdfWatermarkReader.getPage(0))
        pdfWriter.addPage(pageObj)
        base_name=os.path.join(os.getcwd(),'media','result',"bhagwati_invoice.pdf")
    resultPdfFile = open(base_name, 'wb')
    pdfWriter.write(resultPdfFile)
    watermarkFile.close()
    minutesFile.close()
    resultPdfFile.close()
    template=loader.get_template("fields.html")
    link = 'http://{}/{}'.format(request.get_host(), base_name)
    data={
        'pdf_path':link,
     }


    return HttpResponse(template.render(data))
    #return HttpResponse(path_to_pdf_file)

def pdf_view(request):
    fs = FileSystemStorage()
    filename = 'bhagwati_invoice.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')







