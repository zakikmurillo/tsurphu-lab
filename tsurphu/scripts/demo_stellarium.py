from __future__ import annotations
import json
from datetime import datetime, timezone, timedelta

from tsurphu.integraciones.stellarium_rc import StellariumRemoteControlClient as C


def main():
    c = C()

    # Bogotá (puedes cambiar luego)
    c.set_location(latitude=4.7110, longitude=-74.0721, name="Bogota", country="CO")

    # Ejemplo: fija fecha/hora (UTC-5). Ajusta cuando quieras.
    tz = timezone(timedelta(hours=-5))
    dt = datetime(1967, 3, 22, 4, 44, 0, tzinfo=tz)

    # Convertimos a JD usando timestamp (Unix epoch) + offset JD
    jd = dt.timestamp() / 86400.0 + 2440587.5
    c.set_time_jd(jd, 0)  # 0 = no correr el tiempo (congelado)

    # Enfocar Luna
    c.focus("Moon")

    # Extraer info básica
    moon = c.object_info("Moon")
    out = {
        "meta": {
            "location": {"name": "Bogota", "lat": 4.7110, "lon": -74.0721},
            "datetime_local": dt.isoformat(),
            "jd": jd,
        },
        "stellarium_time": c.status().get("time"),
        "moon": {
            "ra": moon.get("ra"),
            "dec": moon.get("dec"),
            "ecl_lon_deg": moon.get("ecl-longitude-deg"),
            "ecl_lat_deg": moon.get("ecl-latitude-deg"),
            "distance_au": moon.get("distance"),
            "phase": moon.get("phase"),
        },
    }

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
