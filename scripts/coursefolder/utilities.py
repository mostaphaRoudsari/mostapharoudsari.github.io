"""collection of functions to create and organize course folder."""
import os
from pyPdf import PdfFileReader, PdfFileWriter
from tempfile import NamedTemporaryFile
from wand.image import Image
import json


def pdf2thumbnails(pathToPdf):
    """Generate thumbnail png images from each page of pdf file.

    You need to install wand and ghostscript on your system.
    Check this discussion for step-by-step workflow
    http://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files
    """
    reader = PdfFileReader(open(pathToPdf, "rb"))
    path, name = os.path.split(pathToPdf)
    for page_num in xrange(reader.getNumPages()):
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(page_num))
        temp = NamedTemporaryFile(prefix=str(page_num), suffix=".pdf", delete=False)
        writer.write(temp)
        temp.close()

        with Image(filename=temp.name, resolution=(300, 300)) as img:
            ar = 300.0 / img.width
            img.resize(300, int(img.height * ar))
            img.compression_quality = 99
            img.save(filename=os.path.join(path, "thumbnail_%d.png" % (page_num)))
        os.remove(temp.name)

    del(reader)


def createfolders(coursefolder, stundentInfo=None):
    """Create folders for students.

    Use this method only once to create the folders for a new course.

    Args:
        coursefolder: Fullpath to the course folder.
        studentsInfo: A json object for students that includes their name and
            familyname. If None the script looks for student.json in coursefolder.
    """
    # load studentsInfo
    if not stundentInfo:
        with open(os.path.join(coursefolder, 'students.json')) as si:
            stundentInfo = eval('\n'.join(si.readlines()))

    # create students folder
    bf = os.path.join(coursefolder, 'students')
    if not os.path.isdir(bf):
        os.mkdir(bf)

    for student in stundentInfo:
        foldername = '{}_{}'.format(student['familyname'], student['name'])
        fullpath = os.path.join(bf, foldername)
        try:
            os.mkdir(fullpath)
        except Exception as e:
            print 'failed to create folder for {}:\n{}'.format(foldername, e)


def updateCourseInformation(coursefolder, assignments, studentsInfo=None):
    """Take student data as a json file and folders and generate a course.json."""
    # load studentsInfo
    if not studentsInfo:
        with open(os.path.join(coursefolder, 'students.json')) as si:
            studentsInfo = eval('\n'.join(si.readlines()))

    courseInfo = {
        'students': studentsInfo
    }

    for student in studentsInfo:
        # find all the assignments and add them under their name
        # also add the assignment to assignments list
        studentFolder = os.path.join(coursefolder, 'students', student['familyname'] + "_" + student['name'])
        student['assignments'] = []

        for assignment in assignments:
            if os.path.isdir(os.path.join(studentFolder, assignment)):
                assignmentFiles = []

                # find all the files
                files = os.listdir(os.path.join(studentFolder, assignment))
                for f in files:
                    if f == "thumbnail_0.png":
                        continue
                    if os.path.isfile(os.path.join(studentFolder, assignment, f)):
                        assignmentFiles.append(f)

                student['assignments'].append({'name': assignment, 'files': assignmentFiles})

    targetFile = os.path.join(coursefolder, "courseInfo.json")
    with open(targetFile, "w") as outf:
        json.dump(courseInfo, outf)


def dumpFiles(assignmentname, source, target, thumbnail=True):
    """copy files from source folder to course folder.

    Args:
        assignmentname: name for assignement.
        source: source folder with students files (e.g. Upenn's coursefolder).
        target: full path to local folder for students.
    """
    # for each file in course folder, find name and family name
    # try to find the student folder
    # create a new folder for this assignement if it's not there yet
    # copy files
    for f in os.listdir(source):
        n, ext = os.path.splitext(f)
        try:
            try:
                name, familyname = n.split('_')[:2]
            except:
                name, familyname = n.split()[:2]
        except Exception as e:
            print 'ERR: Failed to find name, familyname from {}!\n\t\t{}'.format(n, e)
        else:
            # check for the folder
            sf = os.path.join(target, 'students',
                              '{0}_{1}'.format(familyname.lower().strip(),
                                               name.lower().strip()))
            if not os.path.isdir(sf):
                sf = os.path.join(target, 'students',
                                  '{1}_{0}'.format(familyname.lower().strip(),
                                                   name.lower().strip()))
                if not os.path.isdir(sf):
                    print 'ERR: Failed to find folder for {1}_{0}!'.format(name, familyname)
                    continue

            tf = os.path.join(sf, assignmentname)
            try:
                os.mkdir(tf)
            except:
                pass

            try:
                print "Copying {}!".format(f.lower())
                os.rename(os.path.join(source, f),
                          os.path.join(tf, f))
            except Exception, e:
                print 'ERR: Failed to move {} to {}:\n{}'.format(f, tf, e)
            else:
                # if pdf create a thumbnail
                if thumbnail and f.lower().endswith('pdf'):
                    print "create thumbnails for {}".format(f.lower())
                    pdf2thumbnails(os.path.join(tf, f.lower()))


if __name__ == '__main__':
    s = r'C:\UPENN\160919'
    f = r'C:\Users\Administrator\Documents\GitHub\mostapharoudsari.github.io\data\teaching\upenn\arch753\fall16'

    assignments = ("dream-room", "meyerson-hall-canopy", "weather-data-analysis",
                   "weather-data-analysis-II")
    # dumpFiles('weather-data-analysis', s, f)
    updateCourseInformation(f, assignments)
