palaestrAI: A Training Ground for Autonomous Agents
===================================================

About
-----

palaestrAI is a distributed framework to train and test all kinds of
autonomous agents. It provides interfaces to any environment, be it
OpenAI Gym or co-simulation environments via mosaik. palaestrAI can
train and test any kind of autonomous agent in these environments:
From Deep Reinforcement Learning (DRL) algorithms over model-based to
simple rule-based agents, all can train and test with or against
each other in a shared environment.

In short, palaestrAI can...

* ...train and test one or more agent of any algorithm
* ...place the agents on one or several environments at once,
  depending on the agents' algorithm
* ...provides facilities to define and reproducibly run experiments

palaestrAI is the core framework of a whole ecosystem:

* hARL provides implementations of several DRL algorithms and
  interfaces to existing DRL libraries.
* arsenAI provides all facilities needed for proper design
  of experiments.
* palaestrai-mosaik is a interface to the mosaik co-simulation
  software
* palaestrai-environments provides a number of simple,
  easy to use environments for playing with palaestrAI

Documentation can be found at http://docs.palaestr.ai/

Use Cases
---------

palaestrAI is the framework for the Adversarial Resilience Learning
(ARL) reference implementation. The ARL core concept consists of two
agents, attacker and defender agents, working an a common model of a
cyber-phyiscal system (CPS). The attacker's goal is to de-stabilize the CPS,
whereas the defender works to keep the system in a stable and operational
state. Both agents do not perceive their opponent's actions directly, but only
the state of the CPS itself. This imples that none of the agents knows whether
anything they perceive through their sensors is the result of the dynamics of
the CPS itself or of another agent's action.  Also, none of the agents has an
internal model of the CPS. Attacker and defender alike have to explore the CPS
given their sensors and actuators independently and adapt to it. ARL is, in
that sense, suitable to a reinforcement learning approach.  Combined with the
fact the both agents do not simply learn the CPS, but also its respective
opponent, ARL implements system-of-systems deep reinforcement learning.

Installation
------------

palaestrAI is mainly written in Python, with the usual third-party library
here and there. It provides a ``setup.py`` file just as any well-behaved Python
program. Use::

   pip install palaestrai

or for development, clone the palaestrAI repository from
https://gitlab.com/arl2/palaestrai/-/tree/development and run::

   pip install -e .[dev]

(With zsh, you need to escape the parenthesis like this::

   pip install -e .\[dev\]

)

``palaestrai`` comes with shell completion definitions for bash, zsh, and
fish, courtesy of click. They are installed in ``/etc/bash_completion.d``,
``/etc/zsh_completion.d``, and ``/etc/fish_completion.d``, respectively. The
``/etc`` directory is relative to your installation root. I.e., if you
install palaestrai in your virtualenv directory ``~/palaestrai/venv``, then
the completion files will be installed in
``~/palaestrai/venv/etc/{bash,zsh,fish}_completion.d``. (Note that ``pip
install -e`` does not install data files, but in that case you have the files
in the main directory of your git repo clone.) You will have to source the
appropriate file to enable shell completion. To do so automatically, add the
approporiate stanza to your ``~/.bashrc``, ``~/.zshrc``, or ``~/.fishrc``,
respectively. E.g.,

    echo '. /etc/zsh_completion.d/palaestrai_completion.zsh' >> ~/.zshrc

After installation, you can start the dummy experiment run with::

   palaestrai experiment-start tests/fixtures/dummy_run.yml

However, to use all palaestrAI functionalities, some additional setup is
currently required. First, you need to install Docker. You find docker in
your preferred distributions
package manager or you can use the following commands to start a convience
script::

   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

Afterwards, you should add yourself to the Docker group::

   sudo usermod -aG docker $USER

Try if your Docker installation works by typing::

   docker images

(or any other valid docker command). If that's not the case, the easiest way
is to restart your system (or use some magic commands to start the docker
daemon). The next step is to start a Docker container for the store::

   docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:1.7.4-pg12

You only need to run this command once. If you want to start the container
after a system reboot, the following command is sufficient::

   docker start timescaledb

Next, you need to setup the database. Type the following three commands::

   docker exec -it timescaledb psql -U postgres
   CREATE DATABASE Palaestrai;
   exit

Now, you need to add a *store_uri* in your *Palaestrai-runtime.conf.yaml*.
If you followed this guide step-by-step, the following store_uri should do::

   store_uri: postgresql://postgres:password@172.17.0.1:5432/Palaestrai

Finally, you can enable some loggers by changing their value from ERROR to
DEBUG or keep palaestrAI silent.


Usage
-----

After installing (and, probably, setting log levels in the palaestrai-runtime.conf.yaml),
type::

   palaestrai database-create

to create the data store.

Everything that steers palaestrAI is defined through *experiment run* files.
They define which agents, which algorithms, and which environments to use.
You can then either start palaestrAI standalone from the command line as::

    palaestrai experiment-start RUNFILE

E.g.,::

    palaestrai experiment-start my_run.yml

Or you use palaestrAI from your Jupyter notebook::

    import palaestrai
    palaestrai.execute('my_run.yml')

Development
-----------

Handling a Bug
``````````````

If you find any kind of bug, please create an issue in GitLab:

- A prose description of the bug: what did you intend to do, what happened
  instead?
- The error message, if there is any.
- The command line parameters and configuration
- Your version of Python you are using, and the version of all modules
  (``pip freeze`` gives you that).

Contributing
````````````

The typical work flow is as such:

1. File a bug/feature/support request in the issue tracker
2. Create a feature branch to work on your issue. Name it
   ``bug-<num>-<shortname>`` for bugs, ``feature-<num>-<shortname>`` for new
   features, etc.
3. Provide a unit test for the bug/feature you have been working on.
4. Fix the bug/work on the feature.
5. Run ``black -l 79 ./src/palaestrai ./tests`` to auto-format the code
6. Run ``tox`` and clean up all errors. (Run ``tox -e full-docker`` to also run system tests using docker and docker-compose)
7. Request a merge. The merge will happen after a code review;
   work-in-progress code gets first merged into ``development``
8. Once the current development branch has ripened enough, it is merged to
   ``master``. The master branch must contain code that is stable. New
   releases are only tagged on master branch commits.

Coding Style
````````````

Have a look at our architecture document and diagrams in
``doc/architecture.rst``.

We adhere to PEP8_ or black with line length of 79.

Try hard to find fitting names for new modules and subdirectories. If you are
importing your own module as ``import X as Y`` and ``Y`` is
differing semantically from ``X``, it might be the right time to change
the name of ``X``. Please refrain from abbreviated names if it is not
absolutely clear (in two years from now) what the abbreviation signifies.
Specifically, use short variable names in functions, if you like to, but stick
to commonly known and accepted abbreviations, such as ``for i in list`` or
similar things. Avoid confusion with function names from the Python base
library, e.g., do not use ``exp`` as a shorthand for "experiment" (cf.
``math.exp(x, y)``.

Supply docstrings for every class and public function. Otherwise, when you
find yourself writing comments, consider writing better, self-explaining code
instead. When adding "TODO" or "FIXME" comments, make sure somebody else can
understand and begin to work on them. Use type hinting wherever possible.

Functions should not span more than one screen length.

Copyright & Authors
-------------------

All source code, except where otherwise mentioned, is Copyright (C) 2018, 2019
OFFIS e.V. Contributing authors are listed in order of their appeareance in
the file AUTHORS.

The dynamic loader used in the command-line utility relies more or less
verbatim on code from the Python project. See the file ``doc/python-license``.

The code in ``palaestrai.types`` comes from the OpenAI Gym_ project.  See the file
``doc/gym-license.md``.

.. _mosaik: http://mosaik.offis.de/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Gym: https://github.com/openai/gym

Related Repositories
--------------------

See here for a list of palaestrAI-related repositories, for example interfaces to other software or simple agent/environment implementations: https://gitlab.com/arl2
