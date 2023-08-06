import unittest
import pandas as pd
import numpy as np

from stse import dataframes


class TestDataframes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_df = pd.DataFrame({'a': [4, '5', '6'], 'b': ['6', '5', '4']})
        cls.mol_test_df = pd.DataFrame({'SMILES': [4, '5', '6'], 'Molecule': ['6', '5', '4'], 'InChi': [5, 6, 8]})
        cls.nan_test_df = pd.DataFrame({'a': ['', '5', '6'], 'b': ['a', '8', 'None']})
        cls.blank_solution = pd.DataFrame({'a': [np.nan, '5', '6'], 'b': ['a', '8', np.nan]})
        cls.non_num_solution = pd.DataFrame({'a': [np.nan, '5', '6'], 'b': [np.nan, '8', np.nan]})
        return super().setUpClass()
    
    def test_drop_val(self):
        # Test number
        dropped1 = dataframes.drop_val(self.test_df, 'a', 4)
        assert dropped1.equals(pd.DataFrame({'a': ['5', '6'], 'b': ['5', '4']}))
        
        # Test string
        dropped2 = dataframes.drop_val(self.test_df, 'a', '4')
        assert dropped2.equals(self.test_df)
        
        # Test b column
        dropped3 = dataframes.drop_val(self.test_df, 'b', '4')
        assert dropped3.equals(pd.DataFrame({'a': [4, '5'], 'b': ['6', '5']}))
        
    def test_pull_val(self):
        # Test number
        pulled1 = dataframes.pull_val(self.test_df, 'a', 4)
        assert pulled1.equals(pd.DataFrame({'a': [4], 'b': ['6']}).astype(object))
        
        # Test string
        pulled2 = dataframes.pull_val(self.test_df, 'a', '6')
        assert pulled2.equals(pd.DataFrame({'a': ['6'], 'b': ['4']}, index=[2]))
        
        # Test b column
        pulled3 = dataframes.pull_val(self.test_df, 'b', '5')
        assert pulled3.equals(pd.DataFrame({'a': ['5'], 'b': ['5']}, index=[1]))
        
    def test_pull_not_val(self):
        # Test number
        pulled1 = dataframes.pull_not_val(self.test_df, 'a', 4)
        assert pulled1.equals(pd.DataFrame({'a': ['5', '6'], 'b': ['5', '4']}, index=[1, 2]).astype(object))
        
        # Test string
        pulled2 = dataframes.pull_not_val(self.test_df, 'a', '6')
        assert pulled2.equals(pd.DataFrame({'a': [4, '5'], 'b': ['6', '5']}))
        
        # Test b column
        pulled3 = dataframes.pull_not_val(self.test_df, 'b', '5')
        assert pulled3.equals(pd.DataFrame({'a': [4, '6'], 'b': ['6', '4']}, index=[0, 2]))
        
        # Test pull invalid number --> returns what was input
        pulled4 = dataframes.pull_not_val(self.test_df, 'b', '3')
        assert pulled4.equals(self.test_df)
        
    def test_id_nearest_col(self):
        # Test similar variations
        assert dataframes.id_nearest_col(self.mol_test_df, 'smiles') == 'SMILES'
        assert dataframes.id_nearest_col(self.mol_test_df, 'smIles') == 'SMILES'
        assert dataframes.id_nearest_col(self.mol_test_df, 'smes') == 'SMILES'
        
        # Test null return
        assert dataframes.id_nearest_col(self.mol_test_df, 's') == None
        
    def test_remove_header_chars(self):
        test_df1 = self.mol_test_df.copy()
        test_df2 = self.mol_test_df.copy()
        test_df3 = self.mol_test_df.copy()
        test_df1.columns = ['MILE', 'Molecule', 'InChi']
        test_df2.columns = ['SMLES', 'Molecule', 'nCh']
        test_df3.columns = ['SMILES', 'Molecule', 'InCh']
        
        # Test w/ case sensitive on
        assert dataframes.remove_header_chars(self.mol_test_df, 's').equals(test_df1)
        assert dataframes.remove_header_chars(self.mol_test_df, 'S').equals(test_df1)
        
        # Test w/ case sensitive off
        assert dataframes.remove_header_chars(self.mol_test_df, 's', case_insensitive=False).equals(self.mol_test_df)
        assert dataframes.remove_header_chars(self.mol_test_df, 'S', case_insensitive=False).equals(test_df1)
        
        # Test multiple instances
        assert dataframes.remove_header_chars(self.mol_test_df, 'i').equals(test_df2)
        assert dataframes.remove_header_chars(self.mol_test_df, 'i', case_insensitive=False).equals(test_df3)
        
    def test_convert_to_nan(self):
        # Test replace nan
        na_df = dataframes.convert_to_nan(self.nan_test_df)
        assert na_df.equals(self.blank_solution)
        
        # Test case sensitivity
        na_df = dataframes.convert_to_nan(self.nan_test_df, na=('A'))
        assert na_df.equals(pd.DataFrame({'a': ['', '5', '6'], 'b': [np.nan, '8', 'None']}))
        
    def test_non_num_to_nan(self):
        # Test on only first column
        na_df = dataframes.non_num_to_nan(self.nan_test_df, self.nan_test_df.columns[0])
        assert na_df.equals(pd.DataFrame({'a': [np.nan, '5', '6'], 'b': ['a', '8', 'None']}))
        
        # Test on only second column (unchanged)
        na_df = dataframes.non_num_to_nan(self.nan_test_df, self.nan_test_df.columns[1])
        assert na_df.equals(self.nan_test_df)
        
        # Test on both columns
        na_df = dataframes.non_num_to_nan(self.nan_test_df, self.nan_test_df.columns)
        assert na_df.equals(self.non_num_solution)
        
    def test_nan_col_indices(self):
        # Test each col separately
        assert dataframes.nan_col_indices(self.blank_solution, self.blank_solution.columns[0]) == [0]
        assert dataframes.nan_col_indices(self.blank_solution, self.blank_solution.columns[1]) == [2]
        
    def test_remove_nan_cols(self):
        nan_col_df = self.test_df.copy()
        
        # Append new columns
        nan_col_df['c'] = 3*['None']
        nan_col_df['d'] = 3*['nan']
        nan_col_df['e'] = 3*['']
        nan_col_df['f'] = 3*[np.nan]
        
        # Check new columns were added successfully
        assert len(nan_col_df.columns) == 6
        
        # Test blank column removal
        assert dataframes.remove_nan_cols(nan_col_df).equals(self.test_df)
        
    def test_remove_nan_rows(self):
        self.non_num_solution = pd.DataFrame({'a': [np.nan, '5', '6'], 'b': [np.nan, '8', np.nan]})
        
        col_a = dataframes.remove_nan_rows(self.blank_solution, ['a'])
        assert col_a.equals(pd.DataFrame({'a': ['5', '6'], 'b': ['8', np.nan]}))
        
        col_b = dataframes.remove_nan_rows(self.blank_solution, ['b'])
        assert col_b.equals(pd.DataFrame({'a': [np.nan, '5'], 'b': ['a', '8']}))
        
        both_cols = dataframes.remove_nan_rows(self.blank_solution, self.blank_solution.columns)
        assert both_cols.equals(pd.DataFrame({'a': ['5'], 'b': ['8']}))


if __name__ == '__main__':
    unittest.main()