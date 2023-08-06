import unittest
import numpy as np

from stse import bytes


class TestBytes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def test_bit_vect(self):
        # Test non-iterable single index value
        np.testing.assert_array_equal(
            bytes.bit_vect(8, 1), 
            [0, 1, 0, 0, 0, 0, 0, 0]
        )
        
        # Test iterable multi-index value
        np.testing.assert_array_equal(
            bytes.bit_vect(8, [1, 2, 3, 6]), 
            [0, 1, 1, 1, 0, 0, 1, 0]
        )
        
    def test_remove_hot_overlap(self):
        # Test w/ lists
        np.testing.assert_array_equal(
            bytes.remove_hot_overlap([0, 1, 1, 0, 0], [1, 1, 0, 0, 0]),
            [0, 0, 1, 0, 0]
        )
        
        # Test w/ arrays
        np.testing.assert_array_equal(
            bytes.remove_hot_overlap(np.array([0, 1, 1, 0, 0]), np.array([1, 1, 0, 0, 0])),
            [0, 0, 1, 0, 0]
        )


if __name__ == '__main__':
    unittest.main()
