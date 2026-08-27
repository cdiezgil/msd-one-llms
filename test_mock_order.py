from unittest.mock import patch

@patch("os.path.join")
@patch("os.path.abspath")
def test_func(mock_abspath, mock_join):
    print("mock_abspath:", mock_abspath)
    print("mock_join:", mock_join)

test_func()
