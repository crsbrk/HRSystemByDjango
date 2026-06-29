from django.test import Client, TestCase
from django.utils import timezone

from faulty.models import Faulty


class FaultyViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.fault = Faulty.objects.create(
            title='链路中断故障',
            pj_score=2,
            pj_type='硬件',
            pj_manufacturer='华为',
            pj_leader='张三',
            workload_allot=1,
            is_not_delayed=True,
            created_at=timezone.now(),
            body='已处理',
        )

    def test_index_lists_faults(self):
        response = self.client.get('/faulty/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '链路中断故障')

    def test_details_returns_fault(self):
        response = self.client.get('/faulty/details/%s/' % self.fault.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '链路中断故障')

    def test_details_missing_returns_404(self):
        response = self.client.get('/faulty/details/999999/')
        self.assertEqual(response.status_code, 404)
