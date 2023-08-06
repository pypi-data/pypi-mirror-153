#!/usr/bin/env python3
# encoding: UTF-8

# This file is part of turberfield.
#
# Turberfield is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Turberfield is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with turberfield.  If not, see <http://www.gnu.org/licenses/>.


import copy
import enum
import operator
import sys
import textwrap
import unittest
import uuid

from turberfield.dialogue.directives import Entity
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.performer import Performer
from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Stateful
from turberfield.dialogue.types import Player


class FootnoteTests(unittest.TestCase):

    def test_unspoken_footnote_html_to_weasyprint(self):
        content = textwrap.dedent("""
            Don't worry, I'm a doctor. [*]_

            .. [*] Not a medical doctor.

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        self.assertEqual(1, len(model.shots))
        self.assertEqual(1, len(model.shots[0].items))
        line = model.shots[0].items[0]
        self.assertIn('class="call"', line.html)
        self.assertIn('class="footnote"', line.html)
        self.assertIn('role="note"', line.html)
        self.assertTrue(line.html.startswith("<p>"))
        self.assertTrue(line.html.endswith("</p>\n"))
        self.assertNotIn("<p>", line.html[1:])
        self.assertNotIn("</p>", line.html[:-2])

    def test_multispan_unspoken_footnote_html_to_weasyprint(self):
        content = textwrap.dedent("""
            Don't worry, I'm a doctor. [*]_

            .. [*] Not a *medical* doctor.

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        self.assertEqual(1, len(model.shots))
        self.assertEqual(1, len(model.shots[0].items))
        line = model.shots[0].items[0]
        self.assertNotIn('<span class="text"', line.html)
        self.assertIn('class="call"', line.html)
        self.assertIn('class="footnote"', line.html)
        self.assertIn('role="note"', line.html)
        self.assertTrue(line.html.startswith("<p>"))
        self.assertTrue(line.html.endswith("</p>\n"))
        self.assertNotIn("<p>", line.html[1:])
        self.assertNotIn("</p>", line.html[:-2])

    def test_spoken_footnote_reference_html_to_weasyprint(self):
        content = textwrap.dedent("""
            [P]_

                Don't worry, I'm a doctor. [*]_

            .. [*] Not a medical doctor.

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        self.assertEqual(1, len(model.shots))
        self.assertEqual(1, len(model.shots[0].items))
        line = model.shots[0].items[0]
        self.assertIn('class="call"', line.html)
        self.assertIn('class="footnote"', line.html)
        self.assertIn('role="note"', line.html)
        self.assertTrue(line.html.startswith("<p>"))
        self.assertTrue(line.html.endswith("</p>\n"))
        self.assertNotIn("<p>", line.html[1:])
        self.assertNotIn("</p>", line.html[:-2])

    def test_spoken_footnote_html_to_weasyprint(self):
        content = textwrap.dedent("""
            [P]_

                Don't worry, I'm a doctor. [*]_

                .. [*] Not a medical doctor.

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        self.assertEqual(1, len(model.shots))
        self.assertEqual(1, len(model.shots[0].items))
        line = model.shots[0].items[0]
        self.assertIn('class="call"', line.html)
        self.assertIn('class="footnote"', line.html)
        self.assertIn('role="note"', line.html)
        self.assertTrue(line.html.startswith("<p>"))
        self.assertTrue(line.html.endswith("</p>\n"))
        self.assertNotIn("<p>", line.html[1:])
        self.assertNotIn("</p>", line.html[:-2])


class SceneTests(unittest.TestCase):

    def test_one_scene(self):
        content = textwrap.dedent(
            """
            Scene
            =====

            Shot
            ----

            Text
        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select([]))
        model = list(script.run())
        shot, line = next(iter(model))
        self.assertEqual("scene", shot.scene)
        self.assertEqual("shot", shot.name)

    def test_multi_scene(self):
        content = textwrap.dedent(
            """
            Scene 1
            =======

            Shot 1
            ------

            Text

            Scene 2
            =======

            Shot 2
            ------

            Text
        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select([]))
        model = list(script.run())
        shot, line = next(iter(model))
        self.assertEqual("scene 1", shot.scene)
        self.assertEqual("shot 1", shot.name)

    def test_duplicate_shot(self):
        content = textwrap.dedent(
            """
            Scene 1
            =======

            Shot
            ----

            Text

            Scene 2
            =======

            Shot
            ----

            Text
        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select([]))
        model = list(script.run())
        shot, line = next(iter(model))
        self.assertEqual("scene 1", shot.scene)
        self.assertEqual("shot", shot.name)

    def test_duplicate_scene(self):
        content = textwrap.dedent(
            """
            Scene
            =====

            Shot 1
            ------

            Text

            Scene
            =====

            Shot 1
            ------

            Text
        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select([]))
        model = list(script.run())
        shot, line = next(iter(model))
        self.assertEqual("scene", shot.scene)
        self.assertEqual("shot 1", shot.name)

    def test_shot_duplicates_scene(self):
        content = textwrap.dedent(
            """
            Scene 1
            =======

            Shot 1
            ------

            Text

            Scene 2
            =======

            Scene 1
            -------

            Text
        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select([]))
        model = list(script.run())
        shot, line = next(iter(model))
        self.assertEqual("scene 1", shot.scene)
        self.assertEqual("shot 1", shot.name)


class HTMLEscapingTests(unittest.TestCase):

    def test_escape_ampersand(self):
        content = textwrap.dedent("""
            Characters
            ==========

            Ampersand
            ---------

            Three pints of M&B please.

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        line = model.shots[0].items[0]
        self.assertIn("M&amp;B", line.html)

    def test_escape_brackets(self):
        content = textwrap.dedent("""
            Characters
            ==========

            Greater
            -------

            3 > 1

            Less
            ----

            1 < 3

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        for n, shot in enumerate(model.shots):
            with self.subTest(n=n):
                if n:
                    self.assertIn("1 &lt; 3", shot.items[0].html)
                else:
                    self.assertIn("3 &gt; 1", shot.items[0].html)

    def test_noescape_common_characters(self):
        content = textwrap.dedent("""
            Characters
            ==========

            Unchanged
            ---------

            !"*()+-:;'.,@#{}=~

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        line = model.shots[0].items[0]
        self.assertNotIn("&", line.html)

    def test_escape_common_characters(self):
        content = textwrap.dedent("""
            Characters
            ==========

            Changed
            -------

            $%^©£

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        line = model.shots[0].items[0]
        self.assertEqual(5, line.html.count("&"), line.html)


class RstFeatureTests(unittest.TestCase):

    def test_bullet_lists(self):
        content = textwrap.dedent("""
            Scene
            =====

            Shot
            ----

            ABC.

            * Always
            * Be
            * Closing

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        self.assertEqual(["Always", "Be", "Closing"], model.shots[-1].items[-1].text.splitlines())
        self.assertEqual(2, model.shots[-1].items[-1].html.count("ul>"))
        self.assertEqual(6, model.shots[-1].items[-1].html.count("li>"))

    def test_markup_body_text(self):
        content = textwrap.dedent("""
            Markup
            ======

            Emphasis
            --------

            I *keep* telling you.

            I :emphasis:`keep` telling you.

            Strong
            ------

            I **keep** telling you.

            I :strong:`keep` telling you.

            Preformat
            ---------

            I ``keep`` telling you.

            I :literal:`keep` telling you.
        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        for shot in model.shots:
            with self.subTest(shot_name=shot.name):
                self.assertTrue(all("keep" in line.text for line in shot.items))
                self.assertFalse(any("  " in line.text for line in shot.items), shot)
                if shot.name.startswith("em"):
                    self.assertTrue(all('<em class="text">' in line.html for line in shot.items)) 
                    self.assertTrue(all("</em>" in line.html for line in shot.items)) 
                elif shot.name.startswith("strong"):
                    self.assertTrue(all('<strong class="text">' in line.html for line in shot.items)) 
                    self.assertTrue(all("</strong>" in line.html for line in shot.items)) 
                elif shot.name.startswith("pre"):
                    self.assertTrue(all('<pre class="text">' in line.html for line in shot.items)) 
                    self.assertTrue(all("</pre>" in line.html for line in shot.items))

    def test_hyperlink_body_text(self):
        content = textwrap.dedent("""
            Hyperlinks
            ==========

            Standalone
            ----------

            See http://www.python.org for info.

            Embedded
            --------

            See the `Python site <http://www.python.org>`_ for info.

            Named
            -----

            See the `Python home page`_ for info.

            .. _Python home page: http://www.python.org

        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        for shot in model.shots:
            with self.subTest(shot_name=shot.name):
                self.assertFalse(any("  " in line.text for line in shot.items))
                self.assertTrue(all('<a href="http://www.python.org">' in i.html for i in shot.items), shot)

    def test_raw_html(self):
        content = textwrap.dedent("""
            Scene
            =====

            Shot
            ----

            I know what it needs...

            .. raw:: html

                <marquee>Puppies die when you do bad design</marquee>
        """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        self.assertEqual(2, model.shots[-1].items[-1].html.count("marquee"))
        self.assertEqual(0, model.shots[-1].items[-1].text.count("marquee"))
