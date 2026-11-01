Models and diagrams
=======================

Actual tooling structure
----------------------------

This component diagram describes the modules under
``skills/plaidshirt/scripts`` and their imports.
It is a tooling overview rather than an invented class model.

.. image:: ../build/diagrams/components.svg
   :alt: Components of the PlaidShirt tooling

Installation flow
---------------------

This UML activity diagram summarizes conflict checking and writing in
``install_project``. Conflicts are checked before the first mutation.
An operating-system failure while writing can still leave a partial
installation; the operation does not claim transactional guarantees.

.. image:: ../build/diagrams/install-activity.svg
   :alt: UML activity diagram for project installation

Algorithm flowchart
-----------------------

This flowchart summarizes the important decisions in ``run_tasks``.
It uses conventional flowchart symbols and does not claim formal standards
certification.

.. image:: ../build/diagrams/task-pap.svg
   :alt: Algorithm flowchart for configured build jobs

Clearly labeled illustrative models
---------------------------------------

The class diagram below describes the ``InventoryCounter`` Java example
in ``references/docs-java.md``. It is not a Python tooling class.

.. image:: ../build/diagrams/java-example-class.svg
   :alt: UML class diagram of the illustrative Java example

The ER diagram is an invented example of articles and inventory movements.
PlaidShirt itself has no database. Its cardinalities apply only to this example.

.. image:: ../build/diagrams/inventory-example-er.svg
   :alt: Illustrative ER diagram, not this project's database schema

Editable PlantUML and DOT sources live under ``docs/diagrams``.
PlantUML is an example tool for this repository rather than a skill-wide
requirement. The algorithm flowchart uses the JavaScript Graphviz library
Viz.js. Other renderers use the same configurable command interface.

Choose a target project's views from its actual architecture, storage,
and behavior.
