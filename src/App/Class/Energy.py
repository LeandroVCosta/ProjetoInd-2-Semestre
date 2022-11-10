import sys, os

def listarPlano():
    comando = "powercfg /L"
    resposta = os.popen(comando).read().split("\n")
    return resposta

def alterarPlano(GUID):
    comando = "powercfg /S "
    resposta = os.popen(comando + GUID).read()
    if(resposta == ""):
        return "Plano de Energia foi trocado com sucesso!"
    return "Houve um problema ao trocar o plano"

