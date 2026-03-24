"""Load and resolve templates from templates.yaml with deep merge + extends."""

from pathlib import Path
import yaml

_TEMPLATES_FILE = Path(__file__).parent / "templates.yaml"


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base. Lists are replaced, not appended."""
    result = {}
    for k in set(list(base.keys()) + list(override.keys())):
        if k in override and k in base:
            if isinstance(base[k], dict) and isinstance(override[k], dict):
                result[k] = deep_merge(base[k], override[k])
            else:
                result[k] = override[k]
        elif k in override:
            result[k] = override[k]
        else:
            result[k] = base[k]
    return result


def _resolve(name: str, templates: dict, seen: set) -> dict:
    """Resolve a template by name, handling extends chains."""
    if name in seen:
        raise ValueError(f"순환 참조: {' -> '.join(seen)} -> {name}")
    if name not in templates:
        available = ", ".join(templates.keys())
        raise KeyError(f"'{name}' 템플릿을 찾을 수 없습니다. 사용 가능: {available}")

    seen = seen | {name}
    tmpl = templates[name]

    if "extends" in tmpl:
        parent = _resolve(tmpl["extends"], templates, seen)
        child = {k: v for k, v in tmpl.items() if k != "extends"}
        return deep_merge(parent, child)
    return dict(tmpl)


def load_template(name: str = "default") -> dict:
    """Load a named template from templates.yaml, resolving extends."""
    with open(_TEMPLATES_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    templates = data.get("templates", {})
    return _resolve(name, templates, set())
