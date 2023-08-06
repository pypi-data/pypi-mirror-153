..  Titling
    ##++::==~~--''``

Workflow
::::::::

* Act structure
* Plot points
* Objects and memory


Model
:::::

* An persona is a major, named character
* An persona may play other minor characters, eg: as a bystander
* `Hint` is a character
* A role is the association between character and persona
* A shot contains a single action from each participating character
* A scene consists of a sequence of shots (ShotSequence).
  * A scene may only take place in certain locations.
  * A scene specifies required characters
* A SceneSequence is a series of scenes.
* A scene script is a single .rst file
* A frame is a visible container for shots, ie: recent history
* Phases exist between Plot points. They replay Shots until a branch is made. They vary by location
  and actors present.

Interaction
:::::::::::

* Player Character has a phrase book (numbered slots) with user-defined responses to RTE dialogue.

Script Syntax
:::::::::::::

* Persona states are active, passive, mist
* Persona methods are locate? Maybe not.
* Explore corner case Battle Royal:

    - Itchy and Scratchy are active personae. Types are both animal
    - Victim character is type animal
    - Axe object. Passive persona
    - "I hate the way you use me!"
    - Itchy kills/killed by Scratchy; becomes passive
    - Axe becomes active. Matched to character for second loop.
    - Victim to mist
    - Personae can have memory.
    - Compound objects can't be Personae? Pickled not inserted into DB.
    - Add memory to object; 'This is the axe that killed Scratchy'.
