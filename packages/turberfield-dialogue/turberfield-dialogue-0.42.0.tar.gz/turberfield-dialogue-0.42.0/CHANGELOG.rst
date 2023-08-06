..  Titling
    ##++::==~~--''``

.. This is a reStructuredText file.

Change Log
::::::::::

0.42.0
======

* Better handling of duplicate scene names.

0.41.1
======

These changes are intended to allow dialogue file processing to continue despite missing object references.
This is to accomodate a writing workflow which begins with regular `.rst` files, and progressively develops
them to `.dlg.rst` scene scripts.

* Switch from standard library logging to using the LogManager and LogAdapter classes from `turberfield-utils`_.
* Add a custom LogAdapter for colourized output.
* Add path and line data to model objects.
* Improve tolerance of references lacking persona.
* Improve tolerance of missing citations.
* Improve reporting of line numbers where there is an error in property substitution.
* Minimise package dependencies (blessings and simpleaudio are optional now).

0.40.0
======

* Fix a bug preventing duplicate shot names.

0.39.0
======

* `Model.Still` gets width and height.
* Implement `Model.Video`.

0.38.0
======

* Fix implementation of previous feature.

0.37.0
======

* Allow object assignment via property setter.

0.36.0
======

* Fix a bug with regex matching of integer state.

0.35.0
======

* Better collaborative multiple inheritance.

0.34.0
======

* Model implements format string style substitution of references.

0.33.0
======

* Use internal docutils type for SceneScript settings.

0.32.0
======

* Fix an issue on updating to docutils 0.17.

0.31.0
======

* Fix unit tests for Condition when not skipped.
* Permit regular expressions in Condition values.
* `Performer.allows` implements regular expression match where necessary.

0.30.0
======

* Dialogue model permits multiple dots in a condition specifier.
* Performer implements format string style evaluation of conditions.

0.29.0
======

* Improved handling of AttributeError when substituting a persona reference.

0.28.0
======

* Fixed a bug where the current speaker would carry over from a previous
  block quote.

0.27.0
======

This release comprises a refactoring of the parser model. You now get more flexibility,
but you should check your existing projects to see if they are any changes in rendering.

* The `raw:: html` directive is now supported.
* Bullet lists are now recognised and rendered as HTML unordered lists.
* The requirement for two sections has been relaxed, allowing you to render document fragments.

0.26.0
======

* When building the HTML for a dialogue Line, characters are now correctly
  escaped as HTML5 entities.

0.25.0
======

* Hyperlinks are now properly rendered as Line HTML.
* The following rST/HTML5 equivalences are implemented:

    * Emphasis directives (``*`` markup) rendered as HTML with `<em>` tags.
    * Strong directives (``**`` markup) rendered as HTML with `<strong>` tags.
    * Literal directives (`````` markup) rendered as HTML with `<pre>` tags.

0.24.0
======

* `Performer.react` now sets state on the subject of a memory when there's no defined object.
* Fix the interlude in `Cloak` so it works properly in rehearsal.

0.23.0
======

* `Stateful.set_state` now takes multiple positional arguments.

0.22.0
======

* Fix a bug in creating a Persona from an Assembly

0.21.0
======

* The `fx` declaration now has a `label` option. A label may may contain
  substitution references.
* `Still` cues now have a label attribute which takes its value from the `fx`
  declaration. The main use case for this is to provide content for the `alt`
  attribute of an HTML `img` tag.

0.20.0
======

* `SceneScript.Folder` interludes may be `None`.

0.19.0
======

* The `fx` declaration now generates Audio and Stills
* Added documentation for the `Matcher` class.
* Added guidance on alternative for file suffix.

0.18.0
======

* Added a Matcher class which can select folders by their metadata.
* `rehearse` function uses the matcher to branch to different folders.
* `turberfield-dialogue` utility uses the matcher likewise.
* **Interludes from now on must return a metadata dictionary**. Fixed the
  documentation and demo scenarios accordingly.
* Fixed a bug affecting the TerminalHandler when *simpleaudio* is not available.
* Simplified the documentation relating to VSCode.

0.17.0
======

* Fixed a bug in `Performer` which affected `condition` directives.

0.16.0
======

* `Performer` allows `condition` directives to access object `state`.

0.15.0
======

* Added the `condition` directive.

0.14.0
======

* `turberfield-dialogue` tool calls an interlude function after every scene file.

0.13.0
======

* DataObject `id` attribute is now a `uuid.UUID` object.
* The second argument to a property directive may be a substitution reference
* Added a code example for narrative resource discovery.

0.12.0
======

* Refactored the `rehearse` function so it uses `Performer`. Its first argument is now
  documented as a sequence. Legacy behaviour is preserved.

0.11.0
======

* Field lists at the document level are available via the  `metadata` attribute of the model.
* Substitution references to Python values are properly resolved in the bodies of field lists.
* There is a new utility, `turberfield-dialogue` for producing a printable screenplay.
* The viewer module now registers all references with `turberfield.utils.assembly.Assembly`.
* The `Performer` class is now part of the public API.

0.10.1
======

* Changelog fixes.

0.10.0
======

* Substitution references are now permitted in the `resource` argument to
  an FX directive.

0.9.0
=====

* `Turberfield.dialogue.performer` and matching tests implement the new Performer
  class. This was first prototyped in the `bluemonday78` episode of Addison Arches.

0.8.0
=====

* `turberfield-rehearse` **--web** option works tolerably in Firefox.
* Added **strict** mode for casting a rehearsal.
* Interludes now see a sequence of folders they may **branch** to.
* State matching is hierarchical; '31' matches a criterion of '3'.

.. _turberfield-utils: https://github.com/tundish/turberfield-utils
