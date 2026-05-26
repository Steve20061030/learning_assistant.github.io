from models.data_models import LearningStyleProfile, CourseContent, LearningSession, LearningDimension
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random


class ActivityType(Enum):
    INTRODUCTION = "introduction"
    CONCEPT_EXPLANATION = "concept_explanation"
    EXAMPLE_DEMONSTRATION = "example_demonstration"
    PRACTICE_EXERCISE = "practice_exercise"
    QUIZ = "quiz"
    DISCUSSION = "discussion"
    REVISION = "revision"
    ASSESSMENT = "assessment"


@dataclass
class LearningActivity:
    activity_id: str
    activity_type: ActivityType
    title: str
    content: str
    difficulty: float
    estimated_time: int
    adaptive_content: Dict = None
    feedback: Optional[str] = None

    def __post_init__(self):
        if self.adaptive_content is None:
            self.adaptive_content = {}


@dataclass
class LearningPath:
    path_id: str
    course_id: str
    activities: List[LearningActivity]
    current_index: int = 0
    completed_activities: List[str] = None

    def __post_init__(self):
        if self.completed_activities is None:
            self.completed_activities = []


class AdaptiveLearningEngine:
    def __init__(self):
        self.activity_templates: Dict[str, List[LearningActivity]] = {}
        self.difficulty_levels = {
            "easy": 0.3,
            "medium": 0.5,
            "hard": 0.7,
            "expert": 0.9
        }

    def generate_adaptive_path(
        self,
        course_content: CourseContent,
        student_profile: LearningStyleProfile,
        target_topics: List[str]
    ) -> LearningPath:
        import uuid
        path_id = f"path_{course_content.course_id}_{uuid.uuid4().hex[:8]}"
        activities = []

        for topic in target_topics:
            topic_activities = self._generate_topic_activities(topic, student_profile)
            activities.extend(topic_activities)

        activities = self._optimize_path_order(activities, student_profile)

        return LearningPath(
            path_id=path_id,
            course_id=course_content.course_id,
            activities=activities
        )

    def _generate_topic_activities(
        self,
        topic: str,
        profile: LearningStyleProfile
    ) -> List[LearningActivity]:
        activities = []

        activities.append(LearningActivity(
            activity_id=f"{topic}_intro",
            activity_type=ActivityType.INTRODUCTION,
            title=f"Introduction: {topic}",
            content=self._generate_adaptive_introduction(topic, profile),
            difficulty=0.2,
            estimated_time=5,
            adaptive_content=self._get_adaptive_content_config(profile)
        ))

        activities.append(LearningActivity(
            activity_id=f"{topic}_concept",
            activity_type=ActivityType.CONCEPT_EXPLANATION,
            title=f"Concept: {topic}",
            content=self._generate_adaptive_explanation(topic, profile),
            difficulty=0.5,
            estimated_time=15,
            adaptive_content=self._get_adaptive_content_config(profile)
        ))

        activities.append(LearningActivity(
            activity_id=f"{topic}_example",
            activity_type=ActivityType.EXAMPLE_DEMONSTRATION,
            title=f"Example: {topic}",
            content=self._generate_adaptive_example(topic, profile),
            difficulty=0.4,
            estimated_time=10,
            adaptive_content=self._get_adaptive_content_config(profile)
        ))

        activities.append(LearningActivity(
            activity_id=f"{topic}_practice",
            activity_type=ActivityType.PRACTICE_EXERCISE,
            title=f"Practice: {topic}",
            content=self._generate_adaptive_practice(topic, profile),
            difficulty=self._calculate_difficulty(profile),
            estimated_time=20,
            adaptive_content=self._get_adaptive_content_config(profile)
        ))

        return activities

    def _generate_adaptive_introduction(self, topic: str, profile: LearningStyleProfile) -> str:
        if profile.dominant_dimension == LearningDimension.VISUAL:
            return f"""[VISUAL] {topic} - Visual Introduction

[Graphical Introduction]
Let's understand {topic} through an vivid image:

[AI generates relevant diagram here]

[Key Features]
* First point...
* Second point...
* Third point...

[Preview Questions]
1. Where have you encountered this concept before?
2. What problem do you think it mainly solves?"""
        elif profile.dominant_dimension == LearningDimension.VERBAL:
            return f"""[VERBAL] {topic} - Text Introduction

[Concept Definition]
{topic} is... (AI generates detailed definition here)

[Background Knowledge]
Before diving in, let's understand some background...

[Learning Objectives]
After completing this section, you will be able to:
* Understand the core concept of {topic}
* Master basic application methods
* Build foundation for subsequent learning"""
        elif profile.dominant_dimension == LearningDimension.LOGICAL:
            return f"""[LOGICAL] {topic} - Logical Framework

[Formal Definition]
Definition: {topic} <- (AI generates mathematical definition here)

[Logical Structure]
A -> B -> C -> D
That is: ... (AI generates derivation process here)

[Core Principles]
Principle 1: ...
Principle 2: ..."""
        elif profile.dominant_dimension == LearningDimension.PRACTICAL:
            return f"""[PRACTICAL] {topic} - Practice-Oriented

[Real-World Applications]
{topic} has wide applications in real life:
* Scenario 1: ...
* Scenario 2: ...

[Hands-On Try]
Let's start with a simple example to practice...

[Prerequisites]
Need to master first: ..."""
        else:
            return f"""[MIXED] {topic} - Comprehensive Learning

[Overview]
{topic} is an important concept, and we will learn it from multiple perspectives.

[Learning Path]
1. First build intuitive understanding
2. Then deeply understand principles
3. Finally apply in practice"""

    def _generate_adaptive_explanation(self, topic: str, profile: LearningStyleProfile) -> str:
        base_explanation = f"Core content explanation about {topic}"

        if profile.visual_score > 0.6:
            return f"""{base_explanation}

[Diagram Explanation]
[AI-generated diagram showing {topic}'s structure and relationships]

[Key Points]
* Components: -> Show structure diagram
* Workflow: -> Show flowchart
* Key Features: -> Show comparison chart"""
        elif profile.verbal_score > 0.6:
            return f"""{base_explanation}

[Detailed Explanation]
{topic} involves the following important aspects:

First aspect: ...
This is because... (AI generates detailed explanation here)

Second aspect: ...
Specifically... (AI generates in-depth analysis here)

[Terminology]
* Term 1: Definition
* Term 2: Definition"""
        elif profile.logical_score > 0.6:
            return f"""{base_explanation}

[Logical Derivation]
Given condition A...
-> Derivation step 1...
-> Derivation step 2...
-> Conclusion...

[Proof Process]
Theorem: Core theorem related to {topic}
Proof: ..."""
        else:
            return base_explanation

    def _generate_adaptive_example(self, topic: str, profile: LearningStyleProfile) -> str:
        if profile.practical_score > 0.6:
            return f"""[Practical Case]
Case background: ...
Steps:
1. First step...
2. Second step...
3. Third step...

[Code Implementation]
```python
# AI generates example code here
def example():
    pass
```

[Output]
-> Output: ..."""
        else:
            return f"""[Typical Examples]
Example 1: ...
Analysis: ...

Example 2: ...
Analysis: ..."""

    def _generate_adaptive_practice(self, topic: str, profile: LearningStyleProfile) -> str:
        difficulty = self._calculate_difficulty(profile)

        if profile.practical_score > 0.6:
            return f"""[Practice Exercise]
Basic Task (Difficulty: {difficulty:.1f})

Task Description:
Please implement a function to complete...

[Reference Hints]
Hint 1: ...
Hint 2: ...

[Submission Requirements]
* Code standards
* Include test cases"""
        elif profile.logical_score > 0.6:
            return f"""[Logical Reasoning]
1. Given conditions A, B, prove conclusion C

2. Analyze the validity of the following logical relationship:
   A -> B
   B -> C
   Therefore A -> C

3. Calculate and verify: ..."""
        else:
            return f"""[Consolidation Exercise]
Multiple Choice:
1. What are the core characteristics of {topic}?
   A. ... B. ... C. ...

2. Which of the following statements about {topic} is correct?
   A. ... B. ... C. ..."""

    def _get_adaptive_content_config(self, profile: LearningStyleProfile) -> Dict:
        return {
            "include_diagrams": profile.visual_score > 0.5,
            "include_code": profile.practical_score > 0.5,
            "include_proofs": profile.logical_score > 0.5,
            "include_examples": True,
            "detail_level": "high" if profile.verbal_score > 0.5 else "medium",
            "interactive_elements": profile.practical_score > 0.6
        }

    def _calculate_difficulty(self, profile: LearningStyleProfile) -> float:
        base_difficulty = 0.5

        if profile.processing_score > 0.7:
            base_difficulty = 0.7
        elif profile.processing_score < 0.4:
            base_difficulty = 0.4

        if profile.logical_score > 0.7:
            base_difficulty += 0.1

        return min(1.0, max(0.1, base_difficulty))

    def _optimize_path_order(
        self,
        activities: List[LearningActivity],
        profile: LearningStyleProfile
    ) -> List[LearningActivity]:
        if profile.dominant_dimension == LearningDimension.CONCEPTUAL:
            conceptual_first = [a for a in activities if a.activity_type == ActivityType.CONCEPT_EXPLANATION]
            others = [a for a in activities if a.activity_type != ActivityType.CONCEPT_EXPLANATION]
            return conceptual_first + others
        elif profile.practical_score > 0.7:
            practice_first = [a for a in activities if a.activity_type == ActivityType.PRACTICE_EXERCISE]
            others = [a for a in activities if a.activity_type != ActivityType.PRACTICE_EXERCISE]
            return others[:2] + practice_first + others[2:]
        return activities

    def evaluate_activity_performance(
        self,
        activity: LearningActivity,
        response: Dict,
        profile: LearningStyleProfile
    ) -> Tuple[float, Dict]:
        score = 0.0
        feedback = {}
        correct_answers = response.get("correct_answers", 0)
        total_questions = response.get("total_questions", 1)

        score = correct_answers / total_questions if total_questions > 0 else 0.0

        if score < 0.6:
            feedback["level"] = "Needs Improvement"
            feedback["suggestion"] = self._generate_remediation_suggestion(activity, profile)
            feedback["next_activity"] = "revision"
        elif score < 0.8:
            feedback["level"] = "Basic Mastery"
            feedback["suggestion"] = "Continue practicing to consolidate understanding"
            feedback["next_activity"] = "practice"
        else:
            feedback["level"] = "Excellent"
            feedback["suggestion"] = "Consider challenging harder content"
            feedback["next_activity"] = "advance"

        return score, feedback

    def _generate_remediation_suggestion(
        self,
        activity: LearningActivity,
        profile: LearningStyleProfile
    ) -> str:
        suggestions = []

        if profile.visual_score > 0.6:
            suggestions.append("Recommend watching diagram videos or creating mind maps")
        if profile.verbal_score > 0.6:
            suggestions.append("Recommend detailed reading and note-taking")
        if profile.practical_score > 0.6:
            suggestions.append("Recommend starting with simpler examples for hands-on practice")

        return ". ".join(suggestions) if suggestions else "Recommend reviewing related concepts before trying again"

    def adapt_next_activity(
        self,
        current_activity: LearningActivity,
        performance: float,
        profile: LearningStyleProfile,
        remaining_activities: List[LearningActivity]
    ) -> Optional[LearningActivity]:
        if not remaining_activities:
            return None

        if performance < 0.6:
            similar_easier = self._find_similar_easier_activity(
                current_activity, remaining_activities
            )
            if similar_easier:
                return similar_easier

        if performance > 0.85 and remaining_activities:
            harder = self._find_harder_activity(current_activity, remaining_activities)
            if harder:
                return harder

        return remaining_activities[0] if remaining_activities else None

    def _find_similar_easier_activity(
        self,
        current: LearningActivity,
        pool: List[LearningActivity]
    ) -> Optional[LearningActivity]:
        topic = current.activity_id.split("_")[0]
        similar = [a for a in pool if a.activity_id.startswith(topic) and a.difficulty < current.difficulty]
        return similar[0] if similar else None

    def _find_harder_activity(
        self,
        current: LearningActivity,
        pool: List[LearningActivity]
    ) -> Optional[LearningActivity]:
        topic = current.activity_id.split("_")[0]
        similar = [a for a in pool if a.activity_id.startswith(topic) and a.difficulty > current.difficulty]
        return similar[0] if similar else None
