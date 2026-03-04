import random
import matplotlib.pyplot as plt
import simpy
from statistics import stdev as desvest
import os

os.makedirs("graficas", exist_ok=True)

env = simpy.Environment()
RAM = simpy.Container(env, init=100)
CPU = simpy.Resource(env, capacity=1)
RANDOM_SEED = 42
TIEMPOS = []

def process_generator(env, num_processes, RAM, CPU, CPU_SPEED, INTERVAL):
    for i in range(num_processes):
        env.process(process(env, f"Proceso {i+1}", RAM, CPU, CPU_SPEED))
        yield env.timeout(random.expovariate(1.0 / INTERVAL))

def process(env, name, RAM, CPU, CPU_SPEED):
    tiempoInicio = env.now
    memoria = random.randint(1, 10)
    instrucciones = random.randint(1, 10)

    # Solicitar memoria
    yield RAM.get(memoria)

    while instrucciones > 0:
        with CPU.request() as req:
            yield req
            yield env.timeout(1)
            # soltar CPU
            instrucciones -= CPU_SPEED

            # Randomización de estado de eventos
            n = random.randint(1, 21)
        
        if n == 1:
            yield env.timeout(random.randint(1, 5))
        # n == 2 u otro regresa a ready (el loop continúa)

    yield RAM.put(memoria)  
    TIEMPOS.append(env.now - tiempoInicio)

def correr_simulacion(num_processes, INTERVAL, RAM_SIZE=100, CPU_SPEED=3, NUM_CPUS=1):
    TIEMPOS.clear() # Limpiar tiempos para cada nueva simulación
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    RAM = simpy.Container(env, init=RAM_SIZE, capacity= RAM_SIZE)
    CPU = simpy.Resource(env, capacity=NUM_CPUS)

    env.process(process_generator(env, num_processes, RAM, CPU, CPU_SPEED, INTERVAL))
    env.run()

    promedio = sum(TIEMPOS) / len(TIEMPOS) if TIEMPOS else 0
    deviation = desvest(TIEMPOS) if len(TIEMPOS) > 1 else 0
    return promedio, deviation

NUM_PROCESSES = [25, 50, 100, 150, 200] 
INTERVALS = [10, 5, 1]

# --------------- TAREAS ------------
def tarea1y2():
    print("Tarea 1 y 2: Baseline")
    plt.figure(figsize=(10, 6))
    for INTERVAL in INTERVALS:
        promedios = []
        for n in NUM_PROCESSES:
            promedio, deviation = correr_simulacion(n, INTERVAL)
            promedios.append(promedio)
            print(f"Tiempo promedio para {n} procesos con intervalo {INTERVAL}: {promedio:.2f}; Desviación estándar: {deviation:.2f}")
        plt.plot(NUM_PROCESSES, promedios, label=f"Intervalo {INTERVAL}")

    plt.xlabel("Número de Procesos")
    plt.ylabel("Tiempo Promedio")
    plt.title("Tiempo Promedio vs Número de Procesos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("graficas/tarea1y2.png")
    plt.show()

def tarea3a():
    print("\n===== TAREA 3a: RAM = 200 =====")
    plt.figure(figsize=(9, 5))

    for INTERVAL in INTERVALS:
        promedios = []
        for n in NUM_PROCESSES:
            prom, std = correr_simulacion(n, INTERVAL, RAM_SIZE=200)
            promedios.append(prom)
            print(f"  [{INTERVAL}] {n} procesos → promedio: {prom:.2f} | std: {std:.2f}")
        plt.plot(NUM_PROCESSES, promedios, marker='o', label=f"Intervalo {INTERVAL}")
    plt.xlabel("Número de Procesos")
    plt.ylabel("Tiempo Promedio")
    plt.title("Incrementar la memoria a 200: Tiempo Promedio vs Número de Procesos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("graficas/tarea3a.png")
    plt.show()

def tarea3b():
    print("\n===== TAREA 3b: CPU rápido (6 instrucciones) =====")
    plt.figure(figsize=(9, 5))

    for INTERVAL in INTERVALS:
        promedios = []
        for n in NUM_PROCESSES:
            prom, std = correr_simulacion(n, INTERVAL, CPU_SPEED=6)
            promedios.append(prom)
            print(f"  [{INTERVAL}] {n} procesos → promedio: {prom:.2f} | std: {std:.2f}")
        plt.plot(NUM_PROCESSES, promedios, marker='o', label=f"Intervalo {INTERVAL}")

    plt.xlabel("Número de Procesos")
    plt.ylabel("Tiempo Promedio")
    plt.title("CPU rápido (6 inst): Tiempo Promedio vs Número de Procesos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("graficas/tarea3b.png")
    plt.show()

def tarea_3c():
    print("\n===== TAREA 3c: 2 procesadore =====")
    plt.figure(figsize=(9, 5))

    for INTERVAL in INTERVALS:
        promedios = []
        for n in NUM_PROCESSES:
            prom, std = correr_simulacion(n, INTERVAL, NUM_CPUS=2)
            promedios.append(prom)
            print(f"  [{INTERVAL}] {n} procesos → promedio: {prom:.2f} | std: {std:.2f}")
        plt.plot(NUM_PROCESSES, promedios, marker='o', label=f"Intervalo {INTERVAL}")

    plt.xlabel("Número de Procesos")
    plt.ylabel("Tiempo Promedio")
    plt.title("2 CPUs: Tiempo Promedio vs Número de Procesos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("graficas/tarea3c.png")
    plt.show()

if __name__ == "__main__":
    tarea1y2()
    tarea3a()
    tarea3b()
    tarea_3c()