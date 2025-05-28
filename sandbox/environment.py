class GridEnvironment:
    """Simple 1D grid world where an agent seeks an object."""

    def __init__(self, size=5, object_pos=3):
        self.size = size
        self.object_pos = object_pos
        self.agent_pos = 0

    def get_percept(self):
        return 1 if self.agent_pos == self.object_pos else 0

    def take_action(self, action):
        if action == 'right' and self.agent_pos < self.size - 1:
            self.agent_pos += 1
        elif action == 'left' and self.agent_pos > 0:
            self.agent_pos -= 1

        percept = self.get_percept()
        reward = 1.0 if percept else 0.0
        done = percept == 1
        return percept, reward, done
