"""
FSE Experience Learning Engine V2

Production learning layer for autonomous systems.

Responsibilities:
- Convert memory records into learning experiences
- Detect repeat and avoid patterns
- Track learning confidence
- Maintain structured learning history
"""

from copy import deepcopy


class ExperienceLearningEngineV2:
    """
    Production-ready experience learning engine.
    """

    def __init__(self):

        self.experiences = []
        self.learning_cycles = 0
        self.patterns = {
            "strong": 0,
            "weak": 0
        }


    def learn(self, memory_record):

        if not isinstance(memory_record, dict):
            raise TypeError(
                "memory_record must be a dictionary"
            )


        self.learning_cycles += 1


        result = memory_record.get(
            "result",
            "UNKNOWN"
        )


        lesson = self._create_lesson(
            result
        )


        experience = {

            "cycle":
                self.learning_cycles,

            "symbol":
                memory_record.get("symbol"),

            "decision":
                memory_record.get("decision"),

            "confidence":
                memory_record.get(
                    "confidence",
                    0
                ),

            "result":
                result,

            "lesson":
                lesson
        }


        self._update_patterns(
            lesson
        )


        self.experiences.append(
            experience
        )


        return {
            "status": "LEARNED",
            "experience": deepcopy(experience)
        }


    def _create_lesson(self, result):

        if result == "WIN":
            return "REPEAT_PATTERN"

        if result == "LOSS":
            return "AVOID_PATTERN"

        return "UNKNOWN"



    def _update_patterns(self, lesson):

        if lesson == "REPEAT_PATTERN":
            self.patterns["strong"] += 1

        elif lesson == "AVOID_PATTERN":
            self.patterns["weak"] += 1



    def knowledge_update(self):

        return {

            "strong_patterns":
                self.patterns["strong"],

            "weak_patterns":
                self.patterns["weak"],

            "learning_cycles":
                self.learning_cycles
        }



    def history(self):

        return deepcopy(
            self.experiences
        )


    def state(self):

        return {

            "experiences":
                len(self.experiences),

            "cycles":
                self.learning_cycles,

            "patterns":
                deepcopy(self.patterns)
        }
