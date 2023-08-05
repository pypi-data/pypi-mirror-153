.. _usage:

Usage
#####

Here is the list of available commands and sub-commands.

Aliases
=======

LAVA aliases can be managed by:

.. code-block:: shell

    lavacli aliases add <name>
    lavacli aliases delete <name>
    lavacli aliases list
    lavacli aliases show <name>

Device types
============

LAVA device types can be managed by:

.. code-block:: shell

    lavacli device-types add [...]
    lavacli device-types aliases add <name> <alias>
    lavacli device-types aliases delete <name> <alias>
    lavacli device-types aliases list
    lavacli device-types health-check get <name>
    lavacli device-types health-check set <name> <health-check.yaml>
    lavacli device-types list
    lavacli device-types show <name>
    lavacli device-types template get <name>
    lavacli device-types template set <name> <template.jinja2>
    lavacli device-types update [...]

Devices
=======

LAVA devices can be managed by:

.. code-block:: shell

    lavacli devices add [...]
    lavacli devices dict get <hostname>
    lavacli devices dict set <hostname>
    lavacli devices list
    lavacli devices maintenance <hostname>
    lavacli devices show <hostname>
    lavacli devices tags add <hostname> <name>
    lavacli devices tags delete <hostname> <name>
    lavacli devices tags list
    lavacli devices update [...]

Events
======

LAVA events can be used by:

.. code-block:: shell

    lavacli events listen
    lavacli events wait device [...]
    lavacli events wait job [...]
    lavacli events wait worker [...]

Identities
==========

lavacli identities can be managed by:

.. code-block:: shell

    lavacli identities add [...]
    lavacli identities delete <id>
    lavacli identities list
    lavacli identities show <id>

Jobs
====

LAVA jobs can be managed by:

.. code-block:: shell

    lavacli jobs cancel <job_id>
    lavacli jobs config <job_i>
    lavacli jobs definition <job_id>
    lavacli jobs list
    lavacli jobs logs <job_id>
    lavacli jobs queue <device-type>
    lavacli jobs resubmit <job_id>
    lavacli jobs run <definition.yaml>
    lavacli jobs show <job_id>
    lavacli jobs submit <definition.yaml>
    lavacli jobs validate <definition.yaml>
    lavacli jobs wait <job_id>

Lab
===

LAVA lab can be managed by:

.. code-block:: shell

    lavacli lab apply <config>
    lavacli lab import <config>

Results
=======

LAVA results can be managed by:

.. code-block:: shell

    lavacli results <job_id>
    lavacli results <job_id> <suite>
    lavacli results <job_id> <suite> <case>

System
======

LAVA instance can be managed by:

.. code-block:: shell

    lavacli system active
    lavacli system api
    lavacli system export <name>
    lavacli system maintenance
    lavacli system methods list
    lavacli system methods help <method>
    lavacli system methods signature <method>
    lavacli system version
    lavacli system whoami

In order to put a full instance into maintenance, an admin could call **system
maintenance**. This function will:

* set all workers health to *MAINTENANCE*
* wait for all jobs to finish

If the instance should be put into into maintenance immediately, addind **--force** will:

* set all workers health to *MAINTENANCE*
* cancel all running jobs
* wait for all jobs to finish

It also possible to exclude some workers with **--exclude**.

When the maintenance is finished, calling **system active** will move every
worker into *MAINTENANCE* to *ACTIVE*.

Tags
====

LAVA tag can be managed by:

.. code-block:: shell

    lavacli tags add [...]
    lavacli tags delete <tag>
    lavacli tags list
    lavacli tags show <tag>

Utils
=====

Some utilities are available with:

.. code-block:: shell

    lavacli utils logs print <output.yaml>
    lavacli utils templates render <output.yaml>

Printing logs
*************

When working with raw logs, lavacli might help by coloring the logs by levels.

It's also possible to filter the logs by level. To only print the serial output
and the commands sent by LAVA to the board, use:

.. code-block:: shell

    lavacli utils logs print --filter target,input

Available log levels are: exception, error, warning, info, debug, target,
input, feedback, results.

Workers
=======

LAVA workers can be managed by:

.. code-block:: shell

    lavacli workers add [...]
    lavacli workers config get <hostname>
    lavacli workers config set <hostname> <config.yaml>
    lavacli workers env get <hostname>
    lavacli workers env set <hostname> <env.yaml>
    lavacli workers list
    lavacli workers maintenance <hostname>
    lavacli workers update [...]
    lavacli workers show <hostname>
