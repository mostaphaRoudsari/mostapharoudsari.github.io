import os
from pyPdf import PdfFileReader, PdfFileWriter
from tempfile import NamedTemporaryFile
from wand.image import Image


def pdf_to_thumbnails(path_to_pdf, target_folder=None):
    """Generate thumbnail png images from each page of pdf file.

    You need to install wand and ghostscript on your system.
    Check this discussion for step-by-step workflow
    http://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files
    """
    reader = PdfFileReader(open(path_to_pdf, "rb"))
    path, name = os.path.split(path_to_pdf)

    if target_folder:
        path = target_folder

    for page_num in xrange(reader.getNumPages()):
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(page_num))
        temp = NamedTemporaryFile(prefix=str(page_num), suffix=".pdf",
                                  delete=False)
        writer.write(temp)
        temp.close()

        with Image(filename=temp.name, resolution=(300, 300)) as img:
            ar = 300.0 / img.width
            img.resize(300, int(img.height * ar))
            img.compression_quality = 99
            img.save(filename=os.path.join(path, "%s_%d.png" % (name[:-4], page_num)))
        os.remove(temp.name)

    del(reader)


def pdf_folder_to_thumbnails(pdf_folder, target_folder):
    """Convert pdf files inside a folder to thumbnails."""
    for f in os.listdir(pdf_folder):
        if f.lower().endswith('.pdf'):
            path_to_pdf = os.path.join(pdf_folder, f)
            pdf_to_thumbnails(path_to_pdf, target_folder)


def rename_thumbnails(folder):
    """Remove the number at the end of thumbnails."""
    for f in os.listdir(folder):
        if f.lower().endswith('.png'):
            if f[:-4].split('_')[-1].isdigit():
                new_name = '_'.join(f[:-4].split('_')[:-1]) + '.png'
                try:
                    os.rename(os.path.join(folder, f), os.path.join(folder, new_name))
                except WindowsError:
                    # file already exist
                    os.remove(os.path.join(folder, f))


if __name__ == '__main__':
    # test pdf to thumbnails
    project_folder = r"C:\Users\Mostapha\Documents\code\teaching-2017\arch708\mid_review"
    target_folder = os.path.join(project_folder, 'thumbnails')
    # pdf_folder_to_thumbnails(project_folder, target_folder)
    rename_thumbnails(target_folder)
