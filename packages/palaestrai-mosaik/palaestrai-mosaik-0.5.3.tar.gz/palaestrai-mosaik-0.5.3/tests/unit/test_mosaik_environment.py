import unittest
from unittest.mock import MagicMock, patch

from palaestrai_mosaik.mosaik_environment import MosaikEnvironment


class TestMosaikEnvironment(unittest.TestCase):
    @unittest.skip
    @patch(f"{MosaikEnvironment.__module__}.threading.Thread")
    @patch(f"{MosaikEnvironment.__module__}.MosaikWorld")
    def test_start(self, mock_world, mock_thread):
        env = MosaikEnvironment(
            "", "", 0, params={"reward": {"name": "", "params": dict()}}
        )
        mock_world.setup = MagicMock()

        env.start_environment()


if __name__ == "__main__":
    unittest.main()
