from queue import PriorityQueue
import yaml

import global_vars

# Abre o arquivo YML em modo de leitura ('r')
with open('model.yml', 'r', encoding='utf-8') as file:
    # Carrega o conteúdo do arquivo YML de forma segura
    dados = yaml.safe_load(file)

global_vars.seeds = dados['seeds']
global_vars.num_aleatorios_por_seed = dados['rndnumbersPerSeed']
global_vars.count = global_vars.num_aleatorios_por_seed * len(global_vars.seeds)

from models.enums.event_type import EventType
from models.event import Evento
from models.network import Network
from models.queue import QueueTandem
import running

for queue_key in dados['queues']:
    queue_val = dados['queues'][queue_key]
    if 'minArrival' and 'maxArrival' in dados['queues'][queue_key]:
        queue = QueueTandem(servers = queue_val['servers'], capacity = queue_val['capacity'], min_service = queue_val['minService'], max_service = queue_val['maxService'],
                             min_arrival = queue_val['minArrival'], max_arrival = queue_val['maxArrival'])
    else:
        queue = QueueTandem(servers = queue_val['servers'], capacity = queue_val['capacity'], min_service = queue_val['minService'], max_service = queue_val['maxService'])
    global_vars.queues[queue_key] = queue

for network in dados['network']:
    src_name = network['source']
    src_queue = global_vars.queues.get(src_name)
    target_name = network['target']
    probability = network['probability']
    saida = Network(target = target_name, probability = probability)
    src_queue.saidas.append(saida)

for queue in dados['arrivals']:
    arrival_time = dados['arrivals'][queue]
    
    global_vars.eventos.put((arrival_time, Evento(EventType.CHEGADA, arrival_time, queue)))

while running.running:
    # Discard priority number, keep event
    _, evento = global_vars.eventos.get()
    if(evento.tipo == EventType.CHEGADA):
        fila_name = evento.fila
        global_vars.queues[fila_name].chegada(evento)
    
    elif(evento.tipo == EventType.PASSAGEM):
        fila_name = evento.fila
        global_vars.queues[fila_name].passagem(evento)

    elif(evento.tipo == EventType.SAIDA):
        fila_name = evento.fila
        global_vars.queues[fila_name].saida(evento)

print(f'Tempo global final: {global_vars.tempo}')

for queue in global_vars.queues.values():
    queue.times[queue.customers] += (global_vars.tempo - queue.last_event_time)
    print('Fila: ')
    print(f'Loss: {queue.loss}')
    for index, var in enumerate(queue.times):
        print(f'{index}: {var:.3f} -> {100*var/global_vars.tempo:.2f}%')
    print('=-'*20)