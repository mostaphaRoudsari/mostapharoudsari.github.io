import os
import shutil

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
