"""The frontier: the set of nodes search knows about but has not opened yet.

**You implement two methods in this file**, `StackFrontier.choose` and
`QueueFrontier.choose`. Each one is a single line.

Everything else here is bookkeeping and is provided. Read `Frontier` before
you write anything, because it shows you exactly how little is left for the
subclasses to decide.
"""

from typing import Any


class FrontierError(Exception):
    """Raised when a frontier is asked to do something it cannot."""


class EmptyFrontierError(FrontierError):
    """Raised when search asks an empty frontier for a node.

    Search reaching this means every reachable state has been explored and
    none of them was a goal, so the problem has no solution.
    """


class Node:
    """One state, plus how search got to it.

    The `parent` link is what makes a path recoverable at the end. Without
    it search could tell you that a goal is reachable and not one thing
    about how to reach it.
    """

    def __init__(
        self, state: Any, parent: "Node | None", action: str | None
    ) -> None:
        """Record a state and the step that produced it.

        Args:
            state: The state this node stands for.
            parent: The node search expanded to reach this one, or None for
                the starting node.
            action: The action taken from the parent, or None for the
                starting node.
        """
        self.state = state
        self.parent = parent
        self.action = action


class Frontier:
    """Base class holding every part of a frontier that does not vary.

    Adding, membership testing, and emptiness are identical for every
    uninformed search. The subclasses below differ in `choose` and in
    nothing else, which is the point this file exists to make.

    Membership is tracked in a set as well as the list. Scanning the list
    for a state would be correct but linear, and search asks that question
    once per neighbor of every node it expands.
    """

    def __init__(self) -> None:
        """Start with an empty frontier."""
        self.nodes: list[Node] = []
        self._states: set[Any] = set()

    def add(self, node: Node) -> None:
        """Put a node into the frontier.

        Args:
            node: The node to add.
        """
        self.nodes.append(node)
        self._states.add(node.state)

    def contains_state(self, state: Any) -> bool:
        """Return whether some node in the frontier holds this state.

        Args:
            state: The state to look for.

        Returns:
            True if a node with that state is waiting in the frontier.
        """
        return state in self._states

    def empty(self) -> bool:
        """Return whether the frontier holds no nodes."""
        return not self.nodes

    def __len__(self) -> int:
        """Return how many nodes are waiting in the frontier."""
        return len(self.nodes)

    def remove(self) -> Node:
        """Take the next node out of the frontier and return it.

        Provided, and the same for every subclass. It handles the error
        case and the membership set, then delegates the only interesting
        decision to `choose`.

        Returns:
            The node `choose` selected, no longer in the frontier.

        Raises:
            EmptyFrontierError: If the frontier is empty.
        """
        if self.empty():
            raise EmptyFrontierError("the frontier is empty")
        waiting = len(self.nodes)
        node = self.choose()
        if len(self.nodes) != waiting - 1:
            # Guard against the most common way to get `choose` wrong:
            # reading a node without taking it out. Search would then loop
            # on it forever, so failing loudly here beats hanging.
            raise FrontierError(
                "choose returned a node without removing it from "
                "self.nodes, so the frontier never shrinks"
            )
        self._states.discard(node.state)
        return node

    def choose(self) -> Node:
        """Pick the next node and remove it from `self.nodes`.

        This is the method that makes a frontier a stack or a queue.

        Returns:
            The chosen node, which must already have been removed from
            `self.nodes` by the time it is returned.

        Raises:
            NotImplementedError: Always. Subclasses override this.
        """
        raise NotImplementedError("subclasses decide which node comes out")


class StackFrontier(Frontier):
    """Last in, first out. Using this makes `search` depth first."""

    def choose(self) -> Node:
        """Return the most recently added node, removing it.

        Returns:
            The node this frontier says comes out next, already removed
            from `self.nodes`.
        """
        # TODO: one line. Which end of self.nodes does a stack take from?
        raise NotImplementedError(
            "you have to implement StackFrontier.choose first"
        )


class QueueFrontier(Frontier):
    """First in, first out. Using this makes `search` breadth first."""

    def choose(self) -> Node:
        """Return the earliest added node, removing it.

        Returns:
            The node this frontier says comes out next, already removed
            from `self.nodes`.
        """
        # TODO: one line, and only one character different from the other.
        raise NotImplementedError(
            "you have to implement QueueFrontier.choose first"
        )
