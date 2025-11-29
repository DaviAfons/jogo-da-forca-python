import tkinter as tk
from tkinter import messagebox
from jogo import iniciar_jogo, tentar, venceu, perdeu
from palavras import escolher_palavra

class ForcaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Forca")
        
        # Centralizar a janela na tela
        largura = 600
        altura = 650
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (largura / 2)
        y = (screen_height / 2) - (altura / 2)
        self.root.geometry(f"{largura}x{altura}+{int(x)}+{int(y)}")

        # --- SELEÇÃO DE DIFICULDADE ---
        self.frame_dif = tk.Frame(root)
        self.frame_dif.pack(pady=15)

        tk.Label(self.frame_dif, text="Dificuldade:", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        self.dificuldade = tk.StringVar(value="medio")
        opcoes = ["facil", "medio", "dificil"]
        tk.OptionMenu(self.frame_dif, self.dificuldade, *opcoes).pack(side="left")

        tk.Button(root, text="Novo Jogo", command=self.iniciar, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        # Área Principal
        self.frame_jogo = tk.Frame(root)
        self.frame_jogo.pack(expand=True, fill="both")
        
        # Inicia o jogo automaticamente ao abrir
        self.iniciar()

    def iniciar(self):
        # Limpa a tela anterior
        for widget in self.frame_jogo.winfo_children():
            widget.destroy()

        self.palavra_sec = escolher_palavra(self.dificuldade.get())
        self.palavra_oculta, self.tentativas = iniciar_jogo(self.palavra_sec)
        
        # Canvas (Desenho)
        self.canvas = tk.Canvas(self.frame_jogo, width=200, height=250, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.desenhar_base()

        # Palavra Oculta
        self.palavra_label = tk.Label(self.frame_jogo, text=" ".join(self.palavra_oculta), font=("Consolas", 24, "bold"))
        self.palavra_label.pack(pady=10)

        # Mensagem de Status
        self.resultado = tk.Label(self.frame_jogo, text="Escolha uma letra:", font=("Arial", 12))
        self.resultado.pack(pady=5)

        # Teclado Virtual
        self.criar_teclado()

    def criar_teclado(self):
        self.frame_botoes = tk.Frame(self.frame_jogo)
        self.frame_botoes.pack(pady=20)
        self.botoes = []

        alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Cria o teclado em 2 linhas
        for index, letra in enumerate(alfabeto):
            btn = tk.Button(self.frame_botoes, text=letra, width=4, height=2,
                            font=("Arial", 10, "bold"),
                            bg="#f0f0f0",
                            command=lambda l=letra: self.tentar_letra(l))
            
            linha = 0 if index < 13 else 1
            coluna = index if index < 13 else index - 13
            
            btn.grid(row=linha, column=coluna, padx=2, pady=2)
            self.botoes.append(btn)

    def desenhar_base(self):
        self.canvas.create_line(20, 230, 180, 230, width=4)
        self.canvas.create_line(50, 230, 50, 20, width=4)
        self.canvas.create_line(50, 20, 130, 20, width=4)
        self.canvas.create_line(130, 20, 130, 50, width=4)

    def desenhar_parte(self, erro_numero):
        if erro_numero == 1:   # Cabeça
            self.canvas.create_oval(110, 50, 150, 90, width=3)
        elif erro_numero == 2: # Corpo
            self.canvas.create_line(130, 90, 130, 150, width=3)
        elif erro_numero == 3: # Braço esquerdo
            self.canvas.create_line(130, 110, 110, 130, width=3)
        elif erro_numero == 4: # Braço direito
            self.canvas.create_line(130, 110, 150, 130, width=3)
        elif erro_numero == 5: # Perna esquerda
            self.canvas.create_line(130, 150, 110, 180, width=3)
        elif erro_numero == 6: # Perna direita
            self.canvas.create_line(130, 150, 150, 180, width=3)

    def tentar_letra(self, letra):
        # Desabilita visualmente o botão clicado
        for btn in self.botoes:
            if btn['text'] == letra:
                btn['state'] = 'disabled'
                btn['bg'] = '#dddddd'

        self.palavra_oculta, self.tentativas, msg, acertou = tentar(
            self.palavra_sec, self.palavra_oculta, letra, self.tentativas
        )

        self.palavra_label["text"] = " ".join(self.palavra_oculta)
        
        if acertou:
            self.resultado["text"] = "Acertou! " + msg
            self.resultado["fg"] = "green"
        else:
            self.resultado["text"] = msg
            self.resultado["fg"] = "red"
            # Lógica de desenho: Erro 1 desenha cabeça, etc.
            erro_atual = 6 - self.tentativas
            self.desenhar_parte(erro_atual)

        self.verificar_fim_de_jogo()

    def verificar_fim_de_jogo(self):
        if venceu(self.palavra_oculta):
            self.resultado["text"] = "VOCÊ VENCEU! 🎉"
            self.resultado["fg"] = "blue"
            self.desativar_todos_botoes()
            messagebox.showinfo("Fim de Jogo", "Parabéns! Você venceu!")

        elif perdeu(self.tentativas):
            self.resultado["text"] = f"GAME OVER. A palavra era: {self.palavra_sec}"
            self.resultado["fg"] = "red"
            self.desativar_todos_botoes()
            messagebox.showinfo("Fim de Jogo", f"Você perdeu!\nA palavra era: {self.palavra_sec}")

    def desativar_todos_botoes(self):
        for b in self.botoes:
            b["state"] = "disabled"