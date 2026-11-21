"""Servidor local para mostrar la interfaz sin instalar paquetes externos.

Uso desde la raíz del repositorio: python backend/servidor.py
NO publicar en Internet: no implementa autenticación de administradores.
"""
import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
from urllib.parse import urlparse

from smartcommerce.errores import ErrorNegocio, ErrorValidacion, NoEncontrado
from smartcommerce.repositorio_sqlite import RepositorioSQLite
from smartcommerce.servicios import ServicioTienda

RAIZ = Path(__file__).resolve().parent.parent
FRONTEND = RAIZ / "frontend"
DATOS = Path(__file__).resolve().parent / "datos_smartcommerce.db"
SERVICIO = ServicioTienda(RepositorioSQLite(DATOS))
STATIC = {"/": ("index.html", "text/html; charset=utf-8"),
          "/styles.css": ("styles.css", "text/css; charset=utf-8"),
          "/app.js": ("app.js", "application/javascript; charset=utf-8")}


class Manejador(BaseHTTPRequestHandler):
    server_version = "SmartCommerceAcademico/0.2"

    def _json(self, status, obj):
        datos = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def _entrada(self):
        try:
            longitud = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ErrorValidacion("Content-Length incorrecto.") from exc
        if longitud < 1 or longitud > 32_768:
            raise ErrorValidacion("La solicitud debe contener JSON válido (máximo 32 KB).")
        try:
            datos = json.loads(self.rfile.read(longitud))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ErrorValidacion("El cuerpo debe contener JSON válido.") from exc
        if not isinstance(datos, dict):
            raise ErrorValidacion("Se requiere un objeto JSON.")
        return datos

    def _procesar(self, fn):
        try:
            fn()
        except ErrorNegocio as exc:
            self._json(exc.http, {"error": exc.codigo, "mensaje": exc.mensaje})
        except Exception:
            logging.exception("Error inesperado en la petición")
            self._json(500, {"error": "ERROR_INTERNO", "mensaje": "Ocurrió un error del servidor."})

    def do_GET(self):
        self._procesar(self._get)

    def _get(self):
        path = urlparse(self.path).path
        if path in STATIC:
            archivo, tipo = STATIC[path]
            contenido = (FRONTEND / archivo).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(contenido)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(contenido)
        elif path == "/api/productos":
            self._json(200, SERVICIO.productos())
        elif path == "/api/categorias":
            self._json(200, SERVICIO.categorias())
        elif path == "/api/pedidos":
            self._json(200, SERVICIO.pedidos())
        elif path == "/api/indicadores":
            self._json(200, SERVICIO.resumen())
        else:
            raise NoEncontrado("No existe la ruta solicitada.")

    def do_POST(self):
        self._procesar(self._post)

    def _post(self):
        path = urlparse(self.path).path
        datos = self._entrada()
        if path == "/api/pedidos":
            resultado = SERVICIO.confirmar_compra(
                datos.get("cliente"), datos.get("lineas"), datos.get("pago"))
            self._json(201, resultado)
        elif path == "/api/productos":
            resultado = SERVICIO.agregar_producto(
                datos.get("nombre"), datos.get("categoria_id"),
                datos.get("precio_centavos"), datos.get("stock"))
            self._json(201, resultado)
        else:
            m = re.fullmatch(r"/api/pedidos/(\d+)/cancelar", path)
            if m:
                self._json(200, SERVICIO.cancelar(int(m.group(1))))
            else:
                raise NoEncontrado("No existe la ruta solicitada.")

    def do_PATCH(self):
        self._procesar(self._patch)

    def _patch(self):
        path = urlparse(self.path).path
        datos = self._entrada()
        m = re.fullmatch(r"/api/productos/(\d+)/stock", path)
        if not m:
            raise NoEncontrado("No existe la ruta solicitada.")
        self._json(200, SERVICIO.actualizar_stock(int(m.group(1)), datos.get("cantidad")))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    servidor = ThreadingHTTPServer(("127.0.0.1", 8000), Manejador)
    print("SmartCommerce: abre http://127.0.0.1:8000", flush=True)
    print("Para detenerlo: Ctrl+C. Solo para uso local / académico.", flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        servidor.server_close()
