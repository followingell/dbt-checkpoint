from unittest.mock import patch

import pytest

from pre_commit_dbt.dbt_compile import main
from pre_commit_dbt.dbt_compile import prepare_cmd


def test_dbt_compile():
    with patch("pre_commit_dbt.utils.subprocess.Popen") as mock_popen:
        mock_popen.return_value.poll.return_value = 0
        result = main(("test",))
        assert result == 0


def test_dbt_compile_error():
    with patch("pre_commit_dbt.utils.subprocess.Popen") as mock_popen:
        mock_popen.return_value.poll.return_value = 1
        result = main(("test",))
        assert result == 1


@pytest.mark.parametrize(
    "files,global_flags,cmd_flags,expected",
    [
        (["/aa/bb/cc.txt"], None, None, ["dbt", "compile", "-m", "cc"]),
        (
            ["/aa/bb/cc.txt"],
            ["--debug", "--no-write-json"],
            None,
            ["dbt", "--debug", "--no-write-json", "compile", "-m", "cc"],
        ),
        (
            ["/aa/bb/cc.txt"],
            None,
            ["-t", "prod"],
            ["dbt", "compile", "-m", "cc", "-t", "prod"],
        ),
        (
            ["/aa/bb/cc.txt"],
            "",
            ["-t", "prod"],
            ["dbt", "compile", "-m", "cc", "-t", "prod"],
        ),
    ],
)
def test_dbt_compile_cmd(files, global_flags, cmd_flags, expected):
    result = prepare_cmd(files, global_flags, cmd_flags)
    assert result == expected