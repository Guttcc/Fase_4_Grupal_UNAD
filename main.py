# Este archivo ejecuta la simulación de al menos 10 operaciones completas en Software FJ (clientes, servicios y reservas) demostrando manejo de excepciones y resiliencia sin base de datos.

from exceptions import SoftwareFJError, logger
from models.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from services.gestor import GestorSoftwareFJ


def ejecutar_simulacion() -> None:
    """Ejecuta una simulación de 12 operaciones completas con casos exitosos y con error."""
    gestor = GestorSoftwareFJ("Software FJ")
    print("=== INICIO DE SIMULACIÓN - SOFTWARE FJ (SIN BASE DE DATOS) ===\n")

    # 1. Registro válido de cliente
    try:
        c1 = gestor.registrar_cliente(
            id_cliente="CLI-01",
            nombre="Laura Mendoza",
            correo="laura.mendoza@ejemplo.com",
            telefono="+34 612 345 678",
            documento="12345678A",
        )
        print(f"[OP 1 - OK] {c1.describir()}")
    except SoftwareFJError as err:
        print(f"[OP 1 - ERROR] {err}")

    # 2. Registro inválido de cliente (correo mal formado)
    try:
        gestor.registrar_cliente(
            id_cliente="CLI-02",
            nombre="Carlos Ruiz",
            correo="carlos_sin_arroba",
            telefono="600112233",
            documento="87654321B",
        )
        print("[OP 2 - OK] Cliente registrado.")
    except SoftwareFJError as err:
        print(f"[OP 2 - ERROR CONTROLADO] {err}")

    # 3. Registro válido de segundo cliente
    try:
        c2 = gestor.registrar_cliente(
            id_cliente="CLI-03",
            nombre="Valentina Gómez",
            correo="valentina.gomez@ejemplo.com",
            telefono="+57 3104567890",
            documento="1098765432",
        )
        print(f"[OP 3 - OK] {c2.describir()}")
    except SoftwareFJError as err:
        print(f"[OP 3 - ERROR] {err}")

    # 4. Creación correcta de servicios (sala, equipo y asesoría)
    try:
        s_sala = gestor.registrar_servicio(
            ReservaSala(
                id_servicio="SRV-SALA-1",
                nombre="Sala de Conferencias Norte",
                tarifa_base=40.0,
                capacidad_personas=16,
                incluye_proyector=True,
                disponible=True,
            )
        )
        s_equipo = gestor.registrar_servicio(
            AlquilerEquipo(
                id_servicio="SRV-EQ-1",
                nombre="Kit Audio y Micrófonos Inalámbricos",
                tarifa_base=25.0,
                cantidad_unidades=4,
                requiere_fianza=True,
                disponible=True,
            )
        )
        s_asesoria = gestor.registrar_servicio(
            AsesoriaEspecializada(
                id_servicio="SRV-ASE-1",
                nombre="Asesoría Arquitectura y Seguridad",
                tarifa_base=60.0,
                especialidad="Ingeniería de Software",
                modalidad_remota=True,
                disponible=True,
            )
        )
        print(f"[OP 4 - OK] Servicios creados: {s_sala.id}, {s_equipo.id}, {s_asesoria.id}")
    except SoftwareFJError as err:
        print(f"[OP 4 - ERROR] {err}")

    # 5. Creación incorrecta de servicio (capacidad inválida <= 0)
    try:
        gestor.registrar_servicio(
            ReservaSala(
                id_servicio="SRV-SALA-ERR",
                nombre="Sala Fantasma",
                tarifa_base=30.0,
                capacidad_personas=0,
                incluye_proyector=False,
            )
        )
        print("[OP 5 - OK] Servicio creado.")
    except SoftwareFJError as err:
        print(f"[OP 5 - ERROR CONTROLADO] {err}")

    # 6. Creación de servicio no disponible para probar bloqueos posteriores
    try:
        s_inactivo = gestor.registrar_servicio(
            AlquilerEquipo(
                id_servicio="SRV-EQ-OFF",
                nombre="Estación Workstation Render",
                tarifa_base=80.0,
                cantidad_unidades=2,
                requiere_fianza=True,
                disponible=False,
            )
        )
        print(f"[OP 6 - OK] Servicio inactivo registrado para prueba: {s_inactivo.id}")
    except SoftwareFJError as err:
        print(f"[OP 6 - ERROR] {err}")

    # 7. Cotización con variantes de parámetros opcionales (descuento e impuesto)
    try:
        cotizacion = gestor.calcular_cotizacion(
            id_servicio="SRV-SALA-1",
            duracion=3,
            descuento_pct=10.0,
            impuesto_pct=21.0,
            extra=20.0,
        )
        print(f"[OP 7 - OK] Cotización sala (3h, desc 10%, IVA 21%, extra 20): {cotizacion:.2f}")
    except SoftwareFJError as err:
        print(f"[OP 7 - ERROR] {err}")

    # 8. Reserva exitosa y procesamiento completo de sala
    try:
        r1 = gestor.crear_reserva(
            id_reserva="RES-01",
            id_cliente="CLI-01",
            id_servicio="SRV-SALA-1",
            duracion=2,
            descuento_pct=5.0,
            impuesto_pct=10.0,
        )
        total_r1 = r1.procesar()
        print(f"[OP 8 - OK] Reserva {r1.id} procesada. Total: {total_r1:.2f} | Estado: {r1.estado}")
    except SoftwareFJError as err:
        print(f"[OP 8 - ERROR] {err}")

    # 9. Reserva exitosa de asesoría especializada
    try:
        r2 = gestor.crear_reserva(
            id_reserva="RES-02",
            id_cliente="CLI-03",
            id_servicio="SRV-ASE-1",
            duracion=4,
        )
        total_r2 = r2.procesar()
        print(f"[OP 9 - OK] Reserva {r2.id} procesada. Total: {total_r2:.2f} | Estado: {r2.estado}")
    except SoftwareFJError as err:
        print(f"[OP 9 - ERROR] {err}")

    # 10. Reserva fallida por servicio no disponible
    try:
        r3 = gestor.crear_reserva(
            id_reserva="RES-03",
            id_cliente="CLI-01",
            id_servicio="SRV-EQ-OFF",
            duracion=2,
        )
        r3.procesar()
        print("[OP 10 - OK] Reserva procesada.")
    except SoftwareFJError as err:
        print(f"[OP 10 - ERROR CONTROLADO] {err}")

    # 11. Reserva creada y cancelada, luego intento inválido de procesarla
    try:
        r4 = gestor.crear_reserva(
            id_reserva="RES-04",
            id_cliente="CLI-03",
            id_servicio="SRV-EQ-1",
            duracion=3,
        )
        r4.cancelar("Cambio de fecha del cliente")
        r4.procesar()
        print("[OP 11 - OK] Reserva procesada.")
    except SoftwareFJError as err:
        print(f"[OP 11 - ERROR CONTROLADO] {err}")

    # 12. Reserva fallida por cálculo inconsistente (duración negativa / descuento inválido)
    try:
        r5 = gestor.crear_reserva(
            id_reserva="RES-05",
            id_cliente="CLI-01",
            id_servicio="SRV-SALA-1",
            duracion=2,
            descuento_pct=120.0,
        )
        r5.procesar()
        print("[OP 12 - OK] Reserva procesada.")
    except SoftwareFJError as err:
        print(f"[OP 12 - ERROR CONTROLADO] {err}")

    print("\n=== RESUMEN FINAL EN MEMORIA ===")
    print(f"Clientes registrados: {len(gestor.clientes)}")
    print(f"Servicios registrados: {len(gestor.servicios)}")
    print(f"Reservas registradas: {len(gestor.reservas)}")
    for res in gestor.reservas:
        print("  -", res.describir())

    logger.info("Simulación de 12 operaciones finalizada correctamente.")
    print("\nSimulación completada. Revisa 'software_fj.log' para el historial de eventos y errores.")


if __name__ == "__main__":
    ejecutar_simulacion()