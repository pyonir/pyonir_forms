import os
from pathlib import Path

from pyonir import Pyonir, PyonirPlugin
from .formctrl import form_ctrl


class PyonirForms(PyonirPlugin):

    name = 'pyonir_forms'

    def __init__(self, app: Pyonir):
        super().__init__(app, self)

        # Setup templates
        app.TemplateEnvironment.load_template_path(self.templates_dirpath)
        app.TemplateEnvironment.add_filter(form_ctrl)

    @property
    def plugins_dirpath(self) -> Path:
        return Path(self.plugins_dirpath) / self.name

    @property
    def templates_dirpath(self) -> Path:
        """Form html templates use to build dynamic forms from configuration"""
        return Path(self.plugins_dirpath) / 'templates'
