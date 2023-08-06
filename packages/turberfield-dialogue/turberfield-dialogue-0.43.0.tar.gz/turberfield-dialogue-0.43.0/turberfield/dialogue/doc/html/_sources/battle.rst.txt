..  Titling
    ##++::==~~--''``

.. _battle:

Example 1: Battle Royal
:::::::::::::::::::::::

Turberfield comes with a couple of examples. We will start with the simplest.
What we learn here will set us up for the more advanced example later.

This is our first encounter with the Turberfield rehearsal tool. We will use
it to preview the action in the first example.

.. admonition:: What are my options?

    It may be that this is the first time you have launched a Python program from
    your computer's command line. If so, there's a couple of things to understand
    first.

    When you launch a command line program, you do so by typing its name. You then
    follow that with *options* which are extra instructions to control the way the
    program behaves.

    The Turberfield rehearsal tool takes several options. Typing them all out every
    time is an annoyance. So the essential ones are stored in a text file called
    *rehearse.cli*. You can pass this file to the program instead and it will take
    the options from there. You can add more from the command line at the same time
    by typing them afterwards in the usual way.

    To instruct the rehearsal tool to load stored options, precede the path to the options
    file with a `@` symbol.

.. _rehearsal:

Rehearsal
=========

On Linux or MacOSX::

    $ cd sequences/battle
    $ ~/py3.5/bin/turberfield-rehearse @rehearse.cli

On Windows 8.1::

    > cd sequences\battle
    > start %USERPROFILE%\py3.6\Scripts\turberfield-rehearse @rehearse.cli

.. admonition:: You can do this.

    From now on, I'll assume you know how to operate the command line on your computer.
    Further instructions will give the Linux form of commands only, and omit the prompt
    character.

Here's what you should see in your terminal window. The dialogue is delivered incrementally.
There's also a sound effect at the appropriate point::

      Scratchy
              I hate the way you use me,  Itchy  !

      Ol' Rusty Chopper
              **Whack!**

      Itchy
              Uuurrggh!

        Itchy.state = 0

Script file
===========

Let's take a peek at the file which generates the dialogue. You can open
`sequences/battle/combat.rst` to see it in full. Here's the gist of
it below.

.. code-block:: rest
    :emphasize-lines: 13-15, 22-28

    .. entity:: FIGHTER_1
       :states: 1
       :roles: WEAPON

    .. entity:: FIGHTER_2
       :types: logic.Animal
       :states: 1

    .. entity:: WEAPON
       :types: logic.Tool


    [FIGHTER_1]_

        I hate the way you use me, |fighter2| !

    .. fx:: logic slapwhack.wav
       :offset: 0
       :duration: 3000
       :loop: 1

    [WEAPON]_

        **Whack!**

    [FIGHTER_2]_

        Uuurrggh!

    .. property:: FIGHTER_2.state 0

    .. |fighter2| property:: FIGHTER_2.name.firstname

If you look at the yellow highlighted sections, you'll see immediately how they correspond
to lines of dialogue. Notice how they aren't allocated to characters by name. Instead, the
dialogue is written for generic *roles*. Part of Turberfield's job is to match characters to
those roles.

The script file also contains other sections which do not correspond to dialogue. They are called
*directives*. I will explain those in the next section.

.. admonition:: If names be not correct...

   From now on, I'm going to start being precise in what I call things. I will avoid the words
   *Actor* and *Character*, since they suggest a human being.

   In screenplay any thing, whether animate or inanimate, can have a voice.
   So Turberfield calls them **Entities**.

   Entities can have **attributes**. An entity with a *name* attribute is called a **Persona**.
   An entity with *state* attributes is called **Stateful**. In addition to those, you can define
   your own **types** for your entities.  So long as their types match, one entity can play the
   **role** of another entity.

References
==========

Alongside the script file, there is a Python (.py) file.
Python files are called `modules`.
They supply the entities referred to in the script.
You should take a look in detail at `sequences/battle/logic.py`.
Here below are its main features.


.. code-block:: python

    from turberfield.dialogue.model import SceneScript
    from turberfield.dialogue.types import Persona
    from turberfield.dialogue.types import Stateful


    class Animal(Stateful, Persona):
        pass

    class Tool(Stateful, Persona):
        pass

    references = [
        Animal(name="Itchy").set_state(1),
        Animal(name="Scratchy").set_state(1),
        Tool(name="Ol' Rusty Chopper").set_state(1),
    ]

    folder = SceneScript.Folder(
        pkg=__name__,
        description="Cartoon battle demo",
        metadata=None,
        paths=["combat.rst"],
        interludes=None
    )


This file performs five tasks:

    Lines 1 - 5
        Import what we need from Turberfield.
    Lines 8 - 12
        Define some types which are necessary for the scene.
    Lines 14 - 18
        Create some objects to be referenced by the script.
        We also give them a state at the same time.
    Lines 20 - 26
        Declare a folder object which contains our scene script file.
        There are several other elements here, and we'll go into it properly
        later.

Type
====

A type is a concept from Python. You can create types with a `class` declaration
in a Python module. In all these examples, we do no more than inherit behaviour
from other base classes, hence the single `pass` instruction in the class
body.

Notice that two of the entity declarations in the script
file have a `:types:` constraint; Fighter 2 has to be some kind of Animal, and
the Weapon a Tool.

State
=====

The Battle Royal sequence makes use of `state`. Both fighters must be
alive at the beginning of the scene. This is encoded as a simple integer state,
which is set in the Python module when the references are created.

The entity declaration in the script file specifies the state must be 1 in
order for a persona to be cast as one of the fighters in the scene.

A property directive in the scene file zeroes the state of the smitten
fighter. We'll look in more detail how this works in the :ref:`syntax`.

Roles
=====

By default, Turberfield's rehearsal proceeds despite any unmatched entities.
The lines will not be voiced for unmatched parts. If you want to be strict
about only playing fully-cast scene files, you can specify that with an option.

In either case, if *none* of the entities in the scene can be cast, the entire
scene is skipped.

An extra dimension to the casting of entities is the concept of `roles`.
When roles are attached to an entity declaration it means that the
persona which gets cast to play that entity becomes a candidate to
play those other entities too.

In this way, a scene written as a montage of ensemble dialogue could
still be delivered as a monologue were there to be only one persona
available to deliver the lines.

Repeats
=======

By default the rehearsal tool runs through the scene just once. To see the
effect of roles in this example, we'll need the scene to repeat. Launch
the rehearsal again, this time specifying a repetition::

    ~/py3.5/bin/turberfield-rehearse --repeat=1 @rehearse.cli

And you should see the carnage play out, with one inevitable winner left standing::

    Scratchy
          I hate the way you use me,  Itchy  !

    Ol' Rusty Chopper
          **Whack!**

    Itchy
          Uuurrggh!

        Itchy.state = 0

    Ol' Rusty Chopper
          I hate the way you use me,  Scratchy  !

    Ol' Rusty Chopper
          **Whack!**

    Scratchy
          Uuurrggh!

        Scratchy.state = 0


.. _Peek: https://github.com/phw/peek
