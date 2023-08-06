# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from abc import ABC
from pathlib import Path

from jinja2 import Template

from azure.ml.component.dsl._component_generator import BaseGenerator


class CodeBaseGenerator(BaseGenerator, ABC):
    def __init__(self, logger, target_file=None, **kwargs):
        self.logger = logger
        if not target_file:
            target_file = "entry.py"
        self.target_file = target_file
        super(CodeBaseGenerator, self).__init__(**kwargs)

    def to_component_entry_code(self):
        with open(self.tpl_file) as f:
            entry_template = f.read()
            entry_template = Template(entry_template, trim_blocks=True, lstrip_blocks=True)

        return entry_template.render(**{key: getattr(self, key) for key in self.entry_template_keys})

    def to_component_entry_file(self, target_dir=None):
        if target_dir:
            target = Path(target_dir) / self.target_file
        else:
            target = self.target_file
        super(CodeBaseGenerator, self).to_component_entry_file(target=target)
