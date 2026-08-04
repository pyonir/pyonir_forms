from pyonir import DeserializeFile
from ..formctrl import form


def test_form_file():
    file = DeserializeFile('/Users/hypermac/dev/pyonir-plugins/pyonir_forms/contents/@forms/demo-form.md')
    file_form = form(file.data)
    pass