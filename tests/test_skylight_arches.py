from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

import pytest


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def fixture_path() -> Path:
    p = _repo_root() / "tests" / "calendario" / "skylight-arches-2025-2026.yml"
    if not p.exists():
        pytest.skip(f"Fixture missing: {p}")
    return p


@pytest.fixture(scope="session")
def skylight_mod():
    repo = _repo_root()
    sys.path.insert(0, str(repo / "src"))
    from engines import skylight_arches  # type: ignore
    return skylight_arches


def test_fixture_loads_and_is_consistent(skylight_mod, fixture_path: Path):
    fx = skylight_mod.load_fixture(fixture_path)
    assert fx.span_start == date(2025, 3, 1)
    assert fx.span_end == date(2026, 2, 28)

    assert len(fx.padens) > 0
    assert len(fx.lutheps) > 0
    assert len(fx.nyinaks) > 0
    assert len(fx.yenkongs) > 0

    gm = fx.group_map()
    keys = list(gm.keys())
    for i, a in enumerate(keys):
        for b in keys[i + 1 :]:
            assert gm[a].isdisjoint(gm[b])


def test_classify_matches_fixture(skylight_mod, fixture_path: Path):
    fx = skylight_mod.load_fixture(fixture_path)
    mapping = {"padens": "paden", "lutheps": "luthep", "nyinaks": "nyinak", "yenkongs": "yenkong"}

    for group, expected in mapping.items():
        for d in fx.group_map()[group]:
            got = skylight_mod.classify_date(d, fixture_path=fixture_path)
            assert got == expected

    assert skylight_mod.classify_date(date(2025, 3, 1), fixture_path=fixture_path) is None
    assert skylight_mod.classify_date(date(2024, 1, 1), fixture_path=fixture_path) is None
