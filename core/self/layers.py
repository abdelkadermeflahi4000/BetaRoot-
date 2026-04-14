# core/self/layers.py

class SelfLayers:

    def layer1_awareness(self, state):
        return {"last_action": state.get("last_action")}

    def layer2_reflection(self, l1):
        action = l1.get("last_action")

        if action == "EXPLORE":
            return {"reason": "seeking novelty"}

        if action == "ANALYZE":
            return {"reason": "seeking structure"}

        return {"reason": "unknown"}

    def layer3_meta(self, l2):
        reason = l2.get("reason")

        if reason == "seeking novelty":
            return {"strategy": "increase exploration"}

        if reason == "seeking structure":
            return {"strategy": "increase reasoning"}

        return {"strategy": "neutral"}

    def layer4_recursive(self, l3):
        strategy = l3.get("strategy")

        # هنا النظام يبدأ يشك في نفسه
        if strategy == "increase exploration":
            return {"meta_judgment": "too chaotic?"}

        if strategy == "increase reasoning":
            return {"meta_judgment": "too rigid?"}

        return {"meta_judgment": "uncertain"}

class SelfLayers:

    def layer1_awareness(self, state):
        return {"last_action": state.get("last_action")}

    def layer2_reflection(self, l1):
        action = l1.get("last_action")

        if action == "EXPLORE":
            return {"reason": "seeking novelty"}

        if action == "ANALYZE":
            return {"reason": "seeking structure"}

        return {"reason": "unknown"}

    def layer3_meta(self, l2):
        reason = l2.get("reason")

        if reason == "seeking novelty":
            return {"strategy": "increase exploration"}

        if reason == "seeking structure":
            return {"strategy": "increase reasoning"}

        return {"strategy": "neutral"}

    def layer4_recursive(self, l3):
        strategy = l3.get("strategy")

        # هنا النظام يبدأ يشك في نفسه
        if strategy == "increase exploration":
            return {"meta_judgment": "too chaotic?"}

        if strategy == "increase reasoning":
            return {"meta_judgment": "too rigid?"}

        return {"meta_judgment": "uncertain"}
