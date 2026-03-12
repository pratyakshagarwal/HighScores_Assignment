import math
import random
import logging
from typing import Optional
from bson import ObjectId
from app.database import questions_collection

logger = logging.getLogger(__name__)


def probability_correct(ability: float, difficulty: float, discrimination: float) -> float:
    return 1 / (1 + math.exp(-discrimination * (ability - difficulty)))


def update_ability(ability: float, correct: bool, question: dict) -> float:
    try:
        difficulty: float = question["difficulty"]
        discrimination: float = question["discrimination"]

        p = probability_correct(ability, difficulty, discrimination)
        result = 1 if correct else 0

        learning_rate = 0.3 / (1 + 0.5 * discrimination)
        new_ability = ability + learning_rate * discrimination * (result - p)

        return round(max(0.0, min(1.0, new_ability)), 4)

    except KeyError as e:
        logger.error(f"Missing field in question object: {e}")
        return ability
    except Exception as e:
        logger.error(f"Unexpected error in update_ability: {e}")
        return ability


def select_next_question(ability: float, answered_ids: list[ObjectId]) -> Optional[dict]:
    try:
        questions = list(
            questions_collection.find({"_id": {"$nin": answered_ids}})
        )

        if not questions:
            return None

        def question_score(q: dict) -> float:
            p = probability_correct(ability, q["difficulty"], q["discrimination"])
            information = (q["discrimination"] ** 2) * p * (1 - p)
            proximity_penalty = abs(q["difficulty"] - ability)
            return -information + 0.4 * proximity_penalty

        scored = sorted(questions, key=question_score)
        pool_size = min(3, len(scored))
        return random.choice(scored[:pool_size])

    except Exception as e:
        logger.error(f"Error selecting next question: {e}")
        return None