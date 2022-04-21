import requests_mock

from pathlib import Path
from page_loader.scripts.page_loader import download

cwd = Path(__file__).parent


def test_download(tmpdir):
    with requests_mock.Mocker() as m:
        m.get(url='http://test.com', text='Hello, World!')
        path = cwd.joinpath(tmpdir)
        file_name = download('http://test.com', path)
        assert str(file_name) == f'{tmpdir}/test-com.html'
        path_to_file = path.joinpath(file_name)
        assert path_to_file.exists()
