# Este archivo define las clases derivadas de Servicio (ReservaSala, AlquilerEquipo y AsesoriaEspecializada) con polimorfismo y cálculo de costos.

from exceptions import CalculoCostoError, ValidacionError
from models.base import Servicio


class ReservaSala(Servicio):
    """Representa el servicio de reserva de salas en Software FJ."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        capacidad_personas: int,
        incluye_proyector: bool = False,
        disponible: bool = True,
    ):
        self._capacidad_personas = 0
        self._incluye_proyector = bool(incluye_proyector)
        self.capacidad_personas = capacidad_personas
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    @property
    def capacidad_personas(self) -> int:
        """Obtiene la capacidad máxima de personas de la sala."""
        return self._capacidad_personas

    @capacidad_personas.setter
    def capacidad_personas(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ValidacionError("La capacidad de la sala debe ser un entero mayor que cero.")
        self._capacidad_personas = valor

    @property
    def incluye_proyector(self) -> bool:
        """Indica si la sala incluye proyector."""
        return self._incluye_proyector

    def validar_parametros(self) -> None:
        """Valida los parámetros específicos de una sala."""
        if self._capacidad_personas < 1:
            raise ValidacionError("Una sala debe admitir al menos 1 persona.")

    def calcular_costo(
        self,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ) -> float:
        """Calcula el costo por horas de sala con soporte para descuento, impuesto y cargos extra."""
        try:
            if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
                raise CalculoCostoError("La duración en horas de la reserva de sala debe ser mayor que cero.")
            if not (0 <= descuento_pct < 100):
                raise CalculoCostoError("El porcentaje de descuento debe estar entre 0 y 99.9.")
            if impuesto_pct < 0:
                raise CalculoCostoError("El porcentaje de impuesto no puede ser negativo.")
            if extra < 0:
                raise CalculoCostoError("El costo adicional no puede ser negativo.")

            recargo_proyector = 15.0 * duracion if self._incluye_proyector else 0.0
            subtotal = (self.tarifa_base * duracion) + recargo_proyector + extra
            con_descuento = subtotal * (1 - (descuento_pct / 100.0))
            total = con_descuento * (1 + (impuesto_pct / 100.0))

            if total < 0:
                raise CalculoCostoError("El costo total calculado no puede ser negativo.")

            return round(float(total), 2)
        except CalculoCostoError:
            raise
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise CalculoCostoError("Error numérico al calcular el costo de la reserva de sala.") from exc

    def describir(self) -> str:
        """Describe la sala, su capacidad y tarifa base."""
        proyector_txt = "con proyector" if self._incluye_proyector else "sin proyector"
        estado_txt = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio Sala [{self.id}] - {self.nombre} | Capacidad: {self._capacidad_personas} pax "
            f"({proyector_txt}) | Tarifa/h: {self.tarifa_base:.2f} | {estado_txt}"
        )


class AlquilerEquipo(Servicio):
    """Representa el servicio de alquiler de equipos técnicos."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        cantidad_unidades: int,
        requiere_fianza: bool = True,
        disponible: bool = True,
    ):
        self._cantidad_unidades = 0
        self._requiere_fianza = bool(requiere_fianza)
        self.cantidad_unidades = cantidad_unidades
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    @property
    def cantidad_unidades(self) -> int:
        """Obtiene la cantidad de unidades disponibles del equipo."""
        return self._cantidad_unidades

    @cantidad_unidades.setter
    def cantidad_unidades(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ValidacionError("La cantidad de unidades del equipo debe ser un entero mayor que cero.")
        self._cantidad_unidades = valor

    @property
    def requiere_fianza(self) -> bool:
        """Indica si el alquiler requiere fianza."""
        return self._requiere_fianza

    def validar_parametros(self) -> None:
        """Valida los parámetros específicos del alquiler de equipos."""
        if self._cantidad_unidades <= 0:
            raise ValidacionError("Debe haber al menos una unidad para alquilar.")

    def calcular_costo(
        self,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ) -> float:
        """Calcula el costo por días de alquiler con fianza opcional, descuento e impuesto."""
        try:
            if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
                raise CalculoCostoError("La duración en días del alquiler debe ser mayor que cero.")
            if not (0 <= descuento_pct < 100):
                raise CalculoCostoError("El porcentaje de descuento debe estar entre 0 y 99.9.")
            if impuesto_pct < 0:
                raise CalculoCostoError("El porcentaje de impuesto no puede ser negativo.")
            if extra < 0:
                raise CalculoCostoError("El costo adicional no puede ser negativo.")

            fianza = 50.0 if self._requiere_fianza else 0.0
            subtotal = (self.tarifa_base * duracion) + fianza + extra
            con_descuento = subtotal * (1 - (descuento_pct / 100.0))
            total = con_descuento * (1 + (impuesto_pct / 100.0))

            if total < 0:
                raise CalculoCostoError("El costo total calculado no puede ser negativo.")

            return round(float(total), 2)
        except CalculoCostoError:
            raise
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise CalculoCostoError("Error numérico al calcular el costo del alquiler de equipo.") from exc

    def describir(self) -> str:
        """Describe el equipo, unidades y condiciones de alquiler."""
        fianza_txt = "requiere fianza" if self._requiere_fianza else "sin fianza"
        estado_txt = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio Equipo [{self.id}] - {self.nombre} | Unidades: {self._cantidad_unidades} "
            f"({fianza_txt}) | Tarifa/día: {self.tarifa_base:.2f} | {estado_txt}"
        )


class AsesoriaEspecializada(Servicio):
    """Representa el servicio de asesorías técnicas especializadas."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        especialidad: str,
        modalidad_remota: bool = True,
        disponible: bool = True,
    ):
        self._especialidad = ""
        self._modalidad_remota = bool(modalidad_remota)
        self.especialidad = especialidad
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    @property
    def especialidad(self) -> str:
        """Obtiene el área de especialidad de la asesoría."""
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionError("La especialidad de la asesoría debe tener al menos 3 caracteres.")
        self._especialidad = valor.strip()

    @property
    def modalidad_remota(self) -> bool:
        """Indica si la asesoría se puede realizar de forma remota."""
        return self._modalidad_remota

    def validar_parametros(self) -> None:
        """Valida los parámetros específicos de una asesoría."""
        if not self._especialidad:
            raise ValidacionError("La asesoría especializada requiere una especialidad definida.")

    def calcular_costo(
        self,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ) -> float:
        """Calcula el costo por horas de asesoría con descuento, impuesto y recargos opcionales."""
        try:
            if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
                raise CalculoCostoError("La duración en horas de la asesoría debe ser mayor que cero.")
            if not (0 <= descuento_pct < 100):
                raise CalculoCostoError("El porcentaje de descuento debe estar entre 0 y 99.9.")
            if impuesto_pct < 0:
                raise CalculoCostoError("El porcentaje de impuesto no puede ser negativo.")
            if extra < 0:
                raise CalculoCostoError("El costo adicional no puede ser negativo.")

            subtotal = (self.tarifa_base * duracion) + extra
            con_descuento = subtotal * (1 - (descuento_pct / 100.0))
            total = con_descuento * (1 + (impuesto_pct / 100.0))

            if total < 0:
                raise CalculoCostoError("El costo total calculado no puede ser negativo.")

            return round(float(total), 2)
        except CalculoCostoError:
            raise
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise CalculoCostoError("Error numérico al calcular el costo de la asesoría.") from exc

    def describir(self) -> str:
        """Describe la asesoría especializada, modalidad y tarifa."""
        modalidad_txt = "Remota/Presencial" if self._modalidad_remota else "Solo presencial"
        estado_txt = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio Asesoría [{self.id}] - {self.nombre} | Área: {self._especialidad} "
            f"({modalidad_txt}) | Tarifa/h: {self.tarifa_base:.2f} | {estado_txt}"
        )