from django.test import TestCase
from senex.models import PromoBox

class PromoBoxTestCase(TestCase):
    def setUp(self):
        promobox_1 = PromoBox()
        promobox_1.save()
        promobox_2 = PromoBox()
        promobox_2.save()

    def test_promobox_ordering(self):
        """Promoboxes should be returned in order and the orders should be unique"""
        promoboxes = PromoBox.objects.all()
        promobox_3 = PromoBox(ordering=0)
        promobox_3.save()
        self.assertEqual(promoboxes[0].ordering, 0)
        self.assertEqual(promoboxes[1].ordering, 1)
        self.assertEqual(promoboxes[2].ordering, 2)