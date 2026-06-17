import threading
import time
import argparse


def _ler(contador):
    return contador["valor"]


def _escrever(contador, novo_valor):
    contador["valor"] = novo_valor


def tarefa_sem_sincronizacao(contador, M):
    for _ in range(M):
        # Operacao NAO atomica, decomposta explicitamente em 3 passos
        # (ler, somar, escrever) com uma pequena janela de tempo entre
        # leitura e escrita. Essa janela e o que torna a corrida
        # observavel sob o GIL do CPython: ela aumenta a chance de
        # outra thread ler o MESMO valor antigo antes da escrita
        # acontecer, fazendo um incremento "desaparecer".
        valor_atual = _ler(contador)
        novo_valor = valor_atual + 1
        # Janela deliberada entre calculo e escrita (sem isso, o
        # GIL do CPython raramente troca de thread no meio de um
        # "count = count + 1" simples, mascarando a corrida).
        time.sleep(0)
        _escrever(contador, novo_valor)


def tarefa_com_semaforo(contador, M, sem):
    for _ in range(M):
        sem.acquire()
        try:
            valor_atual = _ler(contador)
            novo_valor = valor_atual + 1
            time.sleep(0)
            _escrever(contador, novo_valor)
        finally:
            sem.release()


def executar_versao(nome, func_tarefa, T, M, *extra_args):
    contador = {"valor": 0}
    threads = []

    inicio = time.perf_counter()
    for _ in range(T):
        t = threading.Thread(target=func_tarefa, args=(contador, M, *extra_args))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    fim = time.perf_counter()

    esperado = T * M
    obtido = contador["valor"]
    tempo = fim - inicio

    print(f"[{nome}] esperado={esperado}  obtido={obtido}  "
          f"tempo={tempo:.4f}s  incrementos_perdidos={esperado - obtido}")

    return esperado, obtido, tempo


def main():
    parser = argparse.ArgumentParser(description="Contador concorrente: race condition vs semaforo")
    parser.add_argument("--threads", "-t", type=int, default=8,
                         help="Numero de threads T (default: 8)")
    parser.add_argument("--incrementos", "-m", type=int, default=5_000,
                         help="Incrementos por thread M (default: 5000). "
                              "NOTA: o enunciado sugere M >= 200000 como "
                              "parametro generico, mas em CPython, com o "
                              "GIL, 'count = count + 1' simples raramente "
                              "troca de contexto no meio, mascarando a "
                              "corrida mesmo com M alto. Por isso, para "
                              "TORNAR A CORRIDA OBSERVAVEL em Python, "
                              "introduzimos deliberadamente uma janela "
                              "(time.sleep(0)) entre leitura e escrita, "
                              "conforme o proprio enunciado recomenda "
                              "('ajuste conforme a linguagem'). Com essa "
                              "janela, M=5000 e suficiente para evidenciar "
                              "milhares de incrementos perdidos sem tornar "
                              "a execucao excessivamente longa.")
    parser.add_argument("--execucoes", "-n", type=int, default=3,
                         help="Quantas vezes repetir cada versao (default: 3)")
    args = parser.parse_args()

    T, M = args.threads, args.incrementos

    print("=" * 70)
    print(f"Parametros: T={T} threads, M={M} incrementos/thread, "
          f"esperado=T*M={T * M}")
    print("=" * 70)

    print("\n--- VERSAO 1: SEM SINCRONIZACAO (condicao de corrida) ---")
    resultados_sem = []
    for i in range(args.execucoes):
        print(f"Execucao {i + 1}/{args.execucoes}:")
        resultados_sem.append(executar_versao("SEM SINCRONIZACAO", tarefa_sem_sincronizacao, T, M))

    print("\n--- VERSAO 2: COM SEMAFORO BINARIO (correta) ---")
    resultados_com = []
    for i in range(args.execucoes):
        sem = threading.Semaphore(1)
        print(f"Execucao {i + 1}/{args.execucoes}:")
        resultados_com.append(executar_versao("COM SEMAFORO", tarefa_com_semaforo, T, M, sem))
    print(f"{'Versao':<20}{'Execucao':<10}{'Esperado':<12}{'Obtido':<12}{'Tempo (s)':<10}")
    for idx, (esperado, obtido, tempo) in enumerate(resultados_sem, start=1):
        print(f"{'Sem sincronizacao':<20}{idx:<10}{esperado:<12}{obtido:<12}{tempo:<10.4f}")
    for idx, (esperado, obtido, tempo) in enumerate(resultados_com, start=1):
        print(f"{'Com semaforo':<20}{idx:<10}{esperado:<12}{obtido:<12}{tempo:<10.4f}")


if __name__ == "__main__":
    main()