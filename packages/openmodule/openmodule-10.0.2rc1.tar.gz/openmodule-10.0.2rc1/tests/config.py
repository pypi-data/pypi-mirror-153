import random
import string

# test config for openmodule

NAME = "test"
RESOURCE = "test-resource"
VERSION = "test-version"
random_suffix = "".join(random.choices(string.ascii_letters, k=10))
BROKER_SUB = f"inproc://test-sub-{random_suffix}"
BROKER_PUB = f"inproc://test-pub-{random_suffix}"
