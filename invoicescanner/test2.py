from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
drawing = svg2rlg("/home/ujjwal/scanner/qrcode")
scaleFactor = 1
drawing.width *= scaleFactor
drawing.height *= scaleFactor
drawing.scale(scaleFactor, scaleFactor)
#drawing.shift(200,-675)
drawing.shift(225,-630)
renderPDF.drawToFile(drawing, "realfile.pdf",autoSize=0)



