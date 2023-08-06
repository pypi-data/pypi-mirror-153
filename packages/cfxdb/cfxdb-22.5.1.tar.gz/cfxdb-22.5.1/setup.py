###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from setuptools import setup, find_packages


# read package version
with open('cfxdb/_version.py') as f:
    exec(f.read())  # defines __version__

# read package description
with open('README.rst') as f:
    docstr = f.read()

# we read requirements from requirements*.txt files down below
install_requires = []
extras_require = {
    'dev': []
}

reqs = 'requirements.txt'

# https://mike.zwobble.org/2013/05/adding-git-or-hg-or-svn-dependencies-in-setup-py/
dependency_links = []

with open(reqs) as f:
    for line in f.read().splitlines():
        line = line.strip()
        if not line.startswith('#'):
            parts = line.strip().split(';')
            if len(parts) > 1:
                parts[0] = parts[0].strip()
                parts[1] = ':{}'.format(parts[1].strip())
                if parts[1] not in extras_require:
                    extras_require[parts[1]] = []
                extras_require[parts[1]].append(parts[0])
            else:
                name = parts[0].strip()
                # do NOT (!) touch this! add dependency to either install_requires or dependency_links
                # depending on whether a git+ URL is used or not (eg plain PyPI)
                # https://mike.zwobble.org/2013/05/adding-git-or-hg-or-svn-dependencies-in-setup-py/
                if name.startswith('git+'):
                    dependency_links.append(name)
                elif name != '':
                    install_requires.append(name)

with open('requirements-dev.txt') as f:
    for line in f.read().splitlines():
        extras_require['dev'].append(line.strip())

setup(
    name='cfxdb',
    version=__version__,  # noqa
    description='Crossbar.io Database, based on zLMDB',
    long_description=docstr,
    license='MIT License',
    author='Crossbar.io Technologies GmbH',
    url='https://crossbario.com',
    classifiers=["License :: OSI Approved :: MIT License",
                 "Development Status :: 5 - Production/Stable",
                 "Environment :: No Input/Output (Daemon)",
                 "Framework :: Twisted",
                 "Intended Audience :: Developers",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "Programming Language :: Python :: Implementation :: CPython",
                 "Programming Language :: Python :: Implementation :: PyPy",
                 "Topic :: Internet",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Communications",
                 "Topic :: System :: Distributed Computing",
                 "Topic :: Software Development :: Libraries",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Topic :: Software Development :: Object Brokering"],
    platforms=('Any'),
    python_requires='>=3.7',

    install_requires=install_requires,

    # https://mike.zwobble.org/2013/05/adding-git-or-hg-or-svn-dependencies-in-setup-py/
    dependency_links=dependency_links,

    extras_require=extras_require,

    packages=find_packages(),
    # this flag will make files from MANIFEST.in go into _source_ distributions only
    include_package_data=True,
    data_files=[('.', ['LICENSE', 'README.rst', 'requirements.txt', 'requirements-dev.txt'])],
    zip_safe=True
)
