from django.db.backends.ddl_references import IndexColumns

def test_index_columns():
    # Test case 1: Column with DESC
    ic1 = IndexColumns('mytable', ['name'], lambda x: f'"{x}"', col_suffixes=['DESC'], opclasses=[''])
    print(f"Test case 1 (DESC): {ic1}")

    # Test case 2: Column with opclass
    ic2 = IndexColumns('mytable', ['name'], lambda x: f'"{x}"', col_suffixes=[''], opclasses=['text_pattern_ops'])
    print(f"Test case 2 (opclass): {ic2}")

    # Test case 3: Column with both opclass and DESC
    ic3 = IndexColumns('mytable', ['name'], lambda x: f'"{x}"', col_suffixes=['DESC'], opclasses=['text_pattern_ops'])
    print(f"Test case 3 (opclass and DESC): {ic3}")

if __name__ == '__main__':
    test_index_columns()
