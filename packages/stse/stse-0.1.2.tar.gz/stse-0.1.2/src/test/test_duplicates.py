import unittest
import pandas as pd

from stse import duplicates


class TestDuplicates(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_df = pd.DataFrame({'aa': ['5', '5', '6', 5, 6, '6'], 'b': [1, 2, 3, 4, 5, 6], 
                                     'c': ['a', 'a', 'b', 'b', 'b', 'b']})
        cls.filt_not_dup_sol = pd.DataFrame({'aa': ['5', '6', 5, 6], 'b': [1, 3, 4, 5], 'c': ['a', 'b', 'b', 'b']}, 
                                             index=[0, 2, 3, 4])
        cls.filt_dup_sol = pd.DataFrame({'aa': ['5', '6'], 'b': [2, 6], 'c': ['a', 'b']}, index=[1, 5])
        cls.filt_multi_not_dup_sol = pd.DataFrame({'aa': ['5', '6'], 'b': [1, 3], 'c': ['a', 'b']}, 
                                                   index=[0, 2])
        cls.filt_multi_dup_sol = pd.DataFrame({'aa': ['5', 5, 6, '6'], 'b': [2, 4, 5, 6], 
                                                'c': ['a', 'b', 'b', 'b']}, index=[1, 3, 4, 5])
        cls.average_sol = pd.DataFrame({'aa': ['5', '6', 5, 6], 'b': [1.5, 4.5, 4, 5], 'c': ['a', 'b', 'b', 'b']}, 
                                        index=[0, 2, 3, 4])
        return super().setUpClass()
    
    def test_filter(self):
        # Test filtering out duplicates
        assert duplicates.filter(self.test_df, ['aa']).equals(self.filt_not_dup_sol)
        
        # Test filtering out everything EXCEPT duplicates
        assert duplicates.filter(self.test_df, ['aa'], return_duplicates=True).equals(self.filt_dup_sol)
        
        # Test filtering across multiple subsets
        assert duplicates.filter(self.test_df, ['aa', 'c'], how='any').equals(self.filt_multi_not_dup_sol)
        assert duplicates.filter(self.test_df, ['aa', 'c'], how='any', return_duplicates=True).equals(
            self.filt_multi_dup_sol)
    
    def test_indices(self):
        self.assertEqual(
            duplicates.indices(self.test_df, 'c'), 
            [1, 3, 4, 5]
        )
        
    def test_remove(self):
        assert duplicates.remove(self.test_df, ['aa']).equals(self.filt_not_dup_sol)
        
    def test_average(self):
        assert duplicates.average(self.test_df, ['aa'], average_by='b').equals(self.average_sol)


if __name__ == '__main__':
    unittest.main()
