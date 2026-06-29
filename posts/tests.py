from django.test import Client, TestCase
from django.utils import timezone

from posts.models import Posts


class PostsViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.post = Posts.objects.create(
            title='核心网项目',
            pj_score=10,
            pj_leader='张三',
            workload_allot=1,
            deadline_at=timezone.now(),
            pj_progress=1,
            is_not_delayed=True,
            body='完成',
        )

    def test_index_lists_posts(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '核心网项目')

    def test_details_returns_post(self):
        response = self.client.get('/posts/details/%s/' % self.post.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '核心网项目')

    def test_details_missing_returns_404(self):
        response = self.client.get('/posts/details/999999/')
        self.assertEqual(response.status_code, 404)

    def test_welcome_landing_page(self):
        response = self.client.get('/welcom/')
        self.assertEqual(response.status_code, 200)

    def test_root_renders_welcome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
