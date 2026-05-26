import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.learning_assistant import LearningAssistant
from core.learning_style_analyzer import LearningStyleAnalyzer
from models.data_models import LearningDimension
import json


class LearningAssistantCLI:
    def __init__(self):
        self.assistant = LearningAssistant()
        self.analyzer = LearningStyleAnalyzer()
        self.running = True

    def print_banner(self):
        print("=" * 60)
        print("       🎓 个性化学习助手 🎓")
        print("=" * 60)
        print()

    def print_main_menu(self):
        print("\n📋 主菜单")
        print("-" * 40)
        print("1. 创建学生档案")
        print("2. 完成学习风格评估")
        print("3. 查看学习推荐")
        print("4. 选择课程开始学习")
        print("5. 生成练习题")
        print("6. 生成知识点讲解")
        print("7. 查看学习分析")
        print("8. 结束学习会话")
        print("0. 退出系统")
        print("-" * 40)

    def create_profile(self):
        print("\n📝 创建学生档案")
        print("-" * 40)
        name = input("请输入姓名: ").strip()
        student_id = input("请输入学号: ").strip()

        if not name or not student_id:
            print("❌ 姓名和学号不能为空")
            return

        self.assistant.create_student_profile(student_id, name)
        print(f"✅ 学生档案创建成功！欢迎 {name}！")

    def run_assessment(self):
        if not self.assistant.student:
            print("❌ 请先创建学生档案")
            return

        print("\n📊 学习风格评估")
        print("=" * 40)
        print("请回答以下问题，帮助我们了解您的学习风格...\n")

        questions = self.analyzer.create_initial_assessment()
        responses = []

        for i, q in enumerate(questions):
            print(f"问题 {i+1}/10: {q['question']}")
            for j, opt in enumerate(q['options']):
                print(f"  {j+1}. {opt['text']}")

            while True:
                try:
                    choice = int(input("\n请选择 (1-3): "))
                    if 1 <= choice <= 3:
                        break
                    print("请输入 1, 2 或 3")
                except ValueError:
                    print("请输入有效数字")

            responses.append({
                "question_id": q["id"],
                "selected_option": choice - 1
            })
            print()

        profile = self.assistant.complete_initial_assessment(responses)

        print("\n" + "=" * 40)
        print("📈 评估结果")
        print("=" * 40)
        print(f"\n🎯 您的主导学习维度: {self._get_dimension_name(profile.dominant_dimension)}")
        print(f"\n📊 详细分析:")
        print(f"  - 视觉型: {profile.visual_score:.0%}")
        print(f"  - 语言型: {profile.verbal_score:.0%}")
        print(f"  - 逻辑型: {profile.logical_score:.0%}")
        print(f"  - 实践型: {profile.practical_score:.0%}")
        print(f"  - 社交型: {profile.social_score:.0%}")
        print(f"  - 自主型: {profile.solitary_score:.0%}")

        print(f"\n💡 学习偏好:")
        for pref in profile.learning_preferences:
            print(f"  • {pref}")

        print("\n✅ 评估完成！根据您的学习风格，我们将为您定制学习内容。")

    def _get_dimension_name(self, dimension) -> str:
        names = {
            LearningDimension.VISUAL: "视觉型 (Visual)",
            LearningDimension.VERBAL: "语言型 (Verbal)",
            LearningDimension.LOGICAL: "逻辑型 (Logical)",
            LearningDimension.SOCIAL: "社交型 (Social)",
            LearningDimension.SOLITARY: "自主型 (Solitary)",
            LearningDimension.PRACTICAL: "实践型 (Practical)",
            LearningDimension.CONCEPTUAL: "概念型 (Conceptual)"
        }
        return names.get(dimension, "综合型")

    def show_recommendations(self):
        if not self.assistant.student:
            print("❌ 请先创建学生档案")
            return

        recommendations = self.assistant.get_learning_recommendations()
        print("\n💡 学习推荐")
        print("-" * 40)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

    def start_learning(self):
        if not self.assistant.student:
            print("❌ 请先创建学生档案")
            return

        if not self.assistant.student.learning_style.dominant_dimension:
            print("❌ 请先完成学习风格评估")
            return

        print("\n📚 选择课程")
        print("-" * 40)
        courses = self.assistant.get_available_courses()
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['title']} ({course['course_id']})")

        while True:
            try:
                choice = int(input("\n请选择课程编号: "))
                if 1 <= choice <= len(courses):
                    break
            except ValueError:
                pass
            print("请输入有效编号")

        selected_course = courses[choice - 1]
        print(f"\n📖 已选择: {selected_course['title']}")

        topics = selected_course['topics']
        print("\n📌 可选主题:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")

        print("\n(输入数字选择要学习的主题，逗号分隔，如: 1,2,3)")
        print("(直接回车学习前3个主题)")
        topic_input = input("您的选择: ").strip()

        target_topics = None
        if topic_input:
            try:
                indices = [int(x.strip()) for x in topic_input.split(",")]
                target_topics = [topics[i-1] for i in indices if 1 <= i <= len(topics)]
            except ValueError:
                print("输入格式有误，将使用默认主题")

        if not target_topics:
            target_topics = topics[:3]

        print(f"\n🚀 开始学习: {', '.join(target_topics)}")
        path = self.assistant.start_learning_session(selected_course['course_id'], target_topics)

        print(f"\n📋 学习路径已生成，共 {len(path.activities)} 个学习活动\n")

        self.run_learning_loop(path)

    def run_learning_loop(self, path):
        while True:
            activity = self.assistant.get_current_activity()
            if not activity:
                print("\n✅ 学习路径已完成！")
                break

            print("\n" + "=" * 40)
            print(f"📌 当前活动: {activity.title}")
            print(f"⏱️  预计时间: {activity.estimated_time} 分钟")
            print("-" * 40)
            print(activity.content[:500] + "..." if len(activity.content) > 500 else activity.content)
            print("=" * 40)

            print("\n请完成活动后，选择操作:")
            print("1. 我已完成（继续）")
            print("2. 生成练习题")
            print("3. 获取详细讲解")
            print("4. 提前结束本次学习")

            choice = input("\n您的选择: ").strip()

            if choice == "1":
                response = {"completed": True, "correct_answers": 1, "total_questions": 1}
                result = self.assistant.submit_activity_response(response)
                print(f"\n📊 表现评估: {result['performance']:.0%}")
                print(f"💬 反馈: {result['feedback']}")
            elif choice == "2":
                topic = activity.activity_id.split("_")[0]
                exercises = self.assistant.generate_exercises_for_topic(topic)
                self.show_exercises(exercises)
            elif choice == "3":
                topic = activity.activity_id.split("_")[0]
                explanation = self.assistant.generate_topic_explanation(topic, topic, "high")
                print("\n" + explanation)
            elif choice == "4":
                break

        report = self.assistant.end_learning_session()
        self.show_session_report(report)

    def show_exercises(self, exercises):
        print("\n📝 练习题")
        print("-" * 40)
        for i, ex in enumerate(exercises, 1):
            print(f"\n{i}. [{ex['type']}] {ex['question']}")
            if 'options' in ex:
                for opt in ex['options']:
                    print(f"   {opt}")

    def generate_explanation(self):
        if not self.assistant.student:
            print("❌ 请先创建学生档案")
            return

        print("\n📖 生成知识点讲解")
        print("-" * 40)
        topic = input("请输入要讲解的主题: ").strip()
        if not topic:
            print("❌ 主题不能为空")
            return

        depth = input("讲解深度 (1-简单, 2-中等, 3-详细) [2]: ").strip() or "2"
        depth_map = {"1": "low", "2": "medium", "3": "high"}
        depth_level = depth_map.get(depth, "medium")

        explanation = self.assistant.generate_topic_explanation(topic, topic, depth_level)
        print("\n" + explanation)

    def show_analytics(self):
        if not self.assistant.student:
            print("❌ 请先创建学生档案")
            return

        analytics = self.assistant.get_learning_analytics()
        if not analytics or analytics.get('total_sessions', 0) == 0:
            print("\n📊 当前没有学习记录，请先完成一些学习活动")
            return

        print("\n📊 学习分析报告")
        print("=" * 40)
        print(f"\n🕐 总学习时长: {analytics.get('total_time_minutes', 0)} 分钟")
        print(f"📚 完成会话数: {analytics.get('total_sessions', 0)}")
        print(f"📈 平均表现: {analytics.get('average_performance', 0)}%")
        print(f"⚡ 学习效率: {analytics.get('learning_efficiency', 0)}%")

        mastery = analytics.get('topic_mastery', {})
        if mastery:
            print("\n📊 知识点掌握情况:")
            for topic, score in mastery.items():
                bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
                print(f"  {topic}: [{bar}] {score}%")

        weak_areas = analytics.get('weak_areas', [])
        if weak_areas:
            print(f"\n⚠️ 需要加强: {', '.join(weak_areas)}")

    def show_session_report(self, report):
        print("\n" + "=" * 50)
        print("📋 学习会话报告")
        print("=" * 50)
        print(f"\n📅 日期: {report.get('report_date', 'N/A')[:10]}")
        print(f"📊 平均得分: {report.get('summary', {}).get('average_score', 0)}%")
        print(f"⏱️  学习时长: {report.get('summary', {}).get('total_time_minutes', 0)} 分钟")
        print(f"⚡ 学习效率: {report.get('summary', {}).get('learning_efficiency', 0)}%")

        insights = report.get('profile_insights', {})
        if insights:
            print(f"\n🎯 您的学习风格: {insights.get('dominant_dimension', 'N/A')}")
            print(f"📌 内容偏好: {insights.get('content_preference', 'N/A')}")

        adjustments = report.get('adjustments', [])
        if adjustments:
            print("\n💡 调整建议:")
            for adj in adjustments:
                print(f"  • {adj}")

    def run(self):
        self.print_banner()

        while self.running:
            self.print_main_menu()
            choice = input("\n请输入选项编号: ").strip()

            if choice == "1":
                self.create_profile()
            elif choice == "2":
                self.run_assessment()
            elif choice == "3":
                self.show_recommendations()
            elif choice == "4":
                self.start_learning()
            elif choice == "5":
                if not self.assistant.student:
                    print("❌ 请先创建学生档案")
                else:
                    topic = input("请输入练习题主题: ").strip()
                    exercises = self.assistant.generate_exercises_for_topic(topic)
                    self.show_exercises(exercises)
            elif choice == "6":
                self.generate_explanation()
            elif choice == "7":
                self.show_analytics()
            elif choice == "8":
                if self.assistant.current_session:
                    report = self.assistant.end_learning_session()
                    self.show_session_report(report)
                else:
                    print("没有正在进行的会话")
            elif choice == "0":
                print("\n👋 感谢使用个性化学习助手，再见！")
                self.running = False
            else:
                print("❌ 无效选项，请重新输入")


def main():
    cli = LearningAssistantCLI()
    cli.run()


if __name__ == "__main__":
    main()
