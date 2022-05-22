import os
from pathlib import Path

import pytest
import requests_mock
from requests.exceptions import HTTPError

from page_loader.scripts.page_loader import download

cwd = Path(__file__).parent


@pytest.fixture
def text():
    with open('tests/fixtures/test_page.html', 'r') as f:
        return f.read()


@pytest.fixture
def image():
    with open(
            'tests/fixtures/'
            'page-loader-hexlet-repl-co-assets-professions-nodejs.jpg',
            'rb') as f:
        return f.read()


@pytest.fixture
def css():
    with open(
            'tests/fixtures/page-loader-hexlet-repl-co-assets-application.css',
            'r') as f:
        return f.read()


@pytest.fixture
def html_text():
    with open('tests/fixtures/page-loader-hexlet-repl-co-courses.html',
              'r') as f:
        return f.read()


@pytest.fixture
def js():
    with open('tests/fixtures/page-loader-hexlet-repl-co-script.js', 'r') as f:
        return f.read()


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
        with pytest.raises(HTTPError,
                           match=f'404 Client Error: None for url: {url}'):
            path = cwd.joinpath(tmpdir)
            download(url, path)


def test_download_permission_error(tmpdir):
    with requests_mock.Mocker() as m:
        path = cwd.joinpath(tmpdir)
        os.chmod(path, 555)
        with pytest.raises(PermissionError,
                           match=f'Permissions denied to path {path}'):
            url = 'http://test.com'
            m.get(url=url, text='Hello, World!')
            download(url, path)
        os.chmod(path, 777)


def test_download_page_with_sources(tmpdir, text, image, css, html_text,
                                    js):
    with requests_mock.Mocker() as m:
        url = 'http://test.com'
        image_url = 'http://test.com/assets/professions/nodejs.png'
        css_url = 'http://test.com/assets/application.css'
        html_url = 'http://test.com/courses'
        js_url = 'http://test.com/script.js'
        m.get(url=url, text=text)
        m.get(url=image_url, content=image)
        m.get(url=css_url, text=css)
        m.get(url=html_url, text=html_text)
        m.get(url=js_url, text=js)
        path = cwd.joinpath(tmpdir)
        file_name = download('http://test.com', path)
        assert str(file_name) == f'{tmpdir}/test-com.html'
        path_to_html_file = path.joinpath(file_name)
        assert path_to_html_file.exists()
        path_to_files_dir = path.joinpath(
            'test-com_files')
        assert path_to_files_dir.exists()
        dir_list = os.listdir(path_to_files_dir)
        assert len(dir_list) == 4
        path_to_image = path_to_files_dir.joinpath(
            'test-com-assets-professions-nodejs.jpg')
        path_to_css = path_to_files_dir.joinpath(
            'test-com-assets-application.css')
        path_to_html_text = path_to_files_dir.joinpath(
            'test-com-courses.html')
        path_to_js = path_to_files_dir.joinpath('test-com-script.js')
        assert path_to_image.exists()
        assert path_to_css.exists()
        assert path_to_html_text.exists()
        assert path_to_js.exists()
