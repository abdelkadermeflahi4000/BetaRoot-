class BetaNode:
    """ تمثيل لفرضية علمية داخل الوعاء الموحد """
    def __init__(self, name, prior_alpha=1, prior_beta=1):
        self.name = name
        self.alpha = prior_alpha
        self.beta = prior_beta

    def observe(self, evidence):
        """ تحديث استقرائي بناءً على ملاحظة جديدة (0 أو 1) """
        if evidence == 1:
            self.alpha += 1  # تأكيد (Confirmation)
        else:
            self.beta += 1   # تفنيد (Falsification)

    def certainty(self):
        """ تحويل الحالة الاحتمالية إلى قيمة منطقية (0 إلى 1) """
        return self.alpha / (self.alpha + self.beta)

# مثال للدمج:
hypothesis = BetaNode("Water Boils at 100C")
# ملاحظات تجريبية
observations = [1, 1, 0, 1] # 3 نجاحات وفشل واحد (ربما بسبب الضغط)
for obs in observations:
    hypothesis.observe(obs)

print(f"قيمة اليقين المنطقي في المشروع: {hypothesis.certainty():.2f}")
