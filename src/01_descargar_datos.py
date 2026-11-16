"""
01 - Descarga de datos crudos
-----------------------------
Descarga los datasets públicos de Our World in Data (OWID):
  * owid-energy-data.csv : generación eléctrica por fuente, consumo de energía, etc.
  * owid-co2-data.csv    : emisiones de CO2 por país y año.

Fuente y licencia: Our World in Data (CC BY 4.0)
  https://github.com/owid/energy-data
  https://github.com/owid/co2-data

Uso:
    python src/01_descargar_datos.py
"""
from pathlib import Path
import urllib.request

RAIZ = Path(__file__).resolve().parents[1]
DIR_RAW = RAIZ / "data" / "raw"

FUENTES = {
    "owid-energy-data.csv": "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv",
    "owid-co2-data.csv": "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
}


def descargar(nombre: str, url: str, forzar: bool = False) -> Path:
    destino = DIR_RAW / nombre
    if destino.exists() and not forzar:
        print(f"[omitido] {nombre} ya existe ({destino.stat().st_size / 1e6:.1f} MB)")
        return destino
    print(f"[descargando] {url}")
    urllib.request.urlretrieve(url, destino)
    print(f"[ok] {nombre} ({destino.stat().st_size / 1e6:.1f} MB)")
    return destino


if __name__ == "__main__":
    DIR_RAW.mkdir(parents=True, exist_ok=True)
    for nombre, url in FUENTES.items():
        descargar(nombre, url)
