import os
from pyonir import Pyonir, PyonirPlugin
from .formctrl import FormCtrl, form_ctrl


class PyonirForms(PyonirPlugin):

    def __init__(self, app: Pyonir):

        super().__init__(app, self)
        self.name = 'pyonir_forms'
        self.app_dirpath = os.path.join(app.app_dirpath, app.PLUGINS_DIRNAME, self.name)

        # Setup templates
        app.TemplateEnvironment.load_template_path(self.templates_dirpath)
        app.TemplateEnvironment.add_filter(form_ctrl)

    @property
    def templates_dirpath(self) -> str:
        """Plugin template location"""
        return os.path.join(self.app_dirpath, 'templates')
