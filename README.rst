PyScorecard
===========

PyScorecard is an unofficial Python library for interacting with the US
Department of Education’s College Scorecard API.

Installation
------------

Use the package manager `pip`_ to install PyScorecard.

.. code:: bash

   pip install PyScorecard

Usage
-----

.. code:: python

   from PyScorecard import PyScorecard

   scorecard = PyScorecard()
   scorecard.set_api_key("YOUR_API_KEY_HERE")
   scorecard.set_year("2015")

   scorecard.add_filter("school.degrees_awarded.predominant","=",["2","3"])

   scorecard.add_field("school.name")
   scorecard.add_field("ope6_id")
   scorecard.add_fields(["cost.tuition.in_state","cost.tuition.out_of_state"])

   data = scorecard.fetch_all()

License
-------

`GNU GPL-V2`_

.. _pip: https://pip.pypa.io/en/stable/
.. _GNU GPL-V2: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt