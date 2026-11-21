# Guiones y plan de grabación — Aprendizaje Autónomo 2

**Presentador:** Christian Daniel Alcocer Marroquín  
**Proyecto:** SmartCommerce — Sistema de Gestión de E-commerce  
**IMPORTANTE:** son **dos videos diferentes**, según el enunciado de la Unidad 2. El primero explica el avance; el segundo **demuestra el software en ejecución**.

## VIDEO 1. Explicación del avance (4–5 minutos)

**0:00–0:30 | Portada y continuidad**

> Buenos días. Soy Christian Daniel Alcocer Marroquín, estudiante de Ingeniería en Software de la UIDE. Presento el avance de SmartCommerce correspondiente al Aprendizaje Autónomo 2 de Programación Orientada a Objetos. Durante la primera unidad planificamos un sistema de gestión de comercio electrónico; ahora hemos comenzado a implementarlo y contamos con un prototipo local funcional.

**0:30–1:10 | Selección del alcance y posición**

> En lugar de declarar los nueve módulos como terminados, prioricé un proceso de compra verificable: catálogo, carrito, pedidos, pago simulado e inventario. Considero más importante demostrar reglas correctas y persistencia de información que presentar muchas pantallas sin funcionalidad. Esta decisión también tiene límites: todavía no hemos implementado usuarios, autenticación ni un despliegue público.

**1:10–2:05 | Clases y estructuras de datos**

*En pantalla:* abre `backend/smartcommerce/modelos.py` y `contratos.py`.

> En el código identifiqué clases que representan el comportamiento del sistema. La clase Producto utiliza atributos privados para el precio y el stock, los cuales solo pueden modificarse mediante métodos que validan sus valores. La clase Carrito utiliza internamente un diccionario que relaciona el identificador de cada producto con su cantidad. También definí una interfaz abstracta llamada RepositorioTienda; el servicio depende de esa interfaz y no directamente de la implementación SQLite. De esta manera aplicamos encapsulación, estructuras de datos, herencia y polimorfismo.

**2:05–3:00 | Manejo de errores y operaciones complejas**

*En pantalla:* abre `errores.py` y el método `comprar` en `repositorio_sqlite.py`.

> El sistema contempla errores de validación, productos inexistentes, inventario insuficiente y estados inválidos de un pedido. Cada error produce una respuesta comprensible. En la compra se utiliza una transacción para confirmar el pedido y descontar unidades como una sola operación. Por ejemplo, si dos clientes desean comprar más unidades de las disponibles, la operación debe impedir un stock negativo. Los comentarios del código explican estos controles y su importancia.

**3:00–3:45 | Fuentes y análisis**

*En pantalla:* muestra `docs/Autonomo2_Avance.md`.

> Para el diseño consulté la documentación de Python sobre clases abstractas y SQLite, además de recomendaciones de OWASP sobre seguridad. Evalué los beneficios y limitaciones de cada enfoque. SQLite facilita el prototipo local, aunque para una aplicación empresarial se requeriría evaluar otras soluciones. Del mismo modo, como todavía no se ha integrado autenticación, el sistema se ejecuta exclusivamente de forma local.

**3:45–4:30 | Logros y cierre**

*En pantalla:* muestra GitHub y los resultados de las pruebas.

> Entre los logros se encuentran un catálogo funcional, registro de pedidos, inventario persistente, pagos ficticios y un tablero de indicadores. Además, contamos con pruebas automáticas para validar las reglas de negocio. Como siguiente paso se plantea implementar permisos por rol y continuar con el diseño de la arquitectura completa. Muchas gracias.

## VIDEO 2. Demostración de funcionalidades (4–6 minutos)

**Preparación antes de grabar:**

1. Abre el proyecto local en Windows.
2. Ejecuta `run.bat`. Si aparece el aviso de firewall, no permitas acceso público: la aplicación solo utiliza `127.0.0.1`.
3. Visita <http://127.0.0.1:8000> con el navegador.
4. Deja preparada otra ventana con VS Code abierto en los archivos de clases.
5. Recuerda que el estado del inventario persiste; si ya realizaste compras, sus cantidades pueden diferir de las cifras iniciales.

**0:00–0:35 | Inicio**

> Esta es la versión funcional del prototipo local de SmartCommerce. En pantalla observamos una interfaz web con catálogo, carrito y panel administrativo. No es un sistema de cobros reales, sino una demostración académica de programación orientada a objetos.

*Acción:* enseña el inicio, la URL `127.0.0.1:8000` y el catálogo.

**0:35–1:15 | Catálogo y carrito**

> Puedo buscar productos, filtrarlos por categoría y agregarlos al carrito. Al añadir unidades, el sistema actualiza las cantidades y el total estimado.

*Acción:* busca «Mouse», añade una unidad y entra a Carrito. Cambia cantidad y muestra total.

**1:15–2:10 | Compra aprobada**

> Voy a registrar una compra con el nombre Cliente de Prueba y seleccionar la opción de pago simulado aprobado. Una vez confirmada, se registra el pedido y se descuenta inventario.

*Acción:* confirma compra → Administración → identifica pedido confirmado, ingresos ficticios y stock reducido.

**2:10–2:50 | Cancelación y consistencia**

> Ahora cancelaré el pedido: debe cambiar a estado cancelado, dejar de contabilizarse como venta y restituir exactamente una vez las unidades al inventario.

*Acción:* cancela ese pedido y compara indicadores y stock. La interfaz no permite un segundo clic en el pedido ya cancelado; explica que el backend también lo rechaza.

**2:50–3:35 | Panel administrativo**

> Podemos registrar un producto con precio, categoría y stock, así como modificar existencias. El sistema impide valores negativos porque la regla se comprueba en el backend.

*Acción:* crea «Adaptador USB», precio 12.99 y stock 5; muestra el nuevo producto en catálogo. Si intentas guardar stock negativo, el navegador puede detenerlo antes de enviar la solicitud: la prueba automatizada verifica la regla del servidor.

**3:35–4:15 | Pago rechazado**

> También puedo simular un pago rechazado. En ese caso se conserva un registro de pedido rechazado, pero no se descuentan unidades ni se incrementan las ventas confirmadas.

*Acción:* agrega producto, ve a carrito y elige «Simular rechazo». Luego revisa dashboard y pedidos.

**4:15–5:00 | Pruebas de POO y conclusión**

*Acción:* en terminal abre la carpeta y ejecuta `test.bat` o `python -m unittest discover -s backend/tests -p "test_*.py" -v`.

> Finalmente, muestro las pruebas automáticas que comprueban el funcionamiento de las clases, la encapsulación, los errores y la consistencia del inventario. Esta entrega representa un avance significativo de SmartCommerce. No se ha completado toda la aplicación, pero sí un proceso funcional con clases, interfaz, almacenamiento y pruebas.

## Cómo grabar en Windows

- Alternativa 1: **Herramienta Recortes** de Windows 11 → icono de video → seleccionar área → iniciar grabación, si tu versión admite audio de micrófono.
- Alternativa 2: **OBS Studio** → captura de ventana/pantalla + micrófono → iniciar/detener grabación.
- Muestra la aplicación en pantalla completa y aumenta zoom del navegador si el texto se ve pequeño.
- Revisa audio, duración y los dos archivos MP4; no muestres datos personales ni credenciales.
- Sube ambos videos al medio solicitado en el aula; el repositorio es el lugar de entrega del código.
