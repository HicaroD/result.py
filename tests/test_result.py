import pytest
from typing import Any
import threading
from dataclasses import FrozenInstanceError

from src.result import Result, Ok, Err


def test_ok_and_err_instantiation():
    result_ok = Ok(10)
    result_err = Err("error")

    assert isinstance(result_ok, Result)
    assert isinstance(result_err, Result)

    assert result_ok.is_ok()
    assert not result_ok.is_err()

    assert result_err.is_err()
    assert not result_err.is_ok()


def test_map_on_ok():
    result = Ok(2)
    mapped = result.map(lambda x: x * 10)

    assert isinstance(mapped, Ok)
    assert mapped.unwrap() == 20


def test_ok_method_on_ok():
    result = Ok(2)
    assert result.ok() == 2


def test_err_method_on_ok():
    result = Err(2)
    assert result.ok() == None


def test_ok_method_on_err():
    result = Ok(2)
    assert result.err() == None


def test_err_method_on_err():
    result = Err(2)
    assert result.err() == 2


def test_map_on_err():
    result: Result[int, str] = Err("some error")
    mapped = result.map(lambda x: x * 10)

    assert isinstance(mapped, Err)
    assert mapped.error == "some error"


def test_map_err_on_err():
    result = Err("fail")
    mapped = result.map_err(lambda e: f"{e.upper()}!")

    assert isinstance(mapped, Err)
    assert mapped.error == "FAIL!"


def test_map_err_on_ok():
    result = Ok(100)
    mapped = result.map_err(lambda e: "should not be called")

    assert isinstance(mapped, Ok)
    assert mapped.value == 100


def test_and_then_on_ok():
    def to_result(x: int) -> Result[str, str]:
        return Ok(str(x))

    result = Ok(42)
    chained = result.and_then(to_result)

    assert isinstance(chained, Ok)
    assert chained.value == "42"


def test_and_then_on_err():
    result: Result[int, str] = Err("error")
    chained = result.and_then(lambda x: Ok(x * 10))

    assert isinstance(chained, Err)
    assert chained.error == "error"


def test_unwrap_on_ok():
    result = Ok("success")
    assert result.unwrap() == "success"


def test_unwrap_on_err_raises():
    result: Result[Any, str] = Err("boom")

    with pytest.raises(Exception, match="Called unwrap on Err: boom"):
        result.unwrap()


def test_unwrap_or_on_ok():
    result = Ok(123)
    assert result.unwrap_or(0) == 123


def test_unwrap_or_on_err():
    result = Err("fail")
    assert result.unwrap_or(99) == 99


def test_repr():
    assert repr(Ok(1)) == "Ok(1)"
    assert repr(Err("error")) == "Err('error')"


def test_ok_equality():
    assert Ok(1) == Ok(1)
    assert Ok("abc") == Ok("abc")
    assert Ok(1) != Ok(2)
    assert Ok(1) != Err(1)


def test_err_equality():
    assert Err("x") == Err("x")
    assert Err("x") != Err("y")
    assert Err("x") != Ok("x")


def test_nested_result_handling():
    inner: Result[int, str] = Ok(123)
    outer: Result[Result[int, str], str] = Ok(inner)
    assert outer.unwrap() == Ok(123)


def test_map_is_noop_on_err():
    err = Err("error")
    called = False

    def callback(_):
        nonlocal called
        called = True

    result = err.map(callback)
    assert isinstance(result, Err)
    assert not called


def test_map_err_is_noop_on_ok():
    ok = Ok(42)
    called = False

    def callback(_):
        nonlocal called
        called = True

    result = ok.map_err(callback)
    assert isinstance(result, Ok)
    assert not called


def test_unwrap_or_handles_none_and_falsy_values():
    assert Ok(None).unwrap_or("default") is None  # type: ignore
    assert Ok(0).unwrap_or(999) == 0
    assert Err("fail").unwrap_or(123) == 123


def test_map_propagates_exception():
    def f(x):
        raise ValueError("error!")

    result = Ok(10)
    with pytest.raises(ValueError):
        result.map(f)


def test_map_err_propagates_exception():
    def f(e):
        raise KeyError("unexpected")

    result = Err("fail")
    with pytest.raises(KeyError):
        result.map_err(f)


def test_and_then_propagates_exception():
    def f(x):
        raise RuntimeError("broken")

    result = Ok(10)
    with pytest.raises(RuntimeError):
        result.and_then(f)


def test_thread_safe_read_access():
    ok = Ok(42)
    err = Err("fail")
    results = []

    def check():
        assert ok.is_ok()
        assert ok.unwrap() == 42
        assert err.is_err()
        assert err.unwrap_or("default") == "default"
        results.append(True)

    threads = [threading.Thread(target=check) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 50


def test_repr_ok_and_err():
    assert repr(Ok(123)) == "Ok(123)"
    assert repr(Err("fail")) == "Err('fail')"


def test_ok_is_immutable():
    ok = Ok(1)
    with pytest.raises(FrozenInstanceError):
        ok.value = 2  # type: ignore


def test_err_is_immutable():
    err = Err("fail")
    with pytest.raises(FrozenInstanceError):
        err.error = "other"  # type: ignore
