from toolbox_joacripp.preprocessing import duplicate_count, drop_duplicates
import pandas as pd

def test_duplicate_count():
    """
    Test the duplicate_count function
    """
    data = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 10, 10]})
    count = duplicate_count(data)
    assert count == 2

def test_drop_duplicates():
    """
    Test the drop_duplicates function
    """
    data = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 10, 10]})
    data = drop_duplicates(data)
    assert data.shape == (10, 1)