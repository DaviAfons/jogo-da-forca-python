import random

banco_de_palavras = {
    "facil": ["python", "casa", "carro", "bola", "dog", "gato", "livro", "sol", "lua"],
    "medio": ["computador", "internet", "janela", "teclado", "monitor", "escola", "viagem"],
    "dificil": ["algoritmo", "inteligencia", "processador", "criptografia", "desenvolvimento", "hipopotamo"]
}

def escolher_palavra(dificuldade):
    # Pega a lista da dificuldade ou usa 'medio' como padrão
    lista = banco_de_palavras.get(dificuldade, banco_de_palavras["medio"])
    return random.choice(lista).upper()