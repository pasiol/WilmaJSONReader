WilmaJSONReader
======================

.. image:: https://img.shields.io/pypi/v/WilmaJSONReader.svg
    :target: https://pypi.python.org/pypi/WilmaJSONReader
    :alt: Latest PyPI version

The Wilma rest client.

Usage
-----

From git repo:

 python3 WilmaJSONReader/reader.py rooms 01.01.2020 10.01.2020 some.domain.name user password apikey data/

 .. image:: https://github.com/pasiol/WilmaJSONReader/raw/main/images/rooms.png

As library

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

pip install WilmaJSONReader

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