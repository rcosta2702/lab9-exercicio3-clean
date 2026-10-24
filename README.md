# Exercicio 3 - Clean Architecture e DIP

O dominio fica em `models`. Os casos de uso e a implementacao da persistencia
ficam diretamente na raiz deste exercicio. Todos os casos de uso dependem da
abstracao `IContaRepository`; somente o `main.py` escolhe o adaptador de arquivo TXT.

Os dados sao salvos em `contas.txt`, na raiz do exercicio. Execute `python main.py`.
