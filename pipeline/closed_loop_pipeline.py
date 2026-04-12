class ClosedLoopPipeline:
    def __init__(self, core):
        self.core = core

    def run(self, state, prediction, timestamp):

        output = self.core.step(state, prediction, timestamp)

        # recursive feedback (key idea)
        meta = output["meta_reflection"]

        if meta["reflection"] < 0:
            mode = "adaptive_rewrite"
        elif meta["stability"] < 0.3:
            mode = "exploration"
        else:
            mode = "convergent_reasoning"

        output["mode"] = mode

        return output
