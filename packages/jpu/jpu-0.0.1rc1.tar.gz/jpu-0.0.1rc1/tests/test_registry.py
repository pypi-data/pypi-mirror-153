# mypy: ignore-errors

import jax
import jax.numpy as jnp
import numpy as np

from jpu.registry import UnitRegistry


def test_tree_flatten():
    u = UnitRegistry()
    x = jnp.array([1.4, 2.0, -5.9])
    q = x * u.m

    val, _ = jax.tree_flatten(q)
    assert len(val) == 1
    np.testing.assert_allclose(val[0], x)


def test_jittable():
    u = UnitRegistry()
    x = jnp.array([1.4, 2.0, -5.9])
    q = x * u.m

    @jax.jit
    def func(q):
        assert q.u == u.m
        return q + 4.5 * u.km

    res = func(q)
    assert res.units == u.m
    np.testing.assert_allclose(res.magnitude, x + 4500.0)


def test_ducktype():
    u = UnitRegistry()
    x = jnp.array([1.4, 2.0, -5.9])
    q = x * u.m

    res = q.sum()
    assert res.units == u.m
    np.testing.assert_allclose(res.magnitude, x.sum())

    @jax.jit
    def func(q):
        return q.sum()

    res = func(q)
    assert res.units == u.m
    np.testing.assert_allclose(res.magnitude, x.sum())


def test_unary_ops():
    u = UnitRegistry()

    x = jnp.array([1.4, 2.0, -5.9])
    q = x * u.m

    for func in [
        lambda q: q**2,
        lambda q: q.sum(),
        lambda q: 2 * q,
    ]:
        res = func(q)
        np.testing.assert_allclose(res.magnitude, func(x))
        res = jax.jit(func)(q)
        np.testing.assert_allclose(res.magnitude, func(x))
