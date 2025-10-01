import running

class GeradorAleatorio():
    def __init__(self, max_numbers, seed = 34, a = 1103515245, c = 12345, m = 2**31):
        """
        Inicializa o gerador de números aleatórios.
        
        Args:
            semente (int): O valor inicial (seed).
            a (int): O multiplicador.
            c (int): O incremento.
            m (int): O módulo.
        """

        self.numero_previo = seed
        self.a = a
        self.c = c
        self.m = m
        self.numeros_aleatorios_usados = 0
        self.max_numbers = max_numbers

    def next_random(self):
        """
        Gera o próximo número pseudoaleatório entre 0 e 1.
        Para se ultrapassar o maximo de numeros.
        """
        if(self.max_numbers <= self.numeros_aleatorios_usados):
            print(f'PARANDO POR CHEGAR NO NUMERO MAXIMO: {self.max_numbers}')
            running.running = False
        self.numero_previo = (self.a * self.numero_previo + self.c) % self.m
        self.numeros_aleatorios_usados += 1
        return self.numero_previo / self.m