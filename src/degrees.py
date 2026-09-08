"""The movie graph, presented as a search problem.

Provided. Adapted from the CS50 Introduction to Artificial Intelligence
"degrees" example, used under CC BY-NC-SA 4.0, and rewritten here to satisfy
the `Problem` interface in `src/problems.py`.

Two actors are neighbors when they appeared in a film together, so a path
through this graph is a chain of co-stars. The famous instance is the number
of steps from any actor to Kevin Bacon.

The data is real IMDb data. `data/small` holds sixteen people and is for
checking that your code runs at all. `data/medium` holds six thousand people
carved out around Kevin Bacon, and is the one worth measuring on.
"""

import csv
from collections import defaultdict


class MovieGraph:
    """People connected by the films they appeared in together."""

    def __init__(self, directory: str, source: str, target: str) -> None:
        """Load a dataset and set up a search between two named people.

        Args:
            directory: Folder holding `people.csv`, `movies.csv` and
                `stars.csv`.
            source: The name to search from.
            target: The name to search for.

        Raises:
            ValueError: If either name is missing from or ambiguous in the
                dataset.
        """
        self.names: dict[str, list[str]] = defaultdict(list)
        self.people: dict[str, dict[str, str]] = {}
        self.movies: dict[str, dict[str, str]] = {}
        self.stars: dict[str, set[str]] = defaultdict(set)
        self.cast: dict[str, set[str]] = defaultdict(set)

        with open(f"{directory}/people.csv", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                self.people[row["id"]] = row
                self.names[row["name"].lower()].append(row["id"])

        with open(f"{directory}/movies.csv", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                self.movies[row["id"]] = row

        with open(f"{directory}/stars.csv", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                person, movie = row["person_id"], row["movie_id"]
                if person in self.people and movie in self.movies:
                    self.stars[person].add(movie)
                    self.cast[movie].add(person)

        self.source = self._resolve(source)
        self.target = self._resolve(target)

    def _resolve(self, name: str) -> str:
        """Turn a person's name into their id.

        Args:
            name: The name to look up, case insensitively.

        Returns:
            The matching person id.

        Raises:
            ValueError: If the name is absent, or matches more than one
                person in this dataset.
        """
        matches = self.names.get(name.lower(), [])
        if not matches:
            raise ValueError(f"{name} is not in this dataset")
        if len(matches) > 1:
            raise ValueError(f"{name} matches more than one person")
        return matches[0]

    def name_of(self, person_id: str) -> str:
        """Return a person's name.

        Args:
            person_id: The id to look up.

        Returns:
            The person's name.
        """
        return self.people[person_id]["name"]

    def co_stars(self, person_id: str) -> set[str]:
        """Return everyone who appeared in a film with this person.

        Args:
            person_id: The person to look up.

        Returns:
            The set of co-star ids, never including the person themselves.
        """
        out: set[str] = set()
        for movie in self.stars[person_id]:
            out |= self.cast[movie]
        out.discard(person_id)
        return out

    def initial_state(self) -> str:
        """Return the id of the person the search starts from."""
        return self.source

    def actions(self, state: str) -> list[tuple[str, str]]:
        """Return every co-star of this person, and the film that links them.

        The action name is the film title, so a solution reads as a chain
        of films rather than a chain of anonymous steps.

        Args:
            state: The person id to move out of.

        Returns:
            The `(film_title, co_star_id)` pairs available.
        """
        neighbors = []
        for movie in sorted(self.stars[state]):
            title = self.movies[movie]["title"]
            for person in sorted(self.cast[movie]):
                if person != state:
                    neighbors.append((title, person))
        return neighbors

    def is_goal(self, state: str) -> bool:
        """Return whether this is the person being searched for."""
        return state == self.target
