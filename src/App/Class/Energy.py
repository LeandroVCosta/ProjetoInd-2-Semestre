import sys, os
import wmi
import json

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

def getWatt():
    consumo = 0
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    voltage_infos = w.Sensor()
    try:
     for sensor in voltage_infos:
        if sensor.SensorType == u"Power":
            if sensor.Name == "CPU Package":
                wattCPU = round(sensor.Value,2)
                consumo += wattCPU * 1.10
            if sensor.Name == "GPU Total":
                wattGPU = round(sensor.Value,2)
                consumo += wattGPU
     return round(consumo,2)
    except:
     return 0
