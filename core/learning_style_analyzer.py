from models.data_models import LearningStyleProfile, StudentProfile, LearningDimension, LearningSession
from typing import Dict, List
import json
from datetime import datetime


class LearningStyleAnalyzer:
    def __init__(self):
        self.questionnaire_responses: List[Dict] = []
        self.interaction_patterns: List[Dict] = []

    def create_initial_assessment(self) -> List[Dict]:
        questions = [
            {
                "id": "q1",
                "dimension": "visual",
                "question": "当你学习新知识时，你更喜欢：",
                "options": [
                    {"text": "看图表、图片或视频演示", "score": {"visual": 1.0, "verbal": 0.2}},
                    {"text": "阅读文字说明或听讲解", "score": {"visual": 0.2, "verbal": 0.9}},
                    {"text": "动手实践或操作", "score": {"visual": 0.3, "practical": 1.0}}
                ]
            },
            {
                "id": "q2",
                "dimension": "logical",
                "question": "解决复杂问题时，你倾向于：",
                "options": [
                    {"text": "按照逻辑步骤逐步分析", "score": {"logical": 1.0, "conceptual": 0.3}},
                    {"text": "凭直觉或整体感觉判断", "score": {"logical": 0.2, "conceptual": 0.8}},
                    {"text": "参考他人意见或讨论", "score": {"social": 1.0, "solitary": 0.2}}
                ]
            },
            {
                "id": "q3",
                "dimension": "social",
                "question": "你更喜欢哪种学习方式？",
                "options": [
                    {"text": "和同学一起讨论学习", "score": {"social": 1.0, "solitary": 0.1}},
                    {"text": "独自安静地学习", "score": {"solitary": 1.0, "social": 0.1}},
                    {"text": "有时独学，有时讨论", "score": {"social": 0.5, "solitary": 0.5}}
                ]
            },
            {
                "id": "q4",
                "dimension": "practical",
                "question": "学习编程或数学概念时，你希望：",
                "options": [
                    {"text": "先理解理论再动手实践", "score": {"conceptual": 0.9, "practical": 0.3}},
                    {"text": "直接动手做，从实践中学习", "score": {"practical": 1.0, "conceptual": 0.2}},
                    {"text": "两者结合，边学边做", "score": {"practical": 0.6, "conceptual": 0.6}}
                ]
            },
            {
                "id": "q5",
                "dimension": "perception",
                "question": "回忆已学知识时，你最依赖：",
                "options": [
                    {"text": "视觉形象和图像", "score": {"visual": 1.0, "retention": 0.7}},
                    {"text": "文字描述和语言表达", "score": {"verbal": 0.9, "retention": 0.6}},
                    {"text": "实际操作步骤", "score": {"practical": 1.0, "retention": 0.8}}
                ]
            },
            {
                "id": "q6",
                "dimension": "processing",
                "question": "面对大量新信息时，你倾向于：",
                "options": [
                    {"text": "先全面了解整体框架", "score": {"conceptual": 1.0, "processing": 0.8}},
                    {"text": "深入研究细节再扩展", "score": {"logical": 1.0, "processing": 0.6}},
                    {"text": "选择性吸收关键信息", "score": {"practical": 0.8, "processing": 0.7}}
                ]
            },
            {
                "id": "q7",
                "dimension": "retention",
                "question": "哪种方式能让你更好地记忆知识？",
                "options": [
                    {"text": "制作思维导图或图表", "score": {"visual": 1.0, "conceptual": 0.6}},
                    {"text": "反复阅读和背诵", "score": {"verbal": 1.0, "retention": 0.9}},
                    {"text": "做练习题或应用实践", "score": {"practical": 1.0, "retention": 0.8}}
                ]
            },
            {
                "id": "q8",
                "dimension": "visual",
                "question": "阅读技术文档时，你希望有：",
                "options": [
                    {"text": "大量的代码截图和流程图", "score": {"visual": 1.0}},
                    {"text": "清晰简洁的文字说明", "score": {"verbal": 1.0}},
                    {"text": "具体的代码示例", "score": {"practical": 0.8}}
                ]
            },
            {
                "id": "q9",
                "dimension": "logical",
                "question": "当你遇到错误时，你更可能：",
                "options": [
                    {"text": "分析错误信息，查找逻辑问题", "score": {"logical": 1.0}},
                    {"text": "搜索类似问题的解决方案", "score": {"practical": 0.8}},
                    {"text": "请教他人或查看社区", "score": {"social": 1.0}}
                ]
            },
            {
                "id": "q10",
                "dimension": "conceptual",
                "question": "学习新概念时，你最关注：",
                "options": [
                    {"text": "概念之间的联系和区别", "score": {"conceptual": 1.0, "logical": 0.5}},
                    {"text": "这个概念如何应用到实际", "score": {"practical": 1.0}},
                    {"text": "背后的原理和证明", "score": {"logical": 0.9, "conceptual": 0.5}}
                ]
            }
        ]
        return questions

    def analyze_initial_assessment(self, responses: List[Dict]) -> LearningStyleProfile:
        profile = LearningStyleProfile()

        dimension_scores: Dict[str, List[float]] = {
            "visual": [], "verbal": [], "logical": [], "social": [],
            "solitary": [], "practical": [], "conceptual": []
        }

        for response in responses:
            question_id = response.get("question_id")
            selected_option = response.get("selected_option", 0)
            questions = self.create_initial_assessment()
            question_data = next((q for q in questions if q["id"] == question_id), None)

            if question_data:
                option_scores = question_data["options"][selected_option]["score"]
                for dim, score in option_scores.items():
                    if dim in dimension_scores:
                        dimension_scores[dim].append(score)

        for dimension, scores in dimension_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                setattr(profile, f"{dimension}_score", avg_score)

        profile.perception_score = (profile.visual_score * 0.4 + profile.practical_score * 0.6)
        profile.retention_score = (profile.verbal_score * 0.3 + profile.practical_score * 0.4 + profile.visual_score * 0.3)
        profile.processing_score = (profile.logical_score * 0.5 + profile.conceptual_score * 0.5)

        profile.determine_dominant_dimension()
        profile.learning_preferences = self._generate_preferences(profile)

        return profile

    def _generate_preferences(self, profile: LearningStyleProfile) -> List[str]:
        preferences = []
        if profile.visual_score > 0.7:
            preferences.append("图形化展示")
        if profile.verbal_score > 0.7:
            preferences.append("详细文字说明")
        if profile.logical_score > 0.7:
            preferences.append("结构化分析")
        if profile.social_score > 0.7:
            preferences.append("协作学习")
        if profile.solitary_score > 0.7:
            preferences.append("自主学习")
        if profile.practical_score > 0.7:
            preferences.append("实践应用")
        if profile.conceptual_score > 0.7:
            preferences.append("概念理解")
        return preferences

    def analyze_interaction_patterns(self, session: LearningSession) -> Dict:
        patterns = {
            "content_type_preference": {},
            "avg_engagement_time": 0,
            "exercise_accuracy": 0,
            "revision_frequency": 0
        }

        if not session.activities:
            return patterns

        content_counts: Dict[str, int] = {}
        total_engagement = 0
        correct_count = 0
        revision_count = 0

        for activity in session.activities:
            activity_type = activity.get("type", "unknown")
            content_counts[activity_type] = content_counts.get(activity_type, 0) + 1

            if "engagement_time" in activity:
                total_engagement += activity["engagement_time"]

            if activity.get("correct"):
                correct_count += 1

            if activity_type == "revision":
                revision_count += 1

        patterns["content_type_preference"] = {
            k: v / len(session.activities) for k, v in content_counts.items()
        }
        patterns["avg_engagement_time"] = total_engagement / len(session.activities)
        patterns["exercise_accuracy"] = correct_count / len(session.activities)
        patterns["revision_frequency"] = revision_count / len(session.activities)

        return patterns

    def update_profile_from_interactions(
        self,
        profile: LearningStyleProfile,
        interaction_patterns: Dict
    ) -> LearningStyleProfile:
        content_pref = interaction_patterns.get("content_type_preference", {})

        if "video" in content_pref or "image" in content_pref:
            profile.visual_score = min(1.0, profile.visual_score + 0.05)

        if "text" in content_pref or "reading" in content_pref:
            profile.verbal_score = min(1.0, profile.verbal_score + 0.05)

        if "practice" in content_pref or "exercise" in content_pref:
            profile.practical_score = min(1.0, profile.practical_score + 0.05)

        if interaction_patterns.get("revision_frequency", 0) > 0.3:
            profile.retention_score = min(1.0, profile.retention_score + 0.05)

        if interaction_patterns.get("exercise_accuracy", 0) > 0.8:
            profile.logical_score = min(1.0, profile.logical_score + 0.03)

        profile.determine_dominant_dimension()
        profile.learning_preferences = self._generate_preferences(profile)

        return profile

    def generate_learning_recommendations(self, profile: LearningStyleProfile) -> List[str]:
        recommendations = []

        if profile.dominant_dimension == LearningDimension.VISUAL:
            recommendations.extend([
                "建议使用思维导图整理知识点",
                "观看教学视频时做好截图笔记",
                "将抽象概念可视化表示"
            ])
        elif profile.dominant_dimension == LearningDimension.VERBAL:
            recommendations.extend([
                "详细阅读教材和参考资料",
                "用自己的话复述所学内容",
                "创建术语解释文档"
            ])
        elif profile.dominant_dimension == LearningDimension.LOGICAL:
            recommendations.extend([
                "建立知识点之间的逻辑关系图",
                "分析算法的步骤和复杂度",
                "用数学推导验证结论"
            ])
        elif profile.dominant_dimension == LearningDimension.PRACTICAL:
            recommendations.extend([
                "多动手编写代码实现",
                "通过项目实践巩固知识",
                "做大量练习题和应用案例"
            ])
        elif profile.dominant_dimension == LearningDimension.SOCIAL:
            recommendations.extend([
                "加入学习小组讨论问题",
                "向他人讲解促进理解",
                "参与在线社区交流"
            ])
        elif profile.dominant_dimension == LearningDimension.SOLITARY:
            recommendations.extend([
                "创建个人学习计划",
                "独立完成项目挑战",
                "定期自我测试评估"
            ])
        elif profile.dominant_dimension == LearningDimension.CONCEPTUAL:
            recommendations.extend([
                "对比学习相似概念",
                "了解知识发展历史",
                "构建知识体系框架"
            ])

        if profile.processing_score > 0.7:
            recommendations.append("适合快速浏览大量新知识")

        if profile.retention_score < 0.5:
            recommendations.append("建议采用间隔重复学习方法")

        return recommendations
