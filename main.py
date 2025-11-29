import tkinter as tk
from interface import ForcaGUI

def main():
    janela = tk.Tk()
    app = ForcaGUI(janela)
    
    janela.update() 
    janela.deiconify()

    janela.mainloop()
    
if __name__ == "__main__":
    main()