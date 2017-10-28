"""collection of functions to create and organize course folder."""
import os
import glob
import json


def init_folder(source_folder, target_folder, members_json):
    """copy files from source folder to course folder.
    Args:
        source_folder: source folder with students files.
        target_folder: full path to local folder for students.
        members_json: path to students.json or groups.json file for the assignment.
    """
    # create a set of student names
    with open(members_json, 'rb') as inf:
        data = json.load(inf)
    try:
        members = {'{}_{}'.format(st['family_name'], st['name']).lower() for st in data}
    except KeyError:
        # group project
        members = {st['name'].lower() for st in data}

    # for each file in course folder, find name and family name
    # check if the name and family name matches the student
    # rename and copy it to the new folder
    for f in os.listdir(source_folder):
        if os.path.getsize(os.path.join(source_folder, f)) > 10 ** 8:
            print 'ERR: File size is larger than 100 MB.' \
                'Resubmit the file.\n\t{}'.format(f)
            continue
        n, ext = os.path.splitext(f)
        try:
            try:
                family_name, name = n.lower().split('_')[:2]
            except Exception:
                family_name, name = n.lower().split()[:2]
        except Exception as e:
            print 'ERR: Failed to find name, familyname from {}!\n\t{}'.format(n, e)
        else:
            # if the name is valid
            try:
                assert '{}_{}'.format(family_name, name) in members, \
                    '{} {} is not a student'.format(name, family_name)
            except AssertionError as e:
                print(e)
            else:
                try:
                    print "Copying {}!".format(f.lower())
                    os.rename(os.path.join(source_folder, f),
                              os.path.join(target_folder, f.lower()))
                except Exception as e:
                    print('ERR: Failed to copy {} to {}:\n\t{}'.format(f,
                                                                       target_folder,
                                                                       e))


def collect_assignments(project_folder):
    """Collect assignments from the folders and create assignments.json"""
    # load the current assignments.json file
    assgn_file = os.path.join(project_folder, 'assignments.json')
    assert os.path.isfile(assgn_file), \
        'Cannot find assignments.json file at: {}.'.format(assgn_file)

    with open(assgn_file, 'rb') as inf:
        assignments = json.load(inf)

    # check for the assignments that should be loaded
    for assignment in assignments:
        if not assignment['reload']:
            continue

        assignment['submissions'] = []
        name = assignment['name']
        folder = assignment['folder']
        is_group_project = assignment['is_group_project']
        print('Loading "%s" form "./%s"' % (name, folder))
        # go inside the folder and collect all the available files for each
        # student/group create submission objects
        fullpath = os.path.join(project_folder, folder)
        assert os.path.isdir(fullpath), \
            'Cannot find assignment folder at: {}.'.format(fullpath)
        # load members
        if is_group_project:
            # load groups.json file
            members_json = os.path.join(fullpath, 'groups.json')
        else:
            # load the students file
            members_json = os.path.join(project_folder, 'students.json')

        assert os.path.isfile(members_json), \
            'Cannot find students/group file at: {}.'.format(members_json)

        with open(members_json, 'rb') as memf:
            members = json.load(memf)

        for member in members:
            # load assignments for each member as create a submission object
            if is_group_project:
                key = member['name']
                submission = {
                    'team': member['members'],
                    'team_name': key,
                    'files': [],
                    'thumbnail': 'thumbnails/%s.png' % key
                }
            else:
                key = member['family_name'] + '_' + member['name']
                submission = {
                    'team': [member],
                    'team_name': member['name'] + ' ' + member['family_name'],
                    'files': [],
                    'thumbnail': 'thumbnails/%s.png' % key
                }

            files = glob.glob(os.path.join(fullpath, '%s*' % key))
            if not files:
                continue
            submission['files'] = tuple(os.path.split(f)[-1] for f in files)
            assignment['submissions'].append(submission)

        assignment['reload'] = False

    # write updated assignments
    with open(assgn_file, 'wb') as outf:
        json.dump(assignments, outf, indent=2)


def get_students_info(project_folder, students_json=None, assignments_json=None):
    """create students_info.json from assignments.json.

    Args:
        students_json: full path to students.json.
        assignments_json: full path to assignments.json file created by
            collect_assignments.
    """
    students_json = students_json or os.path.join(project_folder, 'students.json')
    assignments_json = assignments_json or os.path.join(project_folder,
                                                        'assignments.json')
    assert os.path.isfile(students_json), \
        'Cannot find students.json file at: {}.'.format(students_json)

    assert os.path.isfile(assignments_json), \
        'Cannot find assignments.json file at: {}.'.format(assignments_json)

    student_info_file = os.path.join(project_folder, 'students_info.json')

    with open(students_json, 'rb') as inf:
        students = json.load(inf)

    with open(assignments_json, 'rb') as assf:
        assignments = json.load(assf)

    for student in students:
        students_id = student['id']
        student['submissions'] = []
        for assignment in assignments:
            submission = {
                'name': assignment['name'],
                'folder': assignment['folder'],
                'thumbnail': None
            }
            for sub in assignment['submissions']:
                for member in sub['team']:
                    if member['id'] == students_id:
                        submission['thumbnail'] = sub['thumbnail']
                        student['submissions'].append(submission)
                        break

    with open(student_info_file, 'wb') as outf:
        json.dump(students, outf, indent=4)


if __name__ == '__main__':
    project_folder = r"C:\Users\Mostapha\Documents\code\teaching-2017\arch633"
    collect_assignments(project_folder)
    get_students_info(project_folder)
