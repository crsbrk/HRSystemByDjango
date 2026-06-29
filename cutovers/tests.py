from django.test import Client, TestCase
from django.utils import timezone

from cutovers.models import Cutovers


class CutoversViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.cutover = Cutovers.objects.create(
            cutover_num='GJ-001',
            title='核心网割接',
            pj_leader='张三',
            deadline_at=timezone.now(),
            is_not_delayed=True,
            body='完成',
        )

    def test_index_lists_cutovers(self):
        response = self.client.get('/cutovers/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '核心网割接')

    def test_details_returns_cutover(self):
        response = self.client.get('/cutovers/details/%s/' % self.cutover.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '核心网割接')

    def test_details_missing_returns_404(self):
        response = self.client.get('/cutovers/details/999999/')
        self.assertEqual(response.status_code, 404)
