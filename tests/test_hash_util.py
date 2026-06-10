import tempfile
import os
from signalnoise.utils.hash_util import calculate_file_hash


def test_calculate_file_hash():
    # Test empty file hash (standard empty SHA256)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.flush()
        empty_path = f.name
    try:
        empty_hash = calculate_file_hash(empty_path)
        assert empty_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    finally:
        os.remove(empty_path)

    # Test "hello world" file hash
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
        f.write(b"hello world")
        f.flush()
        hello_path = f.name
    try:
        hello_hash = calculate_file_hash(hello_path)
        # sha256("hello world")
        assert hello_hash == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    finally:
        os.remove(hello_path)
