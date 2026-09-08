"""The interface every search problem satisfies.

Provided. You should not need to change this file, but you do need to read
it, because `search` in `src/search.py` is written against this and nothing
else.

A search problem answers exactly three questions:

    where do I start        `initial_state`
    what can I do from here `actions`
    am I done               `is_goal`

Anything that answers those three can be searched by the same code. Your
`search` never learns that it is walking a graph of actors, and that is the
point: swap in a maze or a puzzle and it would not need a single change.
"""

from typing import Any, Protocol


class Problem(Protocol):
    """What `search` expects to be handed.

    A state can be any hashable value. This assignment uses person id
    strings, and `search` only ever compares states and puts them in a set,
    so it never has to care.
    """

    def initial_state(self) -> Any:
        """Return the state the search starts from."""
        ...

    def actions(self, state: Any) -> list[tuple[str, Any]]:
        """Return the `(action_name, resulting_state)` pairs available here."""
        ...

    def is_goal(self, state: Any) -> bool:
        """Return whether this state is a goal state."""
        ...
