from typing import Dict, List, Optional
from models.data_models import CourseContent, StudentProfile, LearningStyleProfile, LearningSession
from core.learning_style_analyzer import LearningStyleAnalyzer
from core.adaptive_learning_engine import AdaptiveLearningEngine, LearningPath, LearningActivity
from core.ai_content_generator import ExerciseGenerator
from core.feedback_optimizer import FeedbackOptimizationSystem
import json
from datetime import datetime


class LearningAssistant:
    def __init__(self):
        self.student: Optional[StudentProfile] = None
        self.analyzer = LearningStyleAnalyzer()
        self.learning_engine = AdaptiveLearningEngine()
        self.exercise_generator = ExerciseGenerator()
        self.feedback_system = FeedbackOptimizationSystem()
        self.current_path: Optional[LearningPath] = None
        self.current_session: Optional[LearningSession] = None
        self.course_library: Dict[str, CourseContent] = {}
        self._initialize_course_library()

    def _initialize_course_library(self):
        self.course_library = {
            "ai_math_thinking": CourseContent(
                course_id="ai_math_thinking",
                title="人工智能的数学思维",
                content_type="course",
                difficulty=0.6,
                topics=["人工智能概述", "机器学习基础", "神经网络", "深度学习", "卷积神经网络"],
                estimated_time=180,
                prerequisites=[]
            ),
            "data_structures": CourseContent(
                course_id="data_structures",
                title="数据结构与算法",
                content_type="course",
                difficulty=0.7,
                topics=["栈和队列", "链表", "树结构", "图算法", "排序算法", "查找算法"],
                estimated_time=240,
                prerequisites=["编程基础"]
            ),
            "discrete_math": CourseContent(
                course_id="discrete_math",
                title="离散数学",
                content_type="course",
                difficulty=0.5,
                topics=["集合论", "图论", "命题逻辑", "谓词逻辑", "代数结构"],
                estimated_time=200,
                prerequisites=[]
            ),
            "computer_systems": CourseContent(
                course_id="computer_systems",
                title="计算机系统",
                content_type="course",
                difficulty=0.6,
                topics=["信息表示", "浮点数", "机器指令", "程序优化", "虚拟内存"],
                estimated_time=190,
                prerequisites=["编程基础"]
            )
        }

    def create_student_profile(self, student_id: str, name: str) -> StudentProfile:
        self.student = StudentProfile(
            student_id=student_id,
            name=name
        )
        return self.student

    def load_assessment_questions(self) -> List[Dict]:
        return self.analyzer.create_initial_assessment()

    def complete_initial_assessment(self, responses: List[Dict]) -> LearningStyleProfile:
        if not self.student:
            raise ValueError("学生档案未创建，请先调用create_student_profile")

        profile = self.analyzer.analyze_initial_assessment(responses)
        self.student.learning_style = profile
        self.student.learning_history.append({
            "event": "initial_assessment",
            "timestamp": datetime.now().isoformat(),
            "profile": profile.to_dict()
        })

        return profile

    def get_learning_recommendations(self) -> List[str]:
        if not self.student:
            return []
        return self.analyzer.generate_learning_recommendations(self.student.learning_style)

    def select_course(self, course_id: str) -> CourseContent:
        if course_id not in self.course_library:
            raise ValueError(f"课程 {course_id} 不存在")
        return self.course_library[course_id]

    def start_learning_session(
        self,
        course_id: str,
        target_topics: Optional[List[str]] = None
    ) -> LearningPath:
        if not self.student:
            raise ValueError("学生档案未创建")

        course = self.select_course(course_id)
        if target_topics is None:
            target_topics = course.topics[:3]

        self.current_path = self.learning_engine.generate_adaptive_path(
            course,
            self.student.learning_style,
            target_topics
        )

        self.current_session = LearningSession(
            session_id=f"session_{datetime.now().timestamp()}",
            student_id=self.student.student_id,
            course_id=course_id,
            topic=", ".join(target_topics),
            timestamp=datetime.now().isoformat()
        )

        return self.current_path

    def get_current_activity(self) -> Optional[LearningActivity]:
        if not self.current_path:
            return None

        if self.current_path.current_index < len(self.current_path.activities):
            return self.current_path.activities[self.current_path.current_index]
        return None

    def submit_activity_response(self, response: Dict) -> Dict:
        current_activity = self.get_current_activity()
        if not current_activity or not self.current_session:
            return {"error": "没有正在进行的活动"}

        performance, evaluation = self.learning_engine.evaluate_activity_performance(
            current_activity,
            response,
            self.student.learning_style
        )

        self.current_session.add_activity(
            activity_type=current_activity.activity_type.value,
            content={
                "activity_id": current_activity.activity_id,
                "response": response,
                "correct": evaluation.get("next_activity") != "revision"
            }
        )

        self.current_session.performance = self.current_session.calculate_performance()

        feedback = self.feedback_system.generate_adaptive_feedback(
            {"correct": evaluation.get("next_activity") != "revision", "score": performance},
            self.student.learning_style
        )

        next_activity = None
        remaining = self.current_path.activities[self.current_path.current_index + 1:]
        if evaluation.get("next_activity") == "revision":
            next_activity = current_activity
        elif evaluation.get("next_activity") == "advance":
            next_activity = self.learning_engine.adapt_next_activity(
                current_activity, performance, self.student.learning_style, remaining
            )
        elif remaining:
            next_activity = remaining[0]

        self.current_path.completed_activities.append(current_activity.activity_id)
        self.current_path.current_index += 1

        return {
            "performance": performance,
            "evaluation": evaluation,
            "feedback": feedback.content,
            "next_activity": next_activity.activity_id if next_activity else None
        }

    def generate_exercises_for_topic(self, topic: str, difficulty: float = 0.5) -> List[Dict]:
        if not self.student:
            raise ValueError("学生档案未创建")

        return self.exercise_generator.generate_practice_exercises(
            topic=topic,
            difficulty=difficulty,
            profile=self.student.learning_style,
            count=5
        )

    def generate_topic_explanation(
        self,
        topic: str,
        concept: str,
        depth: str = "medium"
    ) -> str:
        if not self.student:
            raise ValueError("学生档案未创建")

        generator = self.exercise_generator.__class__()
        return generator.generate_explanation(
            topic=topic,
            concept=concept,
            profile=self.student.learning_style,
            depth=depth
        )

    def generate_quiz(self, topics: List[str], question_count: int = 10) -> Dict:
        if not self.student:
            raise ValueError("学生档案未创建")

        return self.exercise_generator.generate_quiz(
            topics=topics,
            profile=self.student.learning_style,
            question_count=question_count
        )

    def end_learning_session(self) -> Dict:
        if not self.current_session or not self.student:
            return {"error": "没有正在进行的会话"}

        report = self.feedback_system.generate_progress_report(
            self.student.student_id,
            [self.current_session],
            self.student.learning_style
        )

        self.student.course_progress[self.current_session.course_id] = (
            len(self.current_path.completed_activities) / len(self.current_path.activities)
            if self.current_path else 0.0
        )

        self.student.learning_history.append({
            "event": "session_completed",
            "timestamp": datetime.now().isoformat(),
            "session_id": self.current_session.session_id,
            "performance": self.current_session.performance
        })

        self.current_session = None
        self.current_path = None

        return report

    def get_learning_analytics(self) -> Dict:
        if not self.student:
            return {}

        sessions = self._reconstruct_sessions()
        analytics = self.feedback_system.track_learning_progress(
            self.student.student_id,
            sessions
        )

        return {
            "total_sessions": analytics.total_sessions,
            "total_time_minutes": analytics.total_time_spent,
            "average_performance": round(analytics.average_performance * 100, 1),
            "topic_mastery": {k: round(v * 100, 1) for k, v in analytics.topic_mastery.items()},
            "weak_areas": analytics.weakness_areas,
            "learning_efficiency": round(analytics.learning_efficiency * 100, 1)
        }

    def _reconstruct_sessions(self) -> List[LearningSession]:
        sessions = []
        for history_item in self.student.learning_history:
            if history_item.get("event") == "session_completed":
                session = LearningSession(
                    session_id=history_item.get("session_id", ""),
                    student_id=self.student.student_id,
                    course_id="",
                    topic="",
                    timestamp=history_item.get("timestamp", "")
                )
                session.performance = history_item.get("performance", 0.0)
                sessions.append(session)
        return sessions

    def export_student_data(self) -> str:
        if not self.student:
            return "{}"

        data = {
            "student": self.student.to_dict(),
            "courses": [c.to_dict() for c in self.course_library.values()],
            "feedback_history": self.feedback_system.export_feedback_history()
        }

        return json.dumps(data, ensure_ascii=False, indent=2)

    def get_course_topics(self, course_id: str) -> List[str]:
        if course_id in self.course_library:
            return self.course_library[course_id].topics
        return []

    def get_available_courses(self) -> List[Dict]:
        return [
            {"course_id": c.course_id, "title": c.title, "topics": c.topics}
            for c in self.course_library.values()
        ]

    def update_learning_style_from_interactions(self):
        if not self.student or not self.current_session:
            return

        patterns = self.analyzer.analyze_interaction_patterns(self.current_session)
        self.student.learning_style = self.analyzer.update_profile_from_interactions(
            self.student.learning_style,
            patterns
        )
