# -*- coding: utf-8 -*-
# vim: set ts=4

# Copyright 2017 Rémi Duraffort
# This file is part of lavacli.
#
# lavacli is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lavacli is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with lavacli.  If not, see <http://www.gnu.org/licenses/>

import argparse
import json
import time
import sys

from lavacli.utils import safe_yaml


def positive_integer(value):
    int_value = int(value)
    if int_value < 0:
        raise argparse.ArgumentTypeError("%r should be a positive integer" % value)
    return int_value


def configure_parser(parser, version):
    sub = parser.add_subparsers(dest="sub_sub_command", help="Sub commands")
    sub.required = True

    # "add"
    workers_add = sub.add_parser("add", help="add a worker")
    workers_add.add_argument("name", type=str, help="worker name")
    workers_add.add_argument(
        "--description", type=str, default=None, help="worker description"
    )
    workers_add.add_argument(
        "--disabled",
        action="store_true",
        default=False,
        help="create a disabled worker",
    )

    # "config"
    workers_config = sub.add_parser("config", help="worker configuration")
    config_sub = workers_config.add_subparsers(
        dest="sub_sub_sub_command", help="Sub commands"
    )
    config_sub.required = True
    if version >= (2022, 4):
        config_delete = config_sub.add_parser(
            "delete", help="delete the worker configuration"
        )
        config_delete.add_argument("name", type=str, help="worker name")
    config_get = config_sub.add_parser("get", help="get the worker configuration")
    config_get.add_argument("name", type=str, help="worker name")

    config_set = config_sub.add_parser("set", help="set the worker configuration")
    config_set.add_argument("name", type=str, help="worker name")
    config_set.add_argument(
        "config", type=argparse.FileType("r"), help="configuration file"
    )

    if version >= (2020, 4) and version <= (2020, 8):
        # "certificate"
        workers_cert = sub.add_parser("certificate", help="worker certificate")
        cert_sub = workers_cert.add_subparsers(
            dest="sub_sub_sub_command", help="Sub commands"
        )
        cert_sub.required = True
        cert_get = cert_sub.add_parser("get", help="get the worker certificate")
        cert_get.add_argument("name", type=str, help="worker name")

        cert_set = cert_sub.add_parser("set", help="set the worker certificate")
        cert_set.add_argument("name", type=str, help="worker name")
        cert_set.add_argument(
            "certificate", type=argparse.FileType("r"), help="certificate file"
        )

    if version >= (2019, 6):
        # "env"
        workers_env = sub.add_parser("env", help="worker environment")
        env_sub = workers_env.add_subparsers(
            dest="sub_sub_sub_command", help="Sub commands"
        )
        env_sub.required = True
        if version >= (2022, 4):
            env_delete = env_sub.add_parser(
                "delete", help="delete the worker environment"
            )
            env_delete.add_argument("name", type=str, help="worker name")

        env_get = env_sub.add_parser("get", help="get the worker environment")
        env_get.add_argument("name", type=str, help="worker name")

        env_set = env_sub.add_parser("set", help="set the worker environment")
        env_set.add_argument("name", type=str, help="worker name")
        env_set.add_argument(
            "env", type=argparse.FileType("r"), help="environment file"
        )

    if version >= (2022, 1):
        # "env-dut"
        workers_env_dut = sub.add_parser("env-dut", help="worker environment")
        env_dut_sub = workers_env_dut.add_subparsers(
            dest="sub_sub_sub_command", help="Sub commands"
        )
        env_dut_sub.required = True
        if version >= (2022, 4):
            env_dut_delete = env_dut_sub.add_parser(
                "delete", help="delete the dut environment"
            )
            env_dut_delete.add_argument("name", type=str, help="worker name")

        env_dut_get = env_dut_sub.add_parser("get", help="get the dut environment")
        env_dut_get.add_argument("name", type=str, help="worker name")

        env_dut_set = env_dut_sub.add_parser("set", help="set the dut environment")
        env_dut_set.add_argument("name", type=str, help="worker name")
        env_dut_set.add_argument(
            "env", type=argparse.FileType("r"), help="environment file"
        )

    # "list"
    workers_list = sub.add_parser("list", help="list workers")
    out_format = workers_list.add_mutually_exclusive_group()
    out_format.add_argument(
        "--json",
        dest="output_format",
        default=None,
        action="store_const",
        const="json",
        help="print as json",
    )
    out_format.add_argument(
        "--yaml",
        dest="output_format",
        action="store_const",
        const="yaml",
        default=None,
        help="print as yaml",
    )

    # "maintenance"
    workers_maintenance = sub.add_parser("maintenance", help="maintenance the worker")
    workers_maintenance.add_argument("name", type=str, help="worker name")
    workers_maintenance.add_argument(
        "--force",
        default=False,
        action="store_true",
        help="force worker maintenance by canceling running jobs",
    )
    workers_maintenance.add_argument(
        "--no-wait",
        dest="wait",
        default=True,
        action="store_false",
        help="do not wait for the devices to be idle",
    )

    # "show"
    workers_show = sub.add_parser("show", help="show worker details")
    workers_show.add_argument("name", help="worker name")
    out_format = workers_show.add_mutually_exclusive_group()
    out_format.add_argument(
        "--json",
        dest="output_format",
        default=None,
        action="store_const",
        const="json",
        help="print as json",
    )
    out_format.add_argument(
        "--yaml",
        dest="output_format",
        action="store_const",
        const="yaml",
        default=None,
        help="print as yaml",
    )

    # "update"
    update_parser = sub.add_parser("update", help="update worker properties")
    update_parser.add_argument("name", type=str, help="worker name")
    update_parser.add_argument(
        "--description", type=str, default=None, help="worker description"
    )
    if version >= (2017, 12):
        update_parser.add_argument(
            "--health",
            type=str,
            default=None,
            choices=["ACTIVE", "MAINTENANCE", "RETIRED"],
            help="worker health",
        )
    else:
        display = update_parser.add_mutually_exclusive_group()
        display.add_argument(
            "--disable",
            action="store_false",
            default=None,
            dest="display",
            help="disable the worker",
        )
        display.add_argument(
            "--enable",
            action="store_true",
            default=None,
            dest="display",
            help="enable the worker",
        )
    if version >= (2020, 1):
        update_parser.add_argument(
            "--job-limit", type=positive_integer, default=None, help="job limit"
        )


def help_string():
    return "manage workers"


def handle_add(proxy, options, _):
    proxy.scheduler.workers.add(options.name, options.description, options.disabled)
    return 0


def handle_config(proxy, options, _):
    if options.sub_sub_sub_command == "delete":
        config = proxy.scheduler.workers.set_config(options.name, "")
    elif options.sub_sub_sub_command == "get":
        config = proxy.scheduler.workers.get_config(options.name)
        print(str(config).rstrip("\n"))
    else:
        config = options.config.read()
        ret = proxy.scheduler.workers.set_config(options.name, config)
        if not ret:
            print("Unable to store worker configuration")
            return 1
    return 0


def handle_certificate(proxy, options, _):
    if options.sub_sub_sub_command == "get":
        env = proxy.scheduler.workers.get_certificate(options.name)
        print(str(env).rstrip("\n"))
    else:
        certificate = options.certificate.read()
        ret = proxy.scheduler.workers.set_certificate(options.name, certificate)
        if not ret:
            print("Unable to store worker certificate")
            return 1
    return 0


def handle_env(proxy, options, _):
    if options.sub_sub_sub_command == "delete":
        proxy.scheduler.workers.set_env(options.name, "")
    elif options.sub_sub_sub_command == "get":
        env = proxy.scheduler.workers.get_env(options.name)
        print(str(env).rstrip("\n"))
    else:
        env = options.env.read()
        ret = proxy.scheduler.workers.set_env(options.name, env)
        if not ret:
            print("Unable to store worker environment")
            return 1
    return 0


def handle_env_dut(proxy, options, _):
    if options.sub_sub_sub_command == "delete":
        proxy.scheduler.workers.set_env_dut(options.name, "")
    elif options.sub_sub_sub_command == "get":
        env = proxy.scheduler.workers.get_env_dut(options.name)
        print(str(env).rstrip("\n"))
    else:
        env = options.env.read()
        ret = proxy.scheduler.workers.set_env_dut(options.name, env)
        if not ret:
            print("Unable to store worker dut environment")
            return 1
    return 0


def handle_list(proxy, options, _):
    workers = proxy.scheduler.workers.list()
    if options.output_format == "json":
        print(json.dumps(workers))
    elif options.output_format == "yaml":
        safe_yaml.dump(workers, sys.stdout)
    else:
        print("Workers:")
        for worker in workers:
            print("* %s" % worker)
    return 0


def handle_maintenance(proxy, options, _):
    proxy.scheduler.workers.update(options.name, None, "MAINTENANCE")

    if options.force or options.wait:
        worker_devices = proxy.scheduler.workers.show(options.name)["devices"]
        for device in proxy.scheduler.devices.list():
            if device["hostname"] not in worker_devices:
                continue
            current_job = device["current_job"]
            if current_job is not None:
                print("-> waiting for job %s" % current_job)
                # if --force is passed, cancel the job
                if options.force:
                    print("--> canceling")
                    proxy.scheduler.jobs.cancel(current_job)
                while (
                    options.wait
                    and proxy.scheduler.jobs.show(current_job)["state"] != "Finished"
                ):
                    print("--> waiting")
                    time.sleep(5)
    return 0


def handle_show(proxy, options, config):
    worker = proxy.scheduler.workers.show(options.name)
    if options.output_format == "json":
        if "last_ping" in worker:
            worker["last_ping"] = worker["last_ping"].value
        print(json.dumps(worker))
    elif options.output_format == "yaml":
        if "last_ping" in worker:
            worker["last_ping"] = worker["last_ping"].value
        safe_yaml.dump(worker, sys.stdout)
    else:
        print("hostname    : %s" % worker["hostname"])
        print("description : %s" % worker["description"])

        if config["version"] >= (2017, 12):
            print("state       : %s" % worker["state"])
            print("health      : %s" % worker["health"])
        else:
            print("master      : %s" % worker["master"])
            print("hidden      : %s" % worker["hidden"])

        if config["version"] >= (2018, 1):
            print("devices     : %s" % ", ".join(worker["devices"]))
            print("last ping   : %s" % worker["last_ping"])
        else:
            print("devices     : %d" % worker["devices"])

        if config["version"] >= (2020, 1):
            print("job limit   : %d" % worker["job_limit"])

        if config["version"] >= (2020, 6):
            print("version     : %s" % worker["version"])

        if "token" in worker:
            print("token       : %s" % worker["token"])
    return 0


def handle_update(proxy, options, config):
    if config["version"] >= (2020, 1):
        proxy.scheduler.workers.update(
            options.name, options.description, options.health, options.job_limit
        )
    elif config["version"] >= (2017, 12):
        proxy.scheduler.workers.update(
            options.name, options.description, options.health
        )
    else:
        proxy.scheduler.workers.update(
            options.name, options.description, not options.display
        )
    return 0


def handle(proxy, options, config):
    handlers = {
        "add": handle_add,
        "config": handle_config,
        "certificate": handle_certificate,
        "env": handle_env,
        "env-dut": handle_env_dut,
        "list": handle_list,
        "maintenance": handle_maintenance,
        "show": handle_show,
        "update": handle_update,
    }
    return handlers[options.sub_sub_command](proxy, options, config)
