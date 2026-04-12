class GlobalFieldMemoryMixin:
    def add_global_field_data(self, tokens):
        for t in tokens:
            self.storage[str(len(self.storage))] = {
                "content": f"GF token freq_bin={t['freq_bin']} amp={t['amplitude']}",
                "type": "global_field",
                "mode": "alpha",
                "confidence": 0.4,
                "metadata": {
                    "stability_weight": t.get("stability_weight", 0.0)
                }
            }
