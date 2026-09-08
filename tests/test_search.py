"""Checks for Challenge 2.

Readable on purpose. If a check fails, read the test: it says in words what
your code was supposed to do.

Most of these run on `LECTURE_GRAPH`, which is the eight node graph from the
Week 3 Tuesday activity. You traced it by hand in class, so if a test fails
you already know what the right answer looks like.
"""

from typing import Any

import pytest

from degrees import MovieGraph
from frontier import (
    EmptyFrontierError,
    Node,
    QueueFrontier,
    StackFrontier,
)
from search import search

# The Week 3 activity graph. S connects to A and B; A reaches the goal G in
# one step; B leads the long way round through C, D and E, and also to the
# dead end F.
LECTURE_GRAPH = {
    "S": ["A", "B"],
    "A": ["G", "S"],
    "B": ["C", "F", "S"],
    "C": ["B", "D"],
    "D": ["C", "E"],
    "E": ["D", "G"],
    "F": ["B"],
    "G": ["A", "E"],
}


class SimpleGraph:
    """A hand written graph, so the tests do not need the CSV files."""

    def __init__(
        self, edges: dict[str, list[str]], start: str, goal: str
    ) -> None:
        """Wrap an adjacency table as a search problem.

        Args:
            edges: Neighbors of each node, in the order they are generated.
            start: The node to search from.
            goal: The node to search for.
        """
        self.edges = edges
        self.start = start
        self.goal = goal

    def initial_state(self) -> str:
        """Return the starting node."""
        return self.start

    def actions(self, state: str) -> list[tuple[str, str]]:
        """Return the neighbors of a node, each with a step label."""
        return [(f"{state}->{n}", n) for n in self.edges[state]]

    def is_goal(self, state: str) -> bool:
        """Return whether this node is the goal."""
        return state == self.goal


def lecture(start: str = "S", goal: str = "G") -> SimpleGraph:
    """Build the Week 3 activity graph.

    Args:
        start: The node to search from.
        goal: The node to search for.

    Returns:
        The graph as a search problem.
    """
    return SimpleGraph(LECTURE_GRAPH, start, goal)


def nodes(*states: str) -> list[Node]:
    """Build parentless nodes for the frontier tests.

    Args:
        *states: The states to wrap, in order.

    Returns:
        One node per state.
    """
    return [Node(state, None, None) for state in states]


# --- The frontiers -----------------------------------------------------


def test_stack_returns_the_most_recent_node() -> None:
    """A stack is last in, first out."""
    frontier = StackFrontier()
    for node in nodes("a", "b", "c"):
        frontier.add(node)
    assert [frontier.remove().state for _ in range(3)] == ["c", "b", "a"]


def test_queue_returns_the_oldest_node() -> None:
    """A queue is first in, first out."""
    frontier = QueueFrontier()
    for node in nodes("a", "b", "c"):
        frontier.add(node)
    assert [frontier.remove().state for _ in range(3)] == ["a", "b", "c"]


def test_choose_actually_removes_the_node() -> None:
    """`choose` has to shrink the frontier, not just look at it.

    Reading a node without taking it out is the one wrong answer that would
    otherwise make search loop on the same node forever, so the base class
    raises instead of letting it hang.
    """
    for frontier in (StackFrontier(), QueueFrontier()):
        for node in nodes("a", "b"):
            frontier.add(node)
        frontier.remove()
        assert len(frontier) == 1, f"{type(frontier).__name__} did not shrink"


def test_draining_a_frontier_leaves_it_empty() -> None:
    """Removing every node empties the frontier, and then removing raises.

    The raise on its own would pass without `choose` being written at all,
    since the base class checks for emptiness before it delegates. Draining
    the frontier first is what makes this a check on your code.
    """
    for frontier in (StackFrontier(), QueueFrontier()):
        for node in nodes("a", "b", "c"):
            frontier.add(node)
        for _ in range(3):
            frontier.remove()
        assert frontier.empty(), "removing every node did not empty it"
        with pytest.raises(EmptyFrontierError):
            frontier.remove()


# --- The search loop ---------------------------------------------------


def test_search_finds_the_goal() -> None:
    """Search gets from S to G on the lecture graph."""
    result = search(lecture(), QueueFrontier())
    assert result.solved
    assert result.states[0] == "S"
    assert result.states[-1] == "G"


def test_the_path_is_a_real_walk() -> None:
    """Every consecutive pair on the path is one legal step apart."""
    graph = lecture()
    result = search(graph, StackFrontier())
    for before, after in zip(result.states, result.states[1:]):
        reachable = [state for _, state in graph.actions(before)]
        assert after in reachable, f"{before} to {after} is not one step"


def test_actions_line_up_with_states() -> None:
    """There is exactly one action between each pair of states."""
    result = search(lecture(), QueueFrontier())
    assert len(result.actions) == len(result.states) - 1


def test_breadth_first_finds_the_shortest_path() -> None:
    """Two steps, S to A to G. This is the number you got in class."""
    result = search(lecture(), QueueFrontier())
    assert result.path_length == 2
    assert result.states == ["S", "A", "G"]


def test_depth_first_finds_the_long_way_round() -> None:
    """Five steps, the long way, exactly as traced in class.

    If this fails saying the path is 2 steps, your two frontier classes are
    behaving identically.
    """
    result = search(lecture(), StackFrontier())
    assert result.solved
    assert result.path_length == 5
    assert result.states == ["S", "B", "C", "D", "E", "G"]


def test_expansion_counts_match_the_hand_trace() -> None:
    """Four expansions breadth first, seven depth first.

    Depth first expands more here because it walks into the dead end F.
    """
    assert search(lecture(), QueueFrontier()).nodes_expanded == 4
    assert search(lecture(), StackFrontier()).nodes_expanded == 7


def test_no_state_is_expanded_twice() -> None:
    """Expansions never exceed the number of nodes there are to expand."""
    for frontier in (QueueFrontier(), StackFrontier()):
        result = search(lecture(), frontier)
        assert result.nodes_expanded <= len(LECTURE_GRAPH)


def test_max_frontier_is_tracked() -> None:
    """The peak frontier is recorded and is a plausible size."""
    result = search(lecture(), QueueFrontier())
    assert 1 <= result.max_frontier <= len(LECTURE_GRAPH)


def test_unreachable_goal_is_reported_not_crashed_on() -> None:
    """A goal in another component is reported, not raised over."""
    edges: dict[str, list[str]] = dict(LECTURE_GRAPH)
    edges["Z"] = []
    result = search(SimpleGraph(edges, "S", "Z"), QueueFrontier())
    assert not result.solved
    assert result.states == []
    assert result.nodes_expanded > 0


def test_start_that_is_already_the_goal() -> None:
    """Searching from a node to itself is zero steps, not a crash."""
    result = search(lecture("S", "S"), QueueFrontier())
    assert result.solved
    assert result.path_length == 0
    assert result.states == ["S"]


# --- On the real data --------------------------------------------------


def test_runs_on_the_real_dataset() -> None:
    """Breadth first search finds the known short chain in data/small."""
    graph = MovieGraph("data/small", "Kevin Bacon", "Tom Cruise")
    result = search(graph, QueueFrontier())
    assert result.solved
    assert result.path_length == 1
    assert graph.name_of(result.states[0]) == "Kevin Bacon"
    assert graph.name_of(result.states[-1]) == "Tom Cruise"


def test_breadth_first_beats_depth_first_on_real_data() -> None:
    """On the medium set the two searches disagree, and by a lot.

    Breadth first finds a chain of two films. Depth first finds one that is
    very much longer. Both are real chains, which is the point.
    """
    short = search(
        MovieGraph("data/medium", "Kevin Bacon", "Emma Watson"),
        QueueFrontier(),
    )
    long = search(
        MovieGraph("data/medium", "Kevin Bacon", "Emma Watson"),
        StackFrontier(),
    )
    assert short.path_length == 2
    assert long.path_length > 10


def test_search_does_not_care_what_it_is_searching() -> None:
    """The same call works on a hand written graph and on the movie graph.

    Nothing in `search` should mention actors, films, or strings. If this
    fails you have written the movie graph into the search loop.
    """
    results: list[Any] = [
        search(lecture(), QueueFrontier()),
        search(
            MovieGraph("data/small", "Kevin Bacon", "Tom Cruise"),
            QueueFrontier(),
        ),
    ]
    assert all(r.solved for r in results)
