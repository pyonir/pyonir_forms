from pyonir.core.templating import DeserializeFile
import pytest, os


@pytest.fixture(scope="session")
def mock_demo_form() -> DeserializeFile:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file = DeserializeFile(os.path.join(base_path, 'contents/@forms/demo-form.md'))
    return file