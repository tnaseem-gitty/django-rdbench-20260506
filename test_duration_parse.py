from django.utils.dateparse import parse_duration

def test_parse_duration():
    test_cases = [
        ("-1:00:00", "-1:00:00"),
        ("-1 day, 0:00:00", "-1 day, 0:00:00"),
        ("-1:00:00.000001", "-1:00:00.000001"),
        ("1 day, -1:00:00", "1 day, -1:00:00"),
    ]

    for input_str, expected_output in test_cases:
        result = parse_duration(input_str)
        print(f"Input: {input_str}")
        print(f"Result: {result}")
        print(f"Expected: {expected_output}")
        print(f"Pass: {str(result) == expected_output}")
        print()

    print("All tests completed.")

if __name__ == "__main__":
    test_parse_duration()
