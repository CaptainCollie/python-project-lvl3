import os
from pathlib import Path

import pytest
import requests_mock

from page_loader.scripts.page_loader import download

cwd = Path(__file__).parent


def test_download_url(tmpdir):
    with requests_mock.Mocker() as m:
        url = 'http://test.com'
        m.get(url=url, text='Hello, World!')
        path = cwd.joinpath(tmpdir)
        file_name = download(url, path)
        assert str(file_name) == f'{tmpdir}/test-com.html'
        path_to_file = path.joinpath(file_name)
        assert path_to_file.exists()


def test_download_url_with_file_extension(tmpdir):
    with requests_mock.Mocker() as m:
        url = 'http://test.com/image.jpg'
        m.get(url=url, text='Hello, World!')
        path = cwd.joinpath(tmpdir)
        file_name = download(url, path)
        assert str(file_name) == f'{tmpdir}/test-com-image.html'
        path_to_file = path.joinpath(file_name)
        assert path_to_file.exists()


def test_download_directory_do_not_exist(tmpdir):
    with requests_mock.Mocker() as m:
        path = cwd.joinpath(tmpdir + '/does_not_exist_dir')
        with pytest.raises(IOError, match=f'Path {path} does not exist'):
            url = 'http://test.com/image.jpg'
            m.get(url=url, text='Hello, World!')
            download(url, path)


def test_download_connection_error(tmpdir):
    with requests_mock.Mocker() as m:
        url = 'http://test.com'
        m.get(url=url, text='Hello, World!', status_code=404)
        with pytest.raises(ConnectionError,
                           match=f'Connection to {url} failed'):
            path = cwd.joinpath(tmpdir)
            download(url, path)


def test_download_page_with_images(tmpdir):
    with requests_mock.Mocker() as m:
        url = 'http://test.com'
        image_url = 'http://test.com/page-loader-hexlet-repl-co_files/' \
                    'page-loader-hexlet-repl-co-assets-professions-nodejs.png'
        with open('tests/fixtures/test_page.html', 'r') as f:
            text = f.read()
        with open(
                'tests/fixtures/'
                'page-loader-hexlet-repl-co-assets-professions-nodejs.png',
                'rb') as f:
            image = f.read()
        m.get(url=url, text=text)
        m.get(url=image_url, content=image)
        path = cwd.joinpath(tmpdir)
        file_name = download('http://test.com', path)
        assert str(file_name) == f'{tmpdir}/test-com.html'
        path_to_html_file = path.joinpath(file_name)
        assert path_to_html_file.exists()
        path_to_files_dir = path.joinpath(
            'test-com_files')
        assert path_to_files_dir.exists()
        assert len(os.listdir(path_to_files_dir)) != 0
