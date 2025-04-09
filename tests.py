import logging
import unittest

logging.getLogger().setLevel(logging.CRITICAL)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
