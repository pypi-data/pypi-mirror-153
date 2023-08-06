-----------------------------------------------------------
  Interface-KB: A Pythonic API for the PACo Knowledge-Base
-----------------------------------------------------------

|pypi-version|

.. |pypi-version| image:: https://badge.fury.io/py/Interface-KB.svg
    :target: https://badge.fury.io/py/Interface-KB


Interface-KB is a python API to interface with Knowledge-Base instance models written for python 3.6.
The API is developed as part of the Product-Assembly Co-Design (PACo) SBO project.

Interface-KB allows you to handle Knowledge-Base instance models, and gives the key you need to integrate the Knowledge-Base  
structured data model within existing or new algorithms or applications. It supports out-of-the-box:

* Fetching structured data from existing Knowledge-Base instance models,
* Updating structured data from existing Knowledge-Base instance models,
* Adding structured data to a new or existing Knowledge-Base instance model,
* Knowledge-Base interface handling via standardized Interface Objects,
* JSON (de)serialization


Let see how to create an API instance to start using the API functions:

.. code-block:: python

    from Interface_KB import KB_Interface,InterfaceObjects
    API = KB_Interface.KB_Interface(True)
    
    
Installation
------------   

Interface-KB is available on ``pypi``, you can simply install it using ``pip``: 

.. code-block:: bash

    $ pip install Interface-KB
    
Installation using ``pip`` in virtual environment:

    $ py -m pip install --user Interface-KB


Examples and documentation
---------------------------

You can find all usage examples and detailed documentation of all API functions in this page:

https://interface-kb-public-documentation.readthedocs.io/en/main/

