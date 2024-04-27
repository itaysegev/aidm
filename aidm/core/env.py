from abc import ABC, abstractmethod


class Env(ABC):

    @abstractmethod
    def get_current_state(self):
        """

        """
        pass

    @abstractmethod
    def apply_action(self, action):
        """

        """
        pass

    @abstractmethod
    def set_state(self, state):
        """

        """
        pass

    def render(self):
        pass

    def apply_plan(self, plan, render=False):
        if render:
            self.render()
        for action in plan:
            self.apply_action(action)
            if render:
                self.render()

