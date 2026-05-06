from django.db import models
from django.test import SimpleTestCase
from django.db.models import UniqueConstraint
from django.test.utils import isolate_apps
from unittest.mock import patch, MagicMock

@isolate_apps('tests')
class InBulkTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        class TestModel(models.Model):
            slug = models.CharField(max_length=255)

            class Meta:
                constraints = [
                    UniqueConstraint(fields=['slug'], name='unique_slug')
                ]
                app_label = 'tests'

        cls.TestModel = TestModel

    @patch('django.db.models.query.QuerySet.in_bulk')
    def test_in_bulk_with_unique_constraint(self, mock_in_bulk):
        mock_in_bulk.return_value = {
            'test1': MagicMock(slug='test1'),
            'test2': MagicMock(slug='test2'),
            'test3': MagicMock(slug='test3')
        }
        objects = self.TestModel.objects.in_bulk(field_name='slug')
        self.assertEqual(len(objects), 3)
        self.assertIn('test1', objects)
        self.assertIn('test2', objects)
        self.assertIn('test3', objects)
        self.assertEqual(objects['test1'].slug, 'test1')
        self.assertEqual(objects['test2'].slug, 'test2')
        self.assertEqual(objects['test3'].slug, 'test3')
        mock_in_bulk.assert_called_once_with(field_name='slug')

    @patch('django.db.models.query.QuerySet.in_bulk')
    def test_in_bulk_with_id(self, mock_in_bulk):
        mock_in_bulk.return_value = {
            1: MagicMock(slug='test1'),
            2: MagicMock(slug='test2'),
            3: MagicMock(slug='test3')
        }
        objects = self.TestModel.objects.in_bulk()
        self.assertEqual(len(objects), 3)
        self.assertIn(1, objects)
        self.assertIn(2, objects)
        self.assertIn(3, objects)
        self.assertEqual(objects[1].slug, 'test1')
        self.assertEqual(objects[2].slug, 'test2')
        self.assertEqual(objects[3].slug, 'test3')
        mock_in_bulk.assert_called_once_with()

    @patch('django.db.models.query.QuerySet.in_bulk')
    def test_in_bulk_with_ids(self, mock_in_bulk):
        mock_in_bulk.return_value = {
            1: MagicMock(slug='test1'),
            3: MagicMock(slug='test3')
        }
        objects = self.TestModel.objects.in_bulk([1, 3])
        self.assertEqual(len(objects), 2)
        self.assertIn(1, objects)
        self.assertIn(3, objects)
        self.assertEqual(objects[1].slug, 'test1')
        self.assertEqual(objects[3].slug, 'test3')
        mock_in_bulk.assert_called_once_with([1, 3])

    @patch('django.db.models.query.QuerySet.in_bulk')
    def test_in_bulk_with_empty_list(self, mock_in_bulk):
        mock_in_bulk.return_value = {}
        objects = self.TestModel.objects.in_bulk([])
        self.assertEqual(len(objects), 0)
        mock_in_bulk.assert_called_once_with([])

    @patch('django.db.models.query.QuerySet.in_bulk')
    def test_in_bulk_with_invalid_field(self, mock_in_bulk):
        mock_in_bulk.side_effect = ValueError("Invalid field name")
        with self.assertRaises(ValueError):
            self.TestModel.objects.in_bulk(field_name='invalid_field')
        mock_in_bulk.assert_called_once_with(field_name='invalid_field')

    @patch('django.db.models.query.QuerySet.in_bulk')
    def test_in_bulk_with_nonexistent_ids(self, mock_in_bulk):
        mock_in_bulk.return_value = {}
        objects = self.TestModel.objects.in_bulk([999, 1000])
        self.assertEqual(len(objects), 0)
        mock_in_bulk.assert_called_once_with([999, 1000])
