
import java.util.concurrent.*;

public class ComSemaforo {
    static int count = 0;
    static final Semaphore sem = new Semaphore(1, true); // FIFO, justo

    public static void main(String[] args) throws Exception {
        int T = 8;
        int I = 100000;
        ExecutorService pool = Executors.newFixedThreadPool(T);
        Runnable r = () -> {
            for (int i = 0; i < M; i++) {
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

        long time = System.currentTimeMillis();
        for (int i = 0; i < I; i++) {
            pool.submit(r);
        }
        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.MINUTES);

        long tf =System.currentTimeMillis();
        System.out.println("Numero Total de Threads: " + T);
        System.out.println("\nNumero Total de Incrementos: " + I);
        System.out.println("\nValor Esperado: " + T * I);
        System.out.println("\nValor Obtido: " + count);
        long tt = tf - ti;
        System.out.println("\nTempo Total: " + tt + "ms!");
}

