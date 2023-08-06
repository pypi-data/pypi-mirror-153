"""Behavior, Query, and State
=============================

The decision and control part is structured as a directed, possibly
cyclic graph. The following describes `Behavior`, `Query`, and `State`
(BQS) classes. TL;DR: transfer between states of FSM is done by BT.

`Behavior` nodes correspond to *control flow* nodes of Behavior Tree
(BT). `Query` nodes correspond to *condition* nodes of BT. `State` nodes
correspond to root of BT, *action* nodes of BT, as well as states of
Finite State Machine (FSM). BQS differences to BT and FSM are discussed
bellow.

`Behavior` nodes are non-leafy nodes with the member `children`, which
is a list of other BQS nodes. The `children` nodes are processed in an
order corresponding to the behavior of the node subclass. The return
value of the `decide()` method is also specific to the node subclass.

Examples of `Behavior` nodes are `Sequence`, `Fallback`, and `Not`.

`Query` nodes are leaf nodes that query the `world` in read-only
fashion. The decision process cannot stop at the `Query` node.

Examples of `Query` nodes are `AlwaysTrue` and `AlwaysFalse`.

`State` nodes are leaf nodes where the decision process begins and ends.
Every `State` node is the root of BT and must have had some `Behavior`
node assigned to the ``change_state`` member.

`Behavior` and `Query` nodes must implement ``_decide()`` method.

`State` nodes are expected to implement ``_control()`` method.


Inheritance diagram
-------------------

.. inheritance-diagram:: pdc.bqs


Comparison to FSM
-----------------

Compared to FSM, BQS has framework for transition between states.
``change_state`` is the root of the BT, the destination states are
`State` leaves of that BT.


Comparison to BT
----------------

BQS can simulate BT when only one behavior is specified and assigned to
``change_state`` member of every `State`.

Each call to `decide()` always returns some object or ``False``. The
*running* state known from BT is not possible because BT is only used to
change between (FSM) states. (To change between BT actions.)


World
-----

Each BQS node has `world` member. `World` is shared between BQS nodes
and contain the perceived information, the history, and the status (of
the world).

It is possible to define multiple worlds and then assign different BQS
nodes to different worlds. To share information between worlds, the
`State` nodes of the first world can implement method that updates the
second world, i.e., the ``_control(world)`` method.


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


class World:
    """History and status of the world."""
    def __init__(self, history_len=2):
        self.history = [{} for i in range(history_len)]
        self.status = {
            "deciding": False,
            "last_state": None,
            "read_world": 0,
            "write_world": 0}

    def cs(self):
        """Return current (last set) `State`."""
        return self.status["last_state"]

    def cw(self, element=None):
        """Return (element of) current (last update of) world."""
        try:
            return self.history[self.status["read_world"]][element]
        except KeyError:
            return self.history[self.status["read_world"]]

    def include(self, *nodes):
        """Include BQS nodes into the self (world).

        :param nodes: Subclasses of BQS `Node`.
        """
        for n in nodes:
            assert isinstance(n, Node)
            n.world = self

    def _increase_write_world_index(self):
        """Begin addition of new world. Must be atomic."""
        assert self.status["read_world"] == self.status["write_world"]
        self.status["write_world"] += 1
        self.status["write_world"] %= len(self.history)

    def append_blank_world(self):
        """Add new blank world into the history. Must be atomic."""
        self._increase_write_world_index()
        self.history[self.status["write_world"]] = {}

    def append_copied_world(self):
        """Add copy of the last world into the history. Must be atomic."""
        self._increase_write_world_index()
        self.history[self.status["write_world"]] = dict(
            self.history[self.status["read_world"]])

    def append_new_world(self, **kwargs):
        """Add new world from keywords. Must be atomic."""
        self.append_blank_world()
        for k in kwargs:
            self.history[self.status["write_world"]][k] = kwargs[k]

    def world_added(self):
        """New world has been added, mark for read. Must be atomic."""
        assert self.status["read_world"] != self.status["write_world"]
        self.status["read_world"] = self.status["write_world"]


class Node:
    """Base node of BQS graph."""
    def decide(self, *args, **kwargs):
        """Make a decision, return obj or False. Calls `_decide()`."""
        print(self.__class__.__name__)
        ret = self._decide(*args, **kwargs)
        print("{} returns {}".format(self.__class__.__name__, ret))
        return ret

    def _decide(self):
        """Abstract. To be implemented by *Decision* subclasses."""
        raise NotImplementedError("Only for Decision nodes.")

    def control(self, *args, **kwargs):
        """Run a controller. Calls `_control()`."""
        print(self.__class__.__name__)
        ret = self._control(*args, **kwargs)
        print("{} returns {}".format(self.__class__.__name__, ret))
        return ret

    def _control(self):
        """Abstract. To be implemented by *Control* subclasses."""
        raise NotImplementedError("Only for Control nodes.")

    world = World()
    """Shared history of the world."""


class Behavior(Node):
    """Non-leaf decision node of BQS graph.

    No query to `world`. Just tick children.

    Subclasses must implement ``_decide()`` method.
    """
    def __init__(self, *children):
        for c in children:
            assert isinstance(c, Node)
        self.children = children
        """A list of `Node` instances to be evaluated."""


class Query(Node):
    """Read-only query to `world`.

    Leaf node of BQS, but can't end deciding here.

    Subclasses must implement ``_decide()`` method.
    """
    pass


class State(Node):
    """Leaf node where decision process begins and ends.

    Read-only query to `world`.

    Subclasses must have a `Behavior` assigned to ``change_state``
    member.

    Subclasses must implement ``_control()`` method.
    """
    def set_begin(self):
        """Set self as the beginning state."""
        self.world.status["last_state"] = self

    def _decide(self):
        """Transfer between states.

        Needs `Behavior` assigned to the ``change_state``. Return ``True`` if
        the `State` of the `world` has been changed and ``False`` otherwise.
        """
        if self.world.status["deciding"]:
            self.world.status["deciding"] = False
            self.world.status["last_state"] = self
        else:
            self.world.status["deciding"] = True
            self.change_state.decide()
            self.world.status["deciding"] = False
        return self.world.status["last_state"] is not self


# Behavior classes
class Sequence(Behavior):
    """-> in BT."""
    def _decide(self):
        """Return the last child's return if all children succeed or False."""
        ret = True
        ch = 0
        while (self.world.status["deciding"]
                and ch < len(self.children)
                and ret):
            ret = self.children[ch].decide()
            ch += 1
        return ret


class Fallback(Behavior):
    """? in BT."""
    def _decide(self):
        """Return the first successfull child's return or ``False``."""
        ret = False
        ch = 0
        while (self.world.status["deciding"]
                and ch < len(self.children)
                and not ret):
            ret = self.children[ch].decide()
            ch += 1
        return ret


class Not(Behavior):
    """Negation. For one child only."""
    def _decide(self):
        """Return negation of the first child."""
        return not self.children[0].decide()


# Query classes
class AlwaysTrue(Query):
    """Always return ``True``."""
    def _decide(self):
        """Return ``True``."""
        return True


class AlwaysFalse(Query):
    """Always return ``False``."""
    def _decide(self):
        """Return ``False``."""
        return False
