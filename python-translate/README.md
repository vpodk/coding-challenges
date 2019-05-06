# Problem

Given a phone number as a string, generate all possible sequences of words that can be made from letters based on the standard keypad-to-letter relationship (separated by dashes).

For example, starting with characters themselves, you get the candidate set:
- `5 -> j, k, l`
- `96 -> wm, xm, ym, zm, wn, xn, yn, zn, wo, xo, yo, zo`

then refining the candidates to words (from a dictionary), you get the following solution for this phone number:
- `866-5548 -> tool-kit, ...`

Notes About the Problem:
- You may use a predefined dictionary file (such as https://users.cs.duke.edu/~ola/ap/linuxwords) for your word validation;
- 3rd party libraries are not allowed (except in the unit tests).

You are free to make assumptions about anything that is not covered by the rules/problem statement, just indicate those assumptions in your solution.


# Solution

```bash
python3 translate.py 866-5548 < words.txt
took-kit
took-lit
tool-kit
tool-lit
```

```bash
python3 translate.py 686-237 < words.txt
number
nun-ads
ounces
```
