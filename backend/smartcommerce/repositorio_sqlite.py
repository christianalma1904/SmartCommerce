"""Persistencia SQLite del prototipo local de SmartCommerce.

Se utiliza una transacción BEGIN IMMEDIATE en compras/cancelaciones:
validación + actualización de existencias + pedido forman una unidad indivisible.
"""
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from .contratos import RepositorioTienda
from .errores import ErrorValidacion, EstadoInvalido, NoEncontrado, SinExistencias
from .modelos import Producto


class RepositorioSQLite(RepositorioTienda):
    def __init__(self, archivo: str | Path):
        self.__archivo = str(archivo)
        Path(self.__archivo).parent.mkdir(parents=True, exist_ok=True)
        self._inicializar()

    def _conexion(self):
        conn = sqlite3.connect(self.__archivo, timeout=15, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 15000")
        return conn

    @contextmanager
    def _transaccion(self):
        conn = self._conexion()
        try:
            # BEGIN IMMEDIATE toma el bloqueo de escritura desde el inicio:
            # una segunda compra espera en lugar de validar stock obsoleto.
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def _inicializar(self):
        # executescript() finaliza cualquier transacción abierta; por eso
        # el esquema se crea ANTES de la transacción de datos iniciales.
        conn = self._conexion()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    categoria_id INTEGER NOT NULL REFERENCES categorias(id),
                    precio_centavos INTEGER NOT NULL CHECK (precio_centavos > 0),
                    stock INTEGER NOT NULL CHECK (stock >= 0)
                );
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    estado TEXT NOT NULL CHECK (estado IN ('CONFIRMADO','RECHAZADO','CANCELADO')),
                    total_centavos INTEGER NOT NULL CHECK (total_centavos >= 0),
                    fecha TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS detalle_pedido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
                    producto_id INTEGER NOT NULL REFERENCES productos(id),
                    nombre_historico TEXT NOT NULL,
                    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                    precio_centavos INTEGER NOT NULL CHECK (precio_centavos > 0)
                );
            """)
        finally:
            conn.close()
        with self._transaccion() as conn:
            if conn.execute("SELECT COUNT(*) FROM categorias").fetchone()[0] == 0:
                conn.executemany("INSERT INTO categorias (id, nombre) VALUES (?,?)", [
                    (1, "Tecnología"), (2, "Hogar"), (3, "Accesorios")])
            if conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 0:
                conn.executemany("""INSERT INTO productos
                  (nombre, categoria_id, precio_centavos, stock) VALUES (?,?,?,?)""", [
                    ("Audífonos inalámbricos", 1, 4590, 12),
                    ("Teclado compacto", 1, 3299, 8),
                    ("Mouse ergonómico", 1, 1890, 15),
                    ("Lámpara de escritorio", 2, 2745, 4),
                    ("Botella térmica", 2, 1499, 20),
                    ("Cuaderno premium", 3, 850, 3),
                    ("Organizador de cables", 3, 699, 17),
                    ("Soporte para portátil", 3, 2390, 6),
                ])

    @staticmethod
    def _producto(fila) -> dict:
        return Producto(fila["id"], fila["nombre"], fila["categoria"],
                        fila["precio_centavos"], fila["stock"]).como_dict()

    def listar_productos(self) -> list[dict]:
        with closing(self._conexion()) as conn:
            filas = conn.execute("""SELECT p.id,p.nombre,c.nombre AS categoria,
                p.precio_centavos,p.stock FROM productos p
                INNER JOIN categorias c ON c.id=p.categoria_id ORDER BY p.id""").fetchall()
            return [self._producto(f) for f in filas]

    def listar_categorias(self) -> list[dict]:
        with closing(self._conexion()) as conn:
            return [dict(f) for f in conn.execute("SELECT id,nombre FROM categorias ORDER BY id")]

    def crear_producto(self, nombre, categoria_id, precio_centavos, stock) -> dict:
        try:
            with self._transaccion() as conn:
                if not conn.execute("SELECT 1 FROM categorias WHERE id=?", (categoria_id,)).fetchone():
                    raise ErrorValidacion("La categoría seleccionada no existe.")
                cur = conn.execute("""INSERT INTO productos (nombre,categoria_id,precio_centavos,stock)
                    VALUES (?,?,?,?)""", (nombre, categoria_id, precio_centavos, stock))
                identificador = cur.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ErrorValidacion("Los datos del producto no cumplen las restricciones.") from exc
        return next(p for p in self.listar_productos() if p["id"] == identificador)

    def cambiar_stock(self, identificador, cantidad) -> dict:
        with self._transaccion() as conn:
            cur = conn.execute("UPDATE productos SET stock=? WHERE id=?", (cantidad, identificador))
            if cur.rowcount != 1:
                raise NoEncontrado("No existe el producto indicado.")
        return next(p for p in self.listar_productos() if p["id"] == identificador)

    def comprar(self, cliente, lineas, pago) -> dict:
        with self._transaccion() as conn:
            detalles = []
            total = 0
            for linea in lineas:
                fila = conn.execute("""SELECT id,nombre,precio_centavos,stock
                    FROM productos WHERE id=?""", (linea["producto_id"],)).fetchone()
                if fila is None:
                    raise NoEncontrado(f"No existe el producto {linea['producto_id']}.")
                cantidad = linea["cantidad"]
                subtotal = fila["precio_centavos"] * cantidad
                detalles.append({"producto_id": fila["id"], "nombre": fila["nombre"],
                                 "cantidad": cantidad, "precio_centavos": fila["precio_centavos"],
                                 "subtotal_centavos": subtotal})
                total += subtotal
                # También se valida para pago ficticio rechazado: el carrito
                # representa artículos reales, aunque no se confirme la compra.
                if pago == "APROBADO" and fila["stock"] < cantidad:
                    raise SinExistencias(f"No hay suficiente stock de «{fila['nombre']}».")
            estado = "CONFIRMADO" if pago == "APROBADO" else "RECHAZADO"
            cursor = conn.execute("""INSERT INTO pedidos (cliente,estado,total_centavos,fecha)
                VALUES (?,?,?,?)""", (cliente, estado, total,
                                       datetime.now(timezone.utc).isoformat(timespec="seconds")))
            pedido_id = cursor.lastrowid
            for d in detalles:
                conn.execute("""INSERT INTO detalle_pedido
                    (pedido_id,producto_id,nombre_historico,cantidad,precio_centavos)
                    VALUES (?,?,?,?,?)""",
                    (pedido_id, d["producto_id"], d["nombre"], d["cantidad"], d["precio_centavos"]))
                if pago == "APROBADO":
                    # Predicado WHERE stock>=cantidad: segunda defensa contra
                    # ventas simultáneas que pudieran generar stock negativo.
                    cur = conn.execute("""UPDATE productos SET stock=stock-?
                        WHERE id=? AND stock>=?""",
                        (d["cantidad"], d["producto_id"], d["cantidad"]))
                    if cur.rowcount != 1:
                        raise SinExistencias(f"Existencias insuficientes de «{d['nombre']}».")
            return {"id": pedido_id, "cliente": cliente, "estado": estado,
                    "total_centavos": total, "detalles": detalles}

    def listar_pedidos(self) -> list[dict]:
        with closing(self._conexion()) as conn:
            pedidos = [dict(r) for r in conn.execute(
                "SELECT id,cliente,estado,total_centavos,fecha FROM pedidos ORDER BY id DESC")]
            for pedido in pedidos:
                pedido["detalles"] = [dict(r) for r in conn.execute("""
                    SELECT producto_id,nombre_historico AS nombre,cantidad,precio_centavos
                    FROM detalle_pedido WHERE pedido_id=?""", (pedido["id"],))]
            return pedidos

    def cancelar_pedido(self, pedido_id) -> dict:
        with self._transaccion() as conn:
            pedido = conn.execute("SELECT estado FROM pedidos WHERE id=?", (pedido_id,)).fetchone()
            if not pedido:
                raise NoEncontrado("No existe ese pedido.")
            if pedido["estado"] != "CONFIRMADO":
                raise EstadoInvalido("Solo se pueden cancelar pedidos confirmados, una sola vez.")
            # Reintegración dentro de la misma transacción que cambia el estado:
            # un segundo intento falla antes de sumar unidades de nuevo.
            for d in conn.execute("SELECT producto_id,cantidad FROM detalle_pedido WHERE pedido_id=?",
                                  (pedido_id,)).fetchall():
                conn.execute("UPDATE productos SET stock=stock+? WHERE id=?",
                             (d["cantidad"], d["producto_id"]))
            conn.execute("UPDATE pedidos SET estado='CANCELADO' WHERE id=?", (pedido_id,))
        return {"id": pedido_id, "estado": "CANCELADO"}

    def indicadores(self) -> dict:
        with closing(self._conexion()) as conn:
            confirmado = conn.execute("""SELECT COUNT(*),COALESCE(SUM(total_centavos),0)
                FROM pedidos WHERE estado='CONFIRMADO'""").fetchone()
            otros = conn.execute("""SELECT estado,COUNT(*) AS cantidad FROM pedidos
                GROUP BY estado""").fetchall()
            alertas = [dict(x) for x in conn.execute("""SELECT nombre,stock FROM productos
                WHERE stock<=5 ORDER BY stock,nombre""")]
            return {"pedidos_confirmados": confirmado[0], "ventas_centavos": confirmado[1],
                    "pedidos_por_estado": {f["estado"]: f["cantidad"] for f in otros},
                    "productos_stock_bajo": alertas,
                    "total_productos": conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]}
