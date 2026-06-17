import threading
import time
import sys
import faulthandler

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def thread1():
    log("Thread 1: tentando adquirir LOCK_A")
    LOCK_A.acquire()
    log("Thread 1: adquiriu LOCK_A")

    time.sleep(0.05)  # aumenta a chance do deadlock

    log("Thread 1: tentando adquirir LOCK_B")
    LOCK_B.acquire()
    log("Thread 1: adquiriu LOCK_B")

    log("T1 concluiu")
    LOCK_B.release()
    LOCK_A.release()


def thread2():
    log("Thread 2: tentando adquirir LOCK_B")
    LOCK_B.acquire()
    log("Thread 2: adquiriu LOCK_B")

    time.sleep(0.05)

    log("Thread 2: tentando adquirir LOCK_A")
    LOCK_A.acquire()
    log("Thread 2: adquiriu LOCK_A")

    log("T2 concluiu")
    LOCK_A.release()
    LOCK_B.release()


def main():
    TIMEOUT = 3.0  # segundos de espera antes de assumir deadlock e diagnosticar

    log("Iniciando reproducao do DEADLOCK (Thread 1: A->B ; Thread 2: B->A)")

    t1 = threading.Thread(target=thread1, name="Thread-1", daemon=True)
    t2 = threading.Thread(target=thread2, name="Thread-2", daemon=True)

    t1.start()
    t2.start()

    inicio = time.time()
    t1.join(timeout=TIMEOUT)
    restante = max(0.0, TIMEOUT - (time.time() - inicio))
    t2.join(timeout=restante)

    vivos = [t for t in (t1, t2) if t.is_alive()]
    if vivos:
        log("-" * 60)
        log(f"TIMEOUT de {TIMEOUT}s atingido: {len(vivos)} thread(s) ainda "
            f"bloqueada(s) -> DEADLOCK CONFIRMADO.")
        log(f"Threads travadas: {[t.name for t in vivos]}")
        log(f"threading.enumerate() no momento do travamento: "
            f"{[t.name for t in threading.enumerate()]}")
        log("Dump de pilha de cada thread (diagnostico tipo jstack):")
        faulthandler.dump_traceback(file=sys.stdout)
        log("-" * 60)
        log("O programa nao terminaria sozinho (threads travadas para "
            "sempre nos locks). Encerrando o processo manualmente para "
            "fins de demonstracao.")
        sys.exit(1)
    else:
        log("Ambas as threads terminaram sem deadlock nesta execucao "
            "(raro, mas possivel -- rode novamente para reproduzir o "
            "travamento).")


if __name__ == "__main__":
    main()
