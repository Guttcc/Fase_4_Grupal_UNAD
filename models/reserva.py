# Este archivo define la clase Reserva que integra cliente, servicio, duración y estado, gestionando confirmación, cancelación y procesamiento con excepciones.
from exceptions import (
    CalculoCostoError,
    ReservaOperacionError,
    ServicioNoDisponibleError,
    ValidacionError,
    logger,
)
from models.base import Entidad, Servicio
from models.cliente import Cliente


class Reserva(Entidad):
    """Representa una reserva de servicio realizada por un cliente en Software FJ."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ):
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise ValidacionError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ValidacionError("La reserva requiere una instancia válida de Servicio.")
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración de la reserva debe ser un número mayor que cero.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = float(duracion)
        self._descuento_pct = float(descuento_pct)
        self._impuesto_pct = float(impuesto_pct)
        self._extra = float(extra)
        self._estado = "PENDIENTE"
        self._monto_total = 0.0

    @property
    def cliente(self) -> Cliente:
        """Devuelve el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        """Devuelve el servicio reservado."""
        return self._servicio

    @property
    def duracion(self) -> float:
        """Devuelve la duración solicitada."""
        return self._duracion

    @property
    def estado(self) -> str:
        """Devuelve el estado actual de la reserva."""
        return self._estado

    @property
    def monto_total(self) -> float:
        """Devuelve el monto total calculado de la reserva."""
        return self._monto_total

    def confirmar(self) -> None:
        """Confirma la reserva verificando disponibilidad del servicio y estado actual."""
        try:
            if self._estado == "CANCELADA":
                raise ReservaOperacionError(
                    f"No se puede confirmar la reserva {self.id} porque ya fue cancelada."
                )
            if self._estado == "PROCESADA":
                raise ReservaOperacionError(
                    f"La reserva {self.id} ya fue procesada."
                )
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' no está disponible para confirmar la reserva {self.id}."
                )
        except (ReservaOperacionError, ServicioNoDisponibleError):
            logger.error(f"Fallo al confirmar reserva {self.id}.")
            raise
        else:
            self._estado = "CONFIRMADA"
            logger.info(f"Reserva {self.id} confirmada para cliente {self._cliente.id}.")
        finally:
            logger.info(f"Intento de confirmación finalizado en reserva {self.id} (estado actual: {self._estado}).")

    def cancelar(self, motivo: str = "Cancelada por el usuario") -> None:
        """Cancela la reserva si no ha sido ya procesada."""
        try:
            if self._estado == "PROCESADA":
                raise ReservaOperacionError(
                    f"No se puede cancelar la reserva {self.id} porque ya fue procesada."
                )
            if self._estado == "CANCELADA":
                raise ReservaOperacionError(
                    f"La reserva {self.id} ya se encuentra cancelada."
                )
        except ReservaOperacionError:
            logger.error(f"Fallo al cancelar reserva {self.id}: {motivo}")
            raise
        else:
            self._estado = "CANCELADA"
            logger.info(f"Reserva {self.id} cancelada. Motivo: {motivo}")
        finally:
            logger.info(f"Intento de cancelación finalizado en reserva {self.id} (estado actual: {self._estado}).")

    def procesar(self) -> float:
        """Calcula el costo final y marca la reserva como procesada."""
        try:
            if self._estado == "CANCELADA":
                raise ReservaOperacionError(
                    f"No se puede procesar la reserva {self.id} porque está cancelada."
                )
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"No se puede procesar la reserva {self.id}; el servicio '{self._servicio.nombre}' no está disponible."
                )
            if self._estado == "PENDIENTE":
                self.confirmar()

            costo = self._servicio.calcular_costo(
                duracion=self._duracion,
                descuento_pct=self._descuento_pct,
                impuesto_pct=self._impuesto_pct,
                extra=self._extra,
            )
        except (ReservaOperacionError, ServicioNoDisponibleError):
            raise
        except CalculoCostoError as exc:
            logger.error(f"Error de cálculo al procesar reserva {self.id}: {exc}")
            raise ReservaOperacionError(f"Error al procesar el costo de la reserva {self.id}.") from exc
        except Exception as exc:
            logger.error(f"Error inesperado al procesar reserva {self.id}: {exc}")
            raise ReservaOperacionError(f"Fallo inesperado al procesar la reserva {self.id}.") from exc
        else:
            self._monto_total = costo
            self._estado = "PROCESADA"
            logger.info(
                f"Reserva {self.id} procesada con éxito. Cliente: {self._cliente.id}, "
                f"Servicio: {self._servicio.id}, Total: {self._monto_total:.2f}"
            )
            return self._monto_total
        finally:
            logger.info(f"Ciclo de procesamiento cerrado para reserva {self.id} (estado: {self._estado}).")

    def describir(self) -> str:
        """Retorna un resumen del estado y detalle de la reserva."""
        return (
            f"Reserva [{self.id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | Total: {self._monto_total:.2f}"
        )