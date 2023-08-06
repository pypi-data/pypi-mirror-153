"""Part object."""
# Local Modules
from cofactr.kb.entity.types import DataValue, Mainsnak
from cofactr.helpers import identity, get_path

TYPE_TO_RENDERER = {
    "monolingual_text": lambda v: v["text"],
    "quantity": lambda v: v["amount"],
}


def datavalue_to_str(datavalue: DataValue) -> str:
    """Render data-value to string.

    Example in:
        ```
        {
            "value": "CC0603JRNPOABN100",
            "type": "string"
        }
        ```

    Example out:
        `"CC0603JRNPOABN100"`
    """
    renderer = TYPE_TO_RENDERER.get(datavalue["type"], identity)

    return str(renderer(datavalue["value"]))


def mainsnak_to_str(mainsnak: Mainsnak) -> str:
    """Render mainSNAK to string."""
    return datavalue_to_str(get_path(mainsnak, keys=["mainsnak", "datavalue"]))
