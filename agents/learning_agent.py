class LearningAgent:
    def __init__(self, learner):
        self.learner = learner

    def execute(self, query, answers):
        return self.learner.learn(query, answers)
