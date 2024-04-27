import time


class ComputationalResources:

    def __init__(self, iteration_bound=None, time_bound=None):

        # creating the initial state object
        self.iteration_bound = iteration_bound
        self.iteration_count = 0

        self.time_bound = time_bound
        self.init_time = time.time()
        self.current_time = self.init_time

    def reset(self):

        # creating the initial state object
        if self.iteration_bound:
            self.iteration_count = 0

        if self.time_bound:
            self.init_time = time.time()
            self.current_time = self.init_time

    # return whether there are any remaining resources
    def are_exhausted(self):

        if self.iteration_bound:
            if self.iteration_count > self.iteration_bound:
                return True

        if self.time_bound:
            if self.current_time - self.init_time > self.time_bound:
                return True

        return False

    def update(self, cur_iteration= None, cur_time = None):

        if cur_iteration:
            self.iteration_count = cur_iteration
        else:
            self.iteration_count += 1

        if cur_time:
            self.current_time= cur_time
        else:
            self.current_time = time.localtime()

    def __str__(self):
        return '%s'%self.iteration_count