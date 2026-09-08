# Challenge 2 Reflection

Answer all three questions. **300 words minimum across the whole document.**
You are graded on whether the reasoning is correct and specific to the
numbers your own run produced. Replace every `TODO` before you submit.

Run `uv run python src/main.py` before you start writing. Every number these
questions ask for is in its output.

---

> **1. Report your numbers, and explain the two gaps.**
>
> Give the table `main.py` printed for Kevin Bacon and your target: degrees,
> nodes expanded, and peak frontier, for both the queue and the stack.
>
> Then explain **two** differences in it.
>
> **The path.** One search returned a chain many times longer than the
> other. Both chains are real. Say what about `choose` produced the long
> one, in terms of which node left the frontier next. "Depth first goes
> deep" is not an answer.
>
> **The memory.** The two peak frontier numbers are not close either. Say
> which search held more, and why that follows from the order it takes
> nodes out. The branching factor `main.py` printed is worth quoting here.

TODO

---

> **2. Explain the reach table.**
>
> `main.py` prints how many people sit at each distance from Kevin Bacon,
> beside what b to the power d predicts.
>
> The two columns disagree in **both directions**, which is the interesting
> part. At one degree the real number is far larger than the prediction. At
> four degrees the prediction is six figures and the real number is zero.
>
> Explain each. For the first, think about what kind of average b is and
> who Kevin Bacon is in this dataset. For the second, say what b to the
> power d is counting that your search never counted, and **name the line
> in your own `search` that is responsible.**
>
> Then finish the thought: what would have to be true about a problem for
> the right hand column to be the honest answer?

TODO

---

> **3. Choose a search, and say what it costs to be wrong.**
>
> You are building a "how are these two people connected" feature, for a
> real product with real users.
>
> Pick the queue or the stack. Defend it using **two of your own measured
> numbers**. Then describe what a user would actually see if you shipped
> the other one. Be concrete: not "a worse answer" but what is on their
> screen and whether they could tell anything was wrong.
>
> Finish with the honest part. Name one input on which your choice is the
> wrong one, and say how you would notice in production that it had
> happened.

TODO

---

> **AI tool disclosure**
>
> State what AI tools you used on this challenge, if any, and what they
> did. "None" is a complete answer if it is true. Be specific: "I used X to
> explain what a frontier is" and "I used X to write the search loop" are
> very different disclosures.

TODO
