"""
Contract to Layer the Web UI Selector File
"""

import logging
from abc import ABC

from playwright.async_api import Page


class WebUISelectorCapable(ABC):
    """
    A Capable class to cover the Selector Config Type.
    It will add all the functions needed for PLatform specific
    with the custom web ui and Act as a Reference to TypeCheck
    """

    def __init__(self, page: Page, log: logging.Logger, **kwargs):
        self.page = page
        self.log = log
