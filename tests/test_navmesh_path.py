import pytest

from gameplay import navmesh_path as mod

CASES = [
    pytest.param('portal_side', ((0, 0), (0, 1), (1, 1)), 'right', False, id='01_portal_left'),
    pytest.param('portal_side', ((0, 0), (0, 1), (-1, 1)), 'left', False, id='02_portal_right'),
    pytest.param('portal_side', ((0, 0), (0, 1), (0, 2)), 'straight', False, id='03_portal_straight'),
    pytest.param('portal_side', ((0, 0), (0, 1), (0, 0)), 'straight', False, id='04_portal_back'),
    pytest.param('portal_side', ((0, 0), (1, 1), (2, 2)), 'straight', False, id='05_portal_diag'),
    pytest.param('path_cost', ([(0, 0), (3, 4)], 0.0), 5.0, True, id='06_cost_two'),
    pytest.param('path_cost', ([(0, 0), (3, 4), (3, 5)], 0.0), 6.0, True, id='07_cost_three'),
    pytest.param('path_cost', ([(0, 0), (1, 0)], 2.5), 3.5, True, id='08_cost_offmesh'),
    pytest.param('path_cost', ([(0, 0)], 0.0), 0.0, True, id='09_cost_zero'),
    pytest.param('path_cost', ([(0, 0), (1, 1), (2, 2)], 0.0), 2.8284271247461903, True, id='10_cost_diag'),
    pytest.param('clip_path', ([(0, 0), (3, 4), (3, 5)], 10.0), [(0, 0), (3, 4), (3, 5)], False, id='11_clip_full'),
    pytest.param('clip_path', ([(0, 0), (3, 4), (3, 5)], 6.0), [(0, 0), (3, 4), (3, 5)], False, id='12_clip_partial'),
    pytest.param('clip_path', ([(0, 0), (3, 4)], 0.0), [(0, 0)], False, id='13_clip_zero'),
    pytest.param('clip_path', ([(0, 0), (1, 0), (2, 0)], 1.5), [(0, 0), (1, 0)], False, id='14_clip_one'),
    pytest.param('clip_path', ([(0, 0), (1, 0), (2, 0)], 100.0), [(0, 0), (1, 0), (2, 0)], False, id='15_clip_all'),
]


def assert_close(actual, expected):
    if isinstance(expected, tuple):
        assert isinstance(actual, tuple) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_close(actual[key], expected[key])
    else:
        assert actual == pytest.approx(expected)


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_navmesh_path_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert_close(result, expected)
    else:
        assert result == expected
