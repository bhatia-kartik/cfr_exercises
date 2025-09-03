#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

NUM_ROUNDS = 1000000

action_space = [[i, j, 5 - i - j] for i in range(6) for j in range(6 - i)]
num_actions = len(action_space)


regrets_1 = [0]*num_actions
regrets_2 = [0]*num_actions
prob_1 = [1/num_actions]*num_actions
prob_2 = [1/num_actions]*num_actions
prob_sum_1 = [0]*num_actions
prob_sum_2 = [0]*num_actions

def get_action(probabilities):
    ids = [i for i in range(num_actions)]
    return random.choices(ids, probabilities, k=1)[0]

            
#-1 for losing, +1 for winning, 0 for draw (based on # of battlefields won)
def get_utility(your_strat_id, opp_strat_id):
    
    your_strat = action_space[your_strat_id]
    opp_strat = action_space[opp_strat_id]
    
    results = [your_soldiers - opp_soldiers for your_soldiers, opp_soldiers in zip(your_strat, opp_strat)]
    
    battlefields_won = sum(result > 0 for result in results)
        
    utility = (battlefields_won > 1) - (battlefields_won < 1)
    
    return utility

payoff_matrix = [[get_utility(i, j) for j in range(num_actions)] for i in range(num_actions)]

def update_regret(regrets, your_strat_id, opp_strat_id):
    
    # utility = get_utility(your_strat_id, opp_strat_id)
    utility = payoff_matrix[your_strat_id][opp_strat_id]
    
    for i in range(num_actions):
        # potential_utility = get_utility(i, opp_strat_id)
        potential_utility = payoff_matrix[i][opp_strat_id]
        regret = potential_utility - utility
        regrets[i]+=regret

def update_probabilities(your_strat_id, opp_strat_id, regrets, probabilities, probabilities_sum):
    
    update_regret(regrets, your_strat_id, opp_strat_id)
    
    positive_regrets = [max(regret, 0) for regret in regrets]
    pos_regrets_sum = sum(positive_regrets)
    
    for i in range(num_actions):
        probabilities[i] = (positive_regrets[i] / pos_regrets_sum) if (pos_regrets_sum > 0) else (1/num_actions)
        probabilities_sum[i]+=probabilities[i]
        
def get_avg_strategy(strategy_sum):
    normalising_sum = sum(strategy_sum)
    return [prob/normalising_sum for prob in strategy_sum]
        
for i in range(NUM_ROUNDS):
    play_1 = get_action(prob_1)
    play_2 = get_action(prob_2)
    
    update_probabilities(play_1, play_2, regrets_1, prob_1, prob_sum_1)
    update_probabilities(play_2, play_1, regrets_2, prob_2, prob_sum_2)
    
avg_strat_1 = get_avg_strategy(prob_sum_1)
avg_strat_2 = get_avg_strategy(prob_sum_2)

relevant_strats_1 = [action_space[i] for i in range(num_actions) if avg_strat_1[i] > 0.05]

relevant_strats_2 = [action_space[i] for i in range(num_actions) if avg_strat_2[i] > 0.05]

print(avg_strat_1, "\n\n", avg_strat_2, "\n\n", relevant_strats_1, "\n\n", relevant_strats_2)