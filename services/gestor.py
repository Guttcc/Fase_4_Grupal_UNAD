# Este archivo define la clase GestorSoftwareFJ para administrar clientes, servicios y reservas en listas en memoria sin base de datos, registrando eventos y errores en logs.

from exceptions import (
    CalculoCostoError,
    ReservaOperacionError,
    ServicioNoDisponibleError,
    ValidacionError,
    logger,
)
from models.base import Servicio
from models.cliente import Cliente
from models.reserva import Reserva


class GestorSoftwareFJ:
    """Gestiona las operaciones en memoria de Software FJ y registra eventos/errores en log."""

    def __init__(self, nombre_empresa: str = "Software FJ"):
        self.nombre_empresa = nombre_empresa
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        logger.info(f"Sistema inicializado para {self.nombre_empresa} (modo en memoria, sin BD).")

    @property
    def clientes(self) -> list[Cliente]:
        """Devuelve una copia superficial de la lista de clientes registrados."""
        return list(self._clientes)

    @property
    def servicios(self) -> list[Servicio]:
        """Devuelve una copia superficial de la lista de servicios registrados."""
        return list(self._servicios)

    @property
    def reservas(self) -> list[Reserva]:
        """Devuelve una copia superficial de la lista de reservas registradas."""
        return list(self._reservas)

    def registrar_cliente(
        self,
        id_cliente: str,
        nombre: str,
        correo: str,
        telefono: str,
        documento: str,
    ) -> Cliente:
        """Crea, valida y agrega un cliente a la lista en memoria."""
        try:
            if any(c.id == id_cliente.strip() for c in self._clientes if isinstance(id_cliente, str)):
                raise ValidacionError(f"Ya existe un cliente registrado con el ID '{id_cliente}'.")

            cliente = Cliente(
                id_cliente=id_cliente,
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                documento=documento,
            )

            if any(c.documento == cliente.documento for c in self._clientes):
                raise ValidacionError(f"Ya existe un cliente con el documento '{cliente.documento}'.")
        except ValidacionError as exc:
            logger.error(f"Error al registrar cliente '{id_cliente}': {exc}")
            raise
        except Exception as exc:
            logger.error(f"Fallo inesperado al registrar cliente '{id_cliente}': {exc}")
            raise ValidacionError("No se pudo completar el registro del cliente.") from exc
        else:
            self._clientes.append(cliente)
            logger.info(f"Cliente registrado correctamente: {cliente.describir()}")
            return cliente

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        """Valida y registra una instancia de Servicio en la lista en memoria."""
        try:
            if not isinstance(servicio, Servicio):
                raise ValidacionError("Solo se pueden registrar objetos que hereden de Servicio.")
            if any(s.id == servicio.id for s in self._servicios):
                raise ValidacionError(f"Ya existe un servicio registrado con el ID '{servicio.id}'.")

            servicio.validar_parametros()
        except ValidacionError as exc:
            logger.error(f"Error al registrar servicio: {exc}")
            raise
        except Exception as exc:
            logger.error(f"Fallo inesperado al registrar servicio: {exc}")
            raise ValidacionError("Error al validar o registrar el servicio.") from exc
        else:
            self._servicios.append(servicio)
            logger.info(f"Servicio registrado correctamente: {servicio.describir()}")
            return servicio

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por ID o lanza ValidacionError si no existe."""
        for cliente in self._clientes:
            if cliente.id == id_cliente:
                return cliente
        raise ValidacionError(f"Cliente con ID '{id_cliente}' no encontrado.")

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio por ID o lanza ServicioNoDisponibleError si no existe."""
        for servicio in self._servicios:
            if servicio.id == id_servicio:
                return servicio
        raise ServicioNoDisponibleError(f"Servicio con ID '{id_servicio}' no encontrado en el catálogo.")

    def buscar_reserva(self, id_reserva: str) -> Reserva:
        """Busca una reserva por ID o lanza ReservaOperacionError si no existe."""
        for reserva in self._reservas:
            if reserva.id == id_reserva:
                return reserva
        raise ReservaOperacionError(f"Reserva con ID '{id_reserva}' no encontrada.")

    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ) -> Reserva:
        """Crea una reserva verificando cliente, servicio y disponibilidad."""
        try:
            if any(r.id == id_reserva.strip() for r in self._reservas if isinstance(id_reserva, str)):
                raise ReservaOperacionError(f"Ya existe una reserva con el ID '{id_reserva}'.")

            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' ({servicio.id}) no está disponible para nuevas reservas."
                )

            reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente,
                servicio=servicio,
                duracion=duracion,
                descuento_pct=descuento_pct,
                impuesto_pct=impuesto_pct,
                extra=extra,
            )
        except (ValidacionError, ServicioNoDisponibleError, ReservaOperacionError) as exc:
            logger.error(f"Error al crear reserva '{id_reserva}': {exc}")
            raise
        except Exception as exc:
            logger.error(f"Error inesperado al crear reserva '{id_reserva}': {exc}")
            raise ReservaOperacionError(f"No se pudo crear la reserva '{id_reserva}'.") from exc
        else:
            self._reservas.append(reserva)
            logger.info(f"Reserva creada en estado PENDIENTE: {reserva.describir()}")
            return reserva

    def cancelar_reserva(self, id_reserva: str, motivo: str = "Cancelación solicitada") -> None:
        """Localiza y cancela una reserva existente registrando el resultado en el log."""
        try:
            # Verifica primero que el ID exista en la lista de reservas en memoria
            reserva = self.buscar_reserva(id_reserva)
            reserva.cancelar(motivo)
        except ReservaOperacionError as exc:
            logger.error(f"No se pudo cancelar la reserva '{id_reserva}': {exc}")
            raise
        else:
            logger.info(f"Cancelación tramitada desde gestor para reserva '{id_reserva}'.")

    def listar_reservas_por_estado(self, estado: str) -> list[Reserva]:
        """Devuelve las reservas que coinciden con un estado válido del sistema."""
        estado_normalizado = estado.strip().upper() if isinstance(estado, str) else ""
        if estado_normalizado not in Reserva.ESTADOS_VALIDOS:
            logger.warning(f"Consulta de reservas con estado inválido: '{estado}'")
            raise ValidacionError(
                f"Estado '{estado}' no válido. Use uno de: {', '.join(Reserva.ESTADOS_VALIDOS)}."
            )
        return [r for r in self._reservas if r.estado == estado_normalizado]

    def calcular_cotizacion(
        self,
        id_servicio: str,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ) -> float:
        """Calcula el costo de un servicio (polimorfismo y parámetros opcionales) con manejo de errores."""
        try:
            servicio = self.buscar_servicio(id_servicio)
            monto = servicio.calcular_costo(
                duracion=duracion,
                descuento_pct=descuento_pct,
                impuesto_pct=impuesto_pct,
                extra=extra,
            )
        except ServicioNoDisponibleError as exc:
            logger.error(f"Cotización fallida por servicio no disponible '{id_servicio}': {exc}")
            raise CalculoCostoError(f"No se puede cotizar el servicio '{id_servicio}'.") from exc
        except CalculoCostoError as exc:
            logger.error(f"Error en cálculo de cotización para '{id_servicio}': {exc}")
            raise
        else:
            logger.info(
                f"Cotización calculada para servicio '{id_servicio}' (duración={duracion}, "
                f"desc={descuento_pct}%, imp={impuesto_pct}%, extra={extra}): {monto:.2f}"
            )
            return monto
