import random

def variacoes_temperatura(media, desvio_padrao, num_minutos):
    temperatura_atual = media
    temperaturas = []

    for _ in range(num_minutos):
        variacao = random.normalvariate(0, desvio_padrao)
        temperatura_atual += variacao
        temperaturas.append(round(temperatura_atual, 1))

    return temperaturas

media_temperatura = 29
desvio_padrao = 0.2      
num_minutos = 60         

temperaturas = variacoes_temperatura(media_temperatura, desvio_padrao, num_minutos)

for minuto, temperatura in enumerate(temperaturas):
    print(f"{minuto:02d}:00, {temperatura} °C")
