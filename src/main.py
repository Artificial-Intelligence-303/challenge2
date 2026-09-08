"""Run the searches and print the numbers the reflection asks you for.

Provided. Start here once the two `choose` methods and `search` are written.

    uv run python src/main.py           the full run
    uv run python src/main.py small     the sixteen person set, for debugging
"""

import statistics
import sys

from degrees import MovieGraph
from frontier import Node, QueueFrontier, StackFrontier
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
        print(f"\nThe shortest chain, {result.path_length} films:")
        for i, film in enumerate(result.actions):
            first = graph.name_of(result.states[i])
            second = graph.name_of(result.states[i + 1])
            print(f"    {first} and {second} were both in {film}")

    _, deep = results["stack (depth first)"]
    if deep.solved:
        print(
            f"\nDepth first search answered the same question with a chain of "
            f"{deep.path_length} films. Both chains are real."
        )


def show_scale(directory: str) -> None:
    """Print the size of the graph and the branching factor, b."""
    graph = MovieGraph(directory, SOURCE, SOURCE)
    degrees = [len(graph.co_stars(person)) for person in graph.people]
    print("\nTHE GRAPH ITSELF\n")
    print(f"    people in this dataset      {len(graph.people):>8,}")
    print(f"    films                       {len(graph.movies):>8,}")
    print(f"    branching factor b, mean    {statistics.mean(degrees):>8.1f}")
    print(f"    branching factor b, median  {statistics.median(degrees):>8.0f}")
    print(f"    the most co-stars anyone has{max(degrees):>8,}")


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
        f"\nThere is no row past {max(reached)}: by then the search has reached"
        f"\neveryone. The right hand column keeps going anyway. Question 2 of"
        f"\nthe reflection asks you why the two columns come apart."
    )


def main() -> None:
    """Run everything against whichever dataset was asked for."""
    directory = "data/small" if len(sys.argv) > 1 else DATA
    source, target = SOURCE, TARGET
    if directory == "data/small":
        source, target = "Kevin Bacon", "Tom Cruise"
    show_scale(directory)
    show_connection(directory, source, target)
    if directory == DATA:
        show_reach(directory)


if __name__ == "__main__":
    main()
