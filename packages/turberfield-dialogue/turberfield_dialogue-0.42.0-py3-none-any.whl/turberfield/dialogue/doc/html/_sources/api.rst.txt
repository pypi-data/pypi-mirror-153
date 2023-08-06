..  Titling
    ##++::==~~--''``

API Reference
:::::::::::::

This API lets you customise the rehearsal of
a :py:class:`~turberfield.dialogue.model.SceneScript.Folder`
of Turberfield dialogue. You can modify how this performance is presented
in your game by customising or replacing a handler_ function which processes
events_ from the scene script files.

If you need to integrate with a game event loop, then create a
:py:class:`~turberfield.dialogue.performer.Performer` object instead.
This separates event generation from sequencing.

The `scene scripts`_ themselves also have an API, allowing you to interact with
the process by which entities are selected and cast to roles.

There is also a simple :py:class:`~turberfield.dialogue.matcher.Matcher` class
which you can use to compare folder metadata.

Folders
=======

.. autoattribute:: turberfield.dialogue.model.SceneScript.Folder
   :annotation: (pkg, description, metadata, paths, interludes)

   :param pkg: The dotted (importable) name of the package which
        installs the scene script folder.

        Absent proper packaging, you must set this parameter to
        `__name__`. The Python module which declares the folder will
        act as the anchor location for scene files, and all
        referencing paths will need to be made relative to the
        module.
   :param str description: A free text description of the contents
        of the folder.
   :param metadata: An optional sequence or mapping containing
        application-specific metadata.

        This parameter is for the purposes of searching or filtering
        collections of folders against particular criteria.
   :param paths: A list of strings, each of which is the path to a
        scene script file relative to the object declared in the
        parameter **pkg**.

        Path separator is always "**/**" notwithstanding the local
        Operating System.
   :param interludes: A sequence of function objects.
        The sequence should be such as to provide one object for
        each of the scene script files declared in the parameter
        **paths**.

        A function object will be called when its corresponding
        scene script file has been performed.

        See Interludes_ for the required signature of an interlude
        function object.

Scene scripts
=============

.. autoclass:: turberfield.dialogue.model.SceneScript
   :members: scripts, read, select, cast, run
   :member-order: bysource

Events
======

.. autoclass:: turberfield.dialogue.model.Model

.. autoattribute:: turberfield.dialogue.model.Model.Shot
   :annotation: (name, scene, items)

   An event which signals the beginning of a shot in a scene.

.. autoattribute:: turberfield.dialogue.model.Model.Property
   :annotation: (entity, object, attr, val)

   An event which signals a property is to be accessed.

.. autoattribute:: turberfield.dialogue.model.Model.Audio
   :annotation: (package, resource, offset, duration, loop)

   An event which signals an audio cue.

.. autoattribute:: turberfield.dialogue.model.Model.Still
   :annotation: (package, resource, offset, duration, loop, label, width, height)

   An event which signals a still image cue.

.. autoattribute:: turberfield.dialogue.model.Model.Video
   :annotation: (package, resource, offset, duration, loop, label, width, height, poster, url)

   An event which signals a video cue.

.. autoattribute:: turberfield.dialogue.model.Model.Memory
   :annotation: (subject, object, state, text, html)

   An event which signals a memory directive.

.. autoattribute:: turberfield.dialogue.model.Model.Line
   :annotation: (persona, text, html)

   An event which signals a line of dialogue.

.. autoattribute:: turberfield.dialogue.model.Model.Condition
   :annotation: (object, attr, val, operator)

   An event which evaluates a conditional expression.

Interludes
==========

An interlude is a callable object (either a function, an instance
method or a Python object with a callable interface).

It is called by a handler at the end of the performance of a scene script file.
That is the `current scene` file as referred to below.

Here is an example to show the signature of parameters required.

.. py:function:: def my_interlude(folder, index, ensemble, log=None, loop=None):

    :param folder: A :py:class:`~turberfield.dialogue.model.SceneScript.Folder` object.
    :param int index: The index position into **folder.paths** of the current
        scene script file.
    :param ensemble: A sequence of Python objects. It is guaranteed to contain
        all the objects cast to roles in the current scene. It will be used to
        select entities for the next.
    :param log: If supplied, this will be a ``logging.Logger`` object which
        should be used in preference over any other for logging messages from within
        your interlude function.
    :param loop: If supplied, this will be an instance of ``asyncio.BaseEventLoop``.
        That will signal to your function that it operates in an asynchronous
        environment and that no blocking function should be called within it.
    :returntype: dict

        Returning this object gives you the option to control branching of
        your narrative.

        The dictionary data you pass back is matched against the metadata of
        each folder. The folder whose metadata matches closest is the next
        folder to run.

        Return **None** to stop the performance.

Handler
=======

.. autoclass:: turberfield.dialogue.handlers.TerminalHandler
   :members: handle_audio, handle_interlude, handle_line, handle_memory, handle_property, handle_scene, handle_scenescript, handle_shot
   :member-order: bysource

Matcher
=======

.. autoclass:: turberfield.dialogue.matcher.Matcher
   :members: __init__, mapping_key, options
   :member-order: bysource

Performer
=========

.. autoclass:: turberfield.dialogue.performer.Performer
   :members: __init__, next, run, stopped
   :member-order: bysource

Player
======

.. autofunction:: turberfield.dialogue.player.rehearse

.. _simple function: py:func:`turberfield.dialogue.player.rehearse`.
