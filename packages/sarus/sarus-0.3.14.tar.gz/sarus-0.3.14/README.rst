
Sarus

===

Python client for the Sarus Gateway. It provides simple connectors to leverage confidential data while ensuring data privacy. Users can explore & train AI models on sensitive data, via synthetic data browsing, remote training and differential privacy.

Installation
------------

PIP
^^^

To install locally the latest available version :

``pip install sarus``

Usage
-----

Client
^^^^^^

Use this class to connect to **Sarus Gateway**.

.. code-block:: python

   from sarus import Client

   client = Client(url="http://admin.sarus.tech:5000")
   available = client.available_datasets()
   print(f'Datasets available on the server: {available}')
