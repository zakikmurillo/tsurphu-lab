# Stellarium RemoteControl (integración opcional)

Esta carpeta contiene un conector **opcional** para usar *Stellarium* como:

- visor de cielo (interactivo)
- validador externo de nuestros cálculos en M1-CIELO

> Idea: Tsurphu calcula (M1) → Stellarium muestra/confirmar.

## Lo mínimo que debes hacer (sin programar)

1. Instala Stellarium (versión normal).
2. Abre Stellarium.
3. Activa el plugin **RemoteControl**:
   - En Stellarium: *Configuration* (F2) → *Plugins* → **Remote Control**.
   - Marca: **Load at startup** y **Enable**.
   - Reinicia Stellarium.
4. Confirma que el servidor está activo:
   - En tu navegador abre: `http://localhost:8090/api/main/status`
   - Si ves un JSON, ya está.

## Uso desde Python (prueba rápida)

```python
from tsurphu.integraciones.stellarium_rc import StellariumRemoteControlClient

cli = StellariumRemoteControlClient()
print(cli.status())

# Bogotá (aprox): lat 4.7110, lon -74.0721
cli.set_location(latitude=4.7110, longitude=-74.0721, altitude_m=2640, name="Bogotá", country="CO")

# (Opcional) enfocar Luna
cli.focus("Moon")
print(cli.object_info("Moon"))
```

## Nota

- Esta integración no es un requisito del motor Kalachakra.
- Es una herramienta de apoyo para validar y visualizar.
