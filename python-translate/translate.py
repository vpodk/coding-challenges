#!/usr/bin/python3
# -*- coding: utf-8 -*-
# http://google.github.io/styleguide/pyguide.html
#
# Assumptions:
# 1. We don't limit the length of phone number.
# 2. We assume the phone number can contain only numbers and a dash symbol
#   (no spaces).
# 3. We assume 0 and 1 are not valid numbers for the phone number to convert
#   into words (0 and 1 don't have corresponding letters on phone keypad).
#
# Result:
# 1. Big-O performance is O(4^N)

import sys

KEYPAD = {
  '2': ['a', 'b', 'c'],
  '3': ['d', 'e', 'f'],
  '4': ['g', 'g', 'i'],
  '5': ['j', 'k', 'l'],
  '6': ['m', 'n', 'o'],
  '7': ['p', 'q', 'r', 's'],
  '8': ['t', 'u', 'v'],
  '9': ['w', 'x', 'y', 'z']
}


def _find_word(word, dictionary):
    result = []

    for i in range(len(word)):
        if word[:i + 1] in dictionary:
          if i + 1 == len(word):
              result.append(word)
          else:
              tail = _find_word(word[i + 1:], dictionary)
              if tail:
                  result += [word[:i + 1]] + tail

    return result


def main():
  words = ['']
  dictionary = [word.lower().strip() for word in sys.stdin]

  for digit in sys.argv[1]:
      if digit != '-' and digit in KEYPAD:
          words = [word + letter for word in words for letter in KEYPAD[digit]]

  for word in words:
      result = _find_word(word, dictionary)

      if result:
          print('-'.join(result))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()
