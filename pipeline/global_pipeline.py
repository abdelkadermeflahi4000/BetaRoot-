class GlobalPipeline:
    def __init__(self, gf_engine, memory, reasoning):
        self.gf = gf_engine
        self.memory = memory
        self.reasoning = reasoning

    def execute(self, signal):
        output = self.gf.process(signal)

        tokens = output["tokens"]

        # store in memory
        self.memory.add_global_field_data(tokens)

        # reasoning step
        result = self.reasoning.reason_from_global_field(output)

        return {
            "tokens": tokens,
            "analysis": result
        }
