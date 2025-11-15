package org.example;
import java.util.concurrent.*;

public class Sem {
    static int count = 0;

    public static void main(String[] args) throws Exception {
        int T = 8;
        int I = 100000;

        ExecutorService pool = Executors.newFixedThreadPool(T);
        Runnable r = () -> {
            for (int i = 0; i < I; i++) {
                count++;
            }
        };

        long tComeco = System.currentTimeMillis();
        for (int i = 0; i < T; i++){
            pool.submit(r);
        }
        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.MINUTES);
        long tFim = System.currentTimeMillis();
        System.out.println("\nNumero Total de Threads: " + T);
        System.out.println("\nNumero Total de Incrementos: " + I);
        System.out.println("\nValor Esperado: " + T * I);
        System.out.println("\nValor Obtido: " + count);
        long tTot = tFim - tComeco;
        System.out.println("\nTempo Total: " + tTot + "ms");

    }
}
