# Shadowed

> Manage file changes with shadowed copies.

[![Latest Version on PyPI](https://img.shields.io/pypi/v/shadowed.svg)](https://pypi.python.org/pypi/shadowed/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/shadowed.svg)](https://pypi.python.org/pypi/shadowed/)
[![Build Status](https://secure.travis-ci.org/christophevg/shadowed.svg?branch=master)](http://travis-ci.org/christophevg/shadowed)
[![Documentation Status](https://readthedocs.org/projects/shadowed/badge/?version=latest)](https://shadowed.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/christophevg/shadowed/badge.svg?branch=master)](https://coveralls.io/github/christophevg/shadowed?branch=master)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.1.6-blue.svg)](https://github.com/christophevg/pypi-template)


## Getting Started

Shadowed is hosted on PyPi, so...

```bash
% pip install shadowed
```

### Typical Intended Use

Given a folder where you want to maintain files that can be altered by users, and a folder where you can store shadow copies of the original files, maintain the content of maintained files, providing updates and respecting the changes that were made by users in between updates.

#### Initial Setup

```pycon
>>> import shadowed
>>> fs = shadowed.FileSystem(".", ".shadow")
>>> fs.create("README.md", '''# Hello World
... This is the first version of the README file.
... You ca change it, and I will apply future updates, preserving your changes.
... Regards,
... Christophe
... ''')
```

In the meantime on the local filesystem:

```console
% cat README.md 
# Hello World
This is the first version of the README file.
You ca change it, and I will apply future updates, preserving your changes.
Regards,
Christophe
% cat .shadow/README.md 
# Hello World
This is the first version of the README file.
You ca change it, and I will apply future updates, preserving your changes.
Regards,
Christophe
```

#### User Changes

The user decides to improve the file a bit and turns it into:

```markdown
# Hello My World
This is the first version of the README file.
Regards,
the User
```

#### Whoops

I made a typo... Let's fix it and push the change to the user:

```pycon
>>> import shadowed
>>> fs = shadowed.FileSystem(".", ".shadow")
>>> fs.create("README.md", '''# Hello World
... This is the second version of the README file.
... You ca**N** change it, and I will apply future updates, preserving your changes.
... Regards,
... Christophe
... ''')
```

And this results in:

```console
% cat README.md        
# Hello My World
This is the second version of the README file.
Regards,
the User

% cat .shadow/README.md
# Hello World
This is the second version of the README file.
You ca**N** change it, and I will apply future updates, preserving your changes.
Regards,
Christophe
```

All changes by the user are preserved and my improvements are applied.
