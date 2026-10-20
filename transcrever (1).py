"""
Transcritor de Áudio
Autor: Erik Goulart
"""

__title__ = "Transcritor de Áudio"
__author__ = "Erik Goulart"
__version__ = "1.0"

import os
import queue
import sys
import threading
from tkinter import filedialog

# No .exe sem console, stdout/stderr não existem e algumas bibliotecas quebram ao escrever neles
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import customtkinter as ctk
from faster_whisper import WhisperModel

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FORMATOS = [
    ("Áudio", "*.mp3 *.wav *.m4a *.ogg *.flac *.aac *.wma *.mp4"),
    ("Todos os arquivos", "*.*"),
]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{__title__} — por {__author__}")
        self.geometry("820x600")
        self.minsize(640, 480)

        self.arquivo = None
        self.modelo = None
        self.rodando = False
        self.fila = queue.Queue()

        # Cabeçalho
        ctk.CTkLabel(self, text=__title__, font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(20, 2))
        ctk.CTkLabel(self, text="Escolha um áudio e clique em Transcrever", text_color="gray").pack()

        # Escolha do arquivo + botão Transcrever
        linha = ctk.CTkFrame(self, corner_radius=10)
        linha.pack(fill="x", padx=20, pady=(16, 10))

        self.btn_escolher = ctk.CTkButton(linha, text="Escolher áudio", width=140, command=self.escolher)
        self.btn_escolher.pack(side="left", padx=10, pady=10)

        self.lbl_arquivo = ctk.CTkLabel(linha, text="Nenhum arquivo selecionado", anchor="w", text_color="gray")
        self.lbl_arquivo.pack(side="left", fill="x", expand=True)

        self.btn_transcrever = ctk.CTkButton(
            linha, text="Transcrever", width=140, state="disabled",
            fg_color="#2e7d32", hover_color="#1b5e20", command=self.transcrever,
        )
        self.btn_transcrever.pack(side="right", padx=10)

        # Progresso
        prog = ctk.CTkFrame(self, fg_color="transparent")
        prog.pack(fill="x", padx=20)
        self.barra = ctk.CTkProgressBar(prog, height=14)
        self.barra.set(0)
        self.barra.pack(side="left", fill="x", expand=True)
        self.lbl_pct = ctk.CTkLabel(prog, text="0%", width=50)
        self.lbl_pct.pack(side="right", padx=(10, 0))

        self.lbl_status = ctk.CTkLabel(self, text="", text_color="gray", anchor="w")
        self.lbl_status.pack(fill="x", padx=20)

        # Caixa de texto (já tem rolagem)
        self.caixa = ctk.CTkTextbox(self, wrap="word", font=ctk.CTkFont(size=14), corner_radius=10)
        self.caixa.pack(fill="both", expand=True, padx=20, pady=10)

        # Rodapé
        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.pack(fill="x", padx=20, pady=(0, 14))
        ctk.CTkLabel(rodape, text=f"Feito por {__author__}  •  v{__version__}", text_color="gray").pack(side="left")
        ctk.CTkButton(rodape, text="Limpar", width=100, fg_color="gray30", hover_color="gray20",
                      command=self.limpar).pack(side="right")
        ctk.CTkButton(rodape, text="Copiar", width=100, command=self.copiar).pack(side="right", padx=10)

        self.after(100, self.ler_fila)

    # ---------- Ações ----------
    def escolher(self):
        caminho = filedialog.askopenfilename(title="Escolha o áudio", filetypes=FORMATOS)
        if caminho:
            self.arquivo = caminho
            self.lbl_arquivo.configure(text=os.path.basename(caminho), text_color=("black", "white"))
            self.btn_transcrever.configure(state="normal")
            self.zerar_progresso()
            self.lbl_status.configure(text="Pronto para transcrever")

    def transcrever(self):
        if not self.arquivo or self.rodando:
            return
        self.rodando = True
        self.btn_transcrever.configure(state="disabled")
        self.btn_escolher.configure(state="disabled")
        self.caixa.delete("1.0", "end")
        self.zerar_progresso()
        threading.Thread(target=self.trabalho, args=(self.arquivo,), daemon=True).start()

    def copiar(self):
        texto = self.caixa.get("1.0", "end").strip()
        if texto:
            self.clipboard_clear()
            self.clipboard_append(texto)
            self.lbl_status.configure(text="Texto copiado!")

    def limpar(self):
        self.caixa.delete("1.0", "end")
        if not self.rodando:
            self.zerar_progresso()
            self.lbl_status.configure(text="")

    def zerar_progresso(self):
        self.barra.set(0)
        self.lbl_pct.configure(text="0%")

    # ---------- Transcrição (roda em segundo plano) ----------
    def trabalho(self, arquivo):
        try:
            if self.modelo is None:
                self.fila.put(("status", "Carregando modelo... (na primeira vez demora mais)"))
                self.modelo = WhisperModel("small", device="cpu", compute_type="int8")
            self.fila.put(("status", "Transcrevendo..."))
            segmentos, info = self.modelo.transcribe(arquivo, language="pt")
            for s in segmentos:
                self.fila.put(("texto", s.text.strip() + " "))
                if info.duration:
                    self.fila.put(("progresso", min(s.end / info.duration, 1.0)))
            self.fila.put(("fim", None))
        except Exception as erro:
            self.fila.put(("erro", str(erro)))

    def ler_fila(self):
        try:
            while True:
                tipo, valor = self.fila.get_nowait()
                if tipo == "status":
                    self.lbl_status.configure(text=valor)
                elif tipo == "texto":
                    self.caixa.insert("end", valor)
                    self.caixa.see("end")
                elif tipo == "progresso":
                    self.barra.set(valor)
                    self.lbl_pct.configure(text=f"{valor * 100:.0f}%")
                elif tipo == "fim":
                    self.barra.set(1)
                    self.lbl_pct.configure(text="100%")
                    self.lbl_status.configure(text="Concluído!")
                    self.finalizar()
                elif tipo == "erro":
                    self.lbl_status.configure(text=f"Erro: {valor}")
                    self.finalizar()
        except queue.Empty:
            pass
        self.after(100, self.ler_fila)

    def finalizar(self):
        self.rodando = False
        self.btn_transcrever.configure(state="normal")
        self.btn_escolher.configure(state="normal")


if __name__ == "__main__":
    App().mainloop()
