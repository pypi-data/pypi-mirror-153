..  Titling
    ##++::==~~--''``

.. _publishing:

Publishing
::::::::::

The demo examples you've seen so far were arranged as standalone
directories containing a Python module and some scene script files.

You can get started quickly by working this way, but before your
screenplay is ready, you need to have properly configured it as
a Python package.

Packaging gives you the following advantages:

* Versioning_
* Attribution_
* Distribution_
* Installability_
* `Dependency management`_
* Discoverability_

Checklist
=========

Turning your screenplay into a package might be a pain the first time
you do it. But you'll reap the benefits after that. Here's what you have
to do.

#. `Organise your project directory`_
#. `Make a manifest`_
#. `Write a README file`_
#. `Write the setup.py`_

Organise your project directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose your screenplay, **mydrama** is in a single directory of that name.
You have three scene script files; `begin.rst`, `middle.rst`, and `end.rst`.
You have an idea for a soundtrack you call `theme.wav`. And there is one
Python module called `logic.py`. You have saved some options as a file
called `rehearse.cli`::

    mydrama
    ├── begin.rst
    ├── middle.rst
    ├── end.rst
    ├── theme.wav
    ├── logic.py
    └── rehearse.cli

Now create four more empty files as follows::

    ├── __init__.py
    ├── MANIFEST.in
    ├── README.rst
    └── setup.py

There is nothing more to do to `__init__.py`. It stays empty. We will deal
with the other three in turn.

.. important::

   The naming conventions for Python packages are quite strict. Your directory
   name should use only lower case letters. If you want to signify a space in
   the directory name, use an underscore.

   Also, **never use the word 'turberfield' in your package name**.
   It's for software tooling only. 

Make a manifest
~~~~~~~~~~~~~~~

The `MANIFEST.in` file decides which of your source files get
installed. It can filter out any project files created by your text
editor, cache files and the like. It should look like this::

    recursive-include . *.cli
    recursive-include . *.rst
    recursive-include . *.wav

Write a README file
~~~~~~~~~~~~~~~~~~~

The `README.rst` file is an opportunity to describe your drama to
potential collaborators. It is a reStructuredText_ file, so you can include
hyperlinks and other useful structures.

At a minimum, this file should contain your name, email address and
an assertion of your copyright. Other details are up to you.

Write the setup.py
~~~~~~~~~~~~~~~~~~

`setup.py` is like an electronic form which tells the packaging system
everything about your project. Here is the standard boilerplate you should use.

.. code-block:: python

    #!/usr/bin/env python
    # encoding: UTF-8

    from setuptools import setup
    import os.path

    __doc__ = open(
        os.path.join(os.path.dirname(__file__), "README.rst"),
        "r"
    ).read()

    setup(
        name="mydrama",
        version="0.1.0",
        description="A dramatic screenplay",
        author="Ernest Scribbler",
        author_email="escribbler@zmail.com",
        url="http://pypi.python.org/pypi/mydrama",
        long_description=__doc__,
        classifiers=[
            "Framework :: Turberfield",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: Other/Proprietary License",
        ],
        packages=["mydrama"],
        package_dir={"mydrama": "."},
        include_package_data=True,
        install_requires=["turberfield-dialogue"],
        zip_safe=True,
        entry_points={}
    )

Of course, you'll need to alter some details to match the name of your
particular project, here::

        name="mydrama",

... and here::

        packages=["mydrama"],
        package_dir={"mydrama": "."},

In the next few sections, we'll customise a little further.

Versioning
==========

As soon as other people begin to use your dialogue, you'll need to give
them a way of deciding whether they want to use your latest rewrite or
to stick with an earlier revision. Every release of your work will have a
version number to identify it.

You declare the version in the `setup` parameters in `setup.py`::

    version="0.1.0",

The three digits reflect the significance of any new change:

    * Trivial fixes increment the rightmost digit.
    * Significant changes increment the middle version field. This is the
      most frequent case; the number can go as high as you like, even into
      the hundreds.
    * Major changes which are incompatible with previous versions require
      an increment to the leftmost digit. 

Attribution
===========

I'm guessing your name is not Ernest Scribbler. If it is, write in
and let me know! Otherwise, you'll change the following parameters to match
your online identity::

    author="Ernest Scribbler",
    author_email="escribbler@zmail.com",

Distribution
============

The command to create a `distribution` of your project is this::

    ~py3.5/bin/python setup.py sdist

The packaging system creates an installable for you. You'll find
it at `dist/mydrama-0.1.0.tar.gz` or `dist/mydrama-0.1.0.zip`,
depending on your OS.

You can upload that file to a package repository. The most popular is
PyPI_ but there are alternatives, such as Gemfury_.

So you'll need to declare the correct URL to your package once
it gets up there::

        url="http://pypi.python.org/pypi/mydrama",

This is a bit of a chicken-and-egg situation of course. You'll have to
anticipate what the URL is going to be before you upload it, or
else you'll have a misprint in the first release which you'll need to fix
afterwards. 

Installability
==============

With your work properly packaged, you can be confident that others can
start using it with a minimum of fuss.

If you upload it to PyPI_, `pip` will go out and fetch it::

    ~/py3.5/bin/pip install mydrama 

Or you could send your package file by email or on a USB stick. Then
the install command targets the package file like this::

    ~/py3.5/bin/pip install mydrama-0.1.0.tar.gz

Dependency management
=====================

Your package gets to declare which other Python libraries it needs to run.
I already gave you the one essential dependency::

    install_requires=["turberfield-dialogue"],

It's quite possible that your `logic.py` might rely on some other
library to do a particular job. Perhaps you've written a role for a banker
who needs to `calculate loan interest`_.

Whatever PyPI_ package you add to this list will be automatically installed
with your screenplay and available for use from your Python modules.

Discoverability
===============

Publishing your work is a crucial step. But as well as that, you have to
advertise.  When a game developer puts out the call for some dramatic
dialogue, you want to be able to say,
'Yes, there's a scene for that. I wrote it. Here it is.'

So now you need to create a unique global id for the scene you just wrote.

Python helps you here. It has a standard module called `uuid`, which is
short for `unique user id`. Here's how you use it to generate a one-time
code to identify a folder of scenes you just created::

    ~/py3.5/bin/python -c"import uuid; print(uuid.uuid4().hex)"

What you get back is a 32-character code which looks a bit like this::

    c.1de5c.3f5a4abe..937.7.6e55a.8e

I put dots in it so you wouldn't cheat and copy mine. Dots are illegal.
Make your own!

Now you go back to `setup.py` and edit the `entry_points` parameter.
Like this:

.. code-block:: python

    entry_points={
        "turberfield.interfaces.folder": [
            "c.1de5c.3f5a4abe..937.7.6e55a.8e = mydrama.logic:folder",
        ],
    },

Doing this advertises your folder so it can be discovered and used during
the course of a game.

.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _PyPI: https://pypi.python.org/pypi
.. _Gemfury: https://gemfury.com
.. _calculate loan interest: https://pypi.python.org/pypi/tallywallet-common
