from setuptools import find_packages, setup

requirements = """
""".split()

setup(
    name='FlintCLN',
    packages=find_packages(),
    url='https://gitlab.com/ficklin-lab/flintcln',
    version='0.1.0a',
    description='Flint is a linting tool to ensure projects in the Ficklin Research Program follow expected standards.',
    author='Ficklin',
    license='GNU General Public License v3.0',
    python_requires='>=3.6',
    install_requires=requirements,
    tests_require=['nose'],
    test_suite="nose.collector",
    entry_points={'console_scripts': [
        'flint-cln = FlintCLN.cmd:run',
    ]},
)
