# Verificación de la versión C#

Fecha: 23 de octubre de 2026. Compilación sin errores con el compilador C# de
.NET Framework en Windows, usando únicamente System y System.IO.

Se ejecutó el programa compilado con secuencias de entrada de consola y archivos
ficticios en carpetas de trabajo aisladas. Un comprobador externo verificó las
salidas y los archivos; no forma parte del programa académico. No se atribuye
esta automatización al contenido del curso ni se confunde con las once pruebas
de la versión anterior de Python.

Resultado: **25 comprobaciones aprobadas**.

| Comprobaciones | Resultado |
|---|---|
| 1. Inicio sin archivo, listado y ordenamientos vacíos | Aprobado |
| 2. Menú no numérico y fuera de rango | Aprobado |
| 3. Búsqueda y cambio de estado sin registros | Aprobado |
| 4. Alta de Reclamo, Queja y Recomendacion | Aprobado |
| 5. Orden por fecha y desempate por código | Aprobado |
| 6. Correspondencia de todos los campos y estado al ordenar | Aprobado |
| 7. Recarga, búsqueda normalizada y detalle completo | Aprobado |
| 8. Código siguiente después de recargar y ordenar | Aprobado |
| 9. Orden ascendente por código | Aprobado |
| 10. Cancelación antes del registro | Aprobado |
| 11. Fechas imposibles, formato y bisiestos (1900 y 2000) | Aprobado |
| 12. Campos vacíos, delimitador y longitudes excesivas | Aprobado |
| 13. Tipo/estado fuera de rango y cambio a Cerrado | Aprobado |
| 14. Longitudes máximas admitidas | Aprobado |
| 15–21. Archivo con campos incompletos, fecha imposible, estado inválido, marca no ficticia, tipo inválido, código duplicado o prefijo incorrecto | Los siete se rechazan sin alterar el archivo |
| 22. Arreglo lleno: 100 registros | Alta rechazada antes de pedir datos |
| 23. Archivo de más de 100 registros | Carga rechazada sin sobrescribir |
| 24. Archivo de solo lectura al guardar | Error informado; sigue en menú y conserva datos en memoria |
| 25. Fin de entrada durante un registro | Termina sin bloqueo ni registro parcial |

## Reproducción manual

1. Extraer una copia limpia y ejecutar Iniciar.bat. Listar, buscar IS-000001,
   cambiar ese estado y ordenar: debe informar ausencia sin fallar. Ingresar letras
   y 8 en el menú: debe pedir otra opción.
2. Registrar tres ejemplos ficticios con fechas 2026-10-23, 2024-02-29 y 2024-02-29.
   Usar asuntos distintos y referencias REF-A, REF-B y REF-C. Cambiar el estado
   del segundo. Ordenar por fecha: deben aparecer códigos 2, 3 y 1 con sus campos.
3. Guardar y salir. Reabrir, buscar el segundo código con espacios y minúsculas,
   registrar otro ejemplo y verificar que recibe IS-000004. Ordenar por código.
4. Probar 2026-02-30, 1900-02-29, 0000-01-01 y 2026/01/01; deben rechazarse.
   2000-02-29 debe aceptarse. Probar asunto vacío, dos caracteres y delimitador |;
   descripción corta y campos que superen los máximos. Debe volver a pedir el campo.
5. Con el programa cerrado, usar una copia de prueba de registros.txt. Duplicar
   una línea o quitar un campo y reabrir: debe rechazar sin sobrescribirla.
6. Para capacidad, preparar una copia ficticia con 100 códigos diferentes;
   el alta 101 debe rechazarse. Una línea 101 añadida al archivo debe impedir cargar.
7. Marcar el archivo de prueba como solo lectura, abrir, cambiar estado y guardar:
   debe informar el fallo y conservar el estado nuevo en memoria. Quitar el atributo
   antes de reintentar. No realizar esta prueba sobre datos que se necesiten conservar.

No se comprobó el uso en el equipo de la botica ni la aceptación por su personal.
El fallo de guardado se comprobó al abrir un archivo de solo lectura; no se simuló
un corte eléctrico durante la escritura. La escritura directa puede dejar un archivo
parcial si se interrumpe. El proyecto de Visual Studio es una opción de edición;
la ejecución verificada se realiza con el compilador y el lanzador incluidos.
