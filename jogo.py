def iniciar_jogo(palavra):
    # 6 tentativas para corresponder às 6 partes do boneco
    tentativas = 6
    return ["_" for _ in palavra], tentativas


def tentar(palavra_sec, palavra_oculta, letra, tentativas):
    acertou = False
    letra = letra.upper()
    
    if letra in palavra_sec:
        acertou = True
        for i, l in enumerate(palavra_sec):
            if l == letra:
                palavra_oculta[i] = letra
        mensagem = "Boa! Você acertou."
    else:
        tentativas -= 1
        mensagem = f"Errou! Tentativas restantes: {tentativas}"

    return palavra_oculta, tentativas, mensagem, acertou


def venceu(palavra_oculta):
    return "_" not in palavra_oculta


def perdeu(tentativas):
    return tentativas <= 0