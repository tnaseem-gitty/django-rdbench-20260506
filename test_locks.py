import os
from django.core.files import locks

def test_lock_unlock():
    # Create a temporary file
    with open('test_lock_file', 'w') as f:
        f.write('Test content')

    # Open the file for reading
    with open('test_lock_file', 'r') as f:
        # Try to acquire a lock
        lock_acquired = locks.lock(f, locks.LOCK_EX | locks.LOCK_NB)
        print(f"Lock acquired: {lock_acquired}")

        if lock_acquired:
            # Try to unlock
            unlock_success = locks.unlock(f)
            print(f"Unlock successful: {unlock_success}")
        else:
            print("Failed to acquire lock")

    # Clean up
    os.remove('test_lock_file')

if __name__ == "__main__":
    test_lock_unlock()
