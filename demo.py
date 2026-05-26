import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.learning_assistant import LearningAssistant
from core.learning_style_analyzer import LearningStyleAnalyzer
from models.data_models import LearningDimension


def demo_learning_style_analysis():
    print("\n" + "=" * 60)
    print("[DEMO] Learning Style Analysis")
    print("=" * 60)

    analyzer = LearningStyleAnalyzer()
    questions = analyzer.create_initial_assessment()

    print(f"\nGenerated {len(questions)} assessment questions\n")
    print("Sample Questions:")
    for i, q in enumerate(questions[:3]):
        print(f"  {i+1}. {q['question']}")
        for j, opt in enumerate(q['options']):
            print(f"     {j+1}. {opt['text']}")

    responses = [
        {"question_id": "q1", "selected_option": 0},
        {"question_id": "q2", "selected_option": 0},
        {"question_id": "q3", "selected_option": 1},
        {"question_id": "q4", "selected_option": 1},
        {"question_id": "q5", "selected_option": 0},
        {"question_id": "q6", "selected_option": 0},
        {"question_id": "q7", "selected_option": 0},
        {"question_id": "q8", "selected_option": 0},
        {"question_id": "q9", "selected_option": 0},
        {"question_id": "q10", "selected_option": 0},
    ]

    profile = analyzer.analyze_initial_assessment(responses)

    print("\n\n[RESULTS] Analysis Results:")
    print(f"  Dominant Dimension: {profile.dominant_dimension.value if profile.dominant_dimension else 'N/A'}")
    print(f"  Visual: {profile.visual_score:.1%}")
    print(f"  Verbal: {profile.verbal_score:.1%}")
    print(f"  Logical: {profile.logical_score:.1%}")
    print(f"  Practical: {profile.practical_score:.1%}")
    print(f"  Social: {profile.social_score:.1%}")

    recommendations = analyzer.generate_learning_recommendations(profile)
    print("\n[RECOMMENDATIONS] Learning Suggestions:")
    for rec in recommendations[:3]:
        print(f"  * {rec}")


def demo_adaptive_learning():
    print("\n" + "=" * 60)
    print("[DEMO] Adaptive Learning Path")
    print("=" * 60)

    from core.adaptive_learning_engine import AdaptiveLearningEngine
    from models.data_models import LearningStyleProfile, CourseContent

    profile = LearningStyleProfile(
        visual_score=0.8,
        verbal_score=0.5,
        logical_score=0.6,
        social_score=0.3,
        solitary_score=0.7,
        practical_score=0.4,
        conceptual_score=0.5,
        dominant_dimension=LearningDimension.VISUAL
    )

    course = CourseContent(
        course_id="demo_course",
        title="Data Structures and Algorithms",
        content_type="course",
        difficulty=0.7,
        topics=["Stack", "Queue", "LinkedList"],
        estimated_time=60
    )

    engine = AdaptiveLearningEngine()
    path = engine.generate_adaptive_path(course, profile, ["Stack", "Queue"])

    print(f"\n[OK] Generated {len(path.activities)} learning activities for visual learner\n")

    for i, activity in enumerate(path.activities[:4]):
        print(f"  {i+1}. [{activity.activity_type.value}] {activity.title}")
        print(f"     Difficulty: {activity.difficulty:.1f} | Time: {activity.estimated_time}min")
        print()


def demo_ai_content_generation():
    print("\n" + "=" * 60)
    print("[DEMO] AI Content Generation")
    print("=" * 60)

    from core.ai_content_generator import AIGeneratedContent, ExerciseGenerator
    from models.data_models import LearningStyleProfile, LearningDimension

    visual_profile = LearningStyleProfile(
        visual_score=0.9,
        dominant_dimension=LearningDimension.VISUAL
    )

    logical_profile = LearningStyleProfile(
        logical_score=0.9,
        dominant_dimension=LearningDimension.LOGICAL
    )

    generator = AIGeneratedContent()

    print("\n[EXPLANATION] For Visual Learners - 'Stack' Concept:")
    visual_explanation = generator.generate_explanation("Stack", "LIFO", visual_profile, "medium")
    print(visual_explanation[:500] + "...")

    print("\n\n[EXPLANATION] For Logical Learners - 'Stack' Concept:")
    logical_explanation = generator.generate_explanation("Stack", "LIFO", logical_profile, "medium")
    print(logical_explanation[:500] + "...")

    print("\n\n[EXERCISES] Exercise Generation Demo:")
    exercise_gen = ExerciseGenerator()
    exercises = exercise_gen.generate_practice_exercises(
        topic="Stack",
        difficulty=0.5,
        profile=visual_profile,
        count=3
    )

    for i, ex in enumerate(exercises):
        print(f"  {i+1}. [{ex['type']}] {ex['question'][:60]}...")


def demo_feedback_system():
    print("\n" + "=" * 60)
    print("[DEMO] Feedback Optimization System")
    print("=" * 60)

    from core.feedback_optimizer import FeedbackOptimizationSystem
    from models.data_models import LearningSession, LearningStyleProfile

    system = FeedbackOptimizationSystem()
    profile = LearningStyleProfile(
        visual_score=0.7,
        dominant_dimension=LearningDimension.VISUAL
    )

    session = LearningSession(
        session_id="demo_session",
        student_id="student_001",
        course_id="demo_course",
        topic="Stack",
        timestamp="2024-01-01T10:00:00"
    )

    session.add_activity("practice", {"correct": False, "engagement_time": 300})
    session.add_activity("concept", {"correct": True, "engagement_time": 180})

    analytics = system.track_learning_progress("student_001", [session])

    print(f"\n[ANALYTICS] Learning Analysis:")
    print(f"  Total Time: {analytics.total_time_spent} seconds")
    print(f"  Efficiency: {analytics.learning_efficiency:.1%}")
    print(f"  Weak Areas: {', '.join(analytics.weakness_areas) if analytics.weakness_areas else 'None'}")

    feedback = system.generate_adaptive_feedback(
        {"correct": False, "score": 0.4},
        profile
    )

    print(f"\n[FEEDBACK] Adaptive Feedback:")
    print(f"  Type: {feedback.feedback_type}")
    print(f"  Content: {feedback.content[:100]}...")


def demo_full_workflow():
    print("\n" + "=" * 60)
    print("[DEMO] Complete Learning Workflow")
    print("=" * 60)

    assistant = LearningAssistant()

    print("\n[Step 1] Creating Student Profile...")
    assistant.create_student_profile("student_001", "XiaoMing")
    print("   [OK] Profile created")

    print("\n[Step 2] Completing Learning Style Assessment...")
    responses = [
        {"question_id": "q1", "selected_option": 0},
        {"question_id": "q2", "selected_option": 0},
        {"question_id": "q3", "selected_option": 1},
        {"question_id": "q4", "selected_option": 1},
        {"question_id": "q5", "selected_option": 0},
        {"question_id": "q6", "selected_option": 0},
        {"question_id": "q7", "selected_option": 0},
        {"question_id": "q8", "selected_option": 0},
        {"question_id": "q9", "selected_option": 0},
        {"question_id": "q10", "selected_option": 0},
    ]
    profile = assistant.complete_initial_assessment(responses)
    dim_name = profile.dominant_dimension.value if profile.dominant_dimension else 'N/A'
    print(f"   [OK] Assessment complete, Dominant Style: {dim_name}")

    print("\n[Step 3] Getting Learning Recommendations...")
    recommendations = assistant.get_learning_recommendations()
    for rec in recommendations[:2]:
        print(f"   * {rec}")

    print("\n[Step 4] Selecting Course...")
    courses = assistant.get_available_courses()
    print(f"   Available: {[c['title'] for c in courses]}")

    print("\n[Step 5] Starting Learning Session...")
    path = assistant.start_learning_session("data_structures", ["Stack", "Queue"])
    print(f"   [OK] Generated {len(path.activities)} learning activities")

    print("\n[Step 6] Completing Learning Activities...")
    for i in range(min(3, len(path.activities))):
        activity = assistant.get_current_activity()
        if activity:
            print(f"   Learning: {activity.title}")
            result = assistant.submit_activity_response({
                "completed": True,
                "correct_answers": 1,
                "total_questions": 1
            })
            print(f"   Performance: {result['performance']:.0%}")

    print("\n[Step 7] Generating Exercises...")
    exercises = assistant.generate_exercises_for_topic("Stack", 0.5)
    print(f"   [OK] Generated {len(exercises)} exercises")

    print("\n[Step 8] Ending Learning Session...")
    report = assistant.end_learning_session()
    print(f"\n[REPORT] Learning Report:")
    print(f"   Average Score: {report['summary']['average_score']:.0%}")
    print(f"   Learning Efficiency: {report['summary']['learning_efficiency']:.0%}")


def main():
    print("\n" + "=" * 60)
    print("  Personalized Learning Assistant - Demo")
    print("=" * 60)

    try:
        demo_learning_style_analysis()
        demo_adaptive_learning()
        demo_ai_content_generation()
        demo_feedback_system()
        demo_full_workflow()

        print("\n" + "=" * 60)
        print("[OK] All demos completed successfully!")
        print("=" * 60)
        print("\n[USAGE]")
        print("  1. CLI Version: python main.py")
        print("  2. Web Version: python web_app.py (http://localhost:5000)")
        print()

    except Exception as e:
        print(f"\n[ERROR] Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
