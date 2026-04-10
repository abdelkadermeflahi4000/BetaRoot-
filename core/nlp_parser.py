import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedInput:
    input_type: str
    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    raw_text: str = ""


class BetaRootParser:
    def parse(self, text: str) -> ParsedInput:
        text = text.strip()

        # إزالة علامات الاستفهام
        cleaned = text.replace("؟", "").replace("?", "").strip()

        # 1. سؤال حسابي
        if self._is_math_expression(cleaned):
            return ParsedInput(
                input_type="math",
                raw_text=cleaned
            )

        # 2. قاعدة عامة: كل البشر فانون
        match = re.match(r"كل\s+(.+)\s+(.+)", cleaned)
        if match:
            return ParsedInput(
                input_type="rule",
                subject=match.group(1).strip(),
                predicate="is",
                object=match.group(2).strip(),
                raw_text=text
            )

        # 3. حقيقة بسيطة: أرسطو بشر
        words = cleaned.split()
        if len(words) == 2:
            return ParsedInput(
                input_type="fact",
                subject=words[0],
                predicate="is",
                object=words[1],
                raw_text=text
            )

        # 4. سؤال: هل أرسطو فان
        if cleaned.startswith("هل"):
            question = cleaned.replace("هل", "").strip()
            words = question.split()

            if len(words) == 2:
                return ParsedInput(
                    input_type="query",
                    subject=words[0],
                    predicate="is",
                    object=words[1],
                    raw_text=text
                )

        return ParsedInput(
            input_type="unknown",
            raw_text=text
        )

    def _is_math_expression(self, text: str):
        return bool(re.fullmatch(r"[\d\s\+\-\*\/\%\(\)\.]+", text))
