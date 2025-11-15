package org.example;
public class Deadlock {
    static final Object LOCK_A = new Object();
    static final Object LOCK_B = new Object();

    public static void main(String[] args) {

        Thread t1 = new Thread(() -> {
            System.out.println("T1 está tentando pegar a Lock_A! ");
            synchronized (LOCK_A) {
                System.out.println("T1 pegou a Lock_A! ");
                dormir(50);
                System.out.println("T1 está tentando pegar a Lock_B! ");
                synchronized (LOCK_B) {
                    System.out.println("T1 concluiu");
                }
            }
        });

        Thread t2 = new Thread(() -> {
            System.out.println("T2 está tentando pegar a Lock_B! ");
            synchronized (LOCK_B) {
                System.out.println("T2 pegou a Lock_B! ");
                dormir(50);

                System.out.println("T2 tentando pegar a Lock_A! ");
                synchronized (LOCK_A) {
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
