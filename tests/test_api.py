import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app import app


class TestAPI:
    """测试学习助手API"""
    
    def setup_method(self):
        """设置测试客户端"""
        self.client = app.test_client()
        self.client.testing = True
    
    def test_auth_register(self):
        """测试用户注册"""
        response = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'password': 'testpass',
            'name': '测试用户',
            'student_id': 'test001'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert '欢迎' in data['message']
    
    def test_auth_login(self):
        """测试用户登录"""
        # 先注册
        self.client.post('/api/auth/register', json={
            'username': 'loginuser',
            'password': 'loginpass',
            'name': '登录测试',
            'student_id': 'login001'
        })
        
        # 再登录
        response = self.client.post('/api/auth/login', json={
            'username': 'loginuser',
            'password': 'loginpass'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['username'] == 'loginuser'
    
    def test_auth_login_wrong_password(self):
        """测试错误密码登录"""
        response = self.client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is False
    
    def test_auth_status(self):
        """测试登录状态检查"""
        response = self.client.get('/api/auth/status')
        assert response.status_code == 200
        data = response.get_json()
        assert 'logged_in' in data
    
    def test_assessment_questions(self):
        """测试获取评估问题"""
        response = self.client.get('/api/assessment/questions')
        assert response.status_code == 200
        data = response.get_json()
        assert 'questions' in data
    
    def test_courses_list(self):
        """测试获取课程列表"""
        response = self.client.get('/api/courses')
        assert response.status_code == 200
        data = response.get_json()
        assert 'courses' in data
        assert isinstance(data['courses'], list)
    
    def test_course_detail(self):
        """测试获取课程详情"""
        response = self.client.get('/api/course/ai_math')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'course' in data
    
    def test_course_resources(self):
        """测试获取课程资源"""
        response = self.client.get('/api/course/ai_math/resources')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'resources' in data
    
    def test_progress(self):
        """测试获取学习进度"""
        response = self.client.get('/api/progress')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'progress' in data
    
    def test_progress_stats(self):
        """测试获取学习统计"""
        response = self.client.get('/api/progress/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'stats' in data
    
    def test_progress_history(self):
        """测试获取学习历史"""
        response = self.client.get('/api/progress/history')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'history' in data
    
    def test_recommendations(self):
        """测试获取学习推荐"""
        response = self.client.get('/api/recommendations')
        assert response.status_code == 200
        data = response.get_json()
        assert 'recommendations' in data
    
    def test_exercises_generate(self):
        """测试生成练习题"""
        response = self.client.post('/api/exercises/generate', json={
            'topic': 'machine learning',
            'difficulty': 0.5
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'exercises' in data
    
    def test_explanation_generate(self):
        """测试生成讲解"""
        response = self.client.post('/api/explanation/generate', json={
            'topic': 'machine learning',
            'concept': 'neural network',
            'depth': 'medium'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'explanation' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])