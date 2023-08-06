fhs_enyaq_data
==============


enyaq car data to external services for now
abrp

Usage
-----
fhs-enyaq-data send-data-loop

Installation
------------
.. code-block:: bash

  git clone repo
  cd <to_repo>
  pipx install .


or

.. code-block:: bash

  pipx install fhs-enyaq-data


create a yaml config file:
location:  $HOME/.config/fhs_enyaq_data/config.yaml

.. code-block:: bash

  ---
  skoda:
    username: <skoda_username>
    password: <skoda_password>
    vehicle_vin: ""
  abrp:
    token: <abrp generic token>


Compatibility
-------------
python 3.x

Extra info
----------

- about abrp: https://documenter.getpostman.com/view/7396339/SWTK5a8w?version=latest

Licence
-------
MIT

Authors
-------

`fhs_enyaq_data` was written by `Richard de Vos <rdevos72@gmail.com>`_.
