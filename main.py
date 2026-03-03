import random
import simpy

env = simpy.Environment()
RAM = simpy.Container(env, init=100)
CPU = simpy.Resource(env, capacity=1)
RANDOM_SEED = 42
TIEMPOS = []


def proceso(env, name, RAM, CPU, TIME, INTERVAL):
    tiempoInicio = env.now
    memoria = random.randint(1, 10)
    instrucciones = random.expovariate(1/ INTERVAL)

    # Solicitar memoria
    yield RAM.get(memoria)
    print(f"{name} ha solicitado {memoria} unidades de RAM en el tiempo {env.now} estado NEW")

    with CPU.request() as req:
        yield req
        print(f"{name} ha obtenido acceso a la CPU en el tiempo {env.now} estado READY")
        yield env.timeout(1)
        # soltar CPU
        yield req
        instrucciones -= 1

        print(f"{name} ha terminado de usar la CPU en el tiempo {env.now}")
        # Decrementar velocidad del CPU



if __name__ == "__main__":
    main()