..  Titling
    ##++::==~~--''``

.. _cli:

CLI Reference
:::::::::::::

turberfield-dialogue
====================

.. automodule:: turberfield.dialogue.main

.. argparse::
   :ref: turberfield.dialogue.main.parser
   :prog: turberfield-dialogue
   :nodefault:

turberfield-rehearse
====================

.. automodule:: turberfield.dialogue.viewer

.. argparse::
   :ref: turberfield.dialogue.viewer.parser
   :prog: turberfield-rehearse
   :nodefault:

.. caution::

   This tool has a `web mode` which is experimental. It may
   not work perfectly in your web browser.

   It also presents a potential security risk while it is
   running, since its CGI interface facilitates code execution
   on your computer.

   Always check that your PC firewall does not permit outside
   access to the port configured by the program options. If in
   doubt, disconnect your PC from all networks while web mode
   is in operation.
