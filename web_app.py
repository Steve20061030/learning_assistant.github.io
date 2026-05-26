from flask import Flask, render_template, request, jsonify, session
import sys
import os
import hashlib
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.learning_assistant import LearningAssistant
from core.learning_style_analyzer import LearningStyleAnalyzer
from models.data_models import LearningDimension

app = Flask(__name__)
app.secret_key = 'learning_assistant_secret_key_2024'

assistant = LearningAssistant()
analyzer = LearningStyleAnalyzer()

# 模拟用户数据库
users_db = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "name": "管理员",
        "student_id": "admin001"
    }
}


@app.route('/')
def index():
    if 'initialized' not in session:
        session['initialized'] = True
        assistant.create_student_profile("default_user", "学生")

    courses = assistant.get_available_courses()
    profile = assistant.student.learning_style if assistant.student else None

    return render_template(
        'index.html',
        courses=courses,
        profile=profile
    )


# 用户注册
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()
    student_id = data.get('student_id', '').strip()

    if not username or not password or not name or not student_id:
        return jsonify({"success": False, "message": "所有字段都不能为空"})

    if username in users_db:
        return jsonify({"success": False, "message": "用户名已存在"})

    # 存储用户信息
    users_db[username] = {
        "password": hashlib.sha256(password.encode()).hexdigest(),
        "name": name,
        "student_id": student_id,
        "created_at": str(uuid.uuid4())[:8]  # 简化的时间戳
    }

    # 创建学习助手档案
    assistant.create_student_profile(student_id, name)

    session['user'] = username
    return jsonify({"success": True, "message": f"注册成功！欢迎 {name}！"})


# 用户登录
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({"success": False, "message": "用户名或密码不能为空"})

    user = users_db.get(username)
    if not user:
        return jsonify({"success": False, "message": "用户不存在"})

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user['password'] != hashed_password:
        return jsonify({"success": False, "message": "密码错误"})

    session['user'] = username
    
    # 初始化学习助手
    assistant.create_student_profile(user['student_id'], user['name'])

    return jsonify({
        "success": True,
        "message": f"登录成功！欢迎 {user['name']}！",
        "user": {
            "username": username,
            "name": user['name'],
            "student_id": user['student_id']
        }
    })


# 用户登出
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True, "message": "已登出"})


# 检查登录状态
@app.route('/api/auth/status', methods=['GET'])
def check_status():
    if 'user' in session:
        username = session['user']
        user = users_db.get(username)
        if user:
            return jsonify({
                "logged_in": True,
                "user": {
                    "username": username,
                    "name": user['name'],
                    "student_id": user['student_id']
                }
            })
    return jsonify({"logged_in": False})


@app.route('/api/profile/create', methods=['POST'])
def create_profile():
    data = request.json
    name = data.get('name', '')
    student_id = data.get('student_id', '')

    assistant.create_student_profile(student_id, name)
    return jsonify({"success": True, "message": f"欢迎 {name}！"})


@app.route('/api/assessment/questions', methods=['GET'])
def get_assessment_questions():
    questions = analyzer.create_initial_assessment()
    return jsonify({"questions": questions})


@app.route('/api/assessment/submit', methods=['POST'])
def submit_assessment():
    responses = request.json.get('responses', [])
    profile = assistant.complete_initial_assessment(responses)

    return jsonify({
        "success": True,
        "profile": {
            "dominant_dimension": profile.dominant_dimension.value if profile.dominant_dimension else "unknown",
            "visual_score": profile.visual_score,
            "verbal_score": profile.verbal_score,
            "logical_score": profile.logical_score,
            "practical_score": profile.practical_score,
            "social_score": profile.social_score,
            "solitary_score": profile.solitary_score,
            "preferences": profile.learning_preferences
        }
    })


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    recommendations = assistant.get_learning_recommendations()
    return jsonify({"recommendations": recommendations})


@app.route('/api/course/topics', methods=['GET'])
def get_course_topics():
    course_id = request.args.get('course_id', '')
    topics = assistant.get_course_topics(course_id)
    return jsonify({"topics": topics})


# 获取所有课程列表
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    courses = assistant.get_available_courses()
    return jsonify({"courses": courses})


# 获取课程详情
@app.route('/api/course/<course_id>', methods=['GET'])
def get_course_detail(course_id):
    courses = assistant.get_available_courses()
    course = next((c for c in courses if c['course_id'] == course_id), None)
    
    if not course:
        return jsonify({"success": False, "message": "课程不存在"})
    
    # 获取课程主题
    topics = assistant.get_course_topics(course_id)
    
    return jsonify({
        "success": True,
        "course": {
            "course_id": course['course_id'],
            "title": course['title'],
            "description": course.get('description', ''),
            "topics": topics,
            "difficulty": course.get('difficulty', '中等'),
            "estimated_hours": course.get('estimated_hours', 20)
        }
    })


# 获取课程资源
@app.route('/api/course/<course_id>/resources', methods=['GET'])
def get_course_resources(course_id):
    # 模拟课程资源数据
    resources = {
        "ai_math": [
            {"id": "r1", "title": "机器学习入门教程", "type": "video", "duration": "45分钟"},
            {"id": "r2", "title": "神经网络基础", "type": "pdf", "pages": 32},
            {"id": "r3", "title": "矩阵运算练习", "type": "exercise", "count": 20}
        ],
        "data_struct": [
            {"id": "r1", "title": "数据结构导论", "type": "video", "duration": "30分钟"},
            {"id": "r2", "title": "算法设计手册", "type": "pdf", "pages": 128},
            {"id": "r3", "title": "数据结构习题集", "type": "exercise", "count": 50}
        ],
        "discrete_math": [
            {"id": "r1", "title": "离散数学基础", "type": "video", "duration": "50分钟"},
            {"id": "r2", "title": "逻辑与证明", "type": "pdf", "pages": 86},
            {"id": "r3", "title": "组合数学练习", "type": "exercise", "count": 30}
        ],
        "comp_systems": [
            {"id": "r1", "title": "计算机组成原理", "type": "video", "duration": "40分钟"},
            {"id": "r2", "title": "操作系统概念", "type": "pdf", "pages": 156},
            {"id": "r3", "title": "汇编语言练习", "type": "exercise", "count": 25}
        ],
        "algorithms": [
            {"id": "r1", "title": "算法导论", "type": "video", "duration": "55分钟"},
            {"id": "r2", "title": "算法设计与分析", "type": "pdf", "pages": 200},
            {"id": "r3", "title": "算法竞赛题解", "type": "exercise", "count": 100}
        ]
    }
    
    return jsonify({
        "success": True,
        "resources": resources.get(course_id, [])
    })


@app.route('/api/learning/start', methods=['POST'])
def start_learning():
    data = request.json
    course_id = data.get('course_id', '')
    topics = data.get('topics', [])

    try:
        path = assistant.start_learning_session(course_id, topics if topics else None)
        activities = [
            {
                "id": a.activity_id,
                "type": a.activity_type.value,
                "title": a.title,
                "content": a.content,
                "difficulty": a.difficulty,
                "time": a.estimated_time
            }
            for a in path.activities
        ]
        return jsonify({
            "success": True,
            "path_id": path.path_id,
            "activities": activities
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/api/activity/current', methods=['GET'])
def get_current_activity():
    activity = assistant.get_current_activity()
    if activity:
        return jsonify({
            "id": activity.activity_id,
            "type": activity.activity_type.value,
            "title": activity.title,
            "content": activity.content,
            "difficulty": activity.difficulty,
            "time": activity.estimated_time
        })
    return jsonify({"activity": None})


@app.route('/api/activity/submit', methods=['POST'])
def submit_activity():
    response_data = request.json
    result = assistant.submit_activity_response(response_data)
    return jsonify(result)


# 学习进度API

# 获取学习进度
@app.route('/api/progress', methods=['GET'])
def get_progress():
    analytics = assistant.get_learning_analytics()
    return jsonify({
        "success": True,
        "progress": {
            "total_time_minutes": analytics.get('total_time_minutes', 0),
            "total_sessions": analytics.get('total_sessions', 0),
            "average_performance": analytics.get('average_performance', 0),
            "learning_efficiency": analytics.get('learning_efficiency', 0),
            "topic_mastery": analytics.get('topic_mastery', {}),
            "weak_areas": analytics.get('weak_areas', []),
            "completed_courses": analytics.get('completed_courses', []),
            "in_progress_courses": analytics.get('in_progress_courses', [])
        }
    })


# 更新学习进度
@app.route('/api/progress/update', methods=['POST'])
def update_progress():
    data = request.json
    course_id = data.get('course_id', '')
    topic = data.get('topic', '')
    progress = data.get('progress', 0)
    completed = data.get('completed', False)
    
    # 模拟更新进度
    if course_id:
        # 这里可以添加实际的进度更新逻辑
        pass
    
    return jsonify({
        "success": True,
        "message": "进度已更新",
        "data": {
            "course_id": course_id,
            "topic": topic,
            "progress": progress,
            "completed": completed
        }
    })


# 获取学习历史
@app.route('/api/progress/history', methods=['GET'])
def get_progress_history():
    # 模拟学习历史数据
    history = [
        {"date": "2024-01-15", "minutes": 45, "courses": ["ai_math"], "score": 85},
        {"date": "2024-01-16", "minutes": 60, "courses": ["data_struct"], "score": 90},
        {"date": "2024-01-17", "minutes": 30, "courses": ["ai_math"], "score": 88},
        {"date": "2024-01-18", "minutes": 55, "courses": ["discrete_math"], "score": 75},
        {"date": "2024-01-19", "minutes": 40, "courses": ["data_struct"], "score": 92},
        {"date": "2024-01-20", "minutes": 70, "courses": ["algorithms"], "score": 80},
        {"date": "2024-01-21", "minutes": 50, "courses": ["ai_math"], "score": 87}
    ]
    
    return jsonify({
        "success": True,
        "history": history
    })


# 获取学习统计
@app.route('/api/progress/stats', methods=['GET'])
def get_progress_stats():
    analytics = assistant.get_learning_analytics()
    
    stats = {
        "total_learning_time": analytics.get('total_time_minutes', 0),
        "total_sessions": analytics.get('total_sessions', 0),
        "average_score": analytics.get('average_performance', 0),
        "streak_days": 7,
        "completed_topics": 15,
        "total_topics": 40,
        "weekly_average": 45,
        "monthly_average": 1800
    }
    
    return jsonify({
        "success": True,
        "stats": stats
    })


@app.route('/api/exercises/generate', methods=['POST'])
def generate_exercises():
    data = request.json
    topic = data.get('topic', '')
    difficulty = data.get('difficulty', 0.5)

    exercises = assistant.generate_exercises_for_topic(topic, difficulty)
    return jsonify({"exercises": exercises})


@app.route('/api/explanation/generate', methods=['POST'])
def generate_explanation():
    data = request.json
    topic = data.get('topic', '')
    concept = data.get('concept', topic)
    depth = data.get('depth', 'medium')

    explanation = assistant.generate_topic_explanation(topic, concept, depth)
    return jsonify({"explanation": explanation})


@app.route('/api/quiz/generate', methods=['POST'])
def generate_quiz():
    data = request.json
    topics = data.get('topics', [])
    count = data.get('count', 10)

    quiz = assistant.generate_quiz(topics, count)
    return jsonify(quiz)


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    analytics = assistant.get_learning_analytics()
    return jsonify(analytics)


@app.route('/api/session/end', methods=['POST'])
def end_session():
    report = assistant.end_learning_session()
    return jsonify(report)


def create_web_app():
    return app


if __name__ == '__main__':
    print("启动个性化学习助手Web服务...")
    print("访问 http://localhost:5000 开始使用")
    app.run(debug=True, port=5000)
