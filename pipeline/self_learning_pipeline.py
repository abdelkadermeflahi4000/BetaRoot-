class SelfLearningPipeline:
    def __init__(self, learner, reward_engine, memory):
        self.learner = learner
        self.reward_engine = reward_engine
        self.memory = memory

    def run(self, tokens):

        # forward pass
        state = self.learner.forward(tokens)

        # reward computation
        reward = self.reward_engine.evaluate(state)

        # learning update
        self.learner.update(tokens, reward)

        # memory storage
        self.memory.store(tokens, state, reward)

        # decay (forget noise over time)
        self.learner.decay()

        return {
            "state": state.tolist(),
            "reward": reward,
            "weights": self.learner.weights.tolist()
        }
