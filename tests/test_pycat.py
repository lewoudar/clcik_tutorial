from click.testing import CliRunner

from scripts.pycat import cli


def test_pycat(tmp_path):
    hello_file = tmp_path / 'hello.txt'
    hello_file.write_text('hello world!')
    runner = CliRunner()
    result = runner.invoke(cli, [f'{hello_file.resolve()}'])

    assert 0 == result.exit_code
    assert 'hello world!\n' == result.output
