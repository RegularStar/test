import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


# 공통함수(변경없음)
def create_question(question_text, days):
    """
    days: 질문 공개 날짜(pub_date)를 오늘 기준으로 며칠 전/후로 설정
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# 모델 메서드 테스트(변경됨)
class QuestionModelTests(TestCase):
    def setUp(self):
        """
        매 테스트마다 사용할 기본 질문 객체 3종 생성
        """
        now = timezone.now()
        self.future_question = Question(pub_date=now + datetime.timedelta(days=30))
        self.old_question = Question(
            pub_date=now - datetime.timedelta(days=1, seconds=1)
        )
        self.recent_question = Question(
            pub_date=now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        )

    def test_was_published_recently_with_future_question(self):
        """미래 질문은 최근 게시된 것이 아니므로 False"""
        self.assertIs
        (self.future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """1일 이상 지난 과거 질문은 False"""
        self.assertIs
        (self.old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """24시간 이내의 질문은 True"""
        self.assertIs
        (self.recent_question.was_published_recently(), True)


# Index 뷰 테스트(변경없음)
class QuestionIndexViewTests(TestCase):
    def setUp(self):
        self.url = reverse("polls:index")

    def test_no_questions(self):
        """질문이 없을 경우 메시지 출력"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual
        (response.context["latest_question_list"], [])

    def test_past_question(self):
        """과거 질문은 목록에 보여야 함"""
        question = create_question("Past question", days=-30)
        response = self.client.get(self.url)
        self.assertQuerySetEqual
        (response.context["latest_question_list"], [question])

    def test_future_question(self):
        """미래 질문은 목록에 보이면 안 됨"""
        create_question("Future question", days=30)
        response = self.client.get(self.url)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual
        (response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """과거 질문만 목록에 표시되어야 함"""
        past_question = create_question("Past question", days=-30)
        create_question("Future question", days=30)
        response = self.client.get(self.url)
        self.assertQuerySetEqual
        (response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        """과거 질문이 여러 개일 경우 최신 순으로 정렬되어야 함"""
        q1 = create_question("Past question 1", days=-30)
        q2 = create_question("Past question 2", days=-5)
        response = self.client.get(self.url)
        self.assertQuerySetEqual
        (response.context["latest_question_list"], [q2, q1])


# Detail 뷰 테스트(변경없음)
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """미래 질문 상세 페이지는 404 반환"""
        future_question = create_question("Future question", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """과거 질문 상세 페이지는 접근 가능"""
        past_question = create_question("Past question", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
