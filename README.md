# result.py

A Python implementation inspired by Rust's `Result<T, E>`, representing
operations that can either succeed (`Ok`) or fail (`Err`).

## Installation

```bash
$ pip install pytresult
```

## Key Features

- Typed

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

## Patterns

### `if let Ok(...) { }`

- Rust

  ```rust
  fn divide(a: i32, b: i32) -> Result<f32, String> {
      if b == 0 {
          Err("division by zero".to_string())
      } else {
          Ok(a as f32 / b as f32)
      }
  }

  let result = divide(10, 2);

  if let Ok(value) = result {
      println!("Success: {}", value);
  }
  ```

- Python

  ```python
  from result import Result, Ok, Err

  def divide(a: int, b: int) -> Result[int, str]:
      if b == 0:
          return Err("division by zero")
      return Ok(a // b)

  result = divide(10, 2)

  if r := result.ok():
      assert r is not None
      assert r == 5
  ```

### `if let Err(...) { }`

- Rust

  ```rust
  fn divide(a: i32, b: i32) -> Result<f32, String> {
      if b == 0 {
          Err("division by zero".to_string())
      } else {
          Ok(a as f32 / b as f32)
      }
  }

  let result = divide(10, 0);

  if let Err(error) = result {
      println!("Error: {}", error);
  }
  ```

- Python

  ```python
  from result import Result, Ok, Err

  def divide(a: int, b: int) -> Result[int, str]:
      if b == 0:
          return Err("division by zero")
      return Ok(a // b)

  result = divide(10, 0)

  if e := result.err():
      assert e is not None
      assert e == "division by zero"
  ```

## Testing

Tests are written using pytest.

To run the tests:

```bash
poetry run pytest
```
