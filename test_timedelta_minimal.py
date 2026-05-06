import unittest
import sqlite3
import datetime

class TimeDeltaTest(unittest.TestCase):
    def test_timedelta_addition(self):
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        # Convert timedelta to milliseconds
        def timedelta_to_ms(td):
            return td.days * 86400000 + td.seconds * 1000 + td.microseconds // 1000

        # Test the addition of two timedelta values (in milliseconds)
        ms1 = timedelta_to_ms(datetime.timedelta(milliseconds=345))
        ms2 = timedelta_to_ms(datetime.timedelta(days=1))
        
        cursor.execute("SELECT ? + ?", (ms1, ms2))
        result_ms = cursor.fetchone()[0]
        
        result = datetime.timedelta(milliseconds=result_ms)
        expected = datetime.timedelta(days=1, milliseconds=345)

        self.assertEqual(result, expected)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Are they equal? {result == expected}")

        conn.close()

if __name__ == '__main__':
    unittest.main()
