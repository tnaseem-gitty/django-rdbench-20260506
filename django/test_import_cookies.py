try:
    import http.cookies as cookies
    print("Import successful")
except ImportError as e:
    print(f"ImportError: {e}")
    from http import cookies
    print("Import successful")
except ImportError as e:
    print(f"ImportError: {e}")
