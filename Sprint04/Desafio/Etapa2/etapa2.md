# Etapa 2
### É possível reutilizar containers? Em caso positivo, apresente o comando necessário para reiniciar um dos containers parados em seu ambiente Docker? Não sendo possível, justifique sua resposta.

Sim, é possível realizar a reutilização de um container já executado e parado (por executável que chegou ao fim, ou para manual).

Para a criação de um container, utilizamos a seguinte sintaxe: `docker run nome-da-imagem `.

Para a verificação de container e seus status: `docker ps -a`.

E por fim, respondendo objetivamente a pergunta da etapa 2, para reutilizar um container, utilizamos `docker start nome-do-container`. No caso do exercício incluí da flag `-i`para que ficasse evidente a execução do script python, com o resultado à mostra.