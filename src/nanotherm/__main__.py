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

"""
Main module for the nanotherm application.

This module handles the application's entry point and logging configuration.
It provides functionality to set up logging based on different running modes
(debug or deployment).
"""

from nanotherm.config import load_config
from nanotherm.config.logger import setup_logging   
from nanotherm.app import App
import logging 


def main():
    """
    Main entry point for the nanotherm application.
    
    Initializes the application and starts the main processing loop.
    """
    
    config = load_config()
    setup_logging(config['logging'])
    logger = logging.getLogger(__name__)
    logger.info("Finished setup.")
    
    app = App(config)
    app.run()
    
if __name__=='__main__':
    main()