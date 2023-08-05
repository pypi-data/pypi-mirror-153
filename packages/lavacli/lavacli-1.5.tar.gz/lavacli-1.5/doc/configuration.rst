.. _configuration:

Configuration
#############

lavacli can be used with or without a configuration file. Having a
configuration file will help when using more than one lava instance.

Without a configuration file
============================

When using lavacli without any configuration file, the uri should be passed as
a command line argument:

.. code-block:: shell

    lavacli --uri https://validation.linaro.org/RPC2 devices list

The authentication can also be passed in the uri:

.. code-block:: shell

    lavacli --uri https://admin:my_secret_token@validation.linaro.org/RPC2 devices list

Keep in mind, that any user on the same machine will then see the username and
token in the process list.

With a configuration file
=========================

lavacli configuration file is stored in **~/.config/lavacli.yaml**. This is a
YAML dictionary where each key is an *identity*.

.. code-block:: yaml

    default:
      uri: https://validation.linaro.org/RPC2
    validation:
      uri: https://validation.linaro.org/RPC2
    admin@validation:
      uri: https://validation.linaro.org/RPC2
      username: admin
      token: my_secret_token
    staging:
      uri: https://staging.validation.linaro.org/RPC2
      events:
        uri: tcp://staging.validation.linaro.org:5500

When using lavacli, the *identity* can be used with **-i** or **--identity**:

.. code-block:: shell

    lavacli -i admin@validation devices list
    lavacli -i staging events listen

By default, the **default** identity will be used. Hence both commands are
identitical:

.. code-block:: shell

    lavacli devices list
    lavacli -i validation devices list

Available options
*****************

For each identity, you have to set:

* **uri**: the uri of the RPC endpoint.

You can also set:

* **username**: the api username
* **token**: the api token
* **version**: the api version to use when talking to this instance
* **timeout**: the http timeout (defaults to 20 seconds)
* **proxy**: the uri to the proxy
* **verify_ssl_cert**: set it to false to ignore SSL certificates errors (defaults to true)
* **events**: zmq event configuration

The **events** key is a dictionary where you can specify:

* **uri**: the uri of the events stream. If not specified, lavacli will ask the server.
* **socks_proxy**: uri to the socks proxy, if needed
