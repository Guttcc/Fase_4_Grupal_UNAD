# Este archivo define las clases abstractas base del sistema (Entidad y Servicio) para establecer contratos comunes y polimorfismo.
from abc import ABC, abstractmethod
from datetime import datetime
from exceptions import ValidacionError


class Entidad(ABC):
    """Clase abstracta que representa entidades generales dentro de Software FJ."""

    def __init__(self, id_entidad: str):
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ValidacionError("El identificador de la entidad es obligatorio y debe ser un texto válido.")
        self._id = id_entidad.strip()
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Devuelve el identificador único de la entidad."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Devuelve la fecha y hora de creación de la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción legible de la entidad."""


class Servicio(Entidad, ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        self._nombre = ""
        self._tarifa_base = 0.0
        self._disponible = bool(disponible)

        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.validar_parametros()

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del servicio."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionError("El nombre del servicio debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def tarifa_base(self) -> float:
        """Devuelve la tarifa base del servicio."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            raise ValidacionError("La tarifa base del servicio debe ser un número mayor que cero.")
        self._tarifa_base = float(valor)

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible actualmente."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise ValidacionError("El estado de disponibilidad debe ser booleano (True/False).")
        self._disponible = estado

    @abstractmethod
    def validar_parametros(self) -> None:
        """Valida los parámetros específicos de cada tipo de servicio."""

    @abstractmethod
    def calcular_costo(
        self,
        duracion: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ) -> float:
        """Calcula el costo del servicio soportando parámetros opcionales (sobrecarga en Python)."""

    @abstractmethod
    def describir(self) -> str:
        """Describe el servicio y sus condiciones."""