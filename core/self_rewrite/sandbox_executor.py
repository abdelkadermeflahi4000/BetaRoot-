# core/self_rewrite/sandbox_executor.py

class SandboxExecutor:

    def test(self, state, patch):
        test_state = state.copy()

        if patch["operation"] == "increase":
            test_state[patch["target"]] *= patch["factor"]
        else:
            test_state[patch["target"]] /= patch["factor"]

        return test_state
