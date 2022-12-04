# Lab 3
## Exercise 3.1
In this first exercise I tried different strategies but most of them have very small variations between them. \
They can be grouped into five clusters. \
Notice that **each of them, in addition to their specific behaviour, contain a specific trigger ("finishing_or_forced_move") that allows them to ignore the currently scheduled behaviour in order to win the game or when the scheduled behaviour cannot be executed**. \
**Given N the maximum number of objects in a given row and M the current amount** we can generate this classification:
1. The "spreader" family of agents. \
Each turn this kind of agent will take 1 object (standard spreader), M - 1 objects ("aggressive spreader") or a random amount of objects ("random spreader") between 1 and N - 1 from a single row. \
The main characteristic is that it never removes all remaining objects from a row unless it is strictly necessary.
2. The "divergent" family of agents is composed of strategies that tend to "oscillates" between two (in the cases of the standard one and the "challenger" one) or three (if we talk about "the triphase one") behaviours in each turn. \
In the first two versions each agent either takes a certain amount (1 in the first case and M - 1 in the second one) of objects from a row having M > 1 objects or it completely clears a single row. \
It can be seen as a mixture between the standard and the "aggressive" spreader. \
The third version adds a further probability of removing 50% of objects in a single row.
3. The "make strategy" agents are the ones developed in class and they basically clear either the first available row or the last available row with probability p and 1 - p respectively.
4. The "mirrorer" family is perhaps the most complex family of agents and it contains two different forms of strategies:

   * The first one (the "standard" one) tries to copy the opponent's moves following this strategy:
   
      * if the opponent removed K elements from a row, during the next turn it tries to remove K elements from another row or the same one if it still contains more than K objects;
      * if the previous condition cannot be fulfilled then it removes M - 1 objects from a random row;
      * if the opponent clear a row, so does this strategy.
   * The second one (the "reversed" one) is even more complex because it keep track of how many objects the opponent leaves in a row each turn and uses this information for its strategy:
   
      * if the opponent removed N - K elements in a turn, during its turn the will remove an amount of objects equal to K from another row (leaving at most 1 object in that row);
      * if the opponent clears a row, the agent will remove only one object in its next turn;
      * if the opponent removes only 1 object, the agent will entirely clear one random row.
5. The last group of strategies is made of all the agents that cannot be included in any of the other groups.\
Other than strategies developed in class (the optimal strategy, the dummy one, the random one and the Gabriele's one), the interesting ones are mainly two:

   * "nimsum_little_brother" is a variation of the classical nim-sum in the sense that it tries to create a situation in which the opponent will be forced to pick the last object due to the fact that all rows have only 1 or 0 object and during its turn (before playing) there are an odd number of objects still in play. \
   The difference is that this strategy is used from the beginning, but only when all rows except 1 have less than 2 objects each. \
   The early game is used to setup the board for the endgame strategy by trying to leave as many rows as possible with 1 or 0 objects in them.
   The situation that proves that this is not the optimal solution is that it is (rarely) still capable of losing again the other non-optimal ones. 
   * "the balancer" constantly tries to balance the number of objects in each row by removing a certain amount of objects from the row having the biggest M in order to make it equal (in terms of amount of objects) to the one having the second largest M.
### Tournament results (11 rows, 100 games for each pair of strategies)
**STRATEGY&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;WIN RATE** \
Divergent&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;62.5 % \
Divergent challenger&emsp;&emsp;&emsp;75  % \
Spreader&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;15.34\
Aggressive spreader&emsp;&emsp;&emsp;33.9\
Nimsum little brother \
Optimal strategy \
Pure random \
Gabriele's \
Make strategy (0.1) \
Make strategy (0.5) \
Make strategy (0.9) \
Dummy \
Divergent triphase \
The Balancer \
The Mirrorer \
Random spreader \
The reversed Mirrorer 


## Exercise 3.2
