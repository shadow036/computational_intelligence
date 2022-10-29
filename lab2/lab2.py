import random
import logging

N = 5

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

# def mu_plus_one():  # steady state

# def mu_plus_lambda():
    
# def mu_comma_lambda():

# def selection():
    
# def mutation():

# def parent_selection():    

def evaluate(element):  # fitness value to be maximized
    counters = [0 for _ in range(N)]
    if type(element[0]) is int:
        counters = [counters[_]+1 if _ in element else counters[_] for _ in range(N)]
    else:
        for e in element:
            counters = [counters[_]+1 if _ in e else counters[_] for _ in range(N)]
    """
    if the solution under evaluation doesn't contain all required numbers it is not accepted;
    it is better to have a complete solution (containing all required numbers) with partial_fitness < N - 1
    with respect of having an incomplete solution with partial_fitness N - 1 (see "NOTE A" at the end of the file for an example);
    we can picture the counters.count(0) as being an offset equal to -infinity added 
    to the partial_fitness value described below (see "NOTE B" at an equivalent solution)
    
    """
    if counters.count(0) > 0:
        return (None, False)
    """
    for each element 'i' of the counters list:
        -> if it contains 1 (=> 1 occurrence of number 'i' in the solution under evaluation) 
            => fitness = fitness + 1;
        -> if it contains 0 (=> no occurrences of number 'i' in the solution under evaluation) 
            => fitness = fitness + 0;
        -> if it contains j > 1 (=> more than 1 occurences of number 'i' in the solution under evaluation) 
            => fitness = fitness - number of occurences above 1
    """
    partial_fitness = sum([1 - counters[_] if counters[_] > 1 else counters[_] for _ in range(N)])
    return (partial_fitness, True)
            

if __name__ == '__main__':
    input_ = problem(N, seed=42)
    evaluation = evaluate([input_[0], input_[1]])
    print(evaluation)

"""
NOTE A
example with N=5: 
    a) [[0, 1], [0, 2], [0, 3], [0, 4]]: partial_fitness 1 (4 for the 4 exact matches and - 3 for the 4 occurrences of 0)
    b) [[0, 1, 2, 3]]: partial fitness 4 (4 for the 4 exact matches and 0 for the missing number)
"""

"""
NOTE B
full_fitness = sum([1 - counters[_] if counters[_] > 1 else counters[_] for _ in range(N)]) - (infinity if counters.count(0) > 0 else 0)
return full_fitness
"""
