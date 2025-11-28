import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scanner import escanear_ips
from updater import atualizar_agenda
from config import SAIDA_CSV
import os
import threading

class AgendaApp:
    def __init__(self, root):
        self.root = root
        root.title("Atualização de Agenda")
        root.geometry("500x400")
        root.resizable(False, False)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.configure("TLabel", font=("Segoe UI", 10))

        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(expand=True, fill="both")

        ttk.Label(self.frame, text="📋 Atualização de Agenda", font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))

        self.btn_escanear = ttk.Button(self.frame, text="🖥️ Escanear IPs", command=self.escanear)
        self.btn_escanear.pack(fill="x", pady=5)

        self.btn_csv = ttk.Button(self.frame, text="📄 Mostrar arquivo CSV", command=self.mostrar_csv)
        self.btn_csv.pack(fill="x", pady=5)

        self.btn_xml = ttk.Button(self.frame, text="📂 Selecionar agenda XML", command=self.selecionar_xml)
        self.btn_xml.pack(fill="x", pady=5)

        self.btn_atualizar = ttk.Button(self.frame, text="🚀 Atualizar agenda", command=self.iniciar_atualizacao)
        self.btn_atualizar.pack(fill="x", pady=5)

        # Log e barra de progresso
        ttk.Label(self.frame, text="📌 Log:").pack(pady=(10, 0))
        self.log_text = tk.Text(self.frame, height=10, state="disabled")
        self.log_text.pack(fill="both", expand=True)

        self.progress = ttk.Progressbar(self.frame, length=400, mode="determinate")
        self.progress.pack(pady=5)

        self.ips = []
        self.xml_path = None

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()

    def escanear(self):
        try:
            self.log("🔍 Escaneando IPs na rede...")
            self.ips = escanear_ips()
            self.log(f"✔ {len(self.ips)} IPs encontrados.")
            messagebox.showinfo("✔ Sucesso", f"{len(self.ips)} IPs encontrados.")
        except Exception as e:
            self.log(f"❌ Erro: {e}")
            messagebox.showerror("❌ Erro", str(e))

    def mostrar_csv(self):
        if not os.path.exists(SAIDA_CSV):
            messagebox.showwarning("⚠ Aviso", "CSV ainda não gerado.")
            return
        os.startfile(SAIDA_CSV)

    def selecionar_xml(self):
        path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if path:
            self.xml_path = path
            self.log(f"✔ Arquivo XML selecionado: {os.path.basename(path)}")
            messagebox.showinfo("✔ Selecionado", f"Arquivo XML: {os.path.basename(path)}")

    def iniciar_atualizacao(self):
        if not self.ips:
            messagebox.showwarning("⚠ Aviso", "Nenhum IP disponível. Escaneie primeiro.")
            return
        if not self.xml_path:
            messagebox.showwarning("⚠ Aviso", "Selecione o arquivo XML.")
            return
        # Executa atualização em thread separada para não travar a interface
        threading.Thread(target=self.atualizar_agenda_thread, daemon=True).start()

    def atualizar_agenda_thread(self):
        total = len(self.ips)
        self.progress["value"] = 0
        self.progress["maximum"] = total

        for i, ip in enumerate(self.ips, start=1):
            self.log(f"🔹 Processando IP {ip} ({i}/{total})...")
            try:
                atualizar_agenda([ip], self.xml_path)  # passa um IP por vez para log correto
                self.log(f"✔ IP {ip} concluído.")
            except Exception as e:
                self.log(f"❌ Erro no IP {ip}: {e}")

            # atualiza barra de progresso
            self.progress["value"] = i
            self.root.update_idletasks()

        self.log("🚀 Processo concluído para todos os IPs!")
        messagebox.showinfo("✔ Concluído", "Agenda atualizada para todos os IPs.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
