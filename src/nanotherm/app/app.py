# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
#
#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#

import logging

log = logging.getLogger(__name__)

class App:
    def __init__(self, config: dict[str]):
        log.info('Starting main application.')
        
    def run(self):
        print('Hello, world!')