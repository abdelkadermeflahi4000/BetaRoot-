class SuperFrequencyPipeline:
    def __init__(self, router, fusion, osc_engine):
        self.router = router
        self.fusion = fusion
        self.osc = osc_engine

    def run(self, bio_signal, field_signal):

        bio = self.router.process(bio_signal, "biophoton")
        field = self.router.process(field_signal, "field")

        fused = self.fusion.fuse(bio, field)

        result = self.osc.ingest_tokens([
            {"f_bin": i, "amp": v} for i, v in enumerate(fused)
        ])

        return {
            "fused_state": fused,
            "osc_state": result
        }
