# -*- coding: utf-8 -*-
# vim: set ts=4

# Copyright 2022-present Rémi Duraffort
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

import contextlib
from dataclasses import asdict, dataclass, field, fields, MISSING
import difflib
from pathlib import Path
from typing import Any, Dict, List, Set
import xmlrpc

import ruamel.yaml

from lavacli import colors


def print_file_diff(src, dst):
    if src is None:
        print("    | + None")
    elif dst is None:
        print("    | - None")
    else:
        diffs = difflib.unified_diff(src.split("\n"), dst.split("\n"), lineterm="")
        print("    | " + "\n    | ".join(list(diffs)[2:]))


class Base:
    @classmethod
    def new(cls, **kwargs):
        fields_names = [f.name for f in fields(cls)]
        i_kwargs = {}
        v_kwargs = {}
        for k in kwargs:
            if k in fields_names:
                v_kwargs[k] = kwargs[k]
            else:
                i_kwargs[k] = kwargs[k]

        return cls(**v_kwargs)

    def diff(self, data: Dict[str, Any]) -> List[str]:
        return [
            f.name for f in fields(self) if getattr(self, f.name) != data.get(f.name)
        ]


@dataclass
class Device(Base):
    hostname: str
    device_type: str
    worker: str
    description: str = None
    tags: Set[str] = field(default_factory=set)

    def __post_init__(self):
        self.tags = set(self.tags)

    def diff(self, data: Dict[str, Any]) -> List[str]:
        data = data.copy()
        data["tags"] = set(data["tags"])
        if data["description"] in ["", None]:
            data["description"] = self.description
        return super().diff(data)

    def dump(self):
        defaults = {f.name: f.default for f in fields(self) if f.default != MISSING}
        data = {}
        for k, v in asdict(self).items():
            if k in defaults and v == defaults[k]:
                continue
            data[k] = v

        if "description" in data and data["description"] in ["", None]:
            del data["description"]
        if not data["tags"]:
            del data["tags"]
        else:
            data["tags"] = sorted(data["tags"])
        del data["hostname"]
        return data if data else None

    def get_dict(self, base):
        with contextlib.suppress(FileNotFoundError):
            return (base / "devices" / f"{self.hostname}.jinja2").read_text(
                encoding="utf-8"
            )
        return None

    def set_dict(self, base, text):
        (base / "devices").mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(FileNotFoundError):
            return (base / "devices" / f"{self.hostname}.jinja2").write_text(
                text, encoding="utf-8"
            )


@dataclass
class DeviceType(Base):
    name: str
    description: str = ""
    health_disabled: str = False
    health_denominator: str = "hours"
    health_frequency: int = 24
    aliases: Set[str] = field(default_factory=set)
    display: bool = True

    def __post_init__(self):
        self.aliases = set(self.aliases)

    def diff(self, data: Dict[str, Any]) -> List[str]:
        data = data.copy()
        data["aliases"] = set(data["aliases"])
        if data["description"] in ["", None]:
            data["description"] = self.description
        return super().diff(data)

    def dump(self):
        defaults = {f.name: f.default for f in fields(self) if f.default != MISSING}
        data = {}
        for k, v in asdict(self).items():
            if k in defaults and v == defaults[k]:
                continue
            data[k] = v

        if not data["aliases"]:
            del data["aliases"]
        else:
            data["aliases"] = list(data["aliases"])
        if "description" in data and data["description"] in ["", None]:
            del data["description"]
        del data["name"]
        return data if data else None

    def get_health_check(self, base):
        with contextlib.suppress(FileNotFoundError):
            return (base / "health-checks" / f"{self.name}.yaml").read_text(
                encoding="utf-8"
            )
        return None

    def set_health_check(self, base, text):
        (base / "health-checks").mkdir(parents=True, exist_ok=True)
        (base / "health-checks" / f"{self.name}.yaml").write_text(
            text, encoding="utf-8"
        )

    def get_template(self, base):
        with contextlib.suppress(FileNotFoundError):
            return (base / "device-types" / f"{self.name}.jinja2").read_text(
                encoding="utf-8"
            )

    def set_template(self, base, text):
        (base / "device-types").mkdir(parents=True, exist_ok=True)
        (base / "device-types" / f"{self.name}.jinja2").write_text(
            text, encoding="utf-8"
        )


@dataclass
class Worker(Base):
    hostname: str
    description: str = ""
    job_limit: int = 0

    def diff(self, data: Dict[str, Any]) -> List[str]:
        data = data.copy()
        if data["description"] in ["", None]:
            data["description"] = self.description
        return super().diff(data)

    def dump(self):
        defaults = {f.name: f.default for f in fields(self) if f.default != MISSING}
        data = {}
        for k, v in asdict(self).items():
            if k in defaults and v == defaults[k]:
                continue
            data[k] = v

        if "description" in data and data["description"] in ["", None]:
            del data["description"]
        del data["hostname"]
        return data if data else None

    def get_config(self, base):
        with contextlib.suppress(FileNotFoundError):
            return (base / "workers" / self.hostname / "dispatcher.yaml").read_text(
                encoding="utf-8"
            )

    def set_config(self, base, text):
        (base / "workers" / self.hostname).mkdir(parents=True, exist_ok=True)
        (base / "workers" / self.hostname / "dispatcher.yaml").write_text(
            text, encoding="utf-8"
        )

    def get_env(self, base):
        with contextlib.suppress(FileNotFoundError):
            return (base / "workers" / self.hostname / "env.yaml").read_text(
                encoding="utf-8"
            )

    def set_env(self, base, text):
        (base / "workers" / self.hostname).mkdir(parents=True, exist_ok=True)
        (base / "workers" / self.hostname / "env.yaml").write_text(
            text, encoding="utf-8"
        )

    def get_env_dut(self, base):
        with contextlib.suppress(FileNotFoundError):
            return (base / "workers" / self.hostname / "env-dut.yaml").read_text(
                encoding="utf-8"
            )

    def set_env_dut(self, base, text):
        (base / "workers" / self.hostname).mkdir(parents=True, exist_ok=True)
        (base / "workers" / self.hostname / "env-dut.yaml").write_text(
            text, encoding="utf-8"
        )


@dataclass
class Config:
    device_types: Dict[str, DeviceType]
    devices: Dict[str, Device]
    workers: Dict[str, Worker]

    def __post_init__(self):
        self.devices = {n: Device(hostname=n, **d) for n, d in self.devices.items()}
        self.device_types = {
            n: DeviceType(name=n, **(dt if dt is not None else {}))
            for n, dt in self.device_types.items()
        }
        self.workers = {
            h: Worker(hostname=h, **(w if w is not None else {}))
            for h, w in self.workers.items()
        }

    def dump(self):
        return {
            "device_types": {k: self.device_types[k].dump() for k in self.device_types},
            "devices": {k: self.devices[k].dump() for k in self.devices},
            "workers": {k: self.workers[k].dump() for k in self.workers},
        }


def configure_parser(parser, version):
    sub = parser.add_subparsers(dest="sub_sub_command", help="Sub commands")
    sub.required = True

    if version < (2022, 4):
        return

    # "apply"
    lab_apply = sub.add_parser("apply", help="apply configuration")
    lab_apply.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Do not update the configuration",
    )
    lab_apply.add_argument(
        "--resources",
        default=[],
        action="append",
        help="resources to sync",
    )
    lab_apply.add_argument("config", type=Path, help="configuration file")

    # "import"
    lab_apply = sub.add_parser("import", help="import configuration")
    lab_apply.add_argument("config", type=Path, help="configuration file")


def help_string():
    return "manage lab configuration"


def handle_apply(proxy, options, config):
    if not options.resources:
        options.resources = ["devices", "device-types", "workers"]

    lab = Config(**ruamel.yaml.safe_load(options.config.read_text(encoding="utf-8")))
    base = (options.config / ".." / options.config.stem).resolve()

    print(f"{colors.cyan}> device-types{colors.reset}")
    if "device-types" not in options.resources:
        print(f"  {colors.yellow}-> SKIP{colors.reset}")
    else:
        device_types = [dt["name"] for dt in proxy.scheduler.device_types.list(False)]
        for dt in lab.device_types.values():
            if dt.name in device_types:
                print(f"  {colors.green}* {dt.name}{colors.reset}")
            else:
                print(f"  {colors.yellow}* {dt.name}{colors.reset}")
                raise NotImplementedError("Unable to create the device-type")
            data = proxy.scheduler.device_types.show(dt.name)
            diff = dt.diff(data)
            for name in (n for n in diff if n != "aliases"):
                print(
                    f"    {colors.yellow}-> {name}: '{data[name]}' => '{getattr(dt, name)}'{colors.reset}"
                )
            if diff:
                if not options.dry_run:
                    proxy.scheduler.device_types.update(
                        dt.name,
                        dt.description if "description" in diff else None,
                        dt.display if "display" in diff else None,
                        None,
                        dt.health_frequency if "health_frequency" in diff else None,
                        dt.health_denominator if "health_denominator" in diff else None,
                        dt.health_disabled if "health_disabled" in diff else None,
                    )
                if "aliases" in diff:
                    print(f"    {colors.yellow}-> aliases{colors.reset}")
                    missing = dt.aliases.difference(set(data["aliases"]))
                    for alias in missing:
                        print(f"      {colors.green}+ {alias}{colors.reset}")
                        if not options.dry_run:
                            proxy.scheduler.device_types.aliases.add(dt.name, alias)
                    missing = set(data["aliases"]).difference(dt.aliases)
                    for alias in missing:
                        print(f"      {colors.red}- {alias}{colors.reset}")
                        if not options.dry_run:
                            proxy.scheduler.device_types.aliases.delete(dt.name, alias)

            try:
                hc = str(proxy.scheduler.device_types.get_health_check(dt.name))
            except xmlrpc.client.Fault as exc:
                if exc.faultCode != 404:
                    raise
                hc = None
            if dt.get_health_check(base) != hc:
                print(f"    {colors.yellow}-> health-check{colors.reset}")
                print_file_diff(hc, dt.get_health_check(base))
                if not options.dry_run:
                    proxy.scheduler.device_types.set_health_check(
                        dt.name, dt.get_health_check(base)
                    )

            if not data["default_template"] or dt.get_template(base) is not None:
                try:
                    template = str(proxy.scheduler.device_types.get_template(dt.name))
                except xmlrpc.client.Fault as exc:
                    if exc.faultCode != 404:
                        raise
                    template = None
                if dt.get_template(base) != template:
                    print(f"    {colors.yellow}-> template{colors.reset}")
                    print_file_diff(template, dt.get_template(base))
                    if not options.dry_run:
                        proxy.scheduler.device_types.set_template(
                            dt.name, dt.template(base)
                        )

    print(f"{colors.cyan}> workers{colors.reset}")
    if "workers" not in options.resources:
        print(f"  {colors.yellow}-> SKIP{colors.reset}")
    else:
        workers = proxy.scheduler.workers.list()
        for worker in lab.workers.values():
            if worker.hostname in workers:
                print(f"  {colors.green}* {worker.hostname}{colors.reset}")
            else:
                print(f"  {colors.yellow}* {worker.hostname}{colors.reset}")
                if not options.dry_run:
                    proxy.scheduler.workers.add(
                        worker.hostname, worker.description, False
                    )
            data = proxy.scheduler.workers.show(worker.hostname)
            diff = worker.diff(data)
            for name in diff:
                print(
                    f"    {colors.yellow}-> {name}: '{data[name]}' => '{getattr(worker, name)}'{colors.reset}"
                )
            if diff and not options.dry_run:
                proxy.scheduler.workers.update(
                    worker.hostname,
                    worker.description if "description" in diff else None,
                    None,
                    worker.job_limit if "job_limit" in diff else None,
                )

            if not data["default_config"] or worker.get_config(base) is not None:
                try:
                    wconfig = str(proxy.scheduler.workers.get_config(worker.hostname))
                except xmlrpc.client.Fault as exc:
                    if exc.faultCode != 404:
                        raise
                    wconfig = None
                if worker.get_config(base) != wconfig:
                    print(f"    {colors.yellow}-> config{colors.reset}")
                    print_file_diff(wconfig, worker.get_config(base))
                    if not options.dry_run:
                        proxy.scheduler.workers.set_config(
                            dt.name, worker.get_config(base)
                        )

            if not data["default_env"] or worker.get_env(base) is not None:
                try:
                    wenv = str(proxy.scheduler.workers.get_env(worker.hostname))
                except xmlrpc.client.Fault as exc:
                    if exc.faultCode != 404:
                        raise
                    wenv = None
                if worker.get_env(base) != wenv:
                    print(f"    {colors.yellow}-> env{colors.reset}")
                    print_file_diff(wenv, worker.get_env(base))
                    if not options.dry_run:
                        proxy.scheduler.workers.set_env(dt.name, worker.get_env(base))

            if not data["default_env_dut"] or worker.get_env_dut(base) is not None:
                try:
                    wenv_dut = str(proxy.scheduler.workers.get_env_dut(worker.hostname))
                except xmlrpc.client.Fault as exc:
                    if exc.faultCode != 404:
                        raise
                    wenv_dut = None
                if worker.get_env_dut(base) != wenv_dut:
                    print(f"    {colors.yellow}-> env-dut{colors.reset}")
                    print_file_diff(wenv_dut, worker.get_env_dut(base))
                    if not options.dry_run:
                        proxy.scheduler.workers.set_env_dut(
                            dt.name, worker.get_env_dut(base)
                        )

    print(f"{colors.cyan}> devices{colors.reset}")
    if "devices" not in options.resources:
        print(f"  {colors.yellow}-> SKIP{colors.reset}")
    else:
        devices = [d["hostname"] for d in proxy.scheduler.devices.list(True)]
        for device in lab.devices.values():
            if device.hostname in devices:
                print(f"  {colors.green}* {device.hostname}{colors.reset}")
            else:
                print(f"  {colors.yellow}* {device.hostname}{colors.reset}")
                if not options.dry_run:
                    proxy.scheduler.devices.add(
                        device.hostname,
                        device.device_type,
                        device.worker,
                        None,
                        None,
                        None,
                        None,
                        device.description,
                    )
            data = proxy.scheduler.devices.show(device.hostname)
            diff = device.diff(data)
            for name in (n for n in diff if n != "tags"):
                print(
                    f"    {colors.yellow}-> {name}: '{data[name]}' => '{getattr(device, name)}'{colors.reset}"
                )
            if diff:
                if not options.dry_run:
                    proxy.scheduler.devices.update(
                        device.hostname,
                        device.worker if "worker" in diff else None,
                        None,
                        None,
                        None,
                        None,
                        device.description if "description" in diff else None,
                        device.device_type if "device_type" in diff else None,
                    )
                if "tags" in diff:
                    print(f"    {colors.yellow}-> tags{colors.reset}")
                    missing = device.tags.difference(set(data["tags"]))
                    for tag in missing:
                        print(f"      {colors.green}+ {tag}{colors.reset}")
                        if not options.dry_run:
                            proxy.scheduler.devices.tags.add(device.hostname, tag)
                    missing = set(data["tags"]).difference(device.tags)
                    for tag in missing:
                        print(f"      {colors.red}- {tag}{colors.reset}")
                        if not options.dry_run:
                            proxy.scheduler.devices.tags.delete(device.hostname, tag)

            try:
                ddict = str(proxy.scheduler.devices.get_dictionary(device.hostname))
            except xmlrpc.client.Fault as exc:
                if exc.faultCode != 404:
                    raise
                ddict = None

            if device.get_dict(base) != ddict:
                print(f"    {colors.yellow}-> dictionary{colors.reset}")
                print_file_diff(ddict, device.get_dict(base))
                if not options.dry_run:
                    proxy.scheduler.devices.set_dictionary(
                        device.hostname, device.get_dict(base)
                    )


def handle_import(proxy, options, config):
    lab = Config({}, {}, {})
    base = (options.config / ".." / options.config.stem).resolve()

    print(f"{colors.cyan}> device-types{colors.reset}")
    device_types = [dt["name"] for dt in proxy.scheduler.device_types.list(False)]
    for dt in device_types:
        print(f"  {colors.green}* {dt}{colors.reset}")
        data = proxy.scheduler.device_types.show(dt)
        lab.device_types[dt] = DeviceType.new(**data)

        try:
            hc = str(proxy.scheduler.device_types.get_health_check(dt))
        except xmlrpc.client.Fault as exc:
            if exc.faultCode != 404:
                raise
            hc = None
        if hc is not None:
            print(f"  {colors.green}  -> health-check{colors.reset}")
            lab.device_types[dt].set_health_check(base, hc)

        if data["default_template"]:
            print(f"  {colors.green}  -> default template{colors.reset}")
        else:
            try:
                template = str(proxy.scheduler.device_types.get_template(dt))
            except xmlrpc.client.Fault as exc:
                if exc.faultCode != 404:
                    raise
                template = None
            if template is not None:
                print(f"  {colors.green}  -> template{colors.reset}")
                lab.device_types[dt].set_template(base, template)

    print(f"{colors.cyan}> workers{colors.reset}")
    workers = proxy.scheduler.workers.list()
    for worker in workers:
        print(f"  {colors.green}* {worker}{colors.reset}")
        data = proxy.scheduler.workers.show(worker)
        lab.workers[worker] = Worker.new(**data)

        if data["default_config"]:
            print(f"  {colors.green}  -> default config{colors.reset}")
        else:
            try:
                wconfig = str(proxy.scheduler.workers.get_config(worker))
            except xmlrpc.client.Fault as exc:
                if exc.faultCode != 404:
                    raise
                wconfig = None
            if wconfig is not None:
                print(f"  {colors.green}  -> config{colors.reset}")
                lab.workers[worker].set_config(base, wconfig)

        if data["default_env"]:
            print(f"  {colors.green}  -> default env{colors.reset}")
        else:
            try:
                wenv = str(proxy.scheduler.workers.get_env(worker))
            except xmlrpc.client.Fault as exc:
                if exc.faultCode != 404:
                    raise
                wenv = None
            if wenv is not None:
                print(f"  {colors.green}  -> env{colors.reset}")
                lab.workers[worker].set_env(base, wenv)

        if data["default_env_dut"]:
            print(f"  {colors.green}  -> default env-dut{colors.reset}")
        else:
            try:
                wenv_dut = str(proxy.scheduler.workers.get_env_dut(worker))
            except xmlrpc.client.Fault as exc:
                if exc.faultCode != 404:
                    raise
                wenv_dut = None
            if wenv_dut is not None:
                print(f"  {colors.green}  -> env-dut{colors.reset}")
                lab.workers[worker].set_env_dut(base, wenv_dut)

    print(f"{colors.cyan}> devices{colors.reset}")
    devices = [d["hostname"] for d in proxy.scheduler.devices.list(True)]
    for device in devices:
        print(f"  {colors.green}* {device}{colors.reset}")
        data = proxy.scheduler.devices.show(device)
        lab.devices[device] = Device.new(**data)
        try:
            ddict = str(proxy.scheduler.devices.get_dictionary(device))
        except xmlrpc.client.Fault as exc:
            if exc.faultCode != 404:
                raise
            ddict = None
        if ddict is not None:
            print(f"  {colors.green}  -> dictionary{colors.reset}")
            lab.devices[device].set_dict(base, ddict)

    print(f"{colors.yellow}> {options.config}{colors.reset}")
    options.config.write_text(ruamel.yaml.round_trip_dump(lab.dump()), encoding="utf-8")

    return 0


def handle(proxy, options, config):
    handlers = {
        "apply": handle_apply,
        "import": handle_import,
    }
    return handlers[options.sub_sub_command](proxy, options, config)
