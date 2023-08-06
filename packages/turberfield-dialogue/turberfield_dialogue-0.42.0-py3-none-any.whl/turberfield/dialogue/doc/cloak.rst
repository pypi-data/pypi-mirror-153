..  Titling
    ##++::==~~--''``

Example 2: Cloak of Darkness
::::::::::::::::::::::::::::

Turberfield-dialogue is a screenplay system; it's not intended by itself to be
a game framework.

Nonetheless, it strikes me that you might want to use it as a first port
of call when prototyping ideas for a large game. Especially if that game
is to contain a decent amount of dialogue.

So I decided to explore the degree to which this is possible. And here
is my implementation of `Cloak of Darkness`_.
 
.. admonition:: The `Hello World` of adventure games.

    `Cloak of Darkness`_ is a scenario which exercises several features
    that all game frameworks really should support.

    By implementing the game, the framework author demonstrates how those
    features are achieved.

    The game consists of three rooms. In one room is an invisible prize.
    But the prize is damaged by the player every time he visits the room.
    It turns out that the player is carrying an item which when dropped
    in one of the other rooms, allows the prize to be seen.

Interludes
==========

An adventure game is interactive. The action frequently pauses to allow the
player to input a command. In classic text adventures, that command is typed
in to the console.

Turberfield-dialogue has a feature called *interludes*. You may have spotted
that earlier; it's the fifth argument to a
:py:class:`~turberfield.dialogue.model.SceneScript.Folder`.
In :ref:`battle` we put ``None`` which is a way of declining to use interludes. 

An interlude is a function which gets called at the end of a scene script file.
You can define a different function for each if you like. The function sees
the folder you're using. It knows which of the scene files has just finished.
It also gets to see all the references you passed in to the performance.

An interlude function's return value is the metadata for a folder object.
Returning the current folder's metadata is like saying *continue*. Or you can
return different metadata matching another folder and thereby branch the story.

Design
======

My first instinct was to create a scene file for each of the three rooms. Then all
the action for a room goes in to the same file. We will repeat the sequence of
three scenes over and over, with an interlude between them to take user input.

Both the player and the cloak can move location. So we will need a state to
represent that. Also, the message must change every time it is damaged. That could
require another state, but it turns out that a simple Python attribute will suffice.

I want the game to run in :ref:`rehearsal`. Here's where the main problem
arises. The default behaviour is to run sequentially through scenes, and
deliver any dialogue possible. In this case, we only want the action to take
place in the location of the player. Otherwise, we will get ghostly voices
leaking in from other rooms. So we need to ensure that all other roles remain
uncast outside of the current location.
 
In the previous example we used an integer state variable to mark the fighters as
alive or dead. I'll reuse that concept. By default, every entity is masked out.
As the player moves around, certain objects become active, and others go quiet.

Implementation
==============

Logic
~~~~~

We're going through the code now. If Python is new to you, don't worry.
My intention is just to introduce some essential concepts which you can
work to understand later on.

The top of a Python module is where imports go:

.. code-block:: python

    import enum
    from itertools import repeat
    import random

    from turberfield.dialogue.model import SceneScript
    from turberfield.dialogue.types import DataObject
    from turberfield.dialogue.types import Stateful

Next we declare an enumeration state which will define the
location of the player and the cloak:

.. code-block:: python

    @enum.unique
    class Location(enum.Enum):
        foyer = 0
        bar = 1
        cloakroom_floor = 2
        cloakroom_space = 3
        cloakroom_hook = 4

There are no Personas in this game; none of the voices has a name.
But they do have state, and one of them needs attributes. The
useful types to inherit from will be *Stateful* and *DataObject*.

Each of the entities in the game gets its own class declaration:

.. code-block:: python

    class Narrator(Stateful):
        pass

    class Cloak(Stateful):
        pass

    class Prize(Stateful, DataObject):
        pass

So now we can declare an ensemble of entities, setting attributes
and initial state where appropriate:

.. code-block:: python

    ensemble = [
        Narrator().set_state(Location.foyer),
        Cloak().set_state(Location.foyer).set_state(1),
        Prize(message="You win!")
    ]


We will be taking user input and trying to interpret commands.
Here is the world's dumbest text parser. It returns the first
letter of the last word typed into the console:

.. code-block:: python

    def parse_command(cmd):
        try:
            return cmd.strip().split(" ")[-1][0].lower()
        except:
            return None

We want user input at the end of every turn. That's done in a single
interlude function. Should the game grow any larger, it would be better
to give each file its own custom function, but this is good enough for
an example. I'm just going to throw the code at you and see how you get
on:

.. code-block:: python

    def interaction(folder, index, ensemble, *args, cmd="", log=None, **kwargs):
        narrator, cloak, prize, *others = ensemble
        locn = narrator.get_state(Location)
        action = None
        if locn == Location.foyer:
            while action not in ("s", "w", "q"):
                action = parse_command(cmd or input("Enter a command: "))
            if action == "s":
                narrator.set_state(Location.bar)
                if cloak.get_state(Location) == locn:
                    prize.set_state(0)
                else:
                    prize.set_state(1)
            elif action == "w":
                narrator.set_state(Location.cloakroom_space)
                cloak.set_state(1)
            else:
                return None
        elif locn == Location.bar:
            while action != "n":
                action = parse_command(cmd or input("Enter a command: "))

            narrator.set_state(Location.foyer)
            prize.message = prize.message.replace(
                random.choice(prize.message), " ", 1
            )
            prize.set_state(0)
        elif locn == Location.cloakroom_space:
            while action not in ("c", "h", "e"):
                action = parse_command(cmd or input("Enter a command: "))
            if action == "c":
                if cloak.get_state(Location) == Location.cloakroom_space:
                    cloak.set_state(Location.cloakroom_floor)
                else:
                    cloak.set_state(Location.cloakroom_space)
            elif action == "h":
                cloak.set_state(Location.cloakroom_hook)
            else:
                narrator.set_state(Location.foyer)
                if cloak.get_state(Location) != locn:
                    cloak.set_state(0)

        if cloak.get_state(Location) == locn:
            cloak.set_state(narrator.get_state(Location))
            cloak.set_state(1)

        return folder.metadata

So now we can declare the objects *turberfield-rehearse* needs to
see; a collection of all our Python references and a folder object
with details of the game:

.. code-block:: python

    references = ensemble + [Location]

    folder = SceneScript.Folder(
        pkg=__name__,
        description="The 'Hello World' of text games.",
        metadata={},
        paths=["foyer.rst", "bar.rst", "cloakroom.rst"],
        interludes=repeat(interaction)
    )

.. admonition:: Coding.

    Python is a pretty easy language to read, and so far I've been relying on
    that to communicate the essence of how all this works. We have reached a
    point now that you may need to take time over certain aspects of the code
    to fully understand what is going on.

    I recommend you explore the `Python manual`_. First, get to know its
    structure; how it separates the fundamentals of the language from details
    of specific modules which you discover when you realise you need them.

    To begin with, check out the `random module`_ which is very straightforward.
    After that, use the `module index`_ to find the documentation for *Enum*.

Dialogue
~~~~~~~~

Here's where I stop explaining each component of the game. When it comes
to understanding the dialogue, it's best just to study the *.rst* files
in *sequences/cloak*. As a taster, here's what the dialogue for the first
room looks like. It's probably the simplest of the three.

.. code-block:: rest

    .. entity:: NARRATOR
       :types: logic.Narrator
       :states: logic.Location.foyer

    .. entity:: CLOAK
       :types: logic.Cloak
       :states: logic.Location.foyer

    After the fire, a Magician returns
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    From where you stand
    --------------------

    [NARRATOR]_

        This place no longer looks much like a hotel. This would have been the foyer, though.
        You can see the footprint of a grand reception desk running down one side
        of the floor.

    [NARRATOR]_

        The room has been stripped of all it once contained.

    Checking your person
    --------------------

    [CLOAK]_

        You are wearing a long cloak, which gathers around you. It feels furry,
        like velvet, although that's hard to tell by looking. It is so black
        that its folds and textures cannot be perceived.

    [CLOAK]_

        It seems to swallow all light.

    .. memory:: logic.Location.foyer
       :subject: NARRATOR

       The Player visited the foyer.

    Looking around
    --------------

    [NARRATOR]_

        To the North, the door by which you first entered is stuck fast.

    [NARRATOR]_

        There are other doors to the South and West.

Action
======

You can run the game in a similar manner to the previous example::

    cd sequences/cloak
    ~/py3.5/bin/turberfield-rehearse @rehearse.cli

Memory
======

We saw for the first time above the use of a :ref:`memory`. The game scatters
them throughout the action. The result is that a record of the player's
progress builds up in the dialogue database.

The database Turberfield uses for this is SQLite3_. You can access this database
via Python's own `SQLite3 module`_. Or you can install a command line tool and
issue queries that way. Try this to get a report of the passage of a game
session::

    sqlite3 cloak.sl3

    sqlite> select s.name, state.name, note.text 
       ...> from state join touch on state.id = touch.state 
       ...> join entity as s on touch.sbjct = s.id 
       ...> left outer join entity as o on touch.objct = o.id 
       ...> left outer join note on note.touch = touch.id;

    Narrator|foyer          |The Player visited the foyer.
    Cloak   |bar            |The Player wore the cloak in the bar.
    Narrator|foyer          |The Player visited the foyer.
    Cloak   |cloakroom_floor|The Player dropped the cloak.
    Narrator|foyer          |The Player visited the foyer.
    Cloak   |bar            |The Player wore the cloak in the bar.
    Narrator|foyer          |The Player visited the foyer.
    Cloak   |cloakroom_hook |The Player hung the cloak on a hook.
    Narrator|foyer          |The Player visited the foyer.
    Prize   |bar            |The Player read the message as " Yo  w n! ".
    Narrator|foyer          |The Player visited the foyer.

.. _Cloak of Darkness: http://www.firthworks.com/roger/cloak/
.. _Python manual: https://docs.python.org/3/
.. _random module: https://docs.python.org/3/library/random.html#module-random
.. _module index: https://docs.python.org/3/py-modindex.html
.. _SQLite3: https://www.sqlite.org
.. _SQLite3 module: https://docs.python.org/3/library/sqlite3.html#module-sqlite3
