# Pyonir Forms plugin

Pyonir Forms is a lightweight form builder plugin for the Pyonir web framework.

## Installation

A prerequisite that pyonir is already installed.

```bash
> pyonir install plugin:pyonir/pyonir_forms
```

---

## Basic Usage

Create a form control.

```python
from pyonir_forms import form_ctrl

ctrl = form_ctrl({
    "label": "Email Address",
    "type": "email",
    "required": True,
    "placeholder": "name@example.com"
})
```

Result:

```python
ctrl.label
# Email Address

ctrl.props
# {
#     "type": "email",
#     "id": "email_address",
#     "name": "email_address",
#     "placeholder": "name@example.com",
#     "required": True
# }
```

---

## Nested Controls

Controls may contain child controls.

```python
address = form_ctrl({
    "label": "Address",
    "inputs": [
        {
            "label": "Street"
        },
        {
            "label": "City"
        },
        {
            "label": "Zip Code"
        }
    ]
})
```

Generated control names:

```
address_street
address_city
address_zip_code
```

---

## Automatic ID and Name Generation

If an `id` or `name` is not specified, one is automatically generated from the control label.

```python
form_ctrl({
    "label": "First Name"
})
```

Produces:

```python
props = {
    "id": "first_name",
    "name": "first_name",
    "type": "text"
}
```

---

## Boolean HTML Attributes

Boolean HTML attributes are automatically rendered correctly.

```python
form_ctrl({
    "label": "Terms",
    "type": "checkbox",
    "required": True,
    "checked": True
})
```

Renders as

```html
<input required checked ...>
```

---

## Template Variables

String values may contain Python format placeholders.

```python
form_ctrl({
    "label": "Name",
    "placeholder": "Welcome {username}"
})
```

Given the template context

```python
{
    "username": "John"
}
```

The placeholder becomes

```
Welcome John
```

---

## Testing

Run the test suite.

```bash
pytest
```

---

## License

MIT License