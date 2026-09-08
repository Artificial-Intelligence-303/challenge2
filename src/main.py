"""Run the searches and print the numbers the reflection asks you for.

Provided. Start here once the two `choose` methods and `search` are written.

    uv run python src/main.py           the full run
    uv run python src/main.py small     the sixteen person set, for debugging
    uv run python src/main.py lecture   Tuesday's graph, one row per step
"""

import statistics
import sys
from typing import Any

from degrees import MovieGraph
from frontier import (
    Frontier,
    FrontierError,
    Node,
    QueueFrontier,
    StackFrontier,
)
from search import search

DATA = "data/medium"
SOURCE = "Kevin Bacon"
TARGET = "Emma Watson"


def show_connection(directory: str, source: str, target: str) -> None:
    """Run both searches between two people and print what each cost."""
    print(f"\nCONNECTING {source} to {target}\n")
    header = (
        f"{'frontier':<24}{'degrees':>9}{'expanded':>11}"
        f"{'peak frontier':>16}"
    )
    print(header)
    print("-" * len(header))

    results = {}
    for label, frontier in (
        ("queue (breadth first)", QueueFrontier()),
        ("stack (depth first)", StackFrontier()),
    ):
        graph = MovieGraph(directory, source, target)
        result = search(graph, frontier)
        results[label] = (graph, result)
        degrees = result.path_length if result.solved else -1
        print(
            f"{label:<24}{degrees:>9}{result.nodes_expanded:>11}"
            f"{result.max_frontier:>16}"
        )

    graph, result = results["queue (breadth first)"]
    if result.solved:
        print("\nThe shortest chain:")
        for i, film in enumerate(result.actions):
            first = graph.name_of(result.states[i])
            second = graph.name_of(result.states[i + 1])
            print(f"    {first} and {second} were both in {film}")


def show_scale(directory: str) -> None:
    """Print the size of the graph and the branching factor, b."""
    graph = MovieGraph(directory, SOURCE, SOURCE)
    degrees = [len(graph.co_stars(person)) for person in graph.people]
    print("\nTHE DATASET\n")
    print(f"    people                      {len(graph.people):>8,}")
    print(f"    films                       {len(graph.movies):>8,}")
    print(f"    branching factor b, mean    {statistics.mean(degrees):>8.1f}")
    print(f"    branching factor b, median  {statistics.median(degrees):>8.0f}")
    print(f"    most co-stars anyone has    {max(degrees):>8,}")


def show_reach(directory: str) -> None:
    """Print how far the graph reaches, beside what the bound predicts.

    Uses your `QueueFrontier`, so these numbers come out of your code.
    Breadth first order is what makes this table mean anything: a person
    comes out of the queue once, at their true distance from the source.
    """
    graph = MovieGraph(directory, SOURCE, SOURCE)
    source = graph.initial_state()
    frontier = QueueFrontier()
    frontier.add(Node(source, None, None))
    distance = {source: 0}
    reached: dict[int, int] = {}

    while not frontier.empty():
        node = frontier.remove()
        here = distance[node.state]
        reached[here] = reached.get(here, 0) + 1
        for person in sorted(graph.co_stars(node.state)):
            if person not in distance:
                distance[person] = here + 1
                frontier.add(Node(person, node, None))

    degrees = [len(graph.co_stars(p)) for p in graph.people]
    branching = statistics.mean(degrees)

    print(f"\nHOW FAR {SOURCE.upper()} REACHES\n")
    header = f"{'degrees away':>13}{'people':>10}{'running total':>16}"
    print(header + f"{'b^d predicts':>16}")
    print("-" * (len(header) + 16))
    total = 0
    for depth in sorted(reached):
        total += reached[depth]
        predicted = float(branching) ** depth
        print(
            f"{depth:>13}{reached[depth]:>10,}{total:>16,}"
            f"{predicted:>16,.0f}"
        )
    beyond = len(reached)
    predicted = float(branching) ** beyond
    print(f"{beyond:>13}{0:>10}{total:>16,}{predicted:>16,.0f}")
    print(
        f"\nNothing past {max(reached)}: the search has reached everyone by"
        f" then. The b^d\ncolumn keeps climbing anyway, and reflection"
        f" question 2 asks why.\n"
    )


# --- Tuesday's graph ----------------------------------------------------

# The Week 3 activity graph. S connects to A and B; A reaches the goal G in
# one step; B leads the long way round through C, D and E, and also to the
# dead end F. Neighbors are listed alphabetically, which is the rule the
# hand trace used.
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


class LectureGraph:
    """The eight node activity graph, as a search problem."""

    def __init__(self, start: str, goal: str) -> None:
        """Search between two nodes of the activity graph.

        Args:
            start: The node to search from.
            goal: The node to search for.
        """
        self.start = start
        self.goal = goal

    def initial_state(self) -> str:
        """Return the starting node."""
        return self.start

    def actions(self, state: str) -> list[tuple[str, str]]:
        """Return the neighbors of a node, each with a step label.

        Args:
            state: The node to expand.

        Returns:
            One pair per neighbor, in alphabetical order.
        """
        return [(f"{state}->{n}", n) for n in LECTURE_GRAPH[state]]

    def is_goal(self, state: str) -> bool:
        """Return whether this node is the goal.

        Args:
            state: The node to test.

        Returns:
            True if it is the node being searched for.
        """
        return state == self.goal


class TracingFrontier(Frontier):
    """Wraps one of your frontiers and records what it held at each step.

    `search` never looks at the whole frontier, so it cannot print one.
    This sits between the two and writes down what it sees. Every decision
    is still made by your `choose`: this class only watches.

    It subclasses `Frontier` so that `search` will accept it, but every
    method is overridden to defer to `inner`, and the storage it inherits
    goes unused.
    """

    LIMIT = 40

    def __init__(self, inner: Frontier) -> None:
        """Watch a frontier.

        Args:
            inner: The frontier doing the actual work.
        """
        super().__init__()
        self.inner = inner
        self.rows: list[list[str]] = []
        self._open: list[str] | None = None
        self._added: list[str] = []

    def add(self, node: Node) -> None:
        """Add a node, noting that it was added.

        Args:
            node: The node to add.
        """
        self.inner.add(node)
        self._added.append(str(node.state))

    def contains_state(self, state: Any) -> bool:
        """Return whether a state is waiting in the frontier.

        Args:
            state: The state to look for.

        Returns:
            Whatever the wrapped frontier says.
        """
        return self.inner.contains_state(state)

    def empty(self) -> bool:
        """Return whether the frontier holds no nodes."""
        return self.inner.empty()

    def __len__(self) -> int:
        """Return how many nodes are waiting."""
        return len(self.inner)

    def remove(self) -> Node:
        """Take the next node out, closing off the previous row first.

        Returns:
            Whatever the wrapped frontier chose.

        Raises:
            FrontierError: If the run is far longer than this graph allows.
        """
        if len(self.rows) >= self.LIMIT:
            raise FrontierError(
                f"more than {self.LIMIT} nodes came out of the frontier on an "
                "eight node graph, so states are being expanded twice"
            )
        self._close("")
        before = self._contents()
        node = self.inner.remove()
        self._open = [str(len(self.rows) + 1), before, str(node.state)]
        self._added = []
        return node

    def finish(self, solved: bool) -> list[list[str]]:
        """Close the final row and return every row.

        Args:
            solved: Whether the run ended by finding the goal.

        Returns:
            One row per removal: step, frontier before, node taken out,
            what that added, and the frontier after.
        """
        self._close("goal" if solved else "")
        return self.rows

    def choose(self) -> Node:
        """Never reached, because `remove` defers to the wrapped frontier.

        Returns:
            Nothing. It always raises.

        Raises:
            FrontierError: Always.
        """
        raise FrontierError("the wrapped frontier chooses, not this one")

    def _contents(self) -> str:
        """Return the frontier in order, oldest node first."""
        return "[" + ", ".join(str(n.state) for n in self.inner.nodes) + "]"

    def _close(self, adds: str) -> None:
        """Finish the row left open by the previous removal.

        Args:
            adds: Text for the adds column, or empty to use what was added.
        """
        if self._open is None:
            return
        adds = adds or ", ".join(self._added) or "nothing new"
        self.rows.append(self._open + [adds, self._contents()])
        self._open = None


def show_lecture_trace() -> None:
    """Trace both searches over Tuesday's graph, one row per step.

    The columns are the ones on the slides, so a run can be checked
    against a hand trace row by row.
    """
    for label, frontier in (
        ("BREADTH FIRST, WITH A QUEUE", QueueFrontier()),
        ("DEPTH FIRST, WITH A STACK", StackFrontier()),
    ):
        traced = TracingFrontier(frontier)
        header = (
            f"{'step':>4}  {'frontier before':<17}{'take out':<10}"
            f"{'adds':<14}frontier after"
        )
        print(f"\n{label}\n")
        print(header)
        print("-" * len(header))

        stopped = ""
        result = None
        try:
            result = search(LectureGraph("S", "G"), traced)
        except FrontierError as error:
            stopped = str(error)

        for row in traced.finish(result is not None and result.solved):
            print(
                f"{row[0]:>4}  {row[1]:<17}{row[2]:<10}{row[3]:<14}{row[4]}"
            )
        if stopped:
            print(f"\nStopped: {stopped}.")
        elif result is not None and result.solved:
            print(
                f"\n{result.nodes_expanded} expansions, "
                f"{' to '.join(result.states)}, {result.path_length} steps."
            )


def main() -> None:
    """Run whichever mode was asked for."""
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "lecture":
        show_lecture_trace()
        return
    directory = "data/small" if mode else DATA
    source, target = SOURCE, TARGET
    if directory == "data/small":
        source, target = "Kevin Bacon", "Tom Cruise"
    show_scale(directory)
    show_connection(directory, source, target)
    if directory == DATA:
        show_reach(directory)


if __name__ == "__main__":
    main()
