from django.test import TestCase
from my_app.models import Inventory

class InventoryTestCase(TestCase):
    def test_inventory_items(self):
        inventory_items = Inventory.objects.all()
        for item in inventory_items:
            print(item)