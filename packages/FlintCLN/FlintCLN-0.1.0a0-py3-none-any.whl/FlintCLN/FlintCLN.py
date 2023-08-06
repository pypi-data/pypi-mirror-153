import os
import stat
import re
import pprint
import inspect

class FlintCLN(object):

    def __init__(self, project_dir = '.', verbose=False):

        # Intialize class member variables
        self.project_dir = project_dir

        # Contains the list of directories/files that
        # will be subject to linting.
        self.dirs = {}

        # Regular expression patterns used to match files
        # or directories that should be ignored during linting.
        self.ignore_patterns = [
            r'^.*-DEPRECATED$',
            r'^.*-EXPERIMENTAL$',
            r'^.ipynb_checkpoints$'
        ]

        # After crawling the project directory, the paths of any files or
        # dirs that are ignored are stored here.
        self.ignored_objs = []

        # Houses the list of errors found during linting. The keys are
        # the test names that failed.
        self.error_log = {}

        # Houses the list of warnings found during linting. The keys are
        # the test names that failed.
        self.warning_log = {}

        # Intialize the pretty printer.
        self.pp = pprint.PrettyPrinter(indent=3)

        # Contains the list of found README files in the repository.
        self.readmes = []

        # Create a list of READMEs that are missing. If the option to fix the repository
        # is enabled then we can create these READMEs automatically.
        self.missing_readmes = []


        # A list of files that appear in task collection directories which
        # should not be there.
        self.bad_files = []

        # Provides human-readable descriptions of the tests that are performed.
        self.tests = {
            'basedir_required': {
                'description': 'Checks that the base folder of every repository has the required files and directories.',
                'message': 'These files or directories are missing.',
                'name': 'Check Required Base Files'
            },
            'missing_readme': {
                'description': 'Checks that all task directories have READMEs.md files.',
                'message': 'README.md files are missing in these directories.',
                'name': 'Check READMEs'
            },
            'task_ordering_skipped': {
                'description': 'Checks that all task directories do not skip numbers',
                'message': 'The tasks in these directories do not have sequential ordering in the directory prefix (e.g., 01, 02, etc.). There must not be duplicate numbers or missing numbers.',
                'name': 'Check Sequential Tasks'
            },
            'task_collection_dirs': {
                'description': 'Checks that a task collection directory only has task directories and no other files except a README.md or a .gitignore.',
                'message': 'These files appear in a task collection directory and they should not be there.',
                'name': 'Check Test Collection Files'
            }
        }

        # Indicates if the linter should print details about exact problems rather than just a summary.
        self.verbose = verbose


    def addIgnorePattern(self, pattern):
        """
        Allows the caller to include additional patterns specifying files or directories that should be ignored.
        """
        self.ignore_patterns.append(pattern)

    def errors(self):
        """
        """
        return(self.error_log)

    def warnings(self):
        """
        """
        return(self.warning_log)

    def run(self, fix = False):

        # First crawl the directories.
        self.dirs = {
            self.project_dir: {
                'stat':  os.lstat(self.project_dir),
                'children': self._crawlDirs(self.project_dir)
            }
        }

        # Perform linting
        self._lint()

        # If the user has asked to fix the repository then do so.
        if fix:
            self._fix()

    def _lint(self):
        """
        Runs the linter
        """

        # First make sure the root directory has the required folders.
        self._checkRoot()

        # Next make sure all of the READMEs are present.
        self._checkREADMEs(self.project_dir, self.dirs[self.project_dir])

        # Make sure numbering is in the proper order.
        self._checkTaskNumbering(self.project_dir, self.dirs[self.project_dir])

        # Make sure task collection folders only have task directories and READMEs.
        self._checkTaskCollection(self.project_dir, self.dirs[self.project_dir])

    def _fix(self):
        pass

    def printWarnings(self):
        """
        """
        print("{}WARNINGS{}".format('\033[33m', '\033[0m'))
        for testname in self.warning_log.keys():
            print("Test: {} ({})".format(self.tests[testname]['name'], testname))
            print("- Description: {}".format(self.tests[testname]['description']))
            print("- Message: {}".format(self.tests[testname]['message']))
            if self.verbose:
                for objname in self.warning_log[testname]:
                    print("  {}".format(objname))
            else:
                print("  {} occurance(s) failed this test.".format(len(self.warning_log[testname])))
            print()


    def printErrors(self):
        """
        """
        print("{}ERRORS{}".format('\033[91m', '\033[0m'))
        for testname in self.error_log.keys():
            print("Test: {} ({})".format(self.tests[testname]['name'], testname))
            print("- Description: {}".format(self.tests[testname]['description']))
            print("- Message: {}".format(self.tests[testname]['message']))
            if self.verbose:
                for objname in self.error_log[testname]:
                    print("  {}".format(objname))
            else:
                print("  {} occurance(s) failed this test.".format(len(self.error_log[testname])))
            print()


    def printIgnored(self):
        """
        """
        self.pp.pprint(self.ignored_objs)


    def _addError(self, testname, file):
        """
        """
        if not testname in self.tests.keys():
            raise Exception("The testname, {}, is not present in the tests member variable of the FlintCLN class.".format(testname))

        if not testname in self.error_log.keys():
            self.error_log[testname] = []
        self.error_log[testname].append(file)


    def _addWarning(self, testname, file):
        """
        """
        if not testname in self.tests.keys():
            raise Exception("The testname, {}, is not present in the tests member variable of the FlintCLN class.".format(testname))

        if not testname in self.warning_log.keys():
            self.warning_log[testname] = []
        self.warning_log[testname].append(file)


    def _checkRoot(self):
        """
        """
        children = []
        for child in self.dirs[self.project_dir]['children'].keys():
            children.append(os.path.basename(child))

        required = ['00-docs', '01-input_data',  'README.md']
        for f in required:
            if not (f in children):
                self._addError('basedir_required', f)

        desired = ['99-reports', '99-pubs']
        for f in desired:
            if not (f in children):
                self._addWarning('basedir_required', f)


    def _isTask(self, objname, details):
        """
        Checks an object details to see if its a task directory.
        """

        # If this is the base directory then return true
        if objname == self.project_dir:
            return True

        # Skip objects that are not directories.
        if not stat.S_ISDIR(details['stat'].st_mode):
            return False

        # Skip directories without a numeric prefix.
        basename = os.path.basename(objname)
        p = re.compile(r"^\d+\-")
        if not p.search(basename):
            return False

        # Skip directories without children
        if details['children'] is None:
            return False

        return True

    def _checkREADMEs(self, objname, details):
        """
        Recursively checks that all directories with a numeric prefix have a
        README.md inside
        """

        # Skip objects that are not task directories.
        if not self._isTask(objname, details):
            return

        # Check if there is a readme file as a child
        has_readme = False
        for child in details['children'].keys():
            basename = os.path.basename(child)
            if basename == 'README.md':
                has_readme = True

        # If not a README then add an error. If there is one then
        # add it to our list.
        if not has_readme:
            self._addError('missing_readme', objname)
            self.missing_readmes.append(os.path.join(objname, 'README.md'))
        else:
            self.readmes.append(os.path.join(objname, 'README.md'))

        # Iterate through the children of this object and look for
        # a README.
        for childname, childdetails in details['children'].items():
            self._checkREADMEs(childname, childdetails)


    def _checkTaskNumbering(self, objname, details):
        """
        Recursively checks that task directories follow sequential numbering.
        """
        # Skip objects that are not task directories.
        if not self._isTask(objname, details):
            return

        total_tasks = None
        done = False
        p = re.compile(r'^(\d+)')
        for child in sorted(details['children'].keys()):
            child_details = details['children'][child]

            # Recurse
            self._checkTaskNumbering(child, child_details)

            # If we've determined that this folder has a problem then
            # we don't need to check any more children
            if done == True:
                continue

            # If this child is not a directory then we don't need to
            # check the numbering.
            if not stat.S_ISDIR(child_details['stat'].st_mode):
                continue

            # Get the directory prefix number and make sure it's
            # sequential
            basename = os.path.basename(child)
            matches = p.search(basename)
            if matches:
                if len(matches.groups()) > 0:
                    task_num = int(matches.groups()[0])
                    if total_tasks is None:
                        total_tasks = task_num
                        continue
                    if not (total_tasks + 1) == task_num:
                        self._addError('task_ordering_skipped', objname)
                        done = True
                    total_tasks = task_num



    def _checkTaskCollection(self, objname, details):
        """
        Recursively checks that task directories with sub tasks only have no other files but a README.md.
        """
        # Skip objects that are not task directories.
        if not self._isTask(objname, details):
            return

        has_taskdir = False
        has_file = False
        bad_files = []
        for child in sorted(details['children'].keys()):
            child_details = details['children'][child]
            basename = os.path.basename(child)

            # Recurse
            self._checkTaskCollection(child, child_details)

            # Do we have a task directory as a child?
            if self._isTask(child, child_details):
                has_taskdir = True

            # Do we have a file that is not a README.md?
            if stat.S_ISREG(child_details['stat'].st_mode):
                if (not basename == 'README.md') & (not basename == '.gitignore'):
                    has_file = True
                    bad_files.append(child)

        if has_taskdir & has_file:
            for bad_file in  bad_files:
                self._addError('task_collection_dirs', bad_file)
                self.bad_files.append(bad_file);



    def _crawlDirs(self, parent):
        """
        Recursively crawls all of the directories to find those that should be included in linting.
        """
        dirs = {}
        for objname in os.listdir(parent):
            child = os.path.join(parent, objname)
            cstat = os.lstat(child)

            # Ignore anything but files and directories
            if (stat.S_ISDIR(cstat.st_mode)) | (stat.S_ISREG(cstat.st_mode)):
                dirs[child] = {}
                dirs[child]['stat'] = cstat
                dirs[child]['children'] = None

                # Check if the object name matches any of our ignore
                # tests. If so, exclude it.
                skip = False
                for pattern in self.ignore_patterns:
                    p = re.compile(pattern)
                    if p.search(objname):
                        skip = True
                        break

                # If we are to skip this file/dir then move to the next one.
                if skip == True:
                    self.ignored_objs.append(child)
                    continue;

                # If this is a directory crawl it's files.
                if stat.S_ISDIR(cstat.st_mode):
                    dirs[child]['children'] = self._crawlDirs(child)

        return dirs
