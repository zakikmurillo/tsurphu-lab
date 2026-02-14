#!/usr/bin/env python3
"""
repo_audit.py — Auditoría local del repo Tsurphu

Objetivo:
- Encontrar Documento Maestro (nombre + ruta exacta)
- Detectar Object Ledger / Audit Trail / ChangeSetPacket
- Resumir árbol de carpetas (alto nivel)
- Extraer info de git (si está disponible)
- Reportar "qué falta" para correr bootstrap/tests

Uso:
  python .\\tools\\repo_audit.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


KEY_PHRASES: tuple[str, ...] = (
    "Documento Maestro",
    "Document Master",
    "Object Ledger",
    "Audit Trail",
    "ChangeSetPacket",
    "ChangeSetPacket-1",
    "arquitectura 7x",
    "7x",
)

# Heurísticas de nombres probables (no asumimos que existan; solo ayuda a priorizar)
LIKELY_MASTER_NAMES: tuple[str, ...] = (
    "documento_maestro.md",
    "documento-maestro.md",
    "maestro.md",
    "master.md",
    "master_document.md",
    "master-document.md",
    "document_master.md",
    "document-master.md",
    "documento_maestro.txt",
    "documento-maestro.txt",
)

TEXT_EXTS: set[str] = {".md", ".txt", ".rst", ".yaml", ".yml", ".toml", ".py", ".json"}


@dataclass(frozen=True)
class Hit:
    path: Path
    phrase: str
    line_no: int
    line: str


def run(cmd: Sequence[str], cwd: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        return p.returncode, p.stdout.strip()
    except Exception as e:
        return 999, f"[ERROR] No pude ejecutar {cmd!r}: {e}"


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTS:
        return True
    # Evita binarios grandes
    try:
        if path.stat().st_size > 3_000_000:
            return False
    except OSError:
        return False
    return False


def iter_files(root: Path) -> Iterable[Path]:
    # Ignora carpetas típicas
    ignore_dirs = {".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".ruff_cache", "node_modules"}
    for p in root.rglob("*"):
        if any(part in ignore_dirs for part in p.parts):
            continue
        if p.is_file():
            yield p


def grep_phrases(root: Path, phrases: Sequence[str]) -> list[Hit]:
    hits: list[Hit] = []
    for f in iter_files(root):
        if not is_probably_text(f):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue

        for i, line in enumerate(content, start=1):
            for ph in phrases:
                if ph.lower() in line.lower():
                    hits.append(Hit(path=f, phrase=ph, line_no=i, line=line.strip()))
    return hits


def top_level_tree(root: Path) -> list[str]:
    items = []
    for p in sorted(root.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        if p.name in {".git", ".venv", "venv", "__pycache__", "node_modules"}:
            continue
        kind = "DIR " if p.is_dir() else "FILE"
        items.append(f"{kind}  {p.name}")
    return items


def find_likely_master_docs(root: Path) -> list[Path]:
    candidates: list[Path] = []
    # 1) nombres probables en cualquier parte
    lower_map = {p.name.lower(): p for p in iter_files(root)}
    for name in LIKELY_MASTER_NAMES:
        p = lower_map.get(name.lower())
        if p:
            candidates.append(p)

    # 2) cualquier archivo en docs/ que contenga maestro/master en nombre
    docs_dir = root / "docs"
    if docs_dir.exists() and docs_dir.is_dir():
        for p in docs_dir.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".txt"}:
                n = p.name.lower()
                if "maestro" in n or "master" in n:
                    candidates.append(p)

    # Unique preserving order
    seen: set[Path] = set()
    out: list[Path] = []
    for p in candidates:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(rp)
    return out


def main() -> int:
    root = Path.cwd().resolve()

    print("\n=== TSURPHU REPO AUDIT ===")
    print(f"Repo root (cwd): {root}")

    print("\n--- Top-level tree ---")
    for line in top_level_tree(root):
        print("  " + line)

    print("\n--- Git info (si aplica) ---")
    code, out = run(["git", "rev-parse", "--is-inside-work-tree"], root)
    if code == 0 and out.strip() == "true":
        _, branch = run(["git", "branch", "--show-current"], root)
        _, status = run(["git", "status", "--porcelain"], root)
        _, last = run(["git", "log", "-1", "--oneline"], root)
        _, count = run(["git", "rev-list", "--count", "HEAD"], root)
        print(f"  branch: {branch.strip() or '(unknown)'}")
        print(f"  commits: {count.strip() or '(unknown)'}")
        print(f"  last: {last.strip() or '(unknown)'}")
        print(f"  dirty: {'YES' if status.strip() else 'NO'}")
    else:
        print("  (No es un repo git o git no está disponible en PATH)")

    print("\n--- Documento Maestro (detección) ---")
    likely = find_likely_master_docs(root)
    if likely:
        for p in likely:
            print(f"  CANDIDATE: {p}")
    else:
        print("  No encontré candidatos por nombre. Voy a buscar por contenido (frases clave).")

    print("\n--- Búsqueda por contenido (frases clave) ---")
    hits = grep_phrases(root, KEY_PHRASES)
    if not hits:
        print("  No encontré ninguna frase clave en archivos de texto soportados.")
    else:
        # Agrupa por archivo
        by_file: dict[Path, list[Hit]] = {}
        for h in hits:
            by_file.setdefault(h.path.resolve(), []).append(h)

        # Ordena para mostrar primero docs/
        def score(path: Path) -> tuple[int, str]:
            s = 0
            if "docs" in path.parts:
                s -= 10
            if "maestro" in path.name.lower() or "master" in path.name.lower():
                s -= 5
            return (s, str(path))

        for f in sorted(by_file.keys(), key=score):
            print(f"\n  FILE: {f}")
            for h in by_file[f][:20]:
                print(f"    L{h.line_no:04d} [{h.phrase}] {h.line}")
            if len(by_file[f]) > 20:
                print(f"    ... ({len(by_file[f]) - 20} más)")

    print("\n--- Siguiente paso sugerido ---")
    print("  1) Si arriba aparece el Documento Maestro: copia el nombre y ruta y me los pegas aquí.")
    print("  2) Luego ejecutamos: python .\\tools\\tsurphu.py bootstrap (según README del repo).")
    print("  3) Y corremos tests: pytest -q (si existe / está configurado).")

    print("\n=== FIN AUDIT ===\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())