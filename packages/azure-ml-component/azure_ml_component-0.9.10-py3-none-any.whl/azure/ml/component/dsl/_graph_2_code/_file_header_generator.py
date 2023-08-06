# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azure.ml.component.dsl._graph_2_code._base_generator import CodeBaseGenerator
from azure.ml.component.dsl._graph_2_code._utils import FILE_HEADER_TEMPLATE


class CodeFileHeaderGenerator(CodeBaseGenerator):
    DEFAULT_URL = "https://fake_url"

    def __init__(self, logger, url=None):
        self._url = url if url else self.DEFAULT_URL
        super(CodeFileHeaderGenerator, self).__init__(logger=logger)

    @property
    def url(self):
        return self._url

    @property
    def tpl_file(self):
        return FILE_HEADER_TEMPLATE

    @property
    def entry_template_keys(self):
        return [
            "url"
        ]
