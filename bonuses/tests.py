from django.test import Client, TestCase
from django.utils import timezone

from bonuses.models import Bonuses


class BonusesViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.bonus = Bonuses.objects.create(
            title='重大保障加分',
            pj_score=5,
            pj_leader='张三',
            workload_allot=1,
            is_not_delayed=True,
            created_at=timezone.now(),
            body='省公司表扬',
        )

    def test_index_lists_bonuses(self):
        response = self.client.get('/bonuses/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '重大保障加分')

    def test_details_returns_bonus(self):
        response = self.client.get('/bonuses/details/%s/' % self.bonus.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '重大保障加分')

    def test_details_missing_returns_404(self):
        response = self.client.get('/bonuses/details/999999/')
        self.assertEqual(response.status_code, 404)
