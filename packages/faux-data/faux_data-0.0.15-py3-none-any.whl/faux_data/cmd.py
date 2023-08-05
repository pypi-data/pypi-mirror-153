#    Copyright 2022 @jack-tee
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
import os
import pprint
import sys
from typing import List

from jinja2 import Environment, FileSystemLoader

from .template import Template
from .utils import get_parts
from .version import __version__

log = logging.getLogger(__name__)

dir = os.path.dirname(__file__)
env = Environment(loader=FileSystemLoader(f"{dir}/templates"))

def parse_params(args):
    args = " ".join(args)
    parts = get_parts(args)

    #print(parts)
    args_iter = iter(parts)

    params = {}
    elem = ""
    prev_elem = None
    for elem in args_iter:
        if elem.startswith("--"):
            if prev_elem:
                params[prev_elem.strip("-")] = True

            if "=" in elem:
                params[elem.split("=")[0].strip("-")] = elem.split("=")[1]
                continue

        else:
            if prev_elem:
                params[prev_elem.strip("-")] = elem
                prev_elem = None
                continue
            else:
                log.error(f"don't know what to do with {elem}")

        prev_elem = elem

    if prev_elem:
        params[prev_elem.strip("-")] = True

    return  params




def cmd(args: List[str]):
    """The main entry point to the cli."""

    try:
        cmd_args = args[1:]
    except IndexError as e:
        show_help()
        sys.exit(1)

    match cmd_args:
        case [] | ["--help"] | ["-h"]:
            show_help()

        case ['version'] | ['--version']:
            print(__version__)

        case [cmd, filename, *objs]:
            params = parse_params(objs)
            set_debug(params)

            match cmd:
                case 'run':
                    t = Template.from_file(filename, params)
                    t.run()
                    cmd_template = env.get_template("run.jinja")
                    print(cmd_template.render(template=t))

                case 'render':
                    t, v = Template.render_from_file(filename, params)
                    cmd_template = env.get_template("render.jinja")
                    print(cmd_template.render(t=t, v=pprint.pformat(v), filename=filename, params=params))

                case 'sample':
                    t = Template.from_file(filename, params)
                    t.generate()
                    cmd_template = env.get_template("sample.jinja")
                    print(cmd_template.render(template=t, filename=filename))

                case 'sample-all':
                    for root, _, filenames in os.walk(filename):
                        for filename in filenames:
                            if filename.endswith(".yaml"):
                                filepath = os.path.join(root, filename)
                                try:
                                    t = Template.from_file(filepath, params)
                                    t.generate()
                                    print(filepath, "OK")
                                except Exception as e:
                                    print(filepath, e)

                case _ as c:
                    show_help(msg=f"Unrecognised command [{cmd}]. Expected one of render, sample, run or sample-all.")

        case _ as args:
            show_help(msg=f"Unrecognised arguments {args}. Expected faux <command> <arg> [--flag ...].")

def show_help(msg: str = None):
    cmd_template = env.get_template("help.jinja")
    print(cmd_template.render(msg=msg))


def set_debug(params: dict) -> None:
    if params.get("debug"):
        logging.basicConfig(level="DEBUG")
        log.debug(f"Parsed params {params} from args {sys.argv}")
    else:
        logging.basicConfig(level="INFO")


def main():
    cmd(sys.argv)

if __name__ == '__main__':
    cmd(sys.argv)
