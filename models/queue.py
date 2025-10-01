from collections import defaultdict
import global_vars
from models.enums.event_type import EventType
from models.event import Evento
import global_rng

class QueueTandem:
    def __init__(self, servers, capacity, min_service, max_service, min_arrival=-1, max_arrival=-1):
        self.servers = servers
        self.capacity = capacity
        self.min_service = min_service
        self.max_service = max_service
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.last_event_time = 0.0
        self.customers = 0
        self.loss = 0
        self.times = defaultdict(int)
        self.saidas = []

    def chegada(self, evento):
        # Atualiza tempo de ocupação das filas
        self.times[self.customers] += (evento.tempo - self.last_event_time)
        # Atualiza tempos global e local
        self.last_event_time = evento.tempo
        global_vars.tempo = evento.tempo
        # Logica de entrada
        if(self.customers < self.capacity or self.capacity == -1):
            self.customers += 1
            if(self.customers <= self.servers):
                numero_random = global_rng.rng.next_random()
                tempo = evento.tempo + self.min_service + (self.max_service - self.min_service) * numero_random
                if(len(self.saidas) > 0):
                    global_vars.eventos.put((tempo, Evento(EventType.PASSAGEM, tempo, evento.fila)))
                else:
                    global_vars.eventos.put((tempo, Evento(EventType.SAIDA, tempo, evento.fila)))
        else:
            self.loss += 1

        if(evento.tipo == EventType.CHEGADA):
            if(self.min_arrival >= 0):
                numero_random = global_rng.rng.next_random()
                tempo = evento.tempo + self.min_arrival + (self.max_arrival - self.min_arrival) * numero_random
            else:
                print('ERRO: CHEGADA INDEVIDA')
            global_vars.eventos.put((tempo, Evento(EventType.CHEGADA, tempo, evento.fila)))
    
    def passagem(self, evento):
        # Sai da fila atual
        self.saida(evento)
        # Gera numero aleatorio e declara soma acumulada
        aleatorio = global_rng.rng.next_random()
        soma = 0.0
        # Quando bater a probabilidade passa pra fila -> Não bater = fora
        for fila in self.saidas:
            soma += fila.probability
            if(soma >= aleatorio):
                evento.fila = fila.target
                global_vars.queues[evento.fila].chegada(evento)
                return

    def saida(self, evento):
        # Atualiza tempo de ocupação das filas
        self.times[self.customers] += (evento.tempo - self.last_event_time)
        # Atualiza tempos global e local
        self.last_event_time = evento.tempo
        global_vars.tempo = evento.tempo
        # Logica de saída
        self.customers -= 1
        if(self.customers >= self.servers):
            numero_random = global_rng.rng.next_random()
            tempo = evento.tempo + self.min_service + (self.max_service - self.min_service) * numero_random
            if(len(self.saidas) > 0):
                global_vars.eventos.put((tempo, Evento(EventType.PASSAGEM, tempo, evento.fila)))
            else:
                global_vars.eventos.put((tempo, Evento(EventType.SAIDA, tempo, evento.fila)))