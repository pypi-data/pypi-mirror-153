from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

version = {}
with open("stqe/_version.py") as fp:
    exec(fp.read(), version)

setup(
    name='stqe',
    version=version['__version__'],
    description='Python modules used by kernel storage QE team',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/rh-kernel-stqe/python-stqe',
    author='Bruno Goncalves',
    author_email='bgoncalv@redhat.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='stqe, python-stqe, stqe-test',
    packages=find_packages(
        include=['stqe*']
    ),
    python_requires='>=3.6',
    install_requires=['libsan', 'python-augeas', 'fmf==1.0.0', 'pexpect'],
    package_data={
        "": ["*.py", "*.fmf", "*.conf", "*.cfg", ".fmf/version"]
    },
    data_files=[('/etc/', ['multipath.conf', 'san_top.conf']),
                ('/usr/share/man/man1', ['man/stqe-test.1'])],
    scripts=["bin/stqe-test", "bin/stqe-tool", "bin/fc_tool"],
    project_urls={
        'Bug Reports': 'https://gitlab.com/rh-kernel-stqe/python-stqe/issues',
        'Source': 'https://gitlab.com/rh-kernel-stqe/python-stqe',
    },
)