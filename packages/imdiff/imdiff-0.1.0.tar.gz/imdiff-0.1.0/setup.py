import pathlib
import re
import setuptools


def read_version():
    here = pathlib.Path(__file__).parent
    versionfile = here/'imdiff/version.py'
    m = re.search(r"__version__ = '(.*?)'", versionfile.read_text(), re.M)
    return m.group(1)


def setup():
    setuptools.setup(
        name='imdiff',
        version=read_version(),
        description='Compare image files in different directories.',
        author='John T. Goetz',
        author_email='theodore.goetz@gmail.com',
        classifiers=[
            # Development Status
            #   1 - Planning
            #   2 - Pre-Alpha
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            #   6 - Mature
            #   7 - Inactive
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Scientific/Engineering :: Image Processing',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing',
            'Topic :: Utilities',
        ],
        keywords=[
            'test',
            'development',
            'validation',
            'images',
            'comparison',
            'diff',
        ],
        install_requires=['numpy', 'pillow'],
        packages=['imdiff'],
        entry_points={"console_scripts": ["imdiff=imdiff.__main__:main"]}
    )


if __name__ == '__main__':
    setup()
