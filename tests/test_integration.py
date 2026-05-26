import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app import app
from core.learning_assistant import LearningAssistant
from core.learning_style_analyzer import LearningStyleAnalyzer


class TestIntegration:
    """集成测试"""
    
    def setup_method(self):
        """设置测试环境"""
        self.client = app.test_client()
        self.client.testing = True
        self.assistant = LearningAssistant()
        self.analyzer = LearningStyleAnalyzer()
    
    def test_full_learning_flow(self):
        """测试完整学习流程"""
        # 1. 注册用户
        register_response = self.client.post('/api/auth/register', json={
            'username': 'integration_user',
            'password': 'testpass123',
            'name': '集成测试用户',
            'student_id': 'integ001'
        })
        assert register_response.status_code == 200
        register_data = register_response.get_json()
        assert register_data['success'] is True
        
        # 2. 登录
        login_response = self.client.post('/api/auth/login', json={
            'username': 'integration_user',
            'password': 'testpass123'
        })
        assert login_response.status_code == 200
        login_data = login_response.get_json()
        assert login_data['success'] is True
        
        # 3. 获取评估问题
        questions_response = self.client.get('/api/assessment/questions')
        assert questions_response.status_code == 200
        questions_data = questions_response.get_json()
        assert 'questions' in questions_data
        assert len(questions_data['questions']) > 0
        
        # 4. 提交评估
        responses = []
        for i, q in enumerate(questions_data['questions']):
            responses.append({
                'question_id': q['id'],
                'selected_option': 0
            })
        
        assessment_response = self.client.post('/api/assessment/submit', json={
            'responses': responses
        })
        assert assessment_response.status_code == 200
        assessment_data = assessment_response.get_json()
        assert assessment_data['success'] is True
        assert 'profile' in assessment_data
        
        # 5. 获取课程列表
        courses_response = self.client.get('/api/courses')
        assert courses_response.status_code == 200
        courses_data = courses_response.get_json()
        assert len(courses_data['courses']) > 0
        
        # 6. 获取课程详情
        course_id = courses_data['courses'][0]['course_id']
        course_response = self.client.get(f'/api/course/{course_id}')
        assert course_response.status_code == 200
        course_data = course_response.get_json()
        assert course_data['success'] is True
        
        # 7. 获取推荐
        recommendations_response = self.client.get('/api/recommendations')
        assert recommendations_response.status_code == 200
        recommendations_data = recommendations_response.get_json()
        assert 'recommendations' in recommendations_data
        
        # 8. 获取学习进度
        progress_response = self.client.get('/api/progress')
        assert progress_response.status_code == 200
        progress_data = progress_response.get_json()
        assert progress_data['success'] is True
        
        print("✅ 完整学习流程测试通过！")
    
    def test_learning_assistant_flow(self):
        """测试学习助手核心流程"""
        # 创建学生档案
        self.assistant.create_student_profile("test_student", "测试学生")
        assert self.assistant.student is not None
        assert self.assistant.student.name == "测试学生"
        
        # 获取可用课程
        courses = self.assistant.get_available_courses()
        assert isinstance(courses, list)
        assert len(courses) > 0
        
        # 获取课程主题
        if courses:
            course_id = courses[0]['course_id']
            topics = self.assistant.get_course_topics(course_id)
            assert isinstance(topics, list)
        
        # 获取推荐
        recommendations = self.assistant.get_learning_recommendations()
        assert isinstance(recommendations, list)
        
        print("✅ 学习助手核心流程测试通过！")
    
    def test_learning_style_analyzer(self):
        """测试学习风格分析器"""
        # 创建评估问题
        questions = self.analyzer.create_initial_assessment()
        assert isinstance(questions, list)
        assert len(questions) == 10
        
        # 验证问题格式
        for q in questions:
            assert 'id' in q
            assert 'question' in q
            assert 'options' in q
            assert len(q['options']) == 3
        
        print("✅ 学习风格分析器测试通过！")
    
    def test_exercise_generation(self):
        """测试练习题生成"""
        # 生成练习题
        exercises = self.assistant.generate_exercises_for_topic("machine learning")
        assert isinstance(exercises, list)
        
        # 检查练习题格式
        for ex in exercises[:3]:  # 只检查前3道题
            assert 'question' in ex
            assert 'type' in ex
        
        print("✅ 练习题生成测试通过！")
    
    def test_explanation_generation(self):
        """测试讲解生成"""
        # 生成讲解
        explanation = self.assistant.generate_topic_explanation(
            "machine learning", "neural network", "medium"
        )
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        
        print("✅ 讲解生成测试通过！")
    
    def test_analytics(self):
        """测试学习分析"""
        # 创建学生档案
        self.assistant.create_student_profile("analytics_test", "分析测试")
        
        # 获取分析数据
        analytics = self.assistant.get_learning_analytics()
        assert isinstance(analytics, dict)
        assert 'total_time_minutes' in analytics
        assert 'total_sessions' in analytics
        
        print("✅ 学习分析测试通过！")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])