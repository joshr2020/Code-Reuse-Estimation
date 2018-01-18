import binary_compare

def test_getTotalSize():
    dict1 = {'hi': '5', 'bye': '15'}
    assert binary_compare.getTotalSize(dict1) == 26 # bc base 16

def test_jaccard():
    dict1 = {'hi': '5', 'bye': '15', 'shalom': '10', 'pi': '25'}
    dict2 = {'hi': '6', 'bye': '15', 'shalom2': '10', 'pi': '25'}
    assert binary_compare.jaccard(dict1, dict2) == float(58/101)
