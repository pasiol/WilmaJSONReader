WilmaJSONReader
======================

.. image:: https://img.shields.io/pypi/v/WilmaJSONReader.svg
    :target: https://pypi.python.org/pypi/WilmaJSONReader
    :alt: Latest PyPI version

The Wilma rest client.

Supports getting daily data or date range of the resource. Valid resource type are rooms, teachers and students.

Usage
-----

The Wilma JSON schema is quite complex to parse. Easiest way utilize it is use some framework, for example the MongoDB Aggregation Framework.

From git repo::

 python3 WilmaJSONReader/reader.py rooms 01.01.2020 10.01.2020 some.domain.name user password apikey data/

.. image:: https://github.com/pasiol/WilmaJSONReader/raw/main/images/rooms.png

As library::

    from WilmaJSONReader import reader

    ...

    wilma_reader = reader.WilmaJSONReader(
        url,
        user,
        password,
        apikey,
    )
    wilma_reader.login()
    dates = wilma_reader.get_dates("01.01.2020", "10.01.2020", logger)
    
    for day in dates:
        r = wilma_reader.get_schedule(day, "rooms")
        schedules = r.json()
        pprint(schedules)

Installation
------------

Easiest way is install WilmaJSONReader from PyPi. Before installation create Python virtual environment or install it to container image.

Linux && Mac::

    python3 -m venv venv
    source venv/bin/activate

    pip install WilmaJSONReader

    ..

    deactivate

Windows

   `<https://docs.python.org/3.8/library/venv.html>`_

Upgrade::

    pip install WilmaJSONReader -U

Requirements
^^^^^^^^^^^^

Python 3.8 ->

Compatibility
-------------

Licence
-------

GNU GENERAL PUBLIC LICENSE Version 3

Authors
-------

`WilmaJSONReader` was written by `Pasi Ollikainen <pasi.ollikainen@outlook.com>`_.