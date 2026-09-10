import requests
import urllib3
from mcp.server.fastmcp import FastMCP

# --- CONFIGURACIÓN ---
MODO_SIMULACION = True 
MAXIMO_URL = "https://TU_SERVIDOR/maximo/oslc" 
API_KEY = "TU_API_KEY_AQUÍ"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
mcp = FastMCP("Maximo Enterprise")

@mcp.tool()
def consultar_ot(num_ot: str) -> str:
    """Consulta los detalles de una Orden de Trabajo (OT) en Maximo."""
    if MODO_SIMULACION:
        return f"🧪 [SIMULACIÓN] OT {num_ot}: Mantenimiento de Motor, Estado: APROB, Activo: MOT-105"

    endpoint = f"{MAXIMO_URL}/os/mxwodetail"
    params = {"oslc.where": f'wonum="{num_ot}"', "oslc.select": "wonum,description,status,assetnum"}
    headers = {"apikey": API_KEY, "Accept": "application/json"}
    
    try:
        r = requests.get(endpoint, params=params, headers=headers, verify=False, timeout=10)
        r.raise_for_status()
        data = r.json().get("member", [])
        if not data: return f"No se encontró la OT {num_ot}"
        ot = data[0]
        return f"✅ [REAL] OT: {ot.get('wonum')} | Desc: {ot.get('description')} | Estado: {ot.get('status')}"
    except Exception as e:
        return f"❌ Error OT: {str(e)}"

@mcp.tool()
def consultar_inventario(item_num: str, almacen: str = "CENTRAL") -> str:
    """Consulta la disponibilidad de un repuesto o artículo en un almacén específico."""
    if MODO_SIMULACION:
        return (f"🧪 [SIMULACIÓN INVENTARIO]\n"
                f"Artículo: {item_num}\n"
                f"Almacén: {almacen}\n"
                f"Cantidad Disponible: 15 unidades\n"
                f"Ubicación: PASILLO-B2-ESTANTE4")

    # Lógica Real para Inventario (Usa MXINVENTORY)
    endpoint = f"{MAXIMO_URL}/os/mxinventory"
    params = {
        "oslc.where": f'itemnum="{item_num}" and location="{almacen}"',
        "oslc.select": "itemnum,location,curbal,binnum"
    }
    headers = {"apikey": API_KEY, "Accept": "application/json"}

    try:
        r = requests.get(endpoint, params=params, headers=headers, verify=False, timeout=10)
        r.raise_for_status()
        data = r.json().get("member", [])
        if not data: return f"No hay existencias del artículo {item_num} en {almacen}."
        inv = data[0]
        return (f"✅ [REAL] Artículo: {inv.get('itemnum')} | Almacén: {inv.get('location')} | "
                f"Stock: {inv.get('curbal')} | Ubicación: {inv.get('binnum')}")
    except Exception as e:
        return f"❌ Error Inventario: {str(e)}"

if __name__ == "__main__":
    mcp.run()
