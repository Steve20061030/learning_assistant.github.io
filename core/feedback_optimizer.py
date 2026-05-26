from models.data_models import LearningStyleProfile, LearningSession, LearningDimension
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import random


@dataclass
class FeedbackItem:
    feedback_id: str
    feedback_type: str
    content: str
    timestamp: str
    severity: str
    actionable: bool

    def to_dict(self) -> Dict:
        return {
            "feedback_id": self.feedback_id,
            "feedback_type": self.feedback_type,
            "content": self.content,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "actionable": self.actionable
        }


@dataclass
class LearningAnalytics:
    total_sessions: int = 0
    total_time_spent: int = 0
    average_performance: float = 0.0
    topic_mastery: Dict[str, float] = None
    learning_efficiency: float = 0.0
    engagement_trend: List[float] = None
    weakness_areas: List[str] = None

    def __post_init__(self):
        if self.topic_mastery is None:
            self.topic_mastery = {}
        if self.engagement_trend is None:
            self.engagement_trend = []
        if self.weakness_areas is None:
            self.weakness_areas = []


class FeedbackOptimizationSystem:
    def __init__(self):
        self.feedback_history: List[FeedbackItem] = []
        self.analytics = LearningAnalytics()

    def analyze_session_performance(
        self,
        session: LearningSession,
        profile: LearningStyleProfile
    ) -> Dict:
        performance_metrics = {
            "overall_score": session.calculate_performance(),
            "activity_breakdown": {},
            "time_efficiency": 0.0,
            "engagement_level": session.engagement,
            "recommendations": []
        }

        activity_types: Dict[str, List] = {}
        for activity in session.activities:
            atype = activity.get("type", "unknown")
            if atype not in activity_types:
                activity_types[atype] = []
            activity_types[atype].append(activity.get("correct", False))

        for atype, results in activity_types.items():
            if results:
                performance_metrics["activity_breakdown"][atype] = {
                    "attempts": len(results),
                    "correct_rate": sum(results) / len(results)
                }

        total_time = sum(a.get("engagement_time", 0) for a in session.activities)
        if total_time > 0 and session.calculate_performance() > 0:
            performance_metrics["time_efficiency"] = session.calculate_performance() / (total_time / 60)

        performance_metrics["recommendations"] = self._generate_performance_recommendations(
            performance_metrics, profile
        )

        return performance_metrics

    def _generate_performance_recommendations(
        self,
        metrics: Dict,
        profile: LearningStyleProfile
    ) -> List[str]:
        recommendations = []

        if metrics["overall_score"] < 0.6:
            if profile.dominant_dimension == LearningDimension.VISUAL:
                recommendations.append("Recommend using more diagrams and visual materials to aid understanding")
            elif profile.dominant_dimension == LearningDimension.VERBAL:
                recommendations.append("Recommend detailed textbook reading and note-taking")
            elif profile.dominant_dimension == LearningDimension.PRACTICAL:
                recommendations.append("Recommend starting from more basic exercises, progressing gradually")

        activity_breakdown = metrics.get("activity_breakdown", {})
        weak_activities = [k for k, v in activity_breakdown.items() if v["correct_rate"] < 0.6]
        if weak_activities:
            recommendations.append(f"Needs improvement: {', '.join(weak_activities)}")

        if metrics.get("time_efficiency", 0) < 0.5:
            recommendations.append("Learning efficiency has room for improvement, suggest reducing interruptions and focusing")

        return recommendations

    def generate_adaptive_feedback(
        self,
        exercise_result: Dict,
        profile: LearningStyleProfile
    ) -> FeedbackItem:
        feedback_type = self._determine_feedback_type(exercise_result)
        content = self._compose_feedback_content(exercise_result, profile, feedback_type)

        feedback = FeedbackItem(
            feedback_id=f"fb_{datetime.now().timestamp()}",
            feedback_type=feedback_type,
            content=content,
            timestamp=datetime.now().isoformat(),
            severity=self._determine_severity(exercise_result),
            actionable=exercise_result.get("correct", False) is not None
        )

        self.feedback_history.append(feedback)
        return feedback

    def _determine_feedback_type(self, result: Dict) -> str:
        if not result.get("correct", True):
            return "error_analysis"
        elif result.get("score", 0) < 0.7:
            return "improvement_suggestion"
        elif result.get("score", 0) >= 0.9:
            return "achievement"
        else:
            return "encouragement"

    def _compose_feedback_content(
        self,
        result: Dict,
        profile: LearningStyleProfile,
        feedback_type: str
    ) -> str:
        if feedback_type == "error_analysis":
            return self._compose_error_feedback(result, profile)
        elif feedback_type == "improvement_suggestion":
            return self._compose_improvement_feedback(result, profile)
        elif feedback_type == "achievement":
            return self._compose_achievement_feedback(result, profile)
        else:
            return self._compose_encouragement_feedback(result, profile)

    def _compose_error_feedback(self, result: Dict, profile: LearningStyleProfile) -> str:
        base_message = "After analyzing your answer, the following issues were found:\n\n"

        if profile.dominant_dimension == LearningDimension.VISUAL:
            visual_tip = "\n[VISUAL TIP] Recommend drawing a simple diagram to help analyze this problem"
            detailed = f"\n[DETAILED] {result.get('explanation', 'Please refer to the correct answer for analysis')}"
            return base_message + visual_tip + detailed

        elif profile.dominant_dimension == LearningDimension.LOGICAL:
            logic_tip = "\n[LOGICAL TIP] Try analyzing this problem step by step"
            detailed = f"\n[DERIVATION] {result.get('explanation', 'Please derive again')}"
            return base_message + logic_tip + detailed

        elif profile.dominant_dimension == LearningDimension.PRACTICAL:
            practice_tip = "\n[PRACTICAL TIP] The key to this problem is hands-on practice, try writing code implementation"
            return base_message + practice_tip

        else:
            return f"{base_message}Please review related knowledge points before trying again"

    def _compose_improvement_feedback(self, result: Dict, profile: LearningStyleProfile) -> str:
        score = result.get("score", 0)
        improvement = "\n[IMPROVEMENT] "

        if profile.dominant_dimension == LearningDimension.CONCEPTUAL:
            return f"{improvement}Recommend comparing related concepts to find connections and differences"

        if profile.practical_score > 0.6:
            return f"{improvement}Recommend doing more exercises to consolidate understanding"

        return f"{improvement}Current accuracy is {score:.0%}, keep going!"

    def _compose_achievement_feedback(self, result: Dict, profile: LearningStyleProfile) -> str:
        achievements = [
            "Great job! Your performance is outstanding!",
            "Excellent! Keep up this momentum!",
            "Perfect score! You are a learning expert!",
            "Outstanding work! Shows deep understanding of the material!"
        ]
        base = random.choice(achievements)

        if profile.dominant_dimension == LearningDimension.VISUAL:
            return f"{base}\n\nYour visual thinking ability is strong!"
        elif profile.dominant_dimension == LearningDimension.LOGICAL:
            return f"{base}\n\nYour logical reasoning ability is excellent!"

        return base

    def _compose_encouragement_feedback(self, result: Dict, profile: LearningStyleProfile) -> str:
        encouragements = [
            "Good job! Keep it up!",
            "Nice start, keep it up!",
            "Making progress!"
        ]
        base = random.choice(encouragements)

        tips = []
        if profile.visual_score > 0.6:
            tips.append("Try organizing your thoughts with diagrams")
        if profile.practical_score > 0.6:
            tips.append("More hands-on practice will help")

        if tips:
            return f"{base}\n\nSmall suggestions: {', '.join(tips)}"
        return base

    def _determine_severity(self, result: Dict) -> str:
        score = result.get("score", 1.0)
        if score < 0.4:
            return "high"
        elif score < 0.7:
            return "medium"
        return "low"

    def track_learning_progress(
        self,
        student_id: str,
        sessions: List[LearningSession]
    ) -> LearningAnalytics:
        analytics = LearningAnalytics()

        analytics.total_sessions = len(sessions)
        analytics.total_time_spent = sum(
            sum(a.get("engagement_time", 0) for a in s.activities)
            for s in sessions
        )

        if sessions:
            performances = [s.calculate_performance() for s in sessions]
            analytics.average_performance = sum(performances) / len(performances)

        topic_scores: Dict[str, List[float]] = {}
        for session in sessions:
            for activity in session.activities:
                topic = activity.get("topic", "unknown")
                if topic not in topic_scores:
                    topic_scores[topic] = []
                topic_scores[topic].append(1.0 if activity.get("correct") else 0.0)

        analytics.topic_mastery = {
            topic: sum(scores) / len(scores) if scores else 0.0
            for topic, scores in topic_scores.items()
        }

        analytics.weakness_areas = [
            topic for topic, score in analytics.topic_mastery.items()
            if score < 0.6
        ]

        analytics.learning_efficiency = self._calculate_efficiency(sessions)

        if len(sessions) >= 3:
            recent = [s.calculate_performance() for s in sessions[-3:]]
            analytics.engagement_trend = recent

        return analytics

    def _calculate_efficiency(self, sessions: List[LearningSession]) -> float:
        if not sessions:
            return 0.0

        total_correct = sum(
            sum(1 for a in s.activities if a.get("correct"))
            for s in sessions
        )
        total_attempts = sum(len(s.activities) for s in sessions)

        return total_correct / total_attempts if total_attempts > 0 else 0.0

    def suggest_learning_adjustments(
        self,
        analytics: LearningAnalytics,
        profile: LearningStyleProfile
    ) -> List[str]:
        adjustments = []

        if analytics.learning_efficiency < 0.6:
            adjustments.append("Recommend using Pomodoro technique to improve focus")

        if analytics.weakness_areas:
            adjustments.append(f"Key review areas: {', '.join(analytics.weakness_areas)}")
            adjustments.append("Recommend using spaced repetition for weak knowledge points")

        if profile.dominant_dimension == LearningDimension.VISUAL:
            adjustments.append("Recommend using mind map tools to organize knowledge structure")

        if profile.processing_score > 0.7:
            adjustments.append("Your learning speed is fast, can try challenging harder content")

        if len(analytics.engagement_trend) >= 3:
            if analytics.engagement_trend[-1] < analytics.engagement_trend[0]:
                adjustments.append("Recent learning effectiveness has declined, recommend adjusting learning methods")

        return adjustments

    def generate_progress_report(
        self,
        student_id: str,
        sessions: List[LearningSession],
        profile: LearningStyleProfile
    ) -> Dict:
        analytics = self.track_learning_progress(student_id, sessions)
        adjustments = self.suggest_learning_adjustments(analytics, profile)

        report = {
            "student_id": student_id,
            "report_date": datetime.now().isoformat(),
            "summary": {
                "total_sessions": analytics.total_sessions,
                "total_time_minutes": analytics.total_time_spent,
                "average_score": round(analytics.average_performance * 100, 1),
                "learning_efficiency": round(analytics.learning_efficiency * 100, 1)
            },
            "topic_mastery": {
                topic: round(score * 100, 1)
                for topic, score in analytics.topic_mastery.items()
            },
            "weak_areas": analytics.weakness_areas,
            "engagement_trend": [round(e, 2) for e in analytics.engagement_trend],
            "adjustments": adjustments,
            "profile_insights": {
                "dominant_dimension": profile.dominant_dimension.value if profile.dominant_dimension else "unknown",
                "content_preference": profile.get_content_preference(),
                "recommendations": profile.learning_preferences[:3]
            }
        }

        return report

    def export_feedback_history(self) -> List[Dict]:
        return [fb.to_dict() for fb in self.feedback_history]
