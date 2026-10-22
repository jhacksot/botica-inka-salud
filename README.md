# Botica Inka Salud — Evaluación Parcial

Prototipo académico de escritorio creado desde cero con Python y Tkinter.
Curso Fundamentos de Programación CIIN1205P, UPN Cajamarca.
Solo desarrolla los puntos 1 al 5 de la práctica de campo. No es la evaluación final.

## Abrir en Windows

1. Extraer todo el ZIP en una carpeta con permiso de escritura, por ejemplo Documentos.
2. Tener Python 3.10 o posterior con Tcl/Tk (instalador estándar de Python para Windows).
3. Hacer doble clic en `Iniciar.bat`, o ejecutar `py -3 app.py` desde la carpeta del proyecto.

No se necesitan paquetes externos ni internet durante la ejecución. La entrega contiene
código Python; no es un ejecutable `.exe`. Si aparece un error sobre tkinter, reparar la
instalación de Python incluyendo Tcl/Tk. No ejecutar directamente dentro del ZIP.

## Uso

- Elegir Reclamo, Queja o Recomendación y una fecha válida AAAA-MM-DD.
- Escribir asunto (3–100 caracteres), descripción (10–1000) y referencia opcional (hasta 60).
- Confirmar que los datos son ficticios y pulsar Registrar y guardar.
- Copiar el código IS-000001 que aparece en la confirmación.
- Buscar por código; Mostrar todos recupera el listado completo.
- Elegir codigo o fecha y pulsar Ordenar por. El orden es ascendente.
- Seleccionar una fila para ver el detalle o guardar un estado.
- Cerrar y reabrir: los registros y estados siguen disponibles.

El archivo `datos/registros.json` empieza vacío y se guarda junto al programa, no en
la carpeta desde la cual se ejecutó la terminal. Cada registro incluye `ficticio: true`.
El código se calcula a partir del mayor código guardado. No hay eliminación de registros.
Mover toda la carpeta mueve también los datos. El historial Git no incluye los registros
de trabajo; el ZIP sí incluye un archivo vacío para el primer inicio.

## Demostración sugerida

Crear tres casos inventados:

| Tipo | Fecha | Asunto | Descripción |
|---|---|---|---|
| Reclamo | 2026-10-22 | Ejemplo ficticio de producto | Simulación de disconformidad con un producto de demostración. |
| Queja | 2026-10-20 | Ejemplo ficticio de atención | Simulación de una observación sobre la atención de demostración. |
| Recomendación | 2026-10-21 | Ejemplo ficticio de señalización | Simulación de una propuesta para mejorar la señalización del área. |

No son sucesos ocurridos en la botica. La fecha es parte del caso ficticio.

## Archivos y algoritmos

- `app.py`: interfaz y eventos Tkinter.
- `core.py`: validación, código consecutivo, búsqueda secuencial, ordenamiento por inserción,
  persistencia y bloqueo de segunda instancia en Windows.
- `tests/test_core.py`: pruebas automáticas con archivos temporales.
- `datos/registros.json`: almacenamiento local de la demostración.
- `documentacion/`: diagrama de flujo y pseudocódigo.

Ejecutar pruebas: `py -3 -m unittest discover -s tests -v`.

## Alcance y recuperación

Apoyo administrativo interno de demostración. No sustituye el Libro de Reclamaciones
oficial ni recibe legalmente reclamos. No se ha instalado ni validado con personal de la botica.
No ingresar DNI, teléfonos, nombres de clientes, datos médicos o recetas. La casilla es una
confirmación del usuario; no detecta automáticamente datos personales escritos en texto libre.
No hay autenticación, cifrado, historial de estados ni copias automáticas. El estado Cerrado
solo es una etiqueta y no acredita una respuesta al consumidor.

Para respaldar, cerrar el programa y copiar `datos/registros.json` a una ubicación segura.
Si el JSON es inválido, el programa muestra el error y se cierra sin sobrescribirlo. Conservar
una copia del archivo dañado para revisarlo y restaurar una copia válida con el programa cerrado.
Si no hay respaldo y se quiere empezar una demostración nueva, renombrar el archivo dañado
y volver a abrir (la lista empieza vacía). No editar el JSON mientras el programa esté abierto.
Una segunda instancia sobre la misma carpeta se rechaza para evitar escrituras simultáneas.

## Autoría académica

Integrantes, según la información entregada:

- ARON MUÑOZ BECERRA
- CARLOS ANTONY RAMIREZ JIMENEZ
- DALTON EXIMO ARAUJO REYES
- DEIVYS CASTREJON CHAVEZ
- JHACK ANDERSON SOTO CHILON

La elaboración contó con asistencia de Codex. No se atribuyen tareas ni commits individuales
a los integrantes. Revisar y comprender el código antes de la exposición.

## Control de versiones

Se creó un historial local nuevo por indicación de comenzar desde cero. No se reutilizó
ni modificó el repositorio remoto mencionado inicialmente. `historial.bundle` permite
recuperar los commits con `git clone historial.bundle Botica_Inka_Salud`.
El paquete ZIP es la copia lista para ejecutar; el bundle documenta el desarrollo local.
