# Cofactr

Python client library for accessing Cofactr.

## Example

```python
from typing import List
from cofactr.graph import GraphAPI

# Flagship is the default schema.
from cofactr.schema.flagship.part import Part

graph = GraphAPI()

part_res = graph.get_product(id="IM60640MOX6H")
part: Part = part_res["data"]

parts_res = graph.get_products(query="esp32")
parts: List[Part] = parts_res["data"]
```
