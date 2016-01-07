import os
import shutil
import json

def reorganizeAssignments(baseFolder, targetFolder, students):
    """Copy students assignments from folders based on dates
        to folders based on students' name.

        Everyone supposed to name their assignments as
        \YYYYMMDD\familyName_name_optionalNameOfAssignement

        Target structure is:
        \familyname_name\YYYYMMDD\familyname_name_optionalNameOfAssignement
    """

    def getNameFamilyName(filename):
        # find name of the person
        try:
            familyname, name, projectname = filename.split('_')[:3]
        except:
            try:
                familyname, name = filename.split('_')[:2]
            except:
                familyname, name = "", ""

        if name.lower() in names:
            index = names.index(name.lower())
            return names[index], familynames[index]
        else:
            # this case hasn't followed the naming structure
            # let's try to sort it out
            strippedName = filename.replace(" ", "")\
                        .replace("-", "").lower()

            for studentName, studentFamilyName in zip(names, familynames):
                if studentName.replace("-","") in strippedName or \
                    studentFamilyName.replace("-","") in strippedName:

                    return studentName, studentFamilyName

            print "Failed name: %s"%srcFileName
            return None, None


    names = [student['name'] for student in students]
    familynames = [student['familyname'] for student in students]
    baseSubfolders = os.listdir(baseFolder)

    for folder in baseSubfolders:
        fullPath = os.path.join(baseFolder,folder)
        if os.path.isdir(fullPath):
            # collect all the files inside source folder
            srcFiles = os.listdir(fullPath)
            for srcFile in srcFiles:
                srcFileName = os.path.join(fullPath, srcFile)
                if os.path.isfile(srcFileName):
                    name, familyname = getNameFamilyName(srcFile)
                    if not name: continue

                    # create the folder if it is not there
                    # naming is familyname_name
                    tFolder = os.path.join(targetFolder, familyname + "_" + name)
                    if not os.path.isdir(tFolder): os.mkdir(tFolder)

                    stfolder = os.path.join(tFolder, folder)
                    # create a subfolder not already there
                    if not os.path.isdir(stfolder): os.mkdir(stfolder)

                    # copy the source file to target
                    targetFileName = os.path.join(stfolder, srcFile)
                    shutil.copyfile(srcFileName, targetFileName)

# reorganizeAssignments(baseFolder, targetFolder, students)


def genCourseInfo(folder= r"C:\Users\Administrator\Documents\GitHub\mostapharoudsari.github.io\data\teaching\upenn\arch753\fall15", \
                students = "students.json"):
    """Take student data as a json file and folders
        and generate a course.json
    """
    #with open(os.path.join(folder, students), "r") as studentsFile:
    #    students = json.load(studentsFile)

    students = [{'id':'0', 'name':'majed', 'familyname':'albakr', 'email':'malbakr@design.upenn.edu'},
			  {'id':'1', 'name':'seung-hyeok', 'familyname':'bae', 'email':'baeseung@design.upenn.edu'},
              {'id':'2', 'name':'niccolo', 'familyname':'benghi', 'email':'nbenghi@design.upenn.edu'},
			  {'id':'3', 'name':'munazza', 'familyname':'bhatti', 'email':'munazza@design.upenn.edu'},
              {'id':'4', 'name':'cai', 'familyname':'fang', 'email':'caifang@design.upenn.edu'},
			  {'id':'5', 'name':'keun-hyuk', 'familyname':'jang', 'email':'keunj@design.upenn.edu'},
              {'id':'6', 'name':'jaeho', 'familyname':'jin', 'email':'jinjaeho@design.upenn.edu'},
			  {'id':'7', 'name':'ashish', 'familyname':'khemchandani', 'email':'ashishkh@design.upenn.edu'},
              {'id':'8', 'name':'ksenia', 'familyname':'knyazkina', 'email':'kksenia@design.upenn.edu'},
			  {'id':'9', 'name':'shin-yi', 'familyname':'kwan', 'email':'kwans@design.upenn.edu'},
              {'id':'10', 'name':'jee-eun', 'familyname':'lee', 'email':'leejee@design.upenn.edu'},
			  {'id':'11', 'name':'rajika', 'familyname':'maheshwari', 'email':'rajika@design.upenn.edu'},
              {'id':'12', 'name':'pegah', 'familyname':'mahthur', 'email':'pegahmathur__gmail.com'},
              {'id':'14', 'name':'mingbo', 'familyname':'peng', 'email':'mpen@design.upenn.edu'},
			  {'id':'15', 'name':'shengliang', 'familyname':'rong', 'email':'srong@design.upenn.edu'},
              {'id':'16', 'name':'janki', 'familyname':'vyas', 'email':'jankiv@design.upenn.edu'},
			  {'id':'17', 'name':'xi', 'familyname':'yao', 'email':'xiyao@design.upenn.edu'},
              {'id':'18', 'name':'yuntian', 'familyname':'wan', 'email':'wyuntian@design.upenn.edu'}]

    assignments = ["meyerson-hall-canopy", "daylighting-I", "daylighting-II", \
                        "energy-and-daylighting", "indoor-comfort", "final-project"]
    courseInfo = {
        'students': students
    }

    for student in students:
        # find all the assignments and add them under their name
        # also add the assignment to assignments list
        studentFolder = os.path.join(folder, 'students', student['familyname'] + "_" + student['name'])
        student['assignments'] = []

        for assignment in assignments:
            if os.path.isdir(os.path.join(studentFolder, assignment)):
                assignmentFiles = []

                # find all the files
                files = os.listdir(os.path.join(studentFolder, assignment))
                for f in files:
                    if f == "thumbnail_0.png": continue
                    if os.path.isfile(os.path.join(studentFolder, assignment, f)):
                        assignmentFiles.append(f)

                student['assignments'].append({ 'name': assignment, 'files' : assignmentFiles})

    targetFile = os.path.join(folder, "courseInfo.json")
    with open(targetFile, "w") as outf:
        json.dump(courseInfo, outf)

genCourseInfo()
