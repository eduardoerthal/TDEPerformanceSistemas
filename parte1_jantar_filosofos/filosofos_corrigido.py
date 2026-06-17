import threading
import time
import argparse

N = 5  # numero de filosofos

garfos = [threading.Lock() for _ in range(N)]

estado = ["pensando"] * N
estado_lock = threading.Lock()

# Contador de quantas vezes cada filosofo comeu, para demonstrar justica
refeicoes = [0] * N
refeicoes_lock = threading.Lock()


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def set_estado(i, novo_estado):
    with estado_lock:
        estado[i] = novo_estado
    log(f"Filosofo {i}: {novo_estado}")


def filosofo_corrigido(i, repeticoes):
    garfo_esquerda = i
    garfo_direita = (i + 1) % N

    # Hierarquia de recursos: define qual garfo e "left" (menor indice,
    # pedido primeiro) e qual e "right" (maior indice, pedido depois),
    # independente da posicao fisica esquerda/direita do filosofo.
    primeiro = min(garfo_esquerda, garfo_direita)
    segundo = max(garfo_esquerda, garfo_direita)

    for rodada in range(repeticoes):
        set_estado(i, "pensando")
        time.sleep(0.05)

        set_estado(i, "com fome")

        log(f"Filosofo {i} tentando pegar garfo de MENOR indice ({primeiro})")
        garfos[primeiro].acquire()
        log(f"Filosofo {i} pegou garfo de MENOR indice ({primeiro})")

        time.sleep(0.1)

        log(f"Filosofo {i} tentando pegar garfo de MAIOR indice ({segundo})")
        garfos[segundo].acquire()
        log(f"Filosofo {i} pegou garfo de MAIOR indice ({segundo})")

        set_estado(i, "comendo")
        with refeicoes_lock:
            refeicoes[i] += 1
        time.sleep(0.05)

        garfos[segundo].release()
        garfos[primeiro].release()

    log(f"Filosofo {i} terminou todas as rodadas.")


def main():
    parser = argparse.ArgumentParser(
        description="Jantar dos Filosofos - versao corrigida (hierarquia de recursos)"
    )
    parser.add_argument(
        "--repeticoes", type=int, default=5,
        help="Quantas vezes cada filosofo tenta comer (default: 5)"
    )
    args = parser.parse_args()

    log("Iniciando simulacao CORRIGIDA do Jantar dos Filosofos (hierarquia de recursos).")

    threads = []
    for i in range(N):
        t = threading.Thread(target=filosofo_corrigido, args=(i, args.repeticoes))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    log("=" * 60)
    log("Todas as threads terminaram SEM DEADLOCK.")
    log("Numero de refeicoes por filosofo (deve ser igual para todos, "
        "evidenciando justica/ausencia de inanicao):")
    for i, r in enumerate(refeicoes):
        log(f"  Filosofo {i}: {r} refeicao(oes)")
    log("=" * 60)


if __name__ == "__main__":
    main()
