XML/TRXML Selector
==================

Description
-----------

This package provides two scripts: ``xml-python-select`` and
``trxml-python-select``.

``xml-python-select`` selects tags from xml/mxml files, and save the
selected values to file.

``trxml-python-select`` selects fields from trxml/mtrxml files, and save
the selected values to file.

Requirements
------------

Python 3.6+

Installation
------------

::

    pip install xml-selector

See `this
page <https://confluence.textkernel.nl/display/DU/Python+tk-pypi+Repo#Pythontk-pypiRepo-Connecttotk-pypi>`__
about how to install a package from the tk-pypi repo.

Usage
-----

Use xml selector script
~~~~~~~~~~~~~~~~~~~~~~~

The xml selector supports:
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  one or more tagnames:

-  selector could be one tagname ``name``

-  or comma separated tagnames ``langskill,compskill,softskills``

-  multiple sources:

-  e.g. select from xml dir, xml files, mxml file, or directly from
   annotation server

examples:
^^^^^^^^^

::

    #select from xml directory
    xml-python-select --source tests/xmls/ --selector name --output_file name.tsv
    xml-python-select --source tests/xmls/ --selector langskill,compskill,softskill --output_file skill.tsv --with_field_name

    #select from xml file or mxml file
    xml-python-select --source tests/sample.mxml --selector experience --output_file experience.tsv

    #select directly from annotation server
    xml-python-select --source localhost:50249 --selector name --output_file name.tsv --query "set Data2018"

Use trxml selector script
~~~~~~~~~~~~~~~~~~~~~~~~~

The trxml selector supports:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  one or more selectors:

-  selector can be one field: ``name.0.name``

-  or comma separated fields: ``name.0.name,address.0.address``

-  single or multi item:

-  can select field from one item, e.g. ``experienceitem.3.experience``

-  or select field value of all item, e.g. ``experienceitem.experience``
   (or ``experienceitem.*.experience``)

-  multiple sources:

-  e.g. select from trxml dir, trxml files, or mtrxml file

examples:
^^^^^^^^^

::

    # one selector, single item
    trxml-python-select --source tests/trxmls/ --selector name.0.name --output_file name.tsv

    # one selector, multiple item
    trxml-python-select --source tests/sample.mxml --selector experienceitem.experience --output_file experience.tsv

    # more selectors, single item
    trxml-python-select --source tests/trxmls/ --selector name.0.name,address.0.address,phone.0.phone --output_file personal.tsv

    # more selectors, multiple item
    trxml-python-select --source tests/sample.mxml  --itemgroup experienceitem --fields experience,experiencedate --output_file experience.tsv
    trxml-python-select --source tests/sample.mxml  --selector experienceitem.*.experience,experienceitem.*.experiencedate --output_file experience.tsv
    trxml-python-select --source tests/sample.mxml  --selector experienceitem.experience,experienceitem.experiencedate --output_file experience.tsv

Development
-----------

To install package and its dependencies, run the following from project
root directory:

::

    python setup.py install

To work the code and develop the package, run the following from project
root directory:

::

    python setup.py develop

To run unit tests, execute the following from the project root
directory:

::

    python setup.py test

selector and output details:
----------------------------

-  xml-python-select:

   input: documents, selector(s), output

   output:

   -  default (parameter ``with_field_name`` not set):
      ``filename, field_value``

   e.g. select all names with selector ``name``

   +------------+-----------+
   | filename   | value     |
   +============+===========+
   | xxxx       | Chao Li   |
   +------------+-----------+

   -  parameter ``with_field_name`` set:
      ``filename, field_value, field_name``

   e.g. select skills with selector ``compskill,langskill,otherskill``

   +------------+---------+-------------+
   | filename   | value   | field       |
   +============+=========+=============+
   | xxxx       | java    | compskill   |
   +------------+---------+-------------+
   | xxxx       | dutch   | langskill   |
   +------------+---------+-------------+

-  trxml-python-select

   -  input:
   -  documents, selector(s), output,
   -  documents, itemgroup, fields, output

   -  single selector:
   -  single item (``name.0.name``): filename field

   +------------+---------------+
   | filename   | name.0.name   |
   +============+===============+
   | xxxx       | Chao Li       |
   +------------+---------------+

   -  multi items (``skill.*.skill``): filename item\_index field

   +------------+---------------+---------+
   | filename   | item\_index   | field   |
   +============+===============+=========+
   | xxxx       | 0             | java    |
   +------------+---------------+---------+
   | xxxx       | 1             | dutch   |
   +------------+---------------+---------+

   -  multiple selectors
   -  single item: filename, field1, field2 ...

   each selector points to a field of a specific item with a digital
   index, e.g. ``name.0.lastname,name.0.firstname,address.0.country``

   +------------+-------------------+--------------------+---------------------+
   | filename   | name.0.lastname   | name.0.firstname   | address.0.country   |
   +============+===================+====================+=====================+
   | xxxx       | Li                | Chao               | China               |
   +------------+-------------------+--------------------+---------------------+
   | xxxx       | Lee               | Richard            | USA                 |
   +------------+-------------------+--------------------+---------------------+

   -  multi items: filename, item\_index, field1, field2 ...

   each selector points to a field from all items in an itemgroup, e.g.
   ``skill.skill,skill.type,skill.date``

   +------------+---------+---------+-------------+-------------+
   | filename   | skill   | skill   | type        | date        |
   +============+=========+=========+=============+=============+
   | xxxx       | 0       | java    | compskill   | 2001-2005   |
   +------------+---------+---------+-------------+-------------+
   | xxxx       | 1       | dutch   | langskill   | 2002-       |
   +------------+---------+---------+-------------+-------------+