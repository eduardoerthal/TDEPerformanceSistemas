import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def trabalho(nome_thread):
    log(f"{nome_thread}: tentando adquirir LOCK_A")
    LOCK_A.acquire()
    log(f"{nome_thread}: adquiriu LOCK_A")

    time.sleep(0.05)

    log(f"{nome_thread}: tentando adquirir LOCK_B")
    LOCK_B.acquire()
    log(f"{nome_thread}: adquiriu LOCK_B")

    log(f"{nome_thread} concluiu")

    LOCK_B.release()
    LOCK_A.release()


def main():
    log("Iniciando versao CORRIGIDA (Thread 1 e Thread 2: sempre A->B)")

    t1 = threading.Thread(target=trabalho, args=("Thread 1",), name="Thread-1")
    t2 = threading.Thread(target=trabalho, args=("Thread 2",), name="Thread-2")

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    log("-" * 60)
    log("Ambas as threads terminaram SEM DEADLOCK.")
    log("-" * 60)


if __name__ == "__main__":
    main()
