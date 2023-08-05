# stqe

Kernel-QE Storage test suite

### Dependencies
* Python >= 3.6
* pip >= 19

#### RHEL-8.x RHEL-9.x | Fedora
`dnf install python3-netifaces python3-augeas`
#### RHEL-7
`yum install augeas-libs`

### Installation
`python -m pip install stqe --no-binary=stqe`\
or\
`git clone; cd python-stqe`\
`python -m pip install .`

(optional) edit /etc/san_top.conf example

#### How to Uninstall
`python -m pip uninstall stqe`

### Packaging
 While in python-stqe dir:

`python -m pip install build`\
`python -m build`

#### Basic usage
`stqe-test --help`

