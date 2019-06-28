from django.shortcuts import render
#from django.views.generic import TemplateView
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from tika import parser
import PyPDF2
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
def upload(request):
    context = {}
    content = ""
    if request.method=='POST':
        uploaded_file=request.FILES['doccument']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        #print("file is: ",uploaded_file)
        print("#####################################")
        print(uploaded_file)
        pdfreader=PyPDF2.PdfFileReader(uploaded_file,'rb')
        pageobj=pdfreader.getPage(0)
        mycontent=pageobj.extractText()
        print(content)
        # content = ContentFile(mycontent)
        # p=content.name="mytext.txt"
        # p.save()
        #wfile=open('text.txt',"w")

        print("***************************************")
        #page_content=page.extractText()
        print(content)
        print("==========================================")
        myfile=open('/home/ujjwal/scanner/invoicescanner/text.txt',"w")
        #c=content.splitlines()
        myfile.write(content)
        myfile.write(mycontent)
        #print(p)
    return render(request,'index.html')




