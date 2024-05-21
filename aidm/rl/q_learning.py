from collections import defaultdict
import random

# based on
#https://www.gocoder.one/blog/rl-tutorial-with-openai-gym
#https://github.com/chenmagi/q-cartpole-td0

def q_learning(problem, default_value=lambda: 0.0, learning_rate = 0.9, discount_rate = 0.8, epsilon = 1.0, decay_rate= 0.005, num_episodes = 1000, max_steps_per_episode = 99, num_of_trials= 100, log=False, log_file=None):
    q_table = defaultdict(default_value)

    q_table = train(problem, q_table, learning_rate, discount_rate, epsilon, decay_rate, num_episodes, max_steps_per_episode, log, log_file)
    return q_table

def evaluate_q_table(problem, q_table, max_steps_per_episode = 99, num_of_trials= 100, log=False, log_file=None):
    evaluate(problem, q_table, max_steps_per_episode, num_of_trials)

def train(problem, q_table, learning_rate=0.9, discount_rate=0.8, epsilon=1.0, decay_rate=0.005, num_episodes=1000, max_steps_per_episode=99, log=False, log_file=None):

    # training
    for episode in range(num_episodes):

        # reset the environment
        state = problem.reset_env()
        for s in range(max_steps_per_episode):

            # exploration-exploitation tradeoff
            if random.uniform(0,1) < epsilon:
                # explore
                action = problem.env.action_space.sample(state)
            else:
                # exploit
                action = np.argmax(qtable[state,:])

            # take action and observe reward
            [new_state, reward, terminated, truncated, info] = problem.env.step(action)

            # Q-learning update
            qtable[state,action] = qtable[state,action] + learning_rate * (reward + discount_rate * np.max(qtable[new_state,:]) - qtable[state,action])

            # Update to our new state
            state = new_state

            # if done, finish episode
            if terminated:
                break

        # decrease epsilon
        epsilon *= np.exp(-decay_rate)

    print(f"Training completed over {num_episodes} episodes")
    return qtable

def evaluate(problem, qtable, max_steps_per_episode, num_of_trials, render= False, log=False, log_file=None):

    state = problem.reset_env()
    rewards = 0
    for trial in range(num_of_trials):
        for s in range(max_steps_per_episode):

            #print(f"TRAINED AGENT")
            #print("Step {}".format(s+1))

            # get highest value action from the q table
            action = np.argmax(qtable[state,:])

            # perform action
            [new_obs, reward, terminated, truncated, info] = problem.env.step(action)
            rewards += reward
            if render:
                problem.env.render()
                print(f"score: {rewards}")
            state = new_obs
            if terminated == True:
                break
    print(f"Average rewards: {rewards/num_of_trials}" )

def get_max_action(qtable,state):

    state = problem.reset_env()
    rewards = 0
    for trial in range(num_of_trials):
        for s in range(max_steps_per_episode):

            #print(f"TRAINED AGENT")
            #print("Step {}".format(s+1))

            # get highest value action from the q table
            action = np.argmax(qtable[state,:])

            # perform action
            [new_obs, reward, terminated, truncated, info] = problem.env.step(action)
            rewards += reward
            if render:
                problem.env.render()
                print(f"score: {rewards}")
            state = new_obs
            if terminated == True:
                break
    print(f"Average rewards: {rewards/num_of_trials}" )
