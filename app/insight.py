import logging
import os
from collections import defaultdict
from typing import Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import LangChainException

load_dotenv()

logger = logging.getLogger(__name__)

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY is not set in environment variables.")

llm = ChatGroq(model=GROQ_MODEL, temperature=0.7, api_key=GROQ_API_KEY)

prompt_template = PromptTemplate.from_template("""
You are an expert tutor analyzing a student's adaptive test results. Based on the data below, generate a personalized, detailed study plan.

=== STUDENT PERFORMANCE SUMMARY ===

Overall Ability Score: {ability} / 1.0  (0=beginner, 1=expert)
Ability Trend: {ability_trend}
Performance Consistency: {consistency}

Correct Answers: {total_correct} / {total_attempted} ({overall_accuracy}% accuracy)
Best Streak: {max_streak} consecutive correct answers
Average Question Difficulty Attempted: {avg_difficulty} / 1.0

=== TOPIC BREAKDOWN ===
{topic_breakdown}

=== QUESTION-BY-QUESTION HISTORY ===
{question_history}

=== WEAK AREAS ===
{weak_topics}

=== STRONG AREAS ===
{strong_topics}

---

Based on this data, provide:
1. A brief 2-3 sentence honest assessment of this student's current level and learning pattern
2. A prioritized 5-step study plan targeting weak areas (be specific — mention concepts, not just topic names)
3. One practical daily study tip based on their consistency score and streak pattern
4. An estimated timeline to reach ability score 0.8+ if they follow the plan

Be direct, specific, and encouraging. No fluff.
""")

chain = prompt_template | llm


def analyze_session(history: list[dict]) -> tuple[dict, list[str], list[str]]:
    if not history:
        logger.warning("analyze_session called with empty history.")
        return {}, [], []

    topic_stats: dict = defaultdict(lambda: {"attempted": 0, "correct": 0, "difficulties": []})

    for h in history:
        try:
            topic = h["topic"]
            topic_stats[topic]["attempted"] += 1
            topic_stats[topic]["difficulties"].append(h["difficulty"])
            if h["correct"]:
                topic_stats[topic]["correct"] += 1
        except KeyError as e:
            logger.warning(f"Skipping malformed history entry, missing key: {e}")
            continue

    topic_accuracy: dict = {}
    for topic, stat in topic_stats.items():
        acc = stat["correct"] / stat["attempted"]
        topic_accuracy[topic] = {
            "accuracy": round(acc, 2),
            "attempted": stat["attempted"],
            "correct": stat["correct"],
            "avg_difficulty": round(sum(stat["difficulties"]) / len(stat["difficulties"]), 2)
        }

    sorted_topics = sorted(topic_accuracy.items(), key=lambda x: x[1]["accuracy"])
    weak_topics: list[str] = [t[0] for t in sorted_topics[:2]]
    strong_topics: list[str] = [t[0] for t in sorted_topics[-2:] if t[1]["accuracy"] >= 0.6]

    return topic_accuracy, weak_topics, strong_topics


def generate_study_plan(session: dict) -> str:
    try:
        history: list[dict] = session.get("history", [])
        ability: float = round(session.get("ability", 0.5), 3)
        trajectory: list[float] = session.get("ability_trajectory", [ability])
        total_correct: int = session.get("total_correct", 0)
        total_attempted: int = session.get("total_attempted", 0)
        max_streak: int = session.get("max_streak", 0)
        avg_difficulty: float = session.get("avg_difficulty_attempted", 0.0)
        variance: float = session.get("ability_variance", 0.0)

        topic_accuracy, weak_topics, strong_topics = analyze_session(history)

        if len(trajectory) >= 3:
            delta = trajectory[-1] - trajectory[0]
            if delta > 0.1:
                ability_trend = f"Improving (+{round(delta, 2)} overall)"
            elif delta < -0.1:
                ability_trend = f"Declining ({round(delta, 2)} overall)"
            else:
                ability_trend = "Stable (minimal change)"
        else:
            ability_trend = "Not enough data"

        consistency = (
            "Consistent" if variance < 0.02
            else "Inconsistent" if variance > 0.05
            else "Moderately consistent"
        )
        overall_accuracy: int = round((total_correct / total_attempted) * 100) if total_attempted else 0

        topic_breakdown_lines: list[str] = []
        for topic, stats in topic_accuracy.items():
            topic_breakdown_lines.append(
                f"  - {topic}: {stats['correct']}/{stats['attempted']} correct "
                f"({int(stats['accuracy'] * 100)}%) | avg difficulty {stats['avg_difficulty']}"
            )
        topic_breakdown = "\n".join(topic_breakdown_lines) or "No data"

        history_lines: list[str] = []
        for i, h in enumerate(history[-10:], 1):
            status = "✓" if h["correct"] else "✗"
            history_lines.append(
                f"  Q{i}: [{status}] Topic={h['topic']} | "
                f"Difficulty={h['difficulty']} | Ability after={h.get('ability_after', '?')}"
            )
        question_history = "\n".join(history_lines) or "No history"

        response = chain.invoke({
            "ability": ability,
            "ability_trend": ability_trend,
            "consistency": consistency,
            "total_correct": total_correct,
            "total_attempted": total_attempted,
            "overall_accuracy": overall_accuracy,
            "max_streak": max_streak,
            "avg_difficulty": avg_difficulty,
            "topic_breakdown": topic_breakdown,
            "question_history": question_history,
            "weak_topics": ", ".join(weak_topics) or "None identified",
            "strong_topics": ", ".join(strong_topics) or "None identified",
        })

        return response.content

    except LangChainException as e:
        logger.error(f"LLM chain error in generate_study_plan: {e}")
        return "Study plan could not be generated. Please try again."
    except Exception as e:
        logger.error(f"Unexpected error in generate_study_plan: {e}")
        return "Study plan could not be generated due to an unexpected error."