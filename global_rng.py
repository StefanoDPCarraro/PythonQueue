import global_vars
from services.rng_service import GeradorAleatorio

rng = GeradorAleatorio(global_vars.count, seed=global_vars.seeds[0])
