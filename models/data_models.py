from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import json


class LearningDimension(Enum):
    VISUAL = "visual"
    VERBAL = "verbal"
    LOGICAL = "logical"
    SOCIAL = "social"
    SOLITARY = "solitary"
    PRACTICAL = "practical"
    CONCEPTUAL = "conceptual"


@dataclass
class LearningStyleProfile:
    visual_score: float = 0.5
    verbal_score: float = 0.5
    logical_score: float = 0.5
    social_score: float = 0.5
    solitary_score: float = 0.5
    practical_score: float = 0.5
    conceptual_score: float = 0.5

    perception_score: float = 0.5
    retention_score: float = 0.5
    processing_score: float = 0.5

    dominant_dimension: Optional[LearningDimension] = None
    learning_preferences: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "visual_score": self.visual_score,
            "verbal_score": self.verbal_score,
            "logical_score": self.logical_score,
            "social_score": self.social_score,
            "solitary_score": self.solitary_score,
            "practical_score": self.practical_score,
            "conceptual_score": self.conceptual_score,
            "perception_score": self.perception_score,
            "retention_score": self.retention_score,
            "processing_score": self.processing_score,
            "dominant_dimension": self.dominant_dimension.value if self.dominant_dimension else None,
            "learning_preferences": self.learning_preferences
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'LearningStyleProfile':
        profile = cls(
            visual_score=data.get("visual_score", 0.5),
            verbal_score=data.get("verbal_score", 0.5),
            logical_score=data.get("logical_score", 0.5),
            social_score=data.get("social_score", 0.5),
            solitary_score=data.get("solitary_score", 0.5),
            practical_score=data.get("practical_score", 0.5),
            conceptual_score=data.get("conceptual_score", 0.5),
            perception_score=data.get("perception_score", 0.5),
            retention_score=data.get("retention_score", 0.5),
            processing_score=data.get("processing_score", 0.5),
            learning_preferences=data.get("learning_preferences", [])
        )
        if data.get("dominant_dimension"):
            profile.dominant_dimension = LearningDimension(data["dominant_dimension"])
        return profile

    def determine_dominant_dimension(self) -> LearningDimension:
        scores = {
            LearningDimension.VISUAL: self.visual_score,
            LearningDimension.VERBAL: self.verbal_score,
            LearningDimension.LOGICAL: self.logical_score,
            LearningDimension.SOCIAL: self.social_score,
            LearningDimension.SOLITARY: self.solitary_score,
            LearningDimension.PRACTICAL: self.practical_score,
            LearningDimension.CONCEPTUAL: self.conceptual_score
        }
        self.dominant_dimension = max(scores, key=scores.get)
        return self.dominant_dimension

    def get_content_preference(self) -> str:
        if self.visual_score > 0.7:
            return "image"
        elif self.verbal_score > 0.7:
            return "text"
        elif self.logical_score > 0.7:
            return "structure"
        else:
            return "mixed"


@dataclass
class StudentProfile:
    student_id: str
    name: str
    learning_style: LearningStyleProfile = field(default_factory=LearningStyleProfile)
    course_progress: Dict[str, float] = field(default_factory=dict)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    learning_history: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "learning_style": self.learning_style.to_dict(),
            "course_progress": self.course_progress,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "learning_history": self.learning_history
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'StudentProfile':
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            learning_style=LearningStyleProfile.from_dict(data.get("learning_style", {})),
            course_progress=data.get("course_progress", {}),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            learning_history=data.get("learning_history", [])
        )


@dataclass
class CourseContent:
    course_id: str
    title: str
    content_type: str
    difficulty: float
    topics: List[str]
    estimated_time: int
    prerequisites: List[str] = field(default_factory=list)
    related_materials: List[str] = field(default_factory=list)


@dataclass
class LearningSession:
    session_id: str
    student_id: str
    course_id: str
    topic: str
    activities: List[Dict] = field(default_factory=list)
    performance: float = 0.0
    engagement: float = 0.0
    timestamp: str = ""

    def add_activity(self, activity_type: str, content: Dict):
        self.activities.append({
            "type": activity_type,
            "content": content,
            "timestamp": self.timestamp
        })

    def calculate_performance(self) -> float:
        if not self.activities:
            return 0.0
        correct_count = sum(1 for a in self.activities if a.get("correct", False))
        return correct_count / len(self.activities) if self.activities else 0.0
