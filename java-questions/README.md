# Interview questions:


## 1. Simple
Swap the 4th and last letters in the string `"hello"`.

## 2. Medium
What does this code actually do and what type of algorithm does it implement?

```java

static final double SQRT5 = 2.23606797749979; // √5 = Math.sqrt(5)
static final double PHI = 1.618033988749895;  // Φ = (1 + SQRT5) / 2

public static int calculate(int n) {
  if (n > 1) {
    double asymp = Math.pow(PHI, n) / SQRT5;
    return (int) Math.round(asymp);
  }

  return n;
}
```

## 3. Complex
You have calendar data from more than one person.
The data format is:

```js
[
  // Person 1
  [
    // Busy slots.
    [["9:00", "10:30"], ["12:00", "13:00"], ["16:00", "18:00"]],
    // The boundaries of the working day.
    ["9:00", "20:00"]
  ],
  // Person 2
  [
    // Busy slots.
    [["10:00", "11:30"], ["12:30", "14:30"], ["14:30", "15:00"], ["16:00", "17:00"]],
    // The boundaries of the working day.
    ["10:00", "18:30"]
  ]
]
```

Find the optimal way to find the common available slots for all persons.
Expected result is:

```json
[["11:30", "12:00"], ["15:00", "16:00"], ["18:00", "18:30"]]
```
