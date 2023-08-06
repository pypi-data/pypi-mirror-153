from unittest import TestCase
import tempfile
import os
import shutil
from FlintCLN.FlintCLN import FlintCLN

class TestFlintCLN(TestCase):

    def _createProject(self, task_dirs = None, files = None):
        """
        Initializes a fake project repository directory for a test.
        """

        tempdir = tempfile.mkdtemp(prefix='FlintCLN-test')
        self.tempdirs.append(tempdir)

        if not task_dirs is None:
            for task_dir in task_dirs:
                os.mkdir(os.path.join(tempdir, task_dir))

        if not files is None:
            for fpath in files:
                open(os.path.join(tempdir, fpath), 'a').close()

        return(tempdir)


    def _cleanupProject(self, tempdir):
        """
        Removes all files in a fake project directory.
        """
        shutil.rmtree(tempdir)
        self.tempdirs.remove(tempdir)


    def setUp(self):
        """
        Prepares for testing
        """
        self.tempdirs = []


    def tearDown(self):
        """
        Cleans up after testing.
        """
        for tempdir in self.tempdirs:
            shutil.rmtree(tempdir)


    def test_checkRoot(self):
        """
        Tests the _checkRoot() function
        """

        #
        # Create a project with no required directories. All should be reported as missing.
        #
        project_dir = self._createProject()
        flint = FlintCLN(project_dir)
        flint.run()
        errors = flint.errors()
        warnings = flint.warnings()
        self.assertTrue('basedir_required' in errors.keys(), 'Does not include the basedir_required tests when it should.')
        self.assertTrue('00-docs' in errors['basedir_required'], 'Does not error when the 00-docs folder is missing.')
        self.assertTrue('01-input_data' in errors['basedir_required'], 'Does error when the 01-input_data folder is missing.')
        self.assertTrue('README.md' in errors['basedir_required'], 'Does error when the README.md file is missing.')
        self.assertTrue('basedir_required' in warnings.keys())
        self.assertTrue('99-reports' in warnings['basedir_required'], 'Does not warn that the 99-reports folder is missing.')
        self.assertTrue('99-pubs' in warnings['basedir_required'], 'Does not warn that the 99-pubs folder is missing.')
        self._cleanupProject(project_dir)

        #
        # Create a project with all required directories. None should be reported as missing.
        #
        task_dirs = ['00-docs', '01-input_data', '99-reports', '99-pubs']
        files = ['README.md']
        project_dir = self._createProject(task_dirs, files)
        flint = FlintCLN(project_dir)
        flint.run()
        errors = flint.errors()
        warnings = flint.warnings()
        self.assertFalse('basedir_required' in errors.keys(), 'Includes the basedir_required tests when it should not.')
        if 'basedir_required' in errors.keys():
            self.assertFalse('00-docs' in errors['basedir_required'], 'Gives error of missing 00-docs folder when present.')
            self.assertFalse('01-input_data' in errors['basedir_required'], 'Gives error of 01-input_data folder when present.')
            self.assertFalse('README.md' in errors['basedir_required'], 'Gives error of missing README.md folder when present.')
        self.assertFalse('_checkRoot' in warnings.keys())
        if 'basedir_required' in warnings.keys():
            self.assertTrue('99-reports' in warnings['basedir_required'], 'Warns that the 99-reports folder is missing when present.')
            self.assertTrue('99-pubs' in warnings['basedir_required'], 'Warns that the 99-pubs folder is missing when present.')
        self._cleanupProject(project_dir)


    def test_checkREADMEs(self):
        """
        Tests the _test_checkREADMEs() function
        """

        #
        # Create a project with two tasks but with no READMEs
        #
        task_dirs = ['00-docs', '01-input_data', '02-task1', '02-task1/01-subtask1', '03-task2', '99-reports', '99-pubs']
        files = ['README.md']
        project_dir = self._createProject(task_dirs, files)
        flint = FlintCLN(project_dir)
        flint.run()
        errors = flint.errors()
        warnings = flint.warnings()
        self.assertTrue('missing_readme' in errors.keys(), 'Does not include the missing_readme tests when it should.')
        readmes = [
            os.path.join(project_dir, '00-docs'),
            os.path.join(project_dir, '01-input_data'),
            os.path.join(project_dir, '02-task1'),
            os.path.join(project_dir, '02-task1/01-subtask1'),
            os.path.join(project_dir, '03-task2'),
            os.path.join(project_dir, '99-reports'),
            os.path.join(project_dir, '99-pubs'),
        ]
        for readme in readmes:
            self.assertTrue(readme in errors['missing_readme'], 'Does not report a missing README.md in: {}.'.format(readme))
        self._cleanupProject(project_dir)

        #
        # Create a project with two tasks with some  READMEs present and others missing
        #
        task_dirs = ['00-docs', '01-input_data', '02-task1', '02-task1/01-subtask1', '03-task2', '99-reports', '99-pubs']
        files = ['README.md', '02-task1/README.md', '02-task1/01-subtask1/README.md']
        project_dir = self._createProject(task_dirs, files)
        flint = FlintCLN(project_dir)
        flint.run()
        errors = flint.errors()
        warnings = flint.warnings()
        self.assertTrue('missing_readme' in errors.keys(), 'Does not include the missing_readme tests when it should.')

        # Check for missing READMEs.
        readmes = [
            os.path.join(project_dir, '00-docs'),
            os.path.join(project_dir, '01-input_data'),
            os.path.join(project_dir, '03-task2'),
            os.path.join(project_dir, '99-reports'),
            os.path.join(project_dir, '99-pubs'),
        ]
        for readme in readmes:
            self.assertTrue(readme in errors['missing_readme'], 'Does not report a missing README.md in: {}.'.format(readme))

        # Make sure existing README's don't show up in the list of missing.
        readmes = [
            os.path.join(project_dir, '02-task2'),
            os.path.join(project_dir, '02-task2/01-subtask1'),
        ]
        for readme in readmes:
            self.assertFalse(readme in errors['missing_readme'], 'Reports a missing README.md when it is present: {}.'.format(readme))
        self._cleanupProject(project_dir)

        #
        # Create a project with all READMEs present
        #
        task_dirs = ['00-docs', '01-input_data', '02-task1', '02-task1/01-subtask1', '03-task2', '99-reports', '99-pubs']
        files = ['README.md', '00-docs/README.md', '01-input_data/README.md', '02-task1/README.md',
                 '02-task1/01-subtask1/README.md', '03-task2/README.md', '99-reports/README.md', '99-pubs/README.md']
        project_dir = self._createProject(task_dirs, files)
        flint = FlintCLN(project_dir)
        flint.run()
        errors = flint.errors()
        warnings = flint.warnings()
        self.assertFalse('missing_readme' in errors.keys(), 'Includes the missing_readme tests when it should not.')

        # Check for existing READMEs.
        if 'missing_readme' in errors.keys():
            readmes = [
                os.path.join(project_dir, '00-docs'),
                os.path.join(project_dir, '01-input_data'),
                os.path.join(project_dir, '02-task1'),
                os.path.join(project_dir, '02-task1/01-subtask1'),
                os.path.join(project_dir, '03-task2'),
                os.path.join(project_dir, '99-reports'),
                os.path.join(project_dir, '99-pubs'),
            ]
            for readme in readmes:
                self.assertFalse(readme in errors['missing_readme'], 'Reports a missing README.md when it is present: {}.'.format(readme))
            self._cleanupProject(project_dir)



    def test_checkTaskNumbering(self):
        """
        Tests the _checkTaskNumbering() function.
        """
        #
        # Create a project with skipped tasks, and skipped files.
        #
        task_dirs = ['00-docs',
                     '01-input_data',
                     '02-task1',
                     '02-task1/00-subtask1',
                     '02-task1/01-subtask1',
                     '04-task2',
                     '05-task3',
                     '05-task3/01-subtask1',
                     '05-task3/03-subtask2']
        # These files should not report an error because they are not task dirs.
        files = [
            '02-task1/00-subtask1/01_fake_notebook.jpynb',
            '02-task1/00-subtask1/03_fake_notebook.jpynb'
        ]
        project_dir = self._createProject(task_dirs, files)
        flint = FlintCLN(project_dir)
        flint.run()
        errors = flint.errors()
        warnings = flint.warnings()
        self.assertTrue('task_ordering_skipped' in errors.keys(), 'Does not include the task_ordering_skipped tests when it should.')
        self.assertTrue(project_dir in errors['task_ordering_skipped'], 'Should error when the project root folder has misordered tasks.')
        self.assertTrue(os.path.join(project_dir, '05-task3') in errors['task_ordering_skipped'], 'Should error when the 05-task3 folder has misordered tasks.')
        self.assertFalse(os.path.join(project_dir, '02-task1') in errors['task_ordering_skipped'], 'Reports an error in the 02-task1 folder when it should not.')
        self.assertFalse(os.path.join(project_dir, '02-task1/00-subtask1') in errors['task_ordering_skipped'], 'Reports an error in the 02-task1/00-subtask1 folder when it should not.')
        self._cleanupProject(project_dir)

    def test_checkTaskCollection(self):
        """
        Tests the _checkTaskCollection() function.
        """
        #
        # Create a project with inappropriate file in a task directory
        #
        task_dirs = ['00-docs',
                     '01-input_data',
                     '02-task1',
                     '02-task1/00-subtask1',
                     '02-task1/01-subtask1']
        # Add a README.md which is good but also another file which is not good.
        files = [
            '02-task1/README.md',
            '02-task1/.gitignore',
            '02-task1/blah.txt',
            '02-task1/00-subtask1/01-fake_notebook.jpynb'
        ]
        project_dir = self._createProject(task_dirs, files)
        flint = FlintCLN(project_dir)
        flint.run()
        errors = flint.errors()
        warnings = flint.warnings()
        self.assertTrue('task_collection_dirs' in errors.keys(), 'Does not include the task_collection_dirs tests when it should.')
        self.assertTrue(os.path.join(project_dir, '02-task1/blah.txt') in errors['task_collection_dirs'], 'Should error for the 02-task1/blah.txt file.')
        self.assertFalse(os.path.join(project_dir, '02-task1/README.md') in errors['task_collection_dirs'], 'Reports an error for the 02-task1/README>md file when it should not.')
        self.assertFalse(os.path.join(project_dir, '02-task1/.gitignore') in errors['task_collection_dirs'], 'Reports an error for the 02-task1/.gitignore file when it should not.')
        self.assertFalse(os.path.join(project_dir, '02-task1/00-subtask1/01-fake_notebook.jpynb') in errors['task_collection_dirs'], 'Reports an error for the 02-task1/00-subtask1/01-fake_notebook.jpynb file when it should not.')
        self._cleanupProject(project_dir)
