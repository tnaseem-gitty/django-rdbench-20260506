# ISSUE (RESOLVED): Include number of rows matched in bulk_update() return value

## Description

This issue has been resolved. The `bulk_update()` method now returns the number of rows matched, as requested. The implementation can be found in `django/db/models/query.py`, in the `bulk_update` method.

The method now keeps track of the total number of rows matched across all update operations and returns this value at the end of the method.

## Resolution Details

- File: `django/db/models/query.py`
- Method: `bulk_update`
- Change: The method now returns `total_rows_matched`, which is the sum of all rows matched across all update operations.

## Verification

A test case has been added to verify this behavior:

```python
def test_bulk_update_returns_rows_matched(self):
    for note in self.notes:
        note.note = 'updated-%s' % note.id
    rows_matched = Note.objects.bulk_update(self.notes, ['note'])
    self.assertIsNotNone(rows_matched, "bulk_update should return a value")
    self.assertEqual(rows_matched, len(self.notes), "bulk_update should return the number of rows matched")
    self.assertCountEqual(
        Note.objects.values_list('note', flat=True),
        ['updated-%s' % note.id for note in self.notes]
    )
```

This test case confirms that `bulk_update()` returns the correct number of rows matched.

No further action is required for this issue.
