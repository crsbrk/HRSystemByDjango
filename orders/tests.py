from django.test import Client, TestCase
from django.utils import timezone

from orders.models import Orders


class OrdersViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.order = Orders.objects.create(
            orders_num='GD-001',
            title='物联网工单',
            pj_score=1,
            pj_leader='张三',
            workload_allot=1,
            deadline_at=timezone.now(),
            is_not_delayed=True,
            is_finished=True,
            body='完成',
        )

    def test_index_lists_orders(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '物联网工单')

    def test_details_returns_order(self):
        response = self.client.get('/orders/details/%s/' % self.order.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '物联网工单')

    def test_details_missing_returns_404(self):
        response = self.client.get('/orders/details/999999/')
        self.assertEqual(response.status_code, 404)

    def test_index_pagination_second_page_is_valid(self):
        for i in range(20):
            Orders.objects.create(
                orders_num='GD-%s' % i,
                title='批量工单%s' % i,
                pj_score=1,
                pj_leader='张三',
                workload_allot=1,
                deadline_at=timezone.now(),
                is_not_delayed=True,
                is_finished=False,
                body='x',
            )
        response = self.client.get('/orders/?page=2')
        self.assertEqual(response.status_code, 200)
