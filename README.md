# result.py

A Python implementation inspired by Rust's `Result<T, E>`, representing
operations that can either succeed (`Ok`) or fail (`Err`).

## Installation

```bash
$ poetry add "git+https://github.com/HicaroD/result.py"
```

## Motivation

Using Result helps avoid excessive exception handling and promotes more
explicit and robust error handling.

## Usage Example

```python
from result import Result, Ok, Err

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

result = divide(10, 2)

if result.is_ok():
    print("Success:", result.unwrap())
else:
    print("Error:", result)  # or result.unwrap_or(0)
```

## Testing

Tests are written using pytest.

To run the tests:

```bash
poetry run pytest
```
