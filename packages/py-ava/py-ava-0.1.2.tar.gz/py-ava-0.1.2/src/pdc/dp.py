"""Data Processing
==================

The processing of input data in the perception part is structured as a
directed acyclic graph. There may be multiple data source nodes, but
only one sink node. This approach allows parallel processing of data
from multiple sources. Intermediate nodes of the graph may use classes
defined in this module to process the data.


Inheritance diagram
-------------------

.. inheritance-diagram:: pdc.dp


Members
-------

"""
# License
# -------
#
# Copyright (c) 2022 Jiri Vlasak
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


def _get_float(w, i):
    if isinstance(w, list) or isinstance(w, tuple) or isinstance(w, dict):
        return float(w[i])
    else:
        return float(w)


class Filter:
    """Base class for the filters."""
    def update(self, curr):
        """Process curr, return processed.

        :param curr: Float or dict. Measured value.
        """
        print("{} filtering...".format(self.__class__.__name__))
        ret = self._update(curr)
        print("{} returns {}".format(self.__class__.__name__, ret))
        return ret

    def _update(self):
        """Abstract. To be implemented by `Filter` subclasses."""
        raise NotImplementedError("_update() is missing.")


class FiltersChain(Filter):
    """Chain multiple filters that are run in sequence.

    When any of the filters fails, the whole `FiltersChain` fails. To
    avoid problems of sharing filters between `FiltersChain` classes
    (it's Python) in `FiltersChain` constructor always call `Filter`
    constructor::

        FiltersChain(
            Filter(),
            Filter(),
            Filter())

    """
    def __init__(self, *filters):
        for f in filters:
            assert isinstance(f, Filter)
        self.filters = filters
        """A list of filters to be applied."""

    def _update(self, curr):
        """Run multiple filters on curr, stop if any of the filters fails."""
        for f in self.filters:
            curr = f.update(curr)
            if not curr:
                return curr
        return curr


class LowPassFilter(Filter):
    """See https://en.wikipedia.org/wiki/Low-pass_filter"""
    def __init__(self, weight=0.5, keys=[]):
        """Create new `LowPassFilter` object.

        :param weight: Float or list or dict of weights.
        :param keys: The list of keys if dict is provided to `_update()`.
        """
        self.last = None
        self.keys = keys
        if len(self.keys) > 0:
            self.weight = {}
            i = 0
            for k in self.keys:
                self.weight[k] = _get_float(weight, i)
                i += 1
        else:
            self.weight = _get_float(weight, None)

    def _update(self, curr):
        """Compute value of curr in Low-Pass filter fashion."""
        def f(c, w, la):
            return w * c + (1.0 - w) * la
        if self.last is None:
            self.last = curr
        elif isinstance(curr, dict):
            for k in curr:
                if k in self.keys:
                    self.last[k] = f(curr[k], self.weight[k], self.last[k])
                else:
                    self.last[k] = curr[k]
        else:
            self.last = f(curr, self.weight, self.last)
        return self.last


class AlphaBetaFilter(Filter):
    """See https://en.wikipedia.org/wiki/Alpha_beta_filter"""
    def __init__(self, a=0.85, b=0.005, x=None, v=None, dt=0.1, keys=[]):
        """Create new `AlphaBetaFilter` object.

        :param a: Float or list or dict of alpha weights.
        :param b: Float or list or dict of beta weights.
        :param x: Float or list or dict of x starting values.
        :param v: Float or list or dict of v starting values.
        :param dt: Time step of the filter.
        :param keys: The list of keys if dict is provided to `_update()`.
        """
        self.dt = float(dt)
        self.keys = keys
        if len(self.keys) > 0:
            self.alpha = {}
            self.beta = {}
            self.x = None if x is None else {}
            self.v = None if v is None else {}
            i = 0
            for k in self.keys:
                self.alpha[k] = _get_float(a, i)
                self.beta[k] = _get_float(b, i)
                if x is not None:
                    self.x[k] = _get_float(x, i)
                if v is not None:
                    self.v[k] = _get_float(v, i)
                i += 1
        else:
            self.alpha = float(a)
            self.beta = float(b)
            self.x = None if x is None else float(x)
            self.v = None if v is None else float(v)

    def _update(self, curr):
        """Compute value of curr in AB filter fashion."""
        def f(c, a, b, x, v, dt):
            xk = x + (v * dt)
            vk = v
            rk = c - xk

            xk += a * rk
            vk += (b * rk) / dt
            return xk, vk
        if self.x is None:
            self.x = curr
        elif isinstance(curr, dict):
            if self.v is None:
                self.v = {}
                for k in self.keys:
                    self.v[k] = (curr[k] - self.x[k]) / self.dt
            for k in curr:
                if k in self.keys:
                    self.x[k], self.v[k] = f(
                        curr[k],
                        self.alpha[k],
                        self.beta[k],
                        self.x[k],
                        self.v[k],
                        self.dt)
                else:
                    self.x[k] = curr[k]
        else:
            if self.v is None:
                self.v = (curr - self.x) / self.dt
            self.x, self.v = f(
                curr, self.alpha, self.beta, self.x, self.v, self.dt)
        return self.x, self.v
