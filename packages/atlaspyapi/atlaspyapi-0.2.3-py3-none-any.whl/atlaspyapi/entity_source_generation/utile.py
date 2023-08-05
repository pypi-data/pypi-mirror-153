#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import time
from configparser import ConfigParser

import jinja2


# get current time
def current_milli_time():
    return int(round(time.time()))


# set up config file
def init_config(config_file_path: str) -> dict:
    if os.path.isfile(config_file_path):
        config = ConfigParser()
        config.read(config_file_path)
        return config
    else:
        print("config file not found")
        raise FileNotFoundError


# jinja2 util function, it takes a jinja2 template and a dict of attributes, then merges them to generate a target file
def populate_template(file_path: str, context: dict) -> str:
    path, file_name = os.path.split(file_path)
    return (
        jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./"))
        .get_template(file_name)
        .render(context)
    )
