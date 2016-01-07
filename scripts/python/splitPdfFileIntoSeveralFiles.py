students = [{'startPage':'4', 'endPage':'5', 'name':'majed', 'familyname':'albakr'},
            {'startPage':'0', 'endPage':'0', 'name':'seung-hyeok', 'familyname':'bae'},
          {'startPage':'12', 'endPage':'13', 'name':'niccolo', 'familyname':'benghi'},
          {'startPage':'0', 'endPage':'0', 'name':'munazza', 'familyname':'bhatti'},
          {'startPage':'0', 'endPage':'0', 'name':'cai', 'familyname':'fang'},
          {'startPage':'24', 'endPage':'25', 'name':'keun-hyuk', 'familyname':'jang'},
          {'startPage':'0', 'endPage':'0', 'name':'jaeho', 'familyname':'jin'},
          {'startPage':'22', 'endPage':'23', 'name':'ashish', 'familyname':'khemchandani'},
          {'startPage':'30', 'endPage':'31', 'name':'ksenia', 'familyname':'knyazkina'},
          {'startPage':'20', 'endPage':'21', 'name':'shin-yi', 'familyname':'kwan'},
          {'startPage':'17', 'endPage':'19', 'name':'jee-eun', 'familyname':'lee'},
          {'startPage':'32', 'endPage':'33', 'name':'rajika', 'familyname':'maheshwari'},
          {'startPage':'9', 'endPage':'11', 'name':'pegah', 'familyname':'mahthur'},
          {'startPage':'0', 'endPage':'0', 'name':'evan', 'familyname':'oskierko-jeznacki'},
          {'startPage':'1', 'endPage':'3', 'name':'mingbo', 'familyname':'peng'},
          {'startPage':'14', 'endPage':'16', 'name':'shengliang', 'familyname':'rong'},
          {'startPage':'6', 'endPage':'8', 'name':'janki', 'familyname':'vyas'},
          {'startPage':'28', 'endPage':'29', 'name':'xi', 'familyname':'yao'},
          {'startPage':'26', 'endPage':'27', 'name':'yuntian', 'familyname':'wan'}]


students2 = [{'startPage':'10', 'endPage':'12', 'name':'majed', 'familyname':'albakr'},
            {'startPage':'0', 'endPage':'0', 'name':'seung-hyeok', 'familyname':'bae'},
          {'startPage':'25', 'endPage':'27', 'name':'niccolo', 'familyname':'benghi'},
          {'startPage':'0', 'endPage':'0', 'name':'munazza', 'familyname':'bhatti'},
          {'startPage':'0', 'endPage':'0', 'name':'cai', 'familyname':'fang'},
          {'startPage':'28', 'endPage':'30', 'name':'keun-hyuk', 'familyname':'jang'},
          {'startPage':'0', 'endPage':'0', 'name':'jaeho', 'familyname':'jin'},
          {'startPage':'31', 'endPage':'33', 'name':'ashish', 'familyname':'khemchandani'},
          {'startPage':'37', 'endPage':'39', 'name':'ksenia', 'familyname':'knyazkina'},
          {'startPage':'22', 'endPage':'24', 'name':'shin-yi', 'familyname':'kwan'},
          {'startPage':'46', 'endPage':'48', 'name':'jee-eun', 'familyname':'lee'},
          {'startPage':'43', 'endPage':'43', 'name':'rajika', 'familyname':'maheshwari'},
          {'startPage':'13', 'endPage':'15', 'name':'pegah', 'familyname':'mahthur'},
          {'startPage':'0', 'endPage':'0', 'name':'evan', 'familyname':'oskierko-jeznacki'},
          {'startPage':'7', 'endPage':'9', 'name':'mingbo', 'familyname':'peng'},
          {'startPage':'34', 'endPage':'36', 'name':'shengliang', 'familyname':'rong'},
          {'startPage':'4', 'endPage':'6', 'name':'janki', 'familyname':'vyas'},
          {'startPage':'16', 'endPage':'18', 'name':'xi', 'familyname':'yao'},
          {'startPage':'19', 'endPage':'21', 'name':'yuntian', 'familyname':'wan'}]

"""
import os
from pyPdf import PdfFileWriter, PdfFileReader

pdfFile = r"C:\Users\Administrator\Downloads\Daylighting Assignment 002.pdf"
inputpdf = PdfFileReader(open(pdfFile, "rb"))

baseFolder = r"C:\Users\Administrator\Documents\GitHub\mostapharoudsari.github.io\data\teaching\upenn\arch753\fall15\students"

for student in students2:

    if student['startPage'] == student['endPage'] == "0": continue
    print student['name']
    output = PdfFileWriter()
    for i in xrange(int(student['startPage']), int(student['endPage']) + 1):
        output.addPage(inputpdf.getPage(i-1))

    # write the new pdf file
    filename = student["familyname"] + "_" + student["name"]
    filepath = os.path.join(baseFolder, filename, "daylighting-II", filename + ".pdf")
    with open(filepath, "wb") as outputStream:
        output.write(outputStream)
"""
