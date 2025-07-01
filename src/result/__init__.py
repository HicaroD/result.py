from typing import Callable, Generic, TypeVar
import dataclasses

T = TypeVar("T")  # Success type
E = TypeVar("E")  # Error type
U = TypeVar("U")  # Output type for map
F = TypeVar("F")  # Output type for map_err


class Result(Generic[T, E]):
    """
    A Result type inspired by Rust's std::result::Result.

    Represents either a success (`Ok`) or a failure (`Err`).
    """

    def is_ok(self) -> bool:
        """Return True if the result is Ok."""
        return isinstance(self, Ok)

    def is_err(self) -> bool:
        """Return True if the result is Err."""
        return isinstance(self, Err)

    def map(self, f: Callable[[T], U]) -> "Result[U, E]":
        """
        Apply a function to the value inside Ok.

        Args:
            f: A function to apply to the Ok value.

        Returns:
            Ok(f(value)) if Ok, else self as Err.
        """
        if self.is_ok():
            # Here, self is guaranteed to be an Ok. We can use a cast or, in a
            # more robust way, delegate access to the method of the subclass. A
            # more pythonic way (and that already works with its is_ok()) is to
            # use isinstance and then access directly.
            return Ok(f(self.value))  # type: ignore
        return self  # type: ignore

    def map_err(self, f: Callable[[E], F]) -> "Result[T, F]":
        """
        Apply a function to the error inside Err.

        Args:
            f: A function to apply to the Err value.

        Returns:
            Err(f(error)) if Err, else self as Ok.
        """
        if self.is_err():
            # Similarly, here self is guaranteed to be an Err.
            return Err(f(self.error))  # type: ignore
        return self  # type: ignore

    def and_then(self, f: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """
        Chain another operation that returns a Result.

        Args:
            f: A function that returns Result.

        Returns:
            The result of f if Ok, else self as Err.
        """
        if self.is_ok():
            return f(self.value)  # type: ignore
        return self  # type: ignore

    def unwrap(self) -> T:
        """
        Return the Ok value or raises Exception if Err.

        Raises:
            Exception: If result is Err.

        Returns:
            The value inside Ok.
        """
        if self.is_ok():
            return self.value  # type: ignore
        # When self.is_err() is True, self is guaranteed to be an Err,
        # so we can access self.error with type: ignore for MyPy or
        # cast if we prefer more explicit type.
        raise Exception(f"Called unwrap on Err: {self.error}")  # type: ignore

    def ok(self) -> T | None:
        """
        Return the Ok value or None if Err.

        Returns:
            The value inside Ok or None.
        """
        if self.is_ok():
            return self.value  # type: ignore
        return None

    def err(self) -> E | None:
        """
        Return the Err value or None if Ok.

        Returns:
            The error inside Err or None.
        """
        if self.is_err():
            return self.error  # type: ignore
        return None

    def unwrap_or(self, default: T) -> T:
        """
        Return the Ok value or a default if Err.

        Args:
            default: The fallback value.

        Returns:
            The value inside Ok or the default.
        """
        if self.is_ok():
            return self.value  # type: ignore
        return default


@dataclasses.dataclass(frozen=True)
class Ok(Result[T, E]):
    """Represent a success."""

    value: T

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"


@dataclasses.dataclass(frozen=True)
class Err(Result[T, E]):
    """Represent an error."""

    error: E

    def __repr__(self) -> str:
        return f"Err({self.error!r})"
