class TaskDecomposer:
    def decompose(self, task):
        """
        يحول مهمة كبيرة إلى مهام صغيرة
        """

        subject = task.get("subject")

        return [
            {"type": "reason", "task": task},
            {"type": "explore", "task": task},
            {"type": "critic", "task": task}
        ]
