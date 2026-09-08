# Challenge 2: Six Degrees of Kevin Bacon

|                    |                                             |
| :----------------- | :------------------------------------------ |
| `Tuesday 8 Sep`    | Released, in lab                            |
| `Tuesday 15 Sep`   | Due at 2:30pm, the start of lab             |
| `Tuesday 15 Sep`   | Verbal checks, during that same lab session |
| Points             | 3                                           |

Two actors are connected if they were in a film together. Almost everybody in
Hollywood turns out to be a short chain of films away from Kevin Bacon, and
this challenge is you finding those chains in a graph of six thousand real
people.

You are going to write **one** search algorithm. Not two. The difference
between breadth first and depth first search is not two algorithms, it is one
algorithm handed a different container, and you will only really believe that
once the same function has produced both.

Then you will find out that the two answers are not equally good, and that
the standard formula for what search costs does not describe what your code
actually did.

**This is a 90 minute assignment.** There are two things to write and they
are both short. If you are an hour in and have not run anything, come to
office hours rather than pushing on.

## Course learning outcomes

1. **Outcome 2.** Correctly apply search algorithms to solve an agent-based
   problem. You implement breadth first and depth first search and run them
   over a graph of six thousand people.
2. **Outcome 5.** Evaluate intelligent systems while considering their
   social, political, and ethical implications, and communicate their
   outcomes in both written and oral forms. Question 3 of the reflection has
   you choose a search for a real feature and say what a user sees when the
   choice is wrong, and the verbal check is where you defend it out loud.

## What you implement

Two things. Everything else is provided.

### 1. `StackFrontier.choose` and `QueueFrontier.choose`, in `src/frontier.py`

One line each. Read the `Frontier` base class first: adding, membership and
emptiness are already written, because none of them vary. All a subclass
decides is **which node comes out next**, and `choose` has to both pick that
node and remove it from `self.nodes`.

### 2. `search`, in `src/search.py`

The whole loop, once:

```
put the starting node in the frontier
until the frontier is empty:
    record the frontier's size if it is the largest yet
    take a node out and count it as expanded
    if it is the goal, rebuild the path and stop
    mark its state explored
    for each neighbor, add it unless it is explored or already waiting
```

Two details are worth getting right rather than guessing at.

- **Test for the goal when a node comes out of the frontier, not when it goes
  in.** Breadth first search finds the same path either way on this problem,
  so nothing will fail today if you get it wrong. It stops being true in Week
  4, and it is a hard bug to find later.
- **Both membership checks matter.** Skipping "already explored" makes the
  search loop forever, because this graph is full of cycles. Skipping
  "already waiting in the frontier" does not break correctness, but
  duplicates pile up and your expansion counts stop meaning anything.

`reconstruct` is written for you. Walking parent links back to the start is
bookkeeping, not search.

## Checking your work against Tuesday

Most of the tests run on **the eight node graph from Tuesday's activity**, the
one you traced by hand. Breadth first expands 4 nodes and returns a 2 step
path. Depth first expands 7 and returns a 5 step path. If a test fails you
already know what the right answer looks like, and you can compare your
frontier against the one on your own page.

## The data

Real IMDb data, in `data/`.

- **`data/small`** is sixteen people. Use it while you are still getting the
  code to run at all.
- **`data/medium`** is six thousand people, carved out around Kevin Bacon.
  This is the one the reflection is about.

Change `SOURCE` and `TARGET` at the top of `src/main.py` to search between
different people. Be aware the medium set is a slice of IMDb rather than all
of it, so somebody being absent means they are not in this file, not that
they never worked.

## Running it

```
uv run python src/main.py         the full run, on data/medium
uv run python src/main.py small   the sixteen person set, for debugging
uv run pytest                     run the tests
uv run ruff check src tests       check your style
uv run ruff format src tests      fix most style problems automatically
uv run gatorgrade                 run the checks the way they are graded
```

`src/main.py` prints every number the reflection asks for. Run it before you
start writing.

## Style

Same as last time. Your code is checked against the [Google Python Style
Guide](https://google.github.io/styleguide/pyguide.html): 80 character lines,
Google-style docstrings with `Args:` and `Returns:`, `lower_with_under`
function names, imports grouped at the top. `uv run ruff check src tests`
tells you which line and which rule, and `uv run ruff format src tests` fixes
most of it.

## Evaluation

This challenge is worth **3 points**.

| Component                 | Value   |
| :------------------------ | :------ |
| Programming               | 1       |
| Written reflection        | 1       |
| Verbal check              | 1       |
| **Total**                 | **3**   |

### Programming, 1 point

Run by `gatorgrade`, awarded as the fraction of the **code** checks that
pass. These are:

- A stack returns the node added most recently, a queue the one added
  earliest, and choosing a node actually removes it.
- Draining a frontier empties it, and an empty one raises rather than quietly
  returning nothing.
- Search finds the goal on Tuesday's graph, and every step of the path it
  returns is a legal move from the step before it.
- Breadth first returns the 2 step path and depth first the 5 step one, and
  the expansion counts are 4 and 7, matching the hand trace.
- No state is expanded twice, and the peak frontier is tracked.
- An unreachable goal is reported rather than crashed on, and searching from
  a node to itself is zero steps.
- It runs on the real IMDb data, the two searches disagree there, and the
  same `search` works on a hand written graph and on the movie graph without
  changes.
- Style passes `ruff` and type annotations check out under `mypy`.
- No `TODO` markers are left behind, and your search loop carries at least
  three comments explaining your reasoning.

`gatorgrade` also runs two checks on `docs/summary.md`. Those belong to the
reflection below, not to this point.

Autograder results are preliminary. The final grade is determined by the
instructor.

### Written reflection, 1 point

Complete `docs/summary.md`. Three questions and the disclosure, **300 words
minimum across all of them**. You are graded on whether the reasoning is
correct and specific to the numbers you measured, not on length.

Question 2 is the one that carries this challenge. It asks you to explain a
table where the standard formula for the cost of search disagrees with your
own measurement in both directions, and it cannot be answered without the
output in front of you.

### Verbal check, 1 point

During lab you answer two or three questions about your own code **without
looking at it**. Nothing to prepare beyond understanding what you wrote. If
you can say what changes when `pop()` becomes `pop(0)`, and why your search
never expanded more than six thousand things, you will be fine.

## AI use on this challenge

Full policy: **[AI in this course](https://areweagentsyet.com/ai/)**. AI tools
are allowed here, you disclose them, and you have to be able to explain what
you submit.

> ### The skill this time: reproduce the failure yourself
>
> Every challenge names one habit. Last time it was explaining a suggestion
> back before accepting it. This one is what you do when something breaks.
>
> Before you paste an error into anything, get it to happen again on purpose,
> in the smallest case you can build. Which graph. Which frontier. Which
> line. A tool handed "my search does not work" will invent a plausible cause
> and you will spend an hour on it. A tool handed "depth first on the lecture
> graph expands 9 nodes and it should expand 7" gets asked a real question,
> and half the time you have answered it yourself before you finish typing.
>
> `data/small` and the eight node lecture graph exist for exactly this. Do
> not debug against six thousand people.

Concretely, for this assignment:

- **Write the two `choose` methods yourself.** They are one line each and
  they are the entire idea of the week.
- **The search loop is worth struggling with.** It is about twenty lines and
  you will write versions of it for the rest of the term. Getting it handed
  to you now costs you Week 4, where you modify it rather than write it.
- **A tool is genuinely useful** for the parts that are not the point: what a
  `dataclass` is, why an import will not resolve, how `zip` works.
- **A tool cannot give you your numbers.** They come from running your own
  code.

## How this assignment was built

You are asked below to disclose your AI use, so here is mine.

The degrees-of-separation problem comes from CS50's Introduction to
Artificial Intelligence, used under CC BY-NC-SA 4.0. I have set it in this
course before. I used Claude to restructure it so that `search` is written
against a general problem interface rather than against this one graph, and
to draft the tests. I carved the six thousand person dataset out of the full
IMDb set myself so that it would fit in a repository, which means the
distances in it are shorter than they would be on all of IMDb.

I decided the shape: one search rather than two, tests that run on the same
graph you traced in class so the numbers are checkable by hand, and a
reflection built on a table whose two columns disagree.

I ran everything before releasing it. The reference solution passes every
check, the unfinished starter fails every test, and I checked the checks
against wrong implementations rather than only against an empty one. The
wording throughout is mine.

## Disclosing your AI use

At the end of `docs/summary.md` there is a disclosure section. Answer three
things, a sentence or two each:

1. **Which tool.** Name it. If you used more than one, name each.
2. **What you used it for.** Which part of the assignment.
3. **What you did with what it gave you.** Accepted it, edited it, checked it
   against something, or threw it out.

**If you did not use any tool, write that.** That is a complete and perfectly
good answer.

Disclosing costs you nothing. There is no version of this where naming a tool
loses you points.

## Acknowledgments

The degrees-of-separation problem is adapted from [CS50 Introduction to
Artificial Intelligence](https://cs50.harvard.edu/ai/2024/), used under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
License](https://creativecommons.org/licenses/by-nc-sa/4.0/). The film data is
from IMDb.
