"""Test JSON Cut main functions."""
import jsoncut.core
import pytest
import warnings

TEST_DATA = {
    'info': 'test',
    'results': [
        {
            'id': 1719,
            'via': {
                'channel': 'email',
                'source': {
                    'from': {'name': 'John Doe'}
                }
            }
        },
        {
            'id': 1720,
            'via': {
                'channel': 'email',
                'source': {
                    'from': {'name': 'Jane Doe'}
                }
            }
        }
    ]
}

PRUNED_TEST_DATA = [
    {
        'id': 1719,
        'source': {'from': {}}
    },
    {
        'id': 1720,
        'source': {'from': {}}
    }
]


def test_cut():
    """Test core.cut()."""
    rootkey = 'results'
    getkeys = 'id, via.source'
    delkeys = 'source.from.name'
    result = jsoncut.core.cut(TEST_DATA, rootkey=rootkey, getkeys=getkeys,
                              delkeys=delkeys)
    assert result == PRUNED_TEST_DATA

def test_get_items_warnings(capsys):
    """ Test core.get_items issues UserWarning for missing key"""
    
    args = TEST_DATA, 'results', 'info1'
    kwargs = {'fullpath': True}
    with pytest.warns(UserWarning) as w:
        jsoncut.core.get_items(TEST_DATA, ['result'], ['info'], fullpath=True)

    assert w[0].message.args[0] == 'Missing key "\'result\'"' 
