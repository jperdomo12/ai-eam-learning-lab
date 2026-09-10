# Este bloque se usa solo para probar si Claude esta viendo el servicio validando bien la ubicación y archivos de configuración

from mcp.server.fastmcp import FastMCP

# Creamos el servidor
mcp = FastMCP("Maximo")

@mcp.tool()
def verificar_conexion() -> str:
    """Usa esta herramienta para confirmar que el servidor funciona."""
    return "Conexión exitosa con el servidor de Maximo"

if __name__ == "__main__":
    mcp.run()


import requests
from mcp.server.fastmcp import FastMCP
