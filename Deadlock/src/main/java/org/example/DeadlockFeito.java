package org.example;

public class DeadlockFeito {
    static final Object LOCK_A = new Object();
    static final Object LOCK_B = new Object();

    public static void main(String[] args) {

        Thread t1 = new Thread(() -> {
            synchronized (LOCK_A) {
                dormir(50);
                synchronized (LOCK_B) {
                    System.out.println("T1 concluiu");
                }
            }
        });

        Thread t2 = new Thread(() -> {
            synchronized (LOCK_A) {
                dormir(50);
                synchronized (LOCK_B) {
                    System.out.println("T2 concluiu");
                }
            }
        });

        t1.start();
        t2.start();
    }

    static void dormir(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
