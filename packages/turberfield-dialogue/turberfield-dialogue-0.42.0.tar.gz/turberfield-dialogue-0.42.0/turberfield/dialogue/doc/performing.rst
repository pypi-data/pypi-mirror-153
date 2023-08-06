..  Titling
    ##++::==~~--''``

.. _performing:

Performing
::::::::::

Making a name for yourself
==========================

Congratulations on self-publishing your screenplay. You can build on that
and start to socialise the use of the name you chose for your project.

Remember way back when you were putting `__name__` as the **pkg** argument
to declare your :py:class:`~turberfield.dialogue.model.SceneScript.Folder`
object? No need to do that any more. `mydrama` (or whatever you picked
instead) is the name of the package now.

Likewise in scene script files, if there's a particular type you specify
for an entity, that will be `mydrama.logic.VeterinarySurgeon` and so on.
And because you have published your work, the whole world knows what you
mean by that.

Getting discovered
==================

Here's how a Python developer, after installing your package, might look
for some dialogue suited to his modern reimagining of some Shakespearian
tragedy:

.. code-block:: python

    from turberfield.utils.misc import gather_installed

    guid, folder = next(
        (i for i in gather_installed("turberfield.interfaces.folder")
        if "betrayal" in v.metadata),
        (None, None)
    )

Constraining entity selection
=============================

One last tip. The :py:func:`~turberfield.dialogue.player.rehearse` function has
been good to us. But it is very forgiving in the way it allows even
minimally-cast scenes to play through. Sometimes we want all or nothing.
Here is a way to pre-filter scenes so that only those fully cast are performed.

.. code-block:: python

    def is_fully_cast(folder, references):
        for script in SceneScript.scripts(**folder._asdict())
            with script as dialogue:
                selection = dialogue.select(references)
                if all(selection.values()):
                    continue:
                else:
                    return False
        return True

.. _packaging tutorials: http://thuswise.co.uk/packaging-python-for-scale-part-one.html
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _PyPI: https://pypi.python.org/pypi
.. _Gemfury: https://gemfury.com
.. _calculate loan interest: https://pypi.python.org/pypi/tallywallet-common
