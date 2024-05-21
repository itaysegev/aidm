from aidm.core.problem import Problem


def run_episode(agents, problem:Problem, reset:bool=True):
    """ Runs an episode of the given environments """
    obs = env.reset()
    n = len(agents)
    total_rewards = 0.0
    agent_rewards = [0.0 for _ in range(len(agents))]

    done = False
    train_steps = 0

    for _ in range(arglist.max_episode_len):
        if arglist.display:
            env.render()
            time.sleep(0.15)

        (actions_e, actions_a) = env.get_action_set(agents, obs, arglist.method)

        new_obs, rewards, done, info = env.step(actions_e)

        if arglist.method == 'train':
            for idx, key in iterate(actions_e):
                agents[idx].experience_callback(obs[key], actions_a[idx], new_obs[key], rewards[key], done[key])

        for idx, key in iterate(actions_e):
            agent_rewards[idx] += rewards[key]
            total_rewards += rewards[key]

        obs = new_obs
        train_steps += 1

        terminal = False
        if type(done) == type(list):
            terminal = all(done)
        elif type(done) == type(dict):
            terminal = done['__all__']

        if terminal:
            break

    return total_rewards, agent_rewards, train_steps
