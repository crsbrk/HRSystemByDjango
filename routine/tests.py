from django.test import Client, TestCase
from django.utils import timezone

from routine.models import Routine


class RoutineViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.routine = Routine.objects.create(
            title='每日巡检',
            pj_score=1,
            pj_leader='张三',
            workload_allot=1,
            is_not_delayed=True,
            created_at=timezone.now(),
            body='完成',
        )

    def test_index_lists_routines(self):
        response = self.client.get('/routine/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '每日巡检')

    def test_details_returns_routine(self):
        response = self.client.get('/routine/details/%s/' % self.routine.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '每日巡检')

    def test_details_missing_returns_404(self):
        response = self.client.get('/routine/details/999999/')
        self.assertEqual(response.status_code, 404)
