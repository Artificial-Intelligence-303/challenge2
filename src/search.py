"""One search function, and the numbers it reports about its own work.

**You implement `search` in this file.** It is the only search algorithm you
will write for this challenge. Which algorithm it turns out to be is decided
by the frontier you hand it, not by anything you write here.
"""

from dataclasses import dataclass, field
from typing import Any

from frontier import Frontier, Node
from problems import Problem


@dataclass
class SearchResult:
    """What one run of `search` found, and what it cost to find it.

    Attributes:
        states: The states along the solution, starting at the initial
            state and ending at the goal. Empty if there is no solution.
        actions: The action names along that solution, one shorter than
            `states`. Empty if there is no solution.
        nodes_expanded: How many nodes were taken off the frontier and had
            their neighbors generated. This is the course's measure of how
            much work a search did, and it is what you report.
        max_frontier: The largest the frontier ever got during the run.
            This is the memory measure, and it is where breadth first
            search and depth first search differ most sharply.
        solved: Whether a goal was reached at all.
    """

    states: list[Any] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    nodes_expanded: int = 0
    max_frontier: int = 0
    solved: bool = False

    @property
    def path_length(self) -> int:
        """Return the number of steps in the solution.

        Returns:
            The count of actions, which is zero when unsolved.
        """
        return len(self.actions)


def reconstruct(node: Node) -> tuple[list[Any], list[str]]:
    """Walk parent links back to the start and return the path forwards.

    Provided, because this is bookkeeping rather than search.

    Args:
        node: The goal node search stopped on.

    Returns:
        A pair of the states from the initial state to the goal, and the
        actions taken between them.
    """
    states: list[Any] = []
    actions: list[str] = []
    while node.parent is not None:
        states.append(node.state)
        actions.append(node.action or "")
        node = node.parent
    states.append(node.state)
    states.reverse()
    actions.reverse()
    return states, actions


def search(problem: Problem, frontier: Frontier) -> SearchResult:
    """Search `problem` using `frontier`, and report what it cost.

    The algorithm is the same one every time. The frontier decides the
    order states come out, and that order is the entire difference between
    breadth first and depth first search.

    Two rules keep this from looping forever on a graph. A state that has
    already been expanded is never added again, and a state already waiting
    in the frontier is never added twice.

    Args:
        problem: Anything satisfying the `Problem` interface.
        frontier: An empty frontier. A `QueueFrontier` gives breadth first
            search and a `StackFrontier` gives depth first search.

    Returns:
        A `SearchResult`. When no goal is reachable, `solved` is False and
        the counts still describe the work the search did before giving up.
    """
    # TODO: write the search loop. The README has its shape, and the two
    # details worth getting right rather than guessing at.
    raise NotImplementedError("you have to implement search first")
