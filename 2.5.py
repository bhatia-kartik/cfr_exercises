#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import ternary

ROCK = 0
PAPER = 1
SCISSORS = 2
GAME_ACTIONS = [ROCK, PAPER, SCISSORS]
NUM_ACTIONS = 3
NUM_ROUNDS = 10000

strategy_1 = [0.9, 0.1, 0]
strat_list_1 = [tuple(strategy_1)]
strategy_sum_1 = [0, 0, 0]
regret_1 = [0, 0, 0]
strategy_2 = [0, 0.9, 0.1]
strat_list_2 = [tuple(strategy_2)]
strategy_sum_2 = [0, 0, 0]
regret_2 = [0, 0, 0]

def get_move(strategy):
    return random.choices(GAME_ACTIONS, strategy, k=1)[0]

def update_strategy(strategy, regret, strategy_sum, strat_list, your_move, opp_move):    
    action_utility = [0, 0, 0]
    action_utility[opp_move] = 0
    action_utility[(opp_move + 1) % NUM_ACTIONS] = 1 #since rps follows modular arithmetic
    action_utility[(opp_move - 1) % NUM_ACTIONS] = -1
    
    
    for a in range(NUM_ACTIONS):
        regret[a] += action_utility[a] - action_utility[your_move]
    
    positive_regrets = [max(r, 0) for r in regret]
    total_positive = sum(positive_regrets)

    if total_positive > 0:
        for a in range(NUM_ACTIONS):
            strategy[a] = positive_regrets[a] / total_positive
    else:
        for a in range(NUM_ACTIONS):
            strategy[a] = 1 / NUM_ACTIONS
            
    for a in range(NUM_ACTIONS):
        strategy_sum[a] += strategy[a]
        
    strat_list.append(tuple(get_average_strategy(strategy_sum)))

def get_average_strategy(strategy_sum):
    total = sum(strategy_sum)
    if total > 0:
        return [s / total for s in strategy_sum]
    else:
        return [1 / NUM_ACTIONS] * NUM_ACTIONS
    
    
for i in range(NUM_ROUNDS):
    play_1 = get_move(strategy_1)
    play_2 = get_move(strategy_2)
    update_strategy(strategy_1, regret_1, strategy_sum_1, strat_list_1, play_1, play_2)
    update_strategy(strategy_2, regret_2, strategy_sum_2, strat_list_2, play_2, play_1)
    
avg_strat_1 = get_average_strategy(strategy_sum_1)
avg_strat_2 = get_average_strategy(strategy_sum_2)

print(avg_strat_1, avg_strat_2)

figure, tax = ternary.figure(scale=1.0)
figure.set_size_inches(7, 6)
tax.boundary()
tax.gridlines(multiple=0.2, color="black")
tax.set_title("Evolution of CFR RPS Strategies", fontsize=20)
tax.plot(strat_list_1, linewidth=2.0, label="Strategy 1", color="steelblue")
tax.plot(strat_list_2, linewidth=2.0, label="Strategy 2", color="crimson")
tax.ticks(axis='lbr', multiple=0.2, linewidth=1, tick_formats="%.1f")
tax.scatter([strat_list_1[0]], marker='o', label="Inital Strategy 1", color="steelblue")
tax.scatter([strat_list_2[0]], marker='o', label="Inital Strategy 2", color="crimson")
tax.scatter([[0.333, 0.333, 0.333]], marker='*', color='gold', label="Nash Equilibrium", zorder=2, s=60)
tax.legend()
tax.clear_matplotlib_ticks()
tax.show()