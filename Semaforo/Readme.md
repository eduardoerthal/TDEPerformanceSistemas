TDE-3 — Performance Sistemas Ciberfisicos

Descrição do problema

O Jantar dos Filósofos é um exemplo clássico de sincronização que demonstra situações em que vários processos disputam recursos compartilhados.
Cinco filósofos estão sentados ao redor de uma mesa circular, e entre cada par existe um garfo. Para conseguir comer, cada filósofo precisa segurar simultaneamente os dois garfos ao seu lado: o da esquerda e o da direita.

Cada filósofo alterna entre três estados:

Pensando

Fome

Comendo (caso consiga pegar ambos os garfos)

Sem uma estratégia correta de controle de acesso, todos podem pegar apenas um garfo e ficar aguardando o outro indefinidamente, o que leva ao deadlock.

O que é um Deadlock (Impasse)

Deadlock é uma situação onde processos ficam bloqueados permanentemente, cada um esperando por um recurso que nunca será liberado.
Esse impasse só ocorre quando as quatro condições de Coffman estão presentes:

Exclusão mútua — cada recurso só pode ser utilizado por um processo por vez.

Manter e esperar — um processo mantém recursos já adquiridos enquanto aguarda outros.

Não-preempção — os recursos não podem ser retirados à força.

Espera circular — existe um ciclo fechado de processos, onde cada um espera pelo recurso do próximo.

No problema dos filósofos, o impasse surge exatamente por causa da espera circular.

Fome (Starvation)

Starvation acontece quando um processo nunca consegue avançar, mesmo que o sistema continue funcionando.
No jantar dos filósofos, isso pode ocorrer quando um filósofo tenta repetidamente pegar os garfos, mas sempre é ultrapassado pelos demais.

Solução adotada para o impasse

A solução usada segue o princípio de impor uma ordem global aos recursos:

Todos os garfos são numerados de 0 a 4.

Cada filósofo identifica seus dois garfos.

Em seguida, determina:

left = min(garfo_esquerda, garfo_direita)
right = max(garfo_esquerda, garfo_direita)


Cada filósofo sempre tenta adquirir primeiro o garfo de menor índice e só depois o de maior índice.

Pseudocódigo do protocolo
para cada filósofo p:
left  = menor índice entre seus dois garfos
right = maior índice entre seus dois garfos

    repetir para sempre:
        pensar()
        estado[p] <- "com fome"

        adquirir(left)
        adquirir(right)

        estado[p] <- "comendo"
        comer()

        liberar(right)
        liberar(left)

        estado[p] <- "pensando"

Prova da ausência de deadlock

A estratégia elimina a condição de espera circular, essencial para a ocorrência de deadlock.

Por que não há espera circular?

Como todos seguem a mesma regra (pegar primeiro o garfo de menor índice),

Nenhum filósofo pode estar segurando um garfo de número maior enquanto espera por um menor.

Assim, não existe como formar um ciclo de dependências.

Sem espera circular → deadlock impossível.

Considerações sobre a Fome (Starvation)

Embora o protocolo evite deadlock, ele não garante totalmente que nenhum filósofo passe fome.
Na prática, esse risco pode ser reduzido por estratégias como:

Semáforos configurados como justos: Semaphore(1, true)

Acesso aos garfos em ordem FIFO

Políticas de agendamento que favoreçam justiça

Com essas medidas, todos terão oportunidades de comer.

Conclusão
A realização do trabalho apresentou:

Os conceitos de deadlock e starvation

Uma solução que previne o impasse
