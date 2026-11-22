# Este archivo define las excepciones personalizadas del sistema de Software FJ y configura el registro de eventos y errores en archivo de logs.

import logging


def configurar_logger(nombre_archivo: str = "software_fj.log") -> logging.Logger:
    """Configura y devuelve un logger que guarda eventos y errores en un archivo."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evita duplicar handlers si se llama más de una vez
    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo_handler = logging.FileHandler(nombre_archivo, mode="a", encoding="utf-8")
        archivo_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)

    return logger


logger = configurar_logger()


class SoftwareFJError(Exception):
    """Excepción base para errores del sistema de Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


class ValidacionError(SoftwareFJError):
    """Error cuando faltan parámetros o los datos ingresados no son válidos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR_VALIDACION")


class ServicioNoDisponibleError(SoftwareFJError):
    """Error cuando el servicio no existe, está inactivo o no cumple disponibilidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR_SERVICIO_NO_DISPONIBLE")


class ReservaOperacionError(SoftwareFJError):
    """Error en confirmación, cancelación, procesamiento o reglas de reserva."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR_RESERVA")


class CalculoCostoError(SoftwareFJError):
    """Error cuando ocurre un cálculo inconsistente o valores no permitidos en costos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR_CALCULO_COSTO")