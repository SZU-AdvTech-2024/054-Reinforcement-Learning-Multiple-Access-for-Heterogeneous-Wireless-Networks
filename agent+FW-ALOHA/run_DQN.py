import numpy as np
from tqdm import tqdm

from environment import ENVIRONMENT
from DQN_brain import DQN

def return_action(action, n_actions=2):
    one_hot_vector = [0] * n_actions
    one_hot_vector[action] = 1
    return one_hot_vector


def return_observation(o):
    if o == 'S':
        return [1, 0, 0, 0]
    elif o == 'F':
        return [0, 1, 0, 0]
    elif o == 'B':
        return [0, 0, 1, 0]
    elif o == 'I':
        return [0, 0, 0, 1]


def main(W, M, E, F, B, gamma, alpha, idx, max_iter):

    agent_reward_list = []
    aloha_reward_list  = []
    state = env.reset()

    print('------------------------------------------')
    print('---------- Start processing ... ----------')
    print('------------------------------------------')

    for i in tqdm(range(max_iter)): 
        action = agent.choose_action(np.array(state))
        observation, agent_reward, aloha_reward = env.step(action)
        agent_reward_list.append(agent_reward)
        aloha_reward_list.append(aloha_reward)

        # M > 1 
        next_state = state[8:] + return_action(action) + return_observation(observation) + [agent_reward, aloha_reward]

        # store experience
        agent.store_transition(state, action, agent_reward, aloha_reward, next_state)
        if i > 100 and (i % 5 == 0):
            agent.learn()       # internally iterates default (prediction) model
        state = next_state

    with open(f'rewards/reward1_len{max_iter}_W{W}_M{M}_E{E}_F{F}_B{B}_gamma{gamma}_alpha{alpha}_idx{idx}.txt', 'w') as my_agent:
        for i in agent_reward_list:
            my_agent.write(str(i) + '   ')
    with open(f'rewards/reward2_len{max_iter}_W{W}_M{M}_E{E}_F{F}_B{B}_gamma{gamma}_alpha{alpha}_idx{idx}.txt', 'w') as my_aloha:
        for i in aloha_reward_list:
            my_aloha.write(str(i) + '   ') 
        


if __name__ == "__main__":

    n_nodes = 2 # number of nodes
    n_actions = 2 # number of actions

    M = 20 # state length
    E = 1000 # memory size
    F = 20 # target network update frequency
    B = 64 # mini-batch size
    gamma = 0.9 # discount factor

    alpha = 0 # fairness index
    
    max_iter = int(5e4)
    idx = 1


    env = ENVIRONMENT(state_size=int(8*M), 
                      window_size=3
                      )

    agent = DQN(env.state_size,
                    n_nodes,
                    n_actions,  
                    memory_size=E,
                    replace_target_iter=F,
                    batch_size=B,
                    gamma=gamma,
                    epsilon=1,
                    epsilon_min=0.005,
                    epsilon_decay=0.995,
                    alpha=alpha
                    )

    main(env.window_size, M, E, F, B, gamma, alpha, idx, max_iter)