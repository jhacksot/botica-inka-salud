"""Aplicación local para Windows. Ejecutar: py app.py"""
import os
from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import core


class Aplicacion:
    def __init__(self, raiz, ruta):
        self.raiz, self.ruta = raiz, Path(ruta)
        self.registros = core.cargar(self.ruta)
        raiz.title("Botica Inka Salud | Simulación académica EP")
        raiz.geometry("1100x740")
        raiz.minsize(950, 690)
        estilo = ttk.Style(raiz)
        estilo.theme_use("clam")
        estilo.configure("TLabel", font=("Segoe UI", 10))
        estilo.configure("TButton", font=("Segoe UI", 10), padding=6)
        estilo.configure("Treeview", rowheight=27, font=("Segoe UI", 10))
        cont = ttk.Frame(raiz, padding=18)
        cont.pack(fill="both", expand=True)
        ttk.Label(cont, text="BOTICA INKA SALUD", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(cont, text="Registro y seguimiento interno • Evaluación Parcial", font=("Segoe UI", 11)).pack(anchor="w")
        ttk.Label(cont, text="SIMULACIÓN ACADÉMICA · Solo datos ficticios · No reemplaza el Libro de Reclamaciones.",
                  foreground="#865500").pack(anchor="w", pady=(6, 12))
        formulario = ttk.LabelFrame(cont, text="Nuevo registro de demostración", padding=10)
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)
        self.tipo = tk.StringVar(value=core.TIPOS[0])
        self.fecha = tk.StringVar(value=date.today().isoformat())
        self.asunto = tk.StringVar()
        self.referencia = tk.StringVar()
        ttk.Label(formulario, text="Tipo").grid(row=0, column=0, sticky="w", padx=4, pady=5)
        ttk.Combobox(formulario, textvariable=self.tipo, values=core.TIPOS, state="readonly").grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Label(formulario, text="Fecha AAAA-MM-DD").grid(row=0, column=2, padx=10)
        ttk.Entry(formulario, textvariable=self.fecha).grid(row=0, column=3, sticky="ew", padx=4)
        ttk.Label(formulario, text="Asunto").grid(row=1, column=0, sticky="w", padx=4, pady=5)
        ttk.Entry(formulario, textvariable=self.asunto).grid(row=1, column=1, columnspan=3, sticky="ew", padx=4)
        ttk.Label(formulario, text="Descripción").grid(row=2, column=0, sticky="nw", padx=4, pady=5)
        self.descripcion = tk.Text(formulario, height=3, wrap="word", font=("Segoe UI", 10))
        self.descripcion.grid(row=2, column=1, columnspan=3, sticky="ew", padx=4)
        ttk.Label(formulario, text="Referencia opcional").grid(row=3, column=0, sticky="w", padx=4, pady=5)
        ttk.Entry(formulario, textvariable=self.referencia).grid(row=3, column=1, sticky="ew", padx=4)
        self.confirmacion = tk.BooleanVar(value=False)
        ttk.Checkbutton(formulario, text="Confirmo que son datos ficticios sin información personal ni médica",
                        variable=self.confirmacion).grid(row=4, column=0, columnspan=4, sticky="w", pady=4)
        ttk.Button(formulario, text="Registrar y guardar", command=self.registrar).grid(row=5, column=0, columnspan=2, sticky="w", pady=4)
        ttk.Button(formulario, text="Limpiar formulario", command=self.limpiar).grid(row=5, column=3, sticky="e")
        barra = ttk.Frame(cont)
        barra.pack(fill="x", pady=10)
        self.codigo = tk.StringVar()
        ttk.Label(barra, text="Código").pack(side="left")
        ttk.Entry(barra, textvariable=self.codigo, width=15).pack(side="left", padx=6)
        ttk.Button(barra, text="Buscar", command=self.buscar).pack(side="left")
        ttk.Button(barra, text="Mostrar todos", command=self.mostrar).pack(side="left", padx=6)
        self.criterio = tk.StringVar(value="codigo")
        ttk.Combobox(barra, textvariable=self.criterio, values=("codigo", "fecha"), state="readonly", width=10).pack(side="right")
        ttk.Button(barra, text="Ordenar por", command=self.mostrar).pack(side="right", padx=6)
        marco = ttk.Frame(cont)
        marco.pack(fill="both", expand=True)
        columnas = ("codigo", "tipo", "fecha", "asunto", "estado")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", selectmode="browse", height=6)
        for col, ancho in zip(columnas, (115, 120, 105, 410, 120)):
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=ancho, minwidth=80)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        horizontal = ttk.Scrollbar(marco, orient="horizontal", command=self.tabla.xview)
        horizontal.grid(row=1, column=0, sticky="ew")
        self.tabla.configure(yscrollcommand=scroll.set, xscrollcommand=horizontal.set)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        self.tabla.bind("<Double-1>", lambda evento: self.detalle())
        pie = ttk.Frame(cont)
        pie.pack(fill="x", pady=8)
        ttk.Button(pie, text="Ver detalle seleccionado", command=self.detalle).pack(side="left")
        self.estado = tk.StringVar(value=core.ESTADOS[0])
        ttk.Combobox(pie, textvariable=self.estado, values=core.ESTADOS, state="readonly", width=14).pack(side="left", padx=8)
        ttk.Button(pie, text="Guardar estado", command=self.actualizar_estado).pack(side="left")
        self.mensaje = tk.StringVar()
        ttk.Label(cont, textvariable=self.mensaje, foreground="#176244").pack(anchor="w")
        ttk.Label(cont, text=f"Archivo local: {self.ruta}", font=("Segoe UI", 8), wraplength=1020).pack(anchor="w")
        self.mostrar()

    def limpiar(self):
        self.asunto.set("")
        self.referencia.set("")
        self.descripcion.delete("1.0", "end")
        self.confirmacion.set(False)

    def registrar(self):
        if not self.confirmacion.get():
            messagebox.showwarning("Datos de demostración", "Confirme que los datos son ficticios.")
            return
        try:
            nuevo = core.registrar(self.registros, self.ruta, self.tipo.get(), self.fecha.get(),
                                   self.asunto.get(), self.descripcion.get("1.0", "end-1c"), self.referencia.get())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se registró", str(error))
            return
        self.limpiar()
        self.mostrar()
        self.mensaje.set(f"Registro ficticio {nuevo['codigo']} guardado correctamente.")

    def pintar(self, registros):
        self.tabla.delete(*self.tabla.get_children())
        for r in registros:
            self.tabla.insert("", "end", iid=r["codigo"], values=[r[c] for c in ("codigo", "tipo", "fecha", "asunto", "estado")])

    def mostrar(self):
        self.pintar(core.ordenar(self.registros, self.criterio.get()))
        self.mensaje.set(f"{len(self.registros)} registro(s) ficticio(s). Orden ascendente por {self.criterio.get()}.")

    def buscar(self):
        encontrado = core.buscar(self.registros, self.codigo.get())
        self.pintar([encontrado] if encontrado else [])
        self.mensaje.set("Registro ficticio encontrado." if encontrado else "No se encontró ese código. Use Mostrar todos para volver.")

    def seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Seleccionar", "Seleccione una fila de la lista.")
            return None
        return core.buscar(self.registros, seleccion[0])

    def detalle(self):
        registro = self.seleccionado()
        if registro is None:
            return
        ventana = tk.Toplevel(self.raiz)
        ventana.title(f"{registro['codigo']} · FICTICIO")
        ventana.geometry("660x420")
        texto = tk.Text(ventana, wrap="word", padx=16, pady=16, font=("Segoe UI", 11))
        texto.pack(fill="both", expand=True)
        texto.insert("1.0", "SIMULACIÓN ACADÉMICA\n\n" + "\n\n".join(f"{k.capitalize()}: {v}" for k, v in registro.items()))
        texto.configure(state="disabled")

    def actualizar_estado(self):
        registro = self.seleccionado()
        if registro is None:
            return
        try:
            core.cambiar_estado(self.registros, self.ruta, registro["codigo"], self.estado.get())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se guardó el estado", str(error))
            return
        self.mostrar()
        self.mensaje.set(f"Estado de {registro['codigo']} guardado.")


def main():
    raiz = tk.Tk()
    raiz.withdraw()
    ruta = Path(__file__).resolve().parent / "datos" / "registros.json"
    bloqueo = core.BloqueoSesion(ruta.with_suffix(".lock"))
    try:
        if os.name != "nt":
            raise OSError("Esta entrega está preparada para Windows.")
        bloqueo.adquirir()
        Aplicacion(raiz, ruta)
    except (ValueError, OSError) as error:
        messagebox.showerror("No se pudo abrir", f"{error}\n\nEl archivo original se conserva. Revíselo o restaure una copia válida antes de abrir el programa.")
        bloqueo.liberar()
        raiz.destroy()
        return
    def cerrar():
        bloqueo.liberar()
        raiz.destroy()
    raiz.protocol("WM_DELETE_WINDOW", cerrar)
    raiz.deiconify()
    try:
        raiz.mainloop()
    finally:
        bloqueo.liberar()


if __name__ == "__main__":
    main()
