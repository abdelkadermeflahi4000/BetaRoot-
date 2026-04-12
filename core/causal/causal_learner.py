class CausalLearner:
    def __init__(self, graph, extractor):
        self.graph = graph
        self.extractor = extractor
        self.last_tokens = None

    # -------------------------
    # main learning step
    # -------------------------
    def update(self, tokens):

        causal_links = self.extractor.extract(self.last_tokens, tokens)

        # if first step
        if self.last_tokens is None:
            self.last_tokens = tokens
            return {"status": "initialized"}

        # register causal relations
        for link in causal_links:
            cause = f"f_bin_{link[0]}"
            effect = f"delta_{np.sign(link[1])}"

            self.graph.observe(cause, effect, abs(link[1]))

        self.graph.decay_graph()
        self.graph.normalize()

        self.last_tokens = tokens

        return {
            "causal_links": causal_links,
            "graph_size": len(self.graph.graph)
        }
