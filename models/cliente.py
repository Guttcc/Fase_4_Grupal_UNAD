# Este archivo define la clase Cliente con encapsulación de datos personales y validaciones estrictas.
import re
from exceptions import ValidacionError
from models.base import Entidad


class Cliente(Entidad):
    """Representa un cliente de Software FJ con datos personales encapsulados y validados."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str, documento: str):
        super().__init__(id_cliente)
        self._nombre = ""
        self._correo = ""
        self._telefono = ""
        self._documento = ""

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.documento = documento

    @property
    def nombre(self) -> str:
        """Obtiene el nombre completo del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidacionError("El nombre del cliente debe tener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", valor.strip()):
            raise ValidacionError("El correo electrónico del cliente no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Obtiene el teléfono de contacto del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValidacionError("El teléfono debe ser una cadena de texto.")
        limpio = re.sub(r"[\s\-\(\)]", "", valor.strip())
        if not re.match(r"^\+?\d{7,15}$", limpio):
            raise ValidacionError("El teléfono debe contener entre 7 y 15 dígitos (opcional '+' inicial).")
        self._telefono = limpio

    @property
    def documento(self) -> str:
        """Obtiene el documento de identidad del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 5:
            raise ValidacionError("El documento de identidad debe tener al menos 5 caracteres.")
        self._documento = valor.strip().upper()

    def describir(self) -> str:
        """Retorna un resumen legible del cliente."""
        return (
            f"Cliente [{self.id}] - {self.nombre} | Doc: {self.documento} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )