#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, datetime as dt, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "src"))
DOCS = ROOT / "docs"
LEDGER = DOCS / "object-ledger.csv"
CHANGESETS = ROOT / "changesets"
AUDIT = ROOT / "src" / "audit" / "audit-log.jsonl"
REPORTS = ROOT / "reports"

# Motores
from engines.tibetan_year import tibetan_year

def now_utc():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def ensure():
    CHANGESETS.mkdir(parents=True, exist_ok=True)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    if not AUDIT.exists():
        AUDIT.write_text("", encoding="utf-8")

def write_audit(entry: dict):
    ensure()
    with AUDIT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def validate():
    errs = []
    for p in [DOCS/"master.md", DOCS/"changesetpacket-1.md", LEDGER, AUDIT]:
        if not p.exists():
            errs.append(f"Falta: {p}")

    if LEDGER.exists():
        with LEDGER.open("r", encoding="utf-8-sig", newline="") as f:
            r = csv.DictReader(f)
            need = {"ObjectID","Nombre","Estrato_7x","Dueño","MetaAgent","Sensibilidad","Evidencia","Ruta"}
            if set(r.fieldnames or []) != need:
                errs.append("Ledger: columnas incorrectas")
            seen=set()
            for i,row in enumerate(r, start=2):
                oid=(row.get("ObjectID") or "").strip()
                if not oid:
                    errs.append(f"Ledger L{i}: ObjectID vacío")
                    continue
                if oid in seen:
                    errs.append(f"Ledger L{i}: duplicado {oid}")
                seen.add(oid)

    for p in sorted(CHANGESETS.glob("*.json")):
        try:
            obj=json.loads(p.read_text(encoding="utf-8"))
            recorded=(obj.get("integrity",{}).get("packet_hash") or "")
            tmp=dict(obj); tmp["integrity"]=dict(tmp.get("integrity",{})); tmp["integrity"]["packet_hash"]=""
            computed="sha256:"+sha256(canon(tmp))
            if recorded!=computed:
                errs.append(f"{p.name}: hash no coincide")
        except Exception as e:
            errs.append(f"{p.name}: inválido ({e})")

    if errs:
        print("[validate] ERRORES:")
        for e in errs:
            print(" -", e)
        raise SystemExit(2)

    print("[validate] OK ✅")

def make_changeset(change_id: str, actor_role: str, change_type: str, layers: list[str], modules: list[str], objects: list[dict], rationale: str):
    pkt = {
        "packet_version":"1.0",
        "change_id":change_id,
        "timestamp_utc":now_utc(),
        "actor":{"role":actor_role,"id":""},
        "change_type":change_type,
        "scope":{"layers_7x":layers,"modules":modules},
        "objects_affected":objects,
        "rationale":rationale,
        "evidence":[],
        "impact":{"expected_behavior_change":"","risk_level":"low","compatibility":"backward"},
        "rollback":{"needed":False,"plan":""},
        "approval":{"required":True,"approver_role":"Zakik","status":"pending","notes":""},
        "integrity":{"canonicalization":"json-keys-sorted-utf8","hash_alg":"sha256","packet_hash":""}
    }
    tmp=dict(pkt); tmp["integrity"]=dict(tmp["integrity"]); tmp["integrity"]["packet_hash"]=""
    pkt["integrity"]["packet_hash"]="sha256:"+sha256(canon(tmp))
    return pkt

def cmd_validate(_): 
    validate()

def cmd_slice_a(args):
    ensure()

    # Año para cálculo: por ahora usamos el año gregoriano de birth_date (sin ajustar por Losar)
    year = int(args.birth_date.split("-")[0])
    ty = tibetan_year(year, lookups_dir=ROOT / "src" / "engines" / "lookups")

    result = {
        "timestamp_utc": now_utc(),
        "input": {"name": args.name, "birth_date": args.birth_date, "birth_time": args.birth_time, "place": args.place},
        "engine": {"version": "sliceA-0.2", "tibetan_year_engine": "tibetan_year.py"},
        "tibetan": {
            "year_animal": ty.animal,
            "element": ty.element,
            "mewa": ty.mewa if ty.mewa is not None else "TBD",
            "parkha": ty.parkha if ty.parkha is not None else "TBD"
        },
        "interpretation": "Pipeline demo + año (animal/elemento) calculado. Mewa/Parkha aún por tabla validada.",
        "sources_ref": []
    }

    fn = REPORTS / f"sliceA-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"
    fn.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    write_audit({
        "timestamp_utc": result["timestamp_utc"],
        "event":"sliceA_report_created",
        "report_file": "/reports/"+fn.name,
        "engine_version":"sliceA-0.2"
    })

    print(f"[slice-a] OK: {fn}")

def cmd_new_changeset(args):
    ensure()
    objects=[]
    for spec in args.object:
        oid,op,path,sens = spec.split(":")
        objects.append({"object_id":oid,"operation":op,"path":path,"sensitivity":sens})
    pkt=make_changeset(args.change_id, args.actor_role, args.change_type, args.layer, args.module, objects, args.rationale)
    out=CHANGESETS/f"{args.change_id}.json"
    out.write_bytes(canon(pkt))
    write_audit({
        "timestamp_utc": now_utc(),
        "event":"changeset_created",
        "change_id": args.change_id,
        "packet_file": "/changesets/"+out.name,
        "packet_hash": pkt["integrity"]["packet_hash"]
    })
    print(f"[new-changeset] OK: {out}")

def main():
    p=argparse.ArgumentParser(prog="tsurphu")
    sub=p.add_subparsers(dest="cmd", required=True)

    v=sub.add_parser("validate")
    v.set_defaults(func=cmd_validate)

    s=sub.add_parser("slice-a")
    s.add_argument("--name", default="Demo")
    s.add_argument("--birth-date", default="1990-11-02")
    s.add_argument("--birth-time", default="20:30")
    s.add_argument("--place", default="Medellín")
    s.set_defaults(func=cmd_slice_a)

    c=sub.add_parser("new-changeset")
    c.add_argument("--change-id", required=True)
    c.add_argument("--actor-role", default="Engineer")
    c.add_argument("--change-type", default="update", choices=["add","update","deprecate","remove"])
    c.add_argument("--layer", action="append", default=["7x-L7"])
    c.add_argument("--module", action="append", default=["misc"])
    c.add_argument("--object", action="append", required=True, help="ObjectID:op:path:sens")
    c.add_argument("--rationale", required=True)
    c.set_defaults(func=cmd_new_changeset)

    args=p.parse_args()
    args.func(args)

if __name__=="__main__":
    main()

