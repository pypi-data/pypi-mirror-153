.. image:: https://github.com/matthiaskoenig/pkdb_data/workflows/CI-CD/badge.svg
   :target: https://github.com/matthiaskoenig/pkdb_data/workflows/CI-CD
   :alt: GitHub Actions CI/CD Status

.. image:: https://img.shields.io/pypi/v/pkdb_data.svg
   :target: https://pypi.org/project/pkdb_data/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pkdb_data.svg
   :target: https://pypi.org/project/pkdb_data/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/pkdb_data.svg
   :target: http://opensource.org/licenses/LGPL-3.0
   :alt: GNU Lesser General Public License 3

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

pkdb_data: python utilities for PK-DB data
==========================================
This repository stores the curated study data for `https://pk-db.com <https://pk-db.com>`__ and provides helpers for uploading studies to
the database. The available choices are defined as part of this repository.

* `./studies/ <./studies/>`__: curated study data with subfolders based on substances
* `./pkdb_data/info_nodes/ <./pkdb_data/info_nodes/>`__: definition of data base choices
* `./CURATION.md <./CURATION.md>`__: curation guidelines and choices

See the `./CURATION.md <./CURATION.md>`__ for detailed instructions on how to curate studies.

Installation
============
Installation instructions are available `here <https://github.com/matthiaskoenig/pkdb_data/blob/develop/CURATION.md#setup>`__.

Functionality in a nutshell
===========================
The following provides a short overview over the main functionality.
Detailed information is provided in the `./CURATION.md <./CURATION.md>`__.

Upload study
------------
To upload a study use

.. code-block:: console

    (pkdb_data) upload_study -s <study_dir>

Upload studies
--------------
A set of studies can be uploaded via

.. code-block:: console

    (pkdb_data) upload_studies

Use the `-s` flag to only upload subsets, e.g., to upload all `caffeine` and `acetaminophen` studies use

.. code-block:: console

    (pkdb_data) upload_studies -s caffeine acetaminophen


Delete study
------------
.. code-block:: console

    (pkdb_data) delete_study -s <study_sid>


Update InfoNodes
----------------
Modifying and uploading InfoNodes which can be used as choices in the curation is restricted to the admins.
To update the notes modify the information in `./pkdb_data/info_nodes/ <./pkdb_data/info_nodes/>`__ and create the `json` information via

.. code-block:: console

    (pkdb_data) create_nodes

In a second step the nodes are uploaded via

.. code-block:: console

    (pkdb_data) upload_nodes


License
=======

* Source Code: `LGPLv3 <http://opensource.org/licenses/LGPL-3.0>`__
* Documentation: `CC BY-SA 4.0 <http://creativecommons.org/licenses/by-sa/4.0/>`__

The pkdb_data source is released under both the GPL and LGPL licenses version 2 or
later. You may choose which license you choose to use the software under.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License or the GNU Lesser General Public
License as published by the Free Software Foundation, either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

Funding
=======
Matthias König is supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054)
and by the German Research Foundation (DFG) within the Research Unit Programme FOR 5151
"`QuaLiPerF <https://qualiperf.de>`__ (Quantifying Liver Perfusion-Function Relationship in Complex Resection -
A Systems Medicine Approach)" by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA).

© 2017-2022 Jan Grzegorzewski & Matthias König
