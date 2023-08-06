..  Titling
    ##++::==~~--''``

.. _syntax:

Syntax guide
::::::::::::

A Turberfield scene script file represents a sequence of dramatic action.
A single file contains one or more scenes, each of which is composed of
separate shots. A shot can contain dialogue, audio effects and other directives.

A Scene script adopts the reStructuredText_ syntax. By using a defined subset
of that syntax, along with custom extensions, Turberfield defines a format which
visually resembles a traditional screenplay, yet which conforms to a formal data model.

A key feature of the format is that it allows roles to be cast dynamically, such
that objects must match the declared criteria for a role. It is nonetheless possible
for dialogue to refer to personal attributes such as names, using a mechanism of
`substitution references`_.

Naming convention
=================

The file name should contain lower case characters only. It should contain no whitespace
or punctuation characters. Underscores should be used to represent spaces.

The file must have a suffix of **.rst**. If you'd like to distinguish between dialogue
text and regular reStructuredText, then give your scene script file a **.dlg.rst** suffix.

Structure
=========

#. The file should begin with a comment_ identifying it as a Turberfield
   scene script.
#. The file should contain metadata identifying the author(s) in a
   `field list`_. The following fields are recommended:

   * author
   * date
   * copyright

#. The file must contain at least one `entity declaration`_ before any
   scene is defined.
#. The file must contain at least one **scene** section which is created by a
   top-level heading_.
#. Each scene  must contain at least one **shot** section which is created by a
   second-level heading_.
#. Dialogue is defined by a citation_ in a shot section.
   The name given in the citation must match an entity declaration.
   Dialogue may contain `inline markup`_ and `substitution references`_.
#. Shot sections may also contain one or more of these elements:
    * `Property directive`_
    * `FX directive`_
    * `Condition directive`_
    * `Memory directive`_

Elements
========

Entity declaration
~~~~~~~~~~~~~~~~~~

.. rst:directive:: .. entity:: NAME

    The name of an entity should be in upper case.

    ``:roles:``
        A whitespace separated sequence of other entities.
        A match for this entity will be considered for those roles.
        Optional.
    ``:states:``
        A whitespace separated sequence of dotted paths.
        Each path must resolve to a Python Enum class member.
        In addition, a single integer value is also allowed.

        The resolution rules allow for hierarchical states, eg:
            * `3` matches integer states `301`, `38` and `3`.
            * `Location.pub` matches `Location.pub` and `Location.pub_carpark`.

        A candidate for this entity must match *all* these state criteria.
        Optional.
    ``:types:``
        A whitespace separated sequence of dotted paths.
        Each path must resolve to a Python type.
        A candidate for this entity must be an instance of *at least one*
        of these types. Optional.

Property directive
~~~~~~~~~~~~~~~~~~

.. rst:directive:: .. property:: ATTRIBUTE [VALUE]

    This directive takes no other options.

    The property directive acts in two modes.

        * With a single argument it is a `getter`; it returns the attribute value.
          This is the mode to use when defining a substitution reference.
        * With two arguments it is a `setter`; it sets the attribute value.
          This allows you to modify entities during the delivery of dialogue.

FX directive
~~~~~~~~~~~~

.. rst:directive:: .. fx:: PACKAGE RESOURCE

    The FX (effects) directive calls up a visual cue or a sound effect.
    The first argument is the dotted name of the package which contains the asset file.
    The second argument is the path of the file relative to the package location.

    ``:duration:``
        Sets the duration (audio playback, display of still image).
        This value is in milliseconds. Optional.
    ``:loop:``
        The number of times to play the audio or display a still image.
    ``:offset:``
        Sets the point in an audio file at which playback begins.
        This value is in milliseconds.
    ``:label:``
        A text label for the resource. May contain substitution references.

Condition directive
~~~~~~~~~~~~~~~~~~~

.. rst:directive:: .. condition:: ATTRIBUTE VALUE

    This directive takes no other options.

    The condition directive specifies that a comparison be evaluated.
    If VALUE is supplied in parentheses, it is used as a Regular Expression.
    Otherwise, it is treated as a plain string, though it may contain
    substitution references.

    The intended purpose of this directive is to mask off sections of dialogue
    which do not satisfy certain criteria.

.. _memory:

Memory directive
~~~~~~~~~~~~~~~~

.. rst:directive:: .. memory:: STATE

    The Memory directive saves a record to the dialogue database. STATE is the dotted
    path to a Python Enum class value, or else an integer.

    This directive lets you capture relationships between entities and store
    them with a timestamp and a note of explanation.

    ``:subject:``
        The name of an entity which is primarily associated with STATE. With no `object`
        (see below) the interpretation is that the subject is assigned the state. If
        object is defined, the relationship between subject, object and state is
        application-specific.
    ``:object:``
        The name of an entity which is the object of the relationship
        ``(subject, state, object)``. Optional.

    Any paragraphs of inline content to this directive are used as a note which
    accompanies the record in the database. Such paragraphs may contain
    `inline markup`_ and `substitution references`_.

.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _field list: http://docutils.sourceforge.net/docs/user/rst/quickref.html#field-lists
.. _comment: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#comments
.. _inline markup: http://docutils.sourceforge.net/docs/user/rst/quickref.html#inline-markup
.. _heading: http://docutils.sourceforge.net/docs/user/rst/quickref.html#section-structure
.. _citation: http://docutils.sourceforge.net/docs/user/rst/quickref.html#citations
.. _substitution references: http://docutils.sourceforge.net/docs/user/rst/quickref.html#substitution-references-and-definitions
