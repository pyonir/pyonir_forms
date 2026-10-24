import pytest
from pyonir import DeserializeFile
from ..formctrl import FormCtrl, form_ctrl, process_value, form


# ----------------------------------------------------------------------
# form_ctrl
# ----------------------------------------------------------------------

def test_form_file(mock_demo_form: DeserializeFile):
    file_form = form(mock_demo_form.data)
    form_ctrl: FormCtrl = file_form.inputs[0]
    assert form_ctrl
    
def test_string_input_creates_text_control():
    ctrl = form_ctrl("Username")

    assert isinstance(ctrl, FormCtrl)
    assert ctrl.label == "Username"
    assert ctrl.props["type"] == "text"
    assert ctrl.props["name"] == "username"
    assert ctrl.props["id"] == "username"


def test_existing_formctrl_is_returned():
    ctrl = FormCtrl(label="Email")

    assert form_ctrl(ctrl) is ctrl


def test_default_name_and_id_generated():
    ctrl = form_ctrl({
        "label": "First Name"
    })

    assert ctrl.props["name"] == "first_name"
    assert ctrl.props["id"] == "first_name"


def test_existing_name_and_id_preserved():
    ctrl = form_ctrl({
        "label": "First Name",
        "name": "fname",
        "id": "myid"
    })

    assert ctrl.props["name"] == "fname"
    assert ctrl.props["id"] == "myid"


def test_nested_controls():
    ctrl = form_ctrl({
        "label": "Address",
        "inputs": [
            {
                "label": "Street"
            },
            {
                "label": "Zip Code"
            }
        ]
    })

    assert len(ctrl.inputs) == 2

    assert ctrl.inputs[0].props["name"] == "address_street"
    assert ctrl.inputs[1].props["name"] == "address_zip_code"


def test_custom_type():
    ctrl = form_ctrl({
        "label": "Password",
        "type": "password"
    })

    assert ctrl.props["type"] == "password"


def test_html_preserved():
    ctrl = form_ctrl({
        "label": "Terms",
        "html": "<small>Required</small>"
    })

    assert ctrl.html == "<small>Required</small>"


def test_description_preserved():
    ctrl = form_ctrl({
        "label": "Email",
        "description": "Primary email"
    })

    assert ctrl.description == "Primary email"


# ----------------------------------------------------------------------
# Boolean attributes
# ----------------------------------------------------------------------

def test_required_boolean():
    ctrl = form_ctrl({
        "label": "Username",
        "required": True
    })

    assert ctrl.props["required"] is True
    assert "required" in ctrl.input_props


def test_false_boolean_not_rendered():
    ctrl = form_ctrl({
        "label": "Username",
        "required": False
    })

    assert "required" not in ctrl.input_props


def test_multiple_boolean_attributes():
    ctrl = form_ctrl({
        "label": "Agree",
        "required": True,
        "checked": True,
        "disabled": True
    })

    html = ctrl.input_props

    assert "required" in html
    assert "checked" in html
    assert "disabled" in html


# ----------------------------------------------------------------------
# inputprops
# ----------------------------------------------------------------------

def test_inputprops_contains_normal_attributes():
    ctrl = form_ctrl({
        "label": "Email",
        "placeholder": "Enter email"
    })

    html = ctrl.input_props

    assert 'placeholder="Enter email"' in html
    assert 'type="text"' in html


def test_inputprops_escapes_quotes():
    ctrl = form_ctrl({
        "label": "Name",
        "value": 'John "Johnny" Smith'
    })

    assert "&quot;" in ctrl.input_props


def test_none_values_not_rendered():
    ctrl = FormCtrl(
        label="x",
        props={
            "type": "text",
            "placeholder": None
        }
    )

    html = ctrl.input_props

    assert "placeholder" not in html


# ----------------------------------------------------------------------
# process_value
# ----------------------------------------------------------------------

def test_process_non_string():
    assert process_value(123) == 123
    assert process_value(True) is True


def test_process_string_without_template():
    assert process_value("hello") == "hello"


# ----------------------------------------------------------------------
# slug generation through form_ctrl
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "label,expected",
    [
        ("First Name", "first_name"),
        ("ZIP Code", "zip_code"),
        ("Phone #", "phone"),
        ("User-Name", "user_name"),
        ("A   B", "a_b"),
    ],
)
def test_slug_generation(label, expected):
    ctrl = form_ctrl(label)

    assert ctrl.props["id"] == expected
    assert ctrl.props["name"] == expected