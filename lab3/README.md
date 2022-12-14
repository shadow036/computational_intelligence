# Lab 3
## Exercise 3.1
In this first exercise I tried different strategies but most of them have many common traits. \
Notice that **each of them, in addition to their specific behaviour, contains a specific trigger ("finishing_or_forced_move") that allows them to ignore the currently scheduled pattern in order to win the game or when the scheduled behaviour cannot be executed**. \
**Given N the maximum number of objects in a given row and M its current amount** and based on the agents' behaviours and patters, we are then able to group them in five clusters:
1. The "spreader" family of agents. \
Each turn this kind of agent will take 1 object (standard spreader), M - 1 objects ("aggressive spreader") or a random amount of objects between 1 and M - 1 ("random spreader") from a single row. \
The main characteristic of this type of agent is that it never removes all remaining objects from a row unless it is strictly necessary due to the reasons explained above.
2. The "divergent" family of agents is composed of strategies that tend to choose between only two (in the cases of the standard one and the "challenger" one) or three (if we talk about "the triphase one") behaviours in each of their turns. \
In the first two versions each agent either takes a certain amount (1 in the first case and M - 1 in the second one) of objects from a row having M > 1 objects or it completely clears a single row. \
It can be seen as a mixture between the standard and the "aggressive" spreader without the constraint of leaving at least one object per row in almost any situation. \
The third version adds a further choice of removing 50% of the remaining objects in a single row.
3. The "make strategy" agents are the ones developed in class and they basically clear either the first available row or the last available row with probability p and 1 - p respectively.
4. The "mirrorer" family is perhaps the most complex family of agents and it contains two different forms of strategies:

   * The first one (the "standard" one) tries to copy the opponent's moves following this strategy:
   
      * if the opponent removed K elements from a row, during the next turn my agent will try to remove K elements from a row (the same one can be selected again if it still contains more than K objects);
      * if the previous condition cannot be fulfilled then it removes M - 1 objects from a random row;
      * if the opponent clear a row, so does this strategy.
   * The second one (the "reversed" one) is even more complex because it keep track of how many objects the opponent left in a row during each turn and then uses this information for its strategy:
   
      * if the opponent removed N - K elements in a turn, during its own turn the agent will remove an amount of objects equal to K from another row (leaving a minimum of 1 object in that row);
      * if the opponent clears a row, the agent will remove only one object from a row having M > 1 in its next turn;
      * if the opponent removes only 1 object, the agent will entirely clear one random row;
      * In the case that in a given turn the opponent clears a row by removing only one object (the last one) from a row, one of the previous two behaviours will be activate at random while the other one will be ignored.
5. The last group of strategies is made of all the agents that cannot be included in any of the other groups due to their different behavioural design.\
In addition to the strategies which were developed in class (the optimal strategy, the pure random one and the Gabriele's one), the interesting ones are mainly two:

   * "nimsum_little_brother" is a variation of the classical nim-sum in the sense that it tries to create a situation in which the opponent will be forced to pick the last object due to the fact that all rows have only 1 or 0 object and during its turn (before playing) there are an odd number of objects still in play. \
   The difference is that this strategy is used from the beginning, but only when all rows except 1 have less than 2 objects each. \
   The early game is used to setup the board for the endgame strategy by trying to leave as many rows as possible with 1 or 0 objects in them.
   The situation that proves that this is not the optimal solution is that it is (rarely) still capable of losing again the other non-optimal ones; 
   * "the balancer" constantly tries to balance the number of objects in each row by removing a certain amount of objects from the row having the biggest M in order to make it equal (in terms of amount of objects) to the one having the second largest M. \

   One last strategy I introduced is the dummy one, used only for benchmarking and debugging purposes. \
In fact it does absolutely nothing which in the code this is translated in the strategy always removing 0 objects. 
### Tournament results (11 rows, 100 games for each pair of strategies)
All win rates are expressed in percentage\
**STRATEGY&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;TOTAL WIN RATE [opponents - games]&emsp;&emsp;&emsp;WIN RATE BASED ON STARTING ORDER [first - second]** \
Divergent&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;56.250 - 54.188&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;52.875 - 55.500\
Divergent challenger&emsp;&emsp;&emsp;&emsp;50.000 - 54.000&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;54.750 - 53.250\
**Spreader&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;68.750 - 65.188&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;67.250 - 63.125&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(3)**\
Aggressive spreader&emsp;&emsp;&emsp;&emsp;43.750 - 47.250&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; 47.250 - 47.250\
**Nimsum little brother&emsp;&emsp;&emsp;93.750 - 87.125&emsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;89.125 - 85.125&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;(2)**\
**Optimal strategy&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&nbsp;100.000 - 99.812&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;99.875 - 99.750&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(1)**\
Pure random&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;25.000 - 37.938&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;37.250 - 38.625\
Gabriele's&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;43.750 - 45.438&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;47.000 - 43.875\
Make strategy (0.1)&emsp;&emsp;&emsp;&emsp;&nbsp;43.750 - 46.312&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;46.875 - 45.750\
Make strategy (0.5)&emsp;&emsp;&emsp;&emsp;&nbsp;25.000 - 37.062&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;36.625 - 37.500\
Make strategy (0.9)&emsp;&emsp;&emsp;&emsp;&nbsp;12.500 - 24.312&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;24.000 - 24.625\
Dummy&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;0.000 - 0.000&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;0.000 - 0.000\
Divergent triphase&emsp;&emsp;&emsp;&emsp;&nbsp;68.750 - 57.438&nbsp;&nbsp;&nbsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;58.375 - 56.500&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\
The Balancer&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;43.750 - 41.875&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; 43.375 - 40.375\
The Mirrorer&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp; 37.500 - 39.812&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; 42.375 - 37.250\
Random spreader&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;62.500 - 54.250&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;54.625 - 53.875\
The reversed Mirrorer&emsp;&emsp;&emsp;&nbsp;&nbsp;62.500 - 58.000&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&emsp; 57.000 - 59.000\
\
Average&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;49.265 - 50.000&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;50.507 - 49.493 \
\
\
From the results we can see that the best strategies are, as expected, the original nim-sum and its smaller variant. \
The more interesting information obtained from the results table is, along with the relatively good performance of the standard "spreader" (but I didn't really have an idea about which agent could manage to reach the third place), is without any doubt the win rate of the optimal strategy. \
In fact even if it is very high (as expected), it is not 100 % and furthermore it managed to lose at least once when starting first and at least twice when starting second. \
Thinking that one (or more) of the other fixed-rule strategies was able to defeat the optimal one is quite impressive and the agent which had the highest chanches to accomplish this feat was probably the smaller version of the nim-sum itself.

## Exercise 3.2
In the second exercise I tried to parametrize the strategies by giving to some of them an additional parameter p during creation. \
This parameter is used by all agents in "evolving_agents.py" and it is a value between 0 and 1. It affects the strategy of the agents by introducing a different behaviours based on the threshold p.
As a simple form of mutation I just tried to generate other agents having the same "base" behaviour but adding a modification to the parameter p. \
Unfortunately I couldn't complete the exercise but all the functions and the main ideas are present.

## Exercise 3.3
The "min-max" strategy I developed works pretty well but due to the absence of computational optimizations (alpha-beta pruning or hash tables) it is highly inefficient for all situations where N > 3. \
Still the idea behind the code seems ok due to the tests I made with N = 3. \
I tried to implement from scratch the tree containing the various states with the related "backpropagation" algorithm of the final scores. \
I also tried a new version which used a made-up hash table (which was actually a dictionary having the board and the turn as the key) but with that other problems arose.

## Exercise 3.4
Concerning the last exercise, I took inspiration from the maze example but of course I had to modify the logic behind that in order to adapt it to the new context. \
The most important difference is the one regarding the penalties. \
In addition to giving a penalty for each step that doeesn't conclude the game, I also added some positive and negative rewards when the agent is in a position that leads to certain victory or defeat 
In fact in the evaluation phase I set to 0 the penalty for reaching a state that leads to certain victory and in this case the cumulative reward will remain constant for the rest of the game. On the other hand I gave a -10 penalty for reaching a position that will make the agent lose (this -10 penalty will be cumulative until the end of the game, i.e. if the agent reaches a losing position 10 own turns before the end of the game, at the end this will cost the agent at least -100 penalty point).
The rest of the code remains the same, except some other small modifications, namely: \
- in line 35, 36, 37 I initialized the initial thuth value for the last move to -10 if the game was lost
- some modifications were added in order to ensure compatibility with the rest of the code
- I used a function which simulates the outcome each possible action in order to make the best decision (with respect to the agent's beliefs, it's not just brute force) \

The final results seems quite good, with a lot of training games (100000), the agent is able to defeat almost all opponents during the 10000 test matches, except for the optimal strategy which is still difficult to even get a single win against it. \
On average it seems that it is able to deal with relative high N (in the range of 6 - 7).