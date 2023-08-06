=================
The OdooPBX Agent
=================
This repository contains the OdooPBX Agent middlware.

For more documentaion visit `OdooPBX Installation documentation <https://odoopbx.github.io/docs/index.html>`_.

Development installation
========================
Clone the repo and install from it:

.. code:: sh

  git clone  https://github.com/odoopbx/agent.git
  or 
  git clone git@github.com:odoopbx/agent.git
  cd agent
  pip3 install .
  mv salt /srv/
  mv pillar /srv
  salt-call --local state.apply agent
