VirtualEnv Installation
=======================

#. **Requirements**

   You will need python, python-virtualenvwrapper, pip and git

#. **Get the source code**

   Clone source code from the `repository <https://gitlab.com/librespacefoundation/satnogs/satnogs-db>`_::

     $ git clone https://gitlab.com/librespacefoundation/satnogs/satnogs-db.git
     $ cd satnogs-db

#. **Build the environment**

   Set up the virtual environment. On first run you should create it and link it to your project path.::

     $ mkvirtualenv satnogs-db -a .

#. **Configure settings**

   Set your environmental variables::

     $ cp env-dist .env

#. **Install frontend dependencies**

   Install dependencies with ``npm``::

     $ npm install

   Test and copy the newly downlodaded static assets::

     $ ./node_modules/.bin/gulp

#. **Run it!**

   Activate your python virtual environment::

     $ workon satnogs-db

   Just run it::

    (satnogs-db)$ ./bin/djangoctl.sh develop .

#. **Populate database**

   Create, setup and populate the database with demo data::

     (satnogs-db)$ ./bin/djangoctl.sh initialize

   Your satnogs-db development instance is available in localhost:8000. Go hack!
