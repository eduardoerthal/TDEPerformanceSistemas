package org.example;

import java.util.concurrent.*;

public class Com {
    static int count = 0;
    static final Semaphore sem = new Semaphore(1, true); // FIFO, justo

    public static void main(String[] args) throws Exception {
        int T = 8;        // número de threads
        int I = 100000;   // número de incrementos por thread

        ExecutorService pool = Executors.newFixedThreadPool(T);

        Runnable r = () -> {
            for (int i = 0; i < I; i++) {
                try {
                    sem.acquire();
                    count++;
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    sem.release();
                }
            }
        };

        long tInicio = System.currentTimeMillis();

        for (int i = 0; i < T; i++) {
            pool.submit(r);
        }

        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.MINUTES);

        long tf = System.currentTimeMillis();

        System.out.println("\nNumero Total de Threads: " + T);
        System.out.println("Numero Total de Incrementos por thread: " + I);
        System.out.println("Valor Esperado: " + (T * I));
        System.out.println("Valor Obtido: " + count);

        long tt = tf - tInicio;
        System.out.println("Tempo Total: " + tt + " ms");
    }
}
