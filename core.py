"""Lógica del prototipo académico. Únicamente datos ficticios."""
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path

TIPOS = ("Reclamo", "Queja", "Recomendación")
ESTADOS = ("Pendiente", "En revisión", "Cerrado")
CAMPOS = {"codigo", "tipo", "fecha", "asunto", "descripcion", "referencia", "estado", "ficticio"}


def validar_datos(tipo, fecha, asunto, descripcion, referencia=""):
    """Normaliza cadenas y devuelve datos válidos o lanza ValueError."""
    if not all(isinstance(v, str) for v in (tipo, fecha, asunto, descripcion, referencia)):
        raise ValueError("Los campos deben ser texto.")
    tipo, fecha, asunto, descripcion, referencia = [
        v.strip() for v in (tipo, fecha, asunto, descripcion, referencia)]
    if tipo not in TIPOS:
        raise ValueError("Seleccione Reclamo, Queja o Recomendación.")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
        raise ValueError("Use una fecha con formato AAAA-MM-DD.")
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("La fecha no existe en el calendario.") from error
    if not 3 <= len(asunto) <= 100:
        raise ValueError("El asunto debe tener entre 3 y 100 caracteres.")
    if not 10 <= len(descripcion) <= 1000:
        raise ValueError("La descripción debe tener entre 10 y 1000 caracteres.")
    if len(referencia) > 60:
        raise ValueError("La referencia admite como máximo 60 caracteres.")
    return dict(tipo=tipo, fecha=fecha, asunto=asunto,
                descripcion=descripcion, referencia=referencia)


def validar_registros(registros):
    if not isinstance(registros, list):
        raise ValueError("El archivo debe contener una lista JSON.")
    codigos = set()
    for registro in registros:
        if not isinstance(registro, dict) or set(registro) != CAMPOS:
            raise ValueError("Un registro tiene campos inválidos.")
        codigo = registro["codigo"]
        if not isinstance(codigo, str) or not re.fullmatch(r"IS-\d{6,}", codigo):
            raise ValueError("Código interno inválido.")
        if int(codigo[3:]) < 1 or codigo in codigos:
            raise ValueError("Código repetido o fuera de rango.")
        codigos.add(codigo)
        datos = validar_datos(*(registro[k] for k in
                               ("tipo", "fecha", "asunto", "descripcion", "referencia")))
        if any(registro[k] != v for k, v in datos.items()):
            raise ValueError("Hay campos sin normalizar en el archivo.")
        if registro["estado"] not in ESTADOS or registro["ficticio"] is not True:
            raise ValueError("Estado inválido o registro sin marca de simulación.")
    return registros


def cargar(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        return []
    with ruta.open("r", encoding="utf-8") as archivo:
        return validar_registros(json.load(archivo))


def guardar(ruta, registros):
    """Reemplazo atómico: un fallo no sobrescribe el archivo anterior."""
    validar_registros(registros)
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=ruta.parent,
                                         suffix=".tmp", delete=False) as archivo:
            temporal = Path(archivo.name)
            json.dump(registros, archivo, ensure_ascii=False, indent=2)
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, ruta)
    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()


def generar_codigo(registros):
    mayor = 0
    for registro in registros:
        mayor = max(mayor, int(registro["codigo"][3:]))
    return f"IS-{mayor + 1:06d}"


def registrar(registros, ruta, tipo, fecha, asunto, descripcion, referencia=""):
    datos = validar_datos(tipo, fecha, asunto, descripcion, referencia)
    nuevo = dict(codigo=generar_codigo(registros), **datos,
                 estado="Pendiente", ficticio=True)
    guardar(ruta, registros + [nuevo])
    registros.append(nuevo)  # Solo se confirma después de guardar.
    return nuevo


def buscar(registros, codigo):
    codigo = codigo.strip().upper()
    for registro in registros:  # Búsqueda secuencial O(n).
        if registro["codigo"] == codigo:
            return registro
    return None


def ordenar(registros, criterio="codigo"):
    """Inserción O(n²), sobre una copia; fecha ISO y código como desempate."""
    if criterio == "codigo":
        por_fecha = False
    elif criterio == "fecha":
        por_fecha = True
    else:
        raise ValueError("Criterio de ordenamiento inválido.")
    def clave(registro):
        numero = int(registro["codigo"][3:])
        return (registro["fecha"], numero) if por_fecha else numero
    resultado = list(registros)
    for i in range(1, len(resultado)):
        actual = resultado[i]
        j = i - 1
        while j >= 0 and clave(resultado[j]) > clave(actual):
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = actual
    return resultado


def cambiar_estado(registros, ruta, codigo, estado):
    if estado not in ESTADOS:
        raise ValueError("Estado inválido.")
    if buscar(registros, codigo) is None:
        raise ValueError("No se encontró el código.")
    actualizados = [dict(r) for r in registros]
    buscar(actualizados, codigo)["estado"] = estado
    guardar(ruta, actualizados)
    registros[:] = actualizados


class BloqueoSesion:
    """Evita dos instancias que escriban simultáneamente en Windows."""
    def __init__(self, ruta):
        self.ruta = Path(ruta)
        self.archivo = None

    def adquirir(self):
        import msvcrt
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.archivo = self.ruta.open("a+b")
        self.archivo.seek(0, 2)
        if self.archivo.tell() == 0:
            self.archivo.write(b"0")
            self.archivo.flush()
        self.archivo.seek(0)
        try:
            msvcrt.locking(self.archivo.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            self.archivo.close()
            self.archivo = None
            raise OSError("Ya hay otra ventana usando estos datos. Ciérrela primero.")

    def liberar(self):
        if self.archivo is not None:
            import msvcrt
            self.archivo.seek(0)
            msvcrt.locking(self.archivo.fileno(), msvcrt.LK_UNLCK, 1)
            self.archivo.close()
            self.archivo = None
