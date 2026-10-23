# Botica Inka Salud

Programa académico de consola en C# para registrar y consultar reclamos, quejas y recomendaciones ficticias. Apoyo administrativo de demostración; no sustituye el Libro de Reclamaciones.

## Ejecutar en Windows

Requisitos: Windows con .NET Framework 4.7.2 o posterior y su compilador csc.exe. No necesita Python, paquetes externos ni internet. Extraer el ZIP completo en una carpeta con permiso de escritura, abrir PowerShell en ella y ejecutar:

```powershell
.\Iniciar.bat
```

También se puede hacer doble clic en Iniciar.bat. Compila Program.cs en bin/ y ejecuta el programa desde la carpeta del proyecto. Para editar en Visual Studio, abrir BoticaInkaSalud.csproj con las herramientas de .NET Framework 4.7.2 instaladas. El proyecto y el lanzador son configuración de compilación; la lógica académica completa está en Program.cs.

## Ejemplo ficticio de uso

1. Elegir 1, confirmar datos ficticios con 1 y elegir tipo 1 (Reclamo).
2. Fecha 2026-10-23, asunto Ejemplo ficticio, descripción Simulacion academica sin datos de clientes; dejar la referencia vacía.
3. Aparece IS-000001 en memoria. Elegir 3 y buscar ese código.
4. Elegir 4, indicar el código y seleccionar 2 (En revision).
5. Crear otro ejemplo con una fecha anterior y elegir 6 para ordenar por fecha.
6. Elegir 0 para guardar y salir. Reabrir y elegir 2 para comprobar la recuperación.

Menú: registrar, listar con detalle, buscar por código, cambiar estado, ordenar por código o fecha, guardar, guardar y salir. El código continúa desde el mayor cargado. Los textos de tipo y estado se escriben sin tildes para facilitar su uso en consolas Windows; los campos libres conservan los caracteres ingresados.

## Relación con los materiales

Las referencias usan las claves y páginas del resumen técnico recibido, no una división inventada en seis sesiones.

| Técnica | Referencia | Aplicación |
|---|---|---|
| Variables, operadores, condiciones y ciclos | T1.2 pp. 15–23; S07 | Validación y menú do-while/switch |
| Métodos estáticos, parámetros y retornos | T2.1 pp. 5–8; P2; S07 | Operaciones separadas en métodos |
| int.TryParse y out | T2.2 pp. 5–8 | Opciones, fechas y códigos |
| Arreglos con contador y búsqueda secuencial | T3.1 pp. 5–8; T3.2 pp. 5–7 | Capacidad de 100 y consulta |
| Arreglos paralelos | T3.4 pp. 5–7; T4.3 pp. 4–7; S07 | Campos unidos por índice |
| Burbuja, intercambio y CompareTo | T3.3 pp. 5–7; T4.4 pp. 4–7 | Orden ascendente; desempate por código |
| Cadenas, índices, Trim, ToUpper, Substring, Contains, Split | T4.1–T4.4 | Validación y lectura de campos |
| StreamReader, StreamWriter, using, try-catch | T5.2–T5.4 | Cargar y guardar texto |
| Git y commits | T1.1 pp. 5–15 | Historial de la adaptación |

## Datos y limitaciones

- Máximo 100 registros; códigos de IS-000001 a IS-999999. No hay eliminación.
- Asunto de 3–100 caracteres; descripción de 10–1000; referencia opcional de hasta 60. Fecha real AAAA-MM-DD, incluidos años bisiestos. No se admite | en textos.
- registros.txt contiene una línea por caso: codigo|tipo|fecha|asunto|descripcion|referencia|estado|FICTICIO. Se crea localmente y se excluye de Git. No se incluyen registros históricos reales.
- Registrar y cambiar estado modifican la memoria. Guardar con 7 o salir con 0. Cerrar la ventana o terminar la entrada sin guardar pierde los cambios pendientes.
- Un archivo inválido detiene el inicio sin sobrescribirlo. Respaldarlo y corregirlo o restaurar una copia válida antes de volver a iniciar.
- El guardado es directo: un fallo durante la escritura puede dejar el archivo incompleto. El programa informa el error y permite reintentar con los datos en memoria. Copiar manualmente el archivo con el programa cerrado para respaldarlo.
- Usar una sola instancia. No hay bloqueo de sesiones, escritura atómica, cifrado, autenticación, notificaciones, base de datos ni servicios web.
- La marca FICTICIO es una confirmación del usuario; no detecta datos personales. No introducir información real de clientes. Los estados son etiquetas de seguimiento.

## Explicación y verificación

Para exponer: explicar primero el índice compartido de los siete arreglos y el contador; después mostrar el menú, las validaciones, la búsqueda secuencial, el intercambio completo de burbuja y la lectura/escritura por líneas.

Se realizaron 25 comprobaciones del ejecutable mediante entradas de consola preparadas fuera del código entregado. Ver documentacion/verificacion.md para resultados y reproducción manual; no se incluyen frameworks de pruebas. Ver documentacion/adaptacion.md para decisiones técnicas y pseudocódigo.

La versión actual usa C#. La documentación de verificación corresponde a esta versión.
