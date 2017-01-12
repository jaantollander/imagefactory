from click.testing import CliRunner

from imagefactory.cli import main


def test_commands():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert result.output == ''
