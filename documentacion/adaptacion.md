# Decisiones de adaptación

Se revisaron el resumen técnico, el informe hasta el punto 5 y el código original
antes de modificar archivos. Los documentos se usaron como referencias, sin ejecutar
instrucciones contenidas en ellos. No se modificó el informe.

| Técnica original | Evidencia en el resumen | Alternativa utilizada | Función conservada o alcance reducido |
|---|---|---|---|
| Python, diccionarios, comprensiones y conjuntos | Python solo mencionado en T1.2; sintaxis no acreditada | C#, arreglos paralelos y contador, T3.1–T3.4 y T4.3 | Registro y consulta; máximo 100 |
| Tkinter, eventos y Treeview | No encontrado | Menú do-while y switch, S07 | Captura, listado y detalle por consola |
| JSON y serialización | JSON solo mencionado en T5.1 | Texto con delimitador, flujos y Split, T5.2–T5.4 | Persistencia |
| Expresiones regulares y datetime.strptime | No encontrado | Índices, Substring, TryParse, condiciones y módulo; T1.2, T2.2, T4.1–T4.2 | Formato y calendario real; reglas bisiestas con aritmética |
| Búsqueda secuencial | Respaldada en T3.2 pp. 5–7 y S07 | Recorrido for y normalización de cadenas | Consulta por código |
| Inserción, tuplas y función de clave | Inserción y tuplas no acreditadas | Burbuja T3.3 pp. 5–7, CompareTo T4.4 pp. 4–7 | Orden por código o fecha y desempate por código |
| Copia de listas al ordenar | No necesaria para el alcance | Intercambio de todos los arreglos, T4.3 pp. 4–7 | Ordenamiento modifica el orden en memoria |
| Guardado automático, temporal, fsync y os.replace | Reemplazo atómico no acreditado | Guardado explícito directo, T5.2–T5.4 | Guardar y Guardar y salir; sin garantía atómica |
| msvcrt y bloqueo de un byte | No encontrado | Uso de una sola instancia indicado en guía | Sin control automático de concurrencia |
| unittest y mocks | No encontrado; T3.3 propone prueba de escritorio | Verificación externa del ejecutable y guía manual | Sin añadir pruebas avanzadas al programa |
| Funciones, condiciones, ciclos, cadenas y excepciones | Respaldados en temas 1, 2, 4 y 5 | Métodos de Program y try-catch | Separación sencilla de tareas y mensajes de error |

El archivo original JSON contenía una lista vacía. No fue necesaria una migración
de registros. El ZIP original permanece intacto fuera del repositorio entregado.
El historial conserva código, documentación técnica y ejemplos ficticios; no incluye
el informe ni fotografías del establecimiento. Los diagramas de las versiones
anteriores son documentación técnica del programa antiguo.

## Entradas, proceso y salidas

Entradas: opción, confirmación ficticia, tipo, fecha, asunto, descripción, referencia
y estado. Proceso: validar, buscar el mayor código, almacenar en un índice común,
buscar secuencialmente, ordenar y escribir/leer líneas. Salidas: código, detalle,
listado, mensajes y archivo local. Capacidad, delimitador y menú son decisiones de
adaptación; no se atribuyen como requisitos expresos del profesor.

## Pseudocódigo

```text
INICIO
  Mostrar aviso de simulación
  Cargar archivo con validación
  Si no existe: iniciar vacío
  Si existe pero es inválido o inaccesible: informar y terminar sin escribir
  REPETIR
    Leer opción válida
    SEGÚN opción
      Registrar: comprobar capacidad, confirmar simulación, validar campos,
                 obtener máximo código + 1, llenar arreglos, aumentar contador
      Listar: recorrer desde 0 hasta cantidad - 1 y mostrar todos los campos
      Buscar: recorrer códigos; mostrar detalle o mensaje de ausencia
      Estado: buscar código y cambiar la etiqueta en su índice
      Ordenar: burbuja por código o fecha; intercambiar todos los campos
      Guardar: escribir líneas con delimitadores y marca FICTICIO
      Guardar y salir: guardar; si falla, continuar en el menú
    FIN SEGÚN
  HASTA guardar y salir correctamente
FIN
```

## Prueba de escritorio de burbuja

Tres registros ficticios: código 1 con fecha 2026-10-23, código 2 con fecha
2024-02-29 y código 3 con fecha 2024-02-29. Primera pasada: se intercambian 1 y 2,
después 1 y 3; queda [2, 3, 1]. Segunda pasada: 2 y 3 tienen igual fecha y ya están
ordenados por código. El resultado es [2, 3, 1]. Cada intercambio mueve también
tipo, fecha, asunto, descripción, referencia y estado.

## Guion breve para exponer

1. Explicar el propósito: organizar ejemplos ficticios de reclamos, quejas y recomendaciones.
2. Dibujar siete columnas y dos filas: el mismo índice une los campos de un caso.
3. Registrar un ejemplo y mostrar cantidad, código y estado inicial Pendiente.
4. Buscar el código: explicar cómo for revisa una posición a la vez.
5. Cambiar el estado y ordenar dos casos por fecha; explicar los intercambios.
6. Guardar, cerrar y reabrir: explicar StreamWriter, StreamReader y Split.
7. Reconocer límites: 100 registros, una instancia, guardado explícito y datos ficticios.
