XML/TRXML Selector
==================

Description
-----------

This package provides two scripts: ``mine-xml`` and
``mine-trxml``.

``mine-xml`` selects tags from xml/mxml files, and save the
selected values to file.

``mine-trxml`` selects fields from trxml/mtrxml files, and save
the selected values to file.

Status
------------

.. image:: https://travis-ci.org/tilaboy/xml-miner.svg?branch=master
    :target: https://travis-ci.org/tilaboy/xml-miner

.. image:: https://readthedocs.org/projects/xml-miner/badge/?version=latest
    :target: https://xml-miner.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/tilaboy/xml-miner/shield.svg
    :target: https://pyup.io/repos/github/tilaboy/xml-miner/
    :alt: Updates

Requirements
------------

Python 3.6+

Installation
------------

::

    pip install xml-selector


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
    mine-xml --source tests/xmls/ --selector name --output_file name.tsv
    mine-xml --source tests/xmls/ --selector langskill,compskill,softskill --output_file skill.tsv --with_field_name

    #select from xml file or mxml file
    mine-xml --source tests/sample.mxml --selector experience --output_file experience.tsv

    #select directly from annotation server
    mine-xml --source localhost:50249 --selector name --output_file name.tsv --query "set Data2018"

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
    mine-trxml --source tests/trxmls/ --selector name.0.name --output_file name.tsv

    # one selector, multiple item
    mine-trxml --source tests/sample.mxml --selector experienceitem.experience --output_file experience.tsv

    # more selectors, single item
    mine-trxml --source tests/trxmls/ --selector name.0.name,address.0.address,phone.0.phone --output_file personal.tsv

    # more selectors, multiple item
    mine-trxml --source tests/sample.mxml  --itemgroup experienceitem --fields experience,experiencedate --output_file experience.tsv
    mine-trxml --source tests/sample.mxml  --selector experienceitem.*.experience,experienceitem.*.experiencedate --output_file experience.tsv
    mine-trxml --source tests/sample.mxml  --selector experienceitem.experience,experienceitem.experiencedate --output_file experience.tsv

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

-  mine-xml:

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

-  mine-trxml

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
