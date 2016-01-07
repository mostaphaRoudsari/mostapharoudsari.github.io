"""
You need to install wand and ghostscript on your system.
Check this discussion for step-by-step workflow
http://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files

The script generates thumbnail images from all pdf pages
"""
import os
from pyPdf import PdfFileReader, PdfFileWriter
from tempfile import NamedTemporaryFile
from wand.image import Image
import json

def pdf2png(pdfFile):
    reader = PdfFileReader(open(pdfFile, "rb"))
    path, name = os.path.split(pdfFile)
    for page_num in xrange(reader.getNumPages()):
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(page_num))
        temp = NamedTemporaryFile(prefix=str(page_num), suffix=".pdf", delete=False)
        writer.write(temp)
        temp.close()

        with Image(filename = temp.name, resolution=(300, 300)) as img:
            ar = 300.0 / img.width
            img.resize(300, int(img.height * ar))
            img.compression_quality = 99
            img.save(filename= os.path.join(path, "thumbnail_%d.png" % (page_num)))
        os.remove(temp.name)

    del(reader)



"""
with open(courseData, "rb") as cData:
    data = json.load(cData)

    for assignment, files in student["assignments"].items():
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfFile = os.path.join(baseFolder, assignment, f)
                pdf2png(pdfFile)
"""

courseData = r"C:\Users\Administrator\Documents\GitHub\mostapharoudsari.github.io\data\teaching\upenn\arch753\fall15\courseInfo.json"
studentsFolder = os.path.join(os.path.split(courseData)[0], 'students')
folders = ["daylighting-I", "daylighting-II"]
#folders = ["weather-data-analysis", "meyerson-hall-canopy", "energy-and-daylighting", "indoor-comfort"]

with open(courseData, "rb") as cData:
    data = json.load(cData)
    for student in data['students']:
        for assignment in folders:
            folder = os.path.join(studentsFolder, student["familyname"] + "_" + student["name"], assignment)
            thumbnail = os.path.join(folder, "thumbnail_0.png")
            pdfFile = os.path.join(folder, student["familyname"] + "_" + student["name"] + ".pdf")

            if os.path.isdir(folder):
                if not os.path.isfile(thumbnail):
                    pdf2png(pdfFile)
