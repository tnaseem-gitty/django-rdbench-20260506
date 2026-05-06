from datetime import datetime

from django.core.exceptions import FieldError
from django.db import models
from django.db.models import BooleanField, CharField, F, Q
from django.db.models.expressions import Col, Func, Value
from django.db.models.fields.related_lookups import RelatedIsNull
from django.db.models.lookups import Exact, GreaterThan, IsNull, LessThan
from django.db.models.sql import Query
from django.db.models.sql.query import JoinPromoter
from django.test import SimpleTestCase, TestCase
from django.test.utils import isolate_apps, register_lookup

from .models import Author, ExtraInfo, Item, ObjectC, Ranking


class TestQuery(TestCase):
    def test_bulk_update_with_f_expression(self):
        # Create and save the objects first
        extra_info = ExtraInfo.objects.create()
        obj = Author.objects.create(name='test', num=30, extra=extra_info)
        
        # Now update the num with an F expression
        obj.num = F('name')
        
        # Use the actual bulk_update method
        Author.objects.bulk_update([obj], ['num'])

        # Refresh the object from the database
        obj.refresh_from_db()

        # Check if the F expression was preserved
        self.assertEqual(str(obj.num), obj.name)

    def test_negated_nullable(self):
        query = Query(Item)
        where = query.build_where(~Q(modified__lt=datetime(2017, 1, 1)))
        self.assertTrue(where.negated)
        lookup = where.children[0]
        self.assertIsInstance(lookup, LessThan)
        self.assertEqual(lookup.lhs.target, Item._meta.get_field('modified'))
        lookup = where.children[1]
        self.assertIsInstance(lookup, IsNull)
        self.assertEqual(lookup.lhs.target, Item._meta.get_field('modified'))

    def test_foreign_key(self):
        query = Query(Item)
        msg = 'Joined field references are not permitted in this query'
        with self.assertRaisesMessage(FieldError, msg):
            query.build_where(Q(creator__num__gt=2))

    def test_foreign_key_f(self):
        query = Query(Ranking)
        with self.assertRaises(FieldError):
            query.build_where(Q(rank__gt=F('author__num')))

    def test_foreign_key_exclusive(self):
        query = Query(ObjectC, alias_cols=False)
        where = query.build_where(Q(objecta=None) | Q(objectb=None))
        a_isnull = where.children[0]
        self.assertIsInstance(a_isnull, RelatedIsNull)
        self.assertIsInstance(a_isnull.lhs, Col)
        self.assertIsNone(a_isnull.lhs.alias)
        self.assertEqual(a_isnull.lhs.target, ObjectC._meta.get_field('objecta'))
        b_isnull = where.children[1]
        self.assertIsInstance(b_isnull, RelatedIsNull)
        self.assertIsInstance(b_isnull.lhs, Col)
        self.assertIsNone(b_isnull.lhs.alias)
        self.assertEqual(b_isnull.lhs.target, ObjectC._meta.get_field('objectb'))

    def test_clone_select_related(self):
        query = Query(Item)
        query.add_select_related(['creator'])
        clone = query.clone()
        clone.add_select_related(['note', 'creator__extra'])
        self.assertEqual(query.select_related, {'creator': {}})

    def test_iterable_lookup_value(self):
        query = Query(Item)
        where = query.build_where(Q(name=['a', 'b']))
        name_exact = where.children[0]
        self.assertIsInstance(name_exact, Exact)
        self.assertEqual(name_exact.rhs, "['a', 'b']")

    def test_filter_conditional(self):
        query = Query(Item)
        where = query.build_where(Func(output_field=BooleanField()))
        exact = where.children[0]
        self.assertIsInstance(exact, Exact)
        self.assertIsInstance(exact.lhs, Func)
        self.assertIs(exact.rhs, True)

    def test_filter_conditional_join(self):
        query = Query(Item)
        filter_expr = Func('note__note', output_field=BooleanField())
        msg = 'Joined field references are not permitted in this query'
        with self.assertRaisesMessage(FieldError, msg):
            query.build_where(filter_expr)

    def test_filter_non_conditional(self):
        query = Query(Item)
        msg = 'Cannot filter against a non-conditional expression.'
        with self.assertRaisesMessage(TypeError, msg):
            query.build_where(Func(output_field=CharField()))


class JoinPromoterTest(SimpleTestCase):
    def test_repr(self):
        self.assertEqual(
            repr(JoinPromoter('AND', 3, True)),
            "JoinPromoter(connector='AND', num_children=3, negated=True)",
        )
