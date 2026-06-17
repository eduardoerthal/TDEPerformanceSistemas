import threading
import time
import sys
import argparse
import faulthandler

N = 5  # numero de filosofos

# Um Lock por garfo. garfo[i] fica entre o filosofo i e o filosofo (i+1) % N
garfos = [threading.Lock() for _ in range(N)]

# Apenas para logging do estado de cada filosofo
estado = ["pensando"] * N
estado_lock = threading.Lock()


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def set_estado(i, novo_estado):
    with estado_lock:
        estado[i] = novo_estado
    log(f"Filosofo {i}: {novo_estado}")


def filosofo_ingenuo(i, repeticoes):
    garfo_esquerda = i
    garfo_direita = (i + 1) % N

    for rodada in range(repeticoes):
        set_estado(i, "pensando")
        time.sleep(0.05)

        set_estado(i, "com fome")

        # Protocolo ingenuo: sempre pega primeiro o da esquerda, depois o da direita
        log(f"Filosofo {i} tentando pegar garfo da ESQUERDA ({garfo_esquerda})")
        garfos[garfo_esquerda].acquire()
        log(f"Filosofo {i} pegou garfo da ESQUERDA ({garfo_esquerda})")

        # Pausa para aumentar a chance de todos os filosofos 
        # pegarem o garfo da esquerda antes de qualquer um tentar o da direita,
        # o que favorece a ocorrencia do deadlock.
        time.sleep(0.1)

        log(f"Filosofo {i} tentando pegar garfo da DIREITA ({garfo_direita})")
        garfos[garfo_direita].acquire()
        log(f"Filosofo {i} pegou garfo da DIREITA ({garfo_direita})")

        set_estado(i, "comendo")
        time.sleep(0.05)

        garfos[garfo_direita].release()
        garfos[garfo_esquerda].release()

    log(f"Filosofo {i} terminou todas as rodadas.")


def main():
    parser = argparse.ArgumentParser(
        description="Jantar dos Filosofos - versao ingenua (pode causar deadlock)"
    )
    parser.add_argument(
        "--repeticoes", type=int, default=3,
        help="Quantas vezes cada filosofo tenta comer (default: 3)"
    )
    parser.add_argument(
        "--timeout", type=float, default=5.0,
        help="Segundos a esperar antes de assumir deadlock e abortar (default: 5.0)"
    )
    args = parser.parse_args()

    log("Iniciando simulacao INGENUA do Jantar dos Filosofos.")
    log("Esperado: alta probabilidade de DEADLOCK (programa pode nao terminar).")

    threads = []
    for i in range(N):
        t = threading.Thread(
            target=filosofo_ingenuo, args=(i, args.repeticoes), daemon=True
        )
        threads.append(t)
        t.start()

    inicio = time.time()
    for t in threads:
        restante = args.timeout - (time.time() - inicio)
        if restante <= 0:
            break
        t.join(timeout=restante)

    vivos = [t for t in threads if t.is_alive()]
    if vivos:
        log("=" * 60)
        log(f"TIMEOUT de {args.timeout}s atingido: {len(vivos)} thread(s) "
            f"ainda bloqueada(s) -> DEADLOCK CONFIRMADO.")
        log("Estado final de cada filosofo no momento do travamento:")
        with estado_lock:
            for i, e in enumerate(estado):
                log(f"  Filosofo {i}: {e}")
        log("Dump de threads (semelhante a um 'thread dump' / jstack):")
        faulthandler.dump_traceback(file=sys.stdout)
        log("=" * 60)
        log("Encerrando o processo (as threads travadas sao 'daemon' e "
            "serao descartadas).")
        sys.exit(1)
    else:
        log("Todas as threads terminaram sem deadlock nesta execucao "
            "(pode acontecer ocasionalmente devido ao escalonamento -- "
            "rode novamente para reproduzir o travamento).")


if __name__ == "__main__":
    main()
