import logging
import unittest

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.CRITICAL)

    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
