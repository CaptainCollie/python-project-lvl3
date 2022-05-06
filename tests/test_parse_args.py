from page_loader.parse_args import parse_args


def test_parse_args():
    args = parse_args(['-o', './tmp', 'fake-url.com'])
    assert args
    assert args.output == './tmp'
    assert args.url == 'fake-url.com'
