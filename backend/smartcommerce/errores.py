"""Excepciones de dominio para no mezclar errores comerciales y HTTP."""


class ErrorNegocio(Exception):
    """Error controlado que el servidor transforma en mensaje seguro para el usuario."""

    codigo = "ERROR_NEGOCIO"
    http = 400

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class ErrorValidacion(ErrorNegocio):
    codigo = "DATOS_INVALIDOS"
    http = 400


class NoEncontrado(ErrorNegocio):
    codigo = "NO_ENCONTRADO"
    http = 404


class SinExistencias(ErrorNegocio):
    codigo = "STOCK_INSUFICIENTE"
    http = 409


class EstadoInvalido(ErrorNegocio):
    codigo = "ESTADO_INVALIDO"
    http = 409
