The method I used is a slightly customized depth-first search.
The goal was to observe I was able to reach sufficiently small computational time in order to solve also the problems for n > 20.
The idea behind that is that each time I would have found a solution in a certain path, I would immediately update the bound for all following paths.
For example if a find a solution with cost 9, I discard all following partial solutions in the case that the new considered path has cost 9 but a solution hasn't been found yet.
This method was supposed to be beneficial especially for large N but even with the additions of fixed thresholds about tree depth and bloat the more complex problems were still too computationally expensive.

---
case for n = 5
visited nodes: 10
bloat: 0%
optimal solution: list of sublists having indices 0, 1, 3, 11, 16
---
case for n = 10
visited nodes: 1659
bloat: 0%
optimal solution: list of sublists having indices 0, 2, 5, 32, 36
---
case for n = 20
visited nodes: 31565
bloat: 15%
optimal solution: list of sublists having indices 0, 11, 18, 19, 30
---
all other cases were computationally expensive even with continuously updated check and fixed bounds (depth < 9 and bloat <= 100%)