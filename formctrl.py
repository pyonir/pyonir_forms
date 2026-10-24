from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from html import escape
from typing import Any

logger = logging.getLogger(__name__)

HTML_FORM_ATTRIBUTES = {
    "action",
    "method",
    "enctype",
    "accept-charset",
    "autocomplete",
    "name",
    "novalidate",
    "target",
    "rel",
}

HTML_BOOLEAN_ATTRIBUTES = {
    "required",
    "disabled",
    "checked",
    "readonly",
    "hidden",
    "multiple",
    "async",
    "defer",
}


@dataclass
class FormCtrl:
    label: str
    props: dict[str, Any] = field(default_factory=dict)
    inputs: list[FormCtrl] = field(default_factory=list)
    html: str = ""
    description: str | None = None

    @property
    def is_required(self) -> bool:
        return self.props.get('required', False)

    @property
    def is_disabled(self) -> bool:
        return self.props.get('disabled', False)

    @property
    def input_props(self) -> str:
        """
        Generate HTML attributes for this form control.

        Boolean HTML attributes (e.g. 'required', 'checked') are rendered
        without a value, while all other attributes are HTML-escaped and
        rendered as key="value" pairs.

        Returns:
            A space-separated string of HTML attributes suitable for
            inserting directly into an HTML element.
        """

        parts = []

        for key, value in self.props.items():
            if key in HTML_BOOLEAN_ATTRIBUTES:
                if value:
                    parts.append(key)
            elif value is not None:
                parts.append(
                    f'{key}="{escape(str(value), quote=True)}"'
                )

        return " ".join(parts)

@dataclass
class Form:
    props: dict = field(default_factory=dict)
    inputs: list[FormCtrl] = field(default_factory=list)
    js: str = ""
    button: FormCtrl | None = None


def process_value(value: Any, context: dict | None = None) -> Any:
    """
    Resolve Python template placeholders within a string value.

    String values containing format placeholders (e.g. "{username}")
    are formatted using the global template context merged with the
    optional context provided by the caller. Non-string values are
    returned unchanged.

    Args:
        value: The value to process.
        context: Optional template variables that override the global context.

    Returns:
        The formatted value if successful; otherwise the original value.
    """
    if not isinstance(value, str) or "{" not in value:
        return value

    from pyonir import Site

    merged = {
        **(Site.TemplateEnvironment.context if Site else {}),
        **(context or {}),
    }

    try:
        return value.format(**merged)
    except Exception:
        logger.exception("Unable to format '%s'", value)
        return value


def slugify(value: str) -> str:
    """
    Convert a string into a valid HTML identifier.

    The resulting string is normalized by converting to lowercase,
    replacing non-alphanumeric characters with underscores, collapsing
    consecutive underscores, and trimming leading/trailing underscores.

    Args:
        value: The string to normalize.

    Returns:
        A slug suitable for use as an HTML id or name attribute.
    """
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_").lower()


def form_ctrl(
    data: FormCtrl | dict | str,
    parent_label: str | None = None,
    template_context: dict | None = None,
    prop_names: set[str] | None = None
) -> FormCtrl:
    """
    Create a FormCtrl instance from a form definition.

    Accepts an existing FormCtrl, a dictionary describing a form control,
    or a string representing the control label. Child controls are
    processed recursively, template values are resolved, and default
    HTML id/name attributes are generated when not explicitly provided.

    Args:
        data: A FormCtrl, control definition dictionary, or label string.
        parent_label: Parent control label used when deriving nested
            control names and ids.
        template_context: Optional values used to resolve template
            placeholders within control properties.

    Returns:
        A fully initialized FormCtrl instance.
    """
    if isinstance(data, FormCtrl):
        return data

    if isinstance(data, str):
        data = {"label": data}

    label = data.get("label", "")
    html = data.get("html", "") # custom html markup of control input
    input_type = data.get("type", "text")

    props = {
        "type": input_type,
    }

    children: list[FormCtrl] = [
        form_ctrl(
            child,
            parent_label=label,
            template_context=template_context,
        )
        for child in data.pop('inputs',[])
    ]

    for key, value in data.items():
        if (prop_names and key not in prop_names) or key in ("label", "html", "description"):
            continue

        if key in HTML_BOOLEAN_ATTRIBUTES:
            props[key] = bool(value)
            continue

        props[key] = process_value(value, template_context)

    derived = slugify(
        f"{parent_label}_{label}" if parent_label else label
    )
    if derived:
        props.setdefault("name", derived)
        props.setdefault("id", derived)

    return FormCtrl(
        label=label,
        props=props,
        inputs=children,
        html=html,
        description=data.get("description"),
    )

def form(data: dict) -> Form:
    js = data.pop('js','')
    button = data.pop('button', {})
    if button:
        button = form_ctrl(button)
    prop_ctrl = form_ctrl(data, prop_names=HTML_FORM_ATTRIBUTES)
    return Form(props=prop_ctrl.props, inputs=prop_ctrl.inputs, button=button, js=js)