using System;
using System.IO;

namespace BoticaInkaSalud
{
    class Program
    {
        // Cada indice representa el mismo caso en todos los arreglos.
        static int[] codigos = new int[100];
        static string[] tipos = new string[100];
        static string[] fechas = new string[100];
        static string[] asuntos = new string[100];
        static string[] descripciones = new string[100];
        static string[] referencias = new string[100];
        static string[] estados = new string[100];
        static int cantidad = 0;
        static string ruta = "registros.txt";

        static void Main(string[] args)
        {
            Console.WriteLine("BOTICA INKA SALUD - SIMULACION ACADEMICA");
            Console.WriteLine("Solo ejemplos ficticios. No sustituye el Libro de Reclamaciones.");
            if (!Cargar()) return;
            int opcion;
            do
            {
                Console.WriteLine("\n1. Registrar\n2. Listar\n3. Buscar por codigo\n4. Cambiar estado");
                Console.WriteLine("5. Ordenar por codigo\n6. Ordenar por fecha\n7. Guardar\n0. Guardar y salir");
                opcion = LeerOpcion("Opcion: ", 0, 7);
                switch (opcion)
                {
                    case 1: Registrar(); break;
                    case 2: Listar(); break;
                    case 3: Consultar(); break;
                    case 4: CambiarEstado(); break;
                    case 5: Ordenar(false); Listar(); break;
                    case 6: Ordenar(true); Listar(); break;
                    case 7: Guardar(); break;
                    case 0:
                        if (!Guardar()) opcion = 7;
                        break;
                    case -1:
                        Console.WriteLine("Entrada terminada. Los cambios no guardados se pierden.");
                        return;
                }
            } while (opcion != 0);
        }

        static int LeerOpcion(string mensaje, int minimo, int maximo)
        {
            int numero;
            while (true)
            {
                Console.Write(mensaje);
                string texto = Console.ReadLine();
                if (texto == null) return -1;
                if (int.TryParse(texto, out numero) && numero >= minimo && numero <= maximo)
                    return numero;
                Console.WriteLine("Ingrese un numero entre " + minimo + " y " + maximo + ".");
            }
        }

        static bool TextoValido(string texto, int minimo, int maximo)
        {
            return texto.Length >= minimo && texto.Length <= maximo &&
                texto == texto.Trim() && !texto.Contains("|") &&
                !texto.Contains("\r") && !texto.Contains("\n");
        }

        static string LeerTexto(string mensaje, int minimo, int maximo)
        {
            while (true)
            {
                Console.Write(mensaje);
                string texto = Console.ReadLine();
                if (texto == null) return null;
                texto = texto.Trim();
                if (TextoValido(texto, minimo, maximo)) return texto;
                Console.WriteLine("Use de " + minimo + " a " + maximo + " caracteres, sin |.");
            }
        }

        static bool FechaValida(string fecha)
        {
            if (fecha.Length != 10 || fecha[4] != '-' || fecha[7] != '-') return false;
            for (int i = 0; i < fecha.Length; i++)
                if (i != 4 && i != 7 && (fecha[i] < '0' || fecha[i] > '9')) return false;
            int anio, mes, dia;
            if (!int.TryParse(fecha.Substring(0, 4), out anio) ||
                !int.TryParse(fecha.Substring(5, 2), out mes) ||
                !int.TryParse(fecha.Substring(8, 2), out dia)) return false;
            if (anio < 1 || mes < 1 || mes > 12) return false;
            int[] diasMes = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
            if (anio % 400 == 0 || (anio % 4 == 0 && anio % 100 != 0)) diasMes[1] = 29;
            return dia >= 1 && dia <= diasMes[mes - 1];
        }

        static string MostrarCodigo(int numero)
        {
            string texto = "" + numero;
            while (texto.Length < 6) texto = "0" + texto;
            return "IS-" + texto;
        }

        static void Registrar()
        {
            if (cantidad == codigos.Length)
            {
                Console.WriteLine("Capacidad completa: 100 registros.");
                return;
            }
            int mayor = 0;
            for (int i = 0; i < cantidad; i++)
                if (codigos[i] > mayor) mayor = codigos[i];
            if (mayor == 999999)
            {
                Console.WriteLine("Se alcanzo el limite de codigos.");
                return;
            }
            if (LeerOpcion("Confirma datos ficticios: 1 Si, 0 Cancelar: ", 0, 1) != 1) return;
            int tipo = LeerOpcion("1 Reclamo, 2 Queja, 3 Recomendacion: ", 1, 3);
            if (tipo == -1) return;
            string fecha;
            do
            {
                fecha = LeerTexto("Fecha AAAA-MM-DD: ", 10, 10);
                if (fecha == null) return;
                if (!FechaValida(fecha)) Console.WriteLine("Fecha inexistente o formato incorrecto.");
            } while (!FechaValida(fecha));
            string asunto = LeerTexto("Asunto (3-100): ", 3, 100);
            if (asunto == null) return;
            string descripcion = LeerTexto("Descripcion (10-1000, una linea): ", 10, 1000);
            if (descripcion == null) return;
            string referencia = LeerTexto("Referencia opcional (0-60): ", 0, 60);
            if (referencia == null) return;
            string[] opciones = { "Reclamo", "Queja", "Recomendacion" };
            codigos[cantidad] = mayor + 1;
            tipos[cantidad] = opciones[tipo - 1];
            fechas[cantidad] = fecha;
            asuntos[cantidad] = asunto;
            descripciones[cantidad] = descripcion;
            referencias[cantidad] = referencia;
            estados[cantidad] = "Pendiente";
            cantidad++;
            Console.WriteLine("Registrado en memoria: " + MostrarCodigo(mayor + 1) + ". Use Guardar.");
        }

        static int Buscar(string codigo)
        {
            codigo = codigo.Trim().ToUpper();
            for (int i = 0; i < cantidad; i++)
                if (MostrarCodigo(codigos[i]) == codigo) return i;
            return -1;
        }

        static void MostrarRegistro(int i)
        {
            Console.WriteLine("\n" + MostrarCodigo(codigos[i]) + " | FICTICIO | " + tipos[i]);
            Console.WriteLine(fechas[i] + " | " + estados[i] + " | " + asuntos[i]);
            Console.WriteLine("Descripcion: " + descripciones[i]);
            Console.WriteLine("Referencia: " + referencias[i]);
        }

        static void Listar()
        {
            if (cantidad == 0) Console.WriteLine("No hay registros.");
            for (int i = 0; i < cantidad; i++) MostrarRegistro(i);
        }

        static void Consultar()
        {
            string codigo = LeerTexto("Codigo IS-000001: ", 1, 20);
            if (codigo == null) return;
            int indice = Buscar(codigo);
            if (indice == -1) Console.WriteLine("Codigo no encontrado.");
            else MostrarRegistro(indice);
        }

        static void CambiarEstado()
        {
            string codigo = LeerTexto("Codigo: ", 1, 20);
            if (codigo == null) return;
            int indice = Buscar(codigo);
            if (indice == -1)
            {
                Console.WriteLine("Codigo no encontrado.");
                return;
            }
            int opcion = LeerOpcion("1 Pendiente, 2 En revision, 3 Cerrado: ", 1, 3);
            if (opcion == -1) return;
            string[] opciones = { "Pendiente", "En revision", "Cerrado" };
            estados[indice] = opciones[opcion - 1];
            Console.WriteLine("Estado actualizado en memoria. Use Guardar.");
        }

        static void Intercambiar(string[] arreglo, int a, int b)
        {
            string temporal = arreglo[a];
            arreglo[a] = arreglo[b];
            arreglo[b] = temporal;
        }

        static void Ordenar(bool porFecha)
        {
            // Burbuja: se intercambian juntos todos los campos del caso.
            for (int i = 0; i < cantidad - 1; i++)
                for (int j = 0; j < cantidad - 1 - i; j++)
                {
                    bool cambiar = codigos[j] > codigos[j + 1];
                    if (porFecha)
                        cambiar = fechas[j].CompareTo(fechas[j + 1]) > 0 ||
                            (fechas[j] == fechas[j + 1] && codigos[j] > codigos[j + 1]);
                    if (cambiar)
                    {
                        int temporal = codigos[j];
                        codigos[j] = codigos[j + 1];
                        codigos[j + 1] = temporal;
                        Intercambiar(tipos, j, j + 1);
                        Intercambiar(fechas, j, j + 1);
                        Intercambiar(asuntos, j, j + 1);
                        Intercambiar(descripciones, j, j + 1);
                        Intercambiar(referencias, j, j + 1);
                        Intercambiar(estados, j, j + 1);
                    }
                }
        }

        static bool Guardar()
        {
            try
            {
                using (StreamWriter archivo = new StreamWriter(ruta))
                {
                    for (int i = 0; i < cantidad; i++)
                        archivo.WriteLine(MostrarCodigo(codigos[i]) + "|" + tipos[i] + "|" +
                            fechas[i] + "|" + asuntos[i] + "|" + descripciones[i] + "|" +
                            referencias[i] + "|" + estados[i] + "|FICTICIO");
                }
                Console.WriteLine("Datos guardados en registros.txt.");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine("No se pudo guardar: " + ex.Message);
                Console.WriteLine("Los datos siguen en memoria. Reintente; el archivo puede estar incompleto.");
                return false;
            }
        }

        static bool Cargar()
        {
            try
            {
                using (StreamReader archivo = new StreamReader(ruta))
                {
                    while (!archivo.EndOfStream)
                    {
                        string[] campos = archivo.ReadLine().Split('|');
                        int numero = 0;
                        bool valido = campos.Length == 8 && cantidad < codigos.Length;
                        if (valido)
                        {
                            valido = campos[0].Length == 9 &&
                                int.TryParse(campos[0].Substring(3), out numero) &&
                                numero > 0 && numero <= 999999 && campos[0] == MostrarCodigo(numero) &&
                                Buscar(campos[0]) == -1 && FechaValida(campos[2]) &&
                                TextoValido(campos[3], 3, 100) && TextoValido(campos[4], 10, 1000) &&
                                TextoValido(campos[5], 0, 60) && campos[7] == "FICTICIO" &&
                                (campos[1] == "Reclamo" || campos[1] == "Queja" || campos[1] == "Recomendacion") &&
                                (campos[6] == "Pendiente" || campos[6] == "En revision" || campos[6] == "Cerrado");
                        }
                        if (!valido)
                        {
                            Console.WriteLine("Archivo invalido en linea " + (cantidad + 1) + ". No se sobrescribe.");
                            return false;
                        }
                        codigos[cantidad] = numero;
                        tipos[cantidad] = campos[1];
                        fechas[cantidad] = campos[2];
                        asuntos[cantidad] = campos[3];
                        descripciones[cantidad] = campos[4];
                        referencias[cantidad] = campos[5];
                        estados[cantidad] = campos[6];
                        cantidad++;
                    }
                }
                Console.WriteLine("Registros cargados: " + cantidad);
                return true;
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("Archivo inexistente. Inicio sin registros.");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine("No se pudo cargar: " + ex.Message + ". No se sobrescribe.");
                return false;
            }
        }
    }
}
