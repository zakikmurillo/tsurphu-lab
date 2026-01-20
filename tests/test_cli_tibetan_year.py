import json

from orchestration import cli


def test_cli_tibetan_year_plain_output(capsys):
    rc = cli.main(["tibetan-year", "2025"])
    assert rc == 0

    out = capsys.readouterr().out
    assert "TibetanYear" in out
    assert "gregorian_year=2025" in out


def test_cli_tibetan_year_json_output(capsys):
    rc = cli.main(["tibetan-year", "2025", "--json"])
    assert rc == 0

    out = capsys.readouterr().out.strip()
    data = json.loads(out)

    assert data["gregorian_year"] == 2025
    assert data["element"] == "wood"
    assert data["animal"] == "Snake"
    assert data["stem_index"] == 1
    assert data["branch_index"] == 5
    assert data["mewa"] == 5
    assert data["parkha"] == "khon"
