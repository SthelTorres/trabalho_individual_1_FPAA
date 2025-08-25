# trabalho_individual_1_FPAA
Este repositório contém a implementação do **algoritmo de Karatsuba** para multiplicação de inteiros grandes em **Python**, conforme o enunciado do trabalho. O código principal está em `main.py`.  

---

## 1) Descrição do Projeto (lógica linha a linha)

O arquivo `main.py` possui quatro funções principais: `_split_int`, `karatsuba`, `_self_test` e `_run_cli`.

### `_split_int(n, m)`
Divide `|n|` em duas partes na base `10**m`:
~~~python
base = 10 ** m
high, low = divmod(abs(n), base)
return high, low 
~~~
Usa divmod para obter quociente (high) e resto (low).
O sinal é tratado fora (a função trabalha com valor absoluto).
karatsuba(x, y, threshold_digits=16)

1- Validações:
~~~python
if not isinstance(x, int) or not isinstance(y, int):
    raise TypeError(...)
if not isinstance(threshold_digits, int):
    raise TypeError(...)
if threshold_digits < 1:
    raise ValueError(...)
~~~
Garante entradas inteiras e threshold_digits ≥ 1.

2- Sinal e casos-base:
~~~python
sign = -1 if (x < 0) ^ (y < 0) else 1
x, y = abs(x), abs(y)

if x == 0 or y == 0: return 0
if x < 10 or y < 10: return sign * (x * y)
~~~
Determina o sinal do resultado.
Retorna cedo para zero e para 1 dígito (multiplicação direta).

3- Contagem de dígitos e limiar:
~~~python
nx, ny = len(str(x)), len(str(y))
if nx <= threshold_digits and ny <= threshold_digits:
    return sign * (x * y)
~~~
Se ambos têm poucos dígitos, usa multiplicação direta (mais eficiente na prática).

4- Divisão e recursões de Karatsuba:
~~~python
m = max(1, max(nx, ny) // 2)
xh, xl = _split_int(x, m)
yh, yl = _split_int(y, m)

z2 = karatsuba(xh, yh, threshold_digits)
z0 = karatsuba(xl, yl, threshold_digits)
z1 = karatsuba(xh + xl, yh + yl, threshold_digits) - z2 - z0
~~~
Divide cada número em alto/baixo.
Calcula os três termos de Karatsuba: z2, z0 e z1

5- Recomposição:
~~~python
base_m = 10 ** m
result = (z2 * (base_m ** 2)) + (z1 * base_m) + z0
return sign * result
~~~
Retorna o produto combinando os termos.
_self_test()
Executa uma lista de testes válidos (compara com a*b) e inválidos (espera exceções para entradas erradas).
Útil para verificar rapidamente a correção.

_run_cli()
Modo terminal:
Sem argumentos → roda os testes internos.
python main.py x y → imprime x*y via Karatsuba.
python main.py x y threshold → idem, com limiar definido.

## 2) Como Executar o Projeto
Pré-requisitos:
Python 3.10+ instalado.

Passos:
### 1) Rodar os testes internos
python main.py

### 2) Executar uma multiplicação
python main.py 123456789 987654321

### 3) Executar com limiar definido (opcional)
python main.py 123456789 987654321 8

Observação: o threshold_digits não altera o resultado, apenas a estratégia (direta vs. recursiva). Em números muito grandes, pode afetar performance.

## 3) Relatório Técnico
### 3.1 Complexidade Ciclomática

Fluxo de controle da função karatsuba:
Entrada
Validações (tipos e threshold ≥ 1)
Tratamento de sinal
Caso-base zero
Caso-base 1 dígito
Checagem de limiar
Split em m dígitos (xh,xl,yh,yl)
Três chamadas recursivas (z2, z0, z1)
Recomposição e retorno

Contagem:
Nós (N) = 9
Arestas (E) = 11
Componentes (P) = 1

Complexidade ciclomática:
M = E − N + 2P = 11 − 9 + 2*1 = 4
Interpretação: 4 caminhos independentes — baixa complexidade, boa manutenibilidade.

Grafo (Mermaid):
flowchart TD

  A([Início]) --> B{Validações}
  
  B -- inválido --> X[[Erro]]
  
  B -- ok --> C[Tratar sinal]
  
  C --> D{x==0 or y==0?}
  
  D -- sim --> R0[return 0]
  
  D -- não --> E{x<10 or y<10?}
  
  E -- sim --> R1[return x*y]
  
  E -- não --> F{<= threshold?}
  
  F -- sim --> R2[return x*y]
  
  F -- não --> G[Divide em xh,xl,yh,yl]
  
  G --> H[z2 = K(xh,yh)]
  
  H --> I[z0 = K(xl,yl)]
  
  I --> J[z1 = K(xh+xl,yh+yl)-z2-z0]
  
  J --> K[Recomposição]
  
  K --> R[return resultado]
  

### 3.2 Análise Assintótica
Tempo
Recorrência:
T(n) = 3T(n/2) + O(n)

Pelo Teorema Mestre:
T(n) = O(n^log2(3)) ≈ O(n^1.585)

Melhor caso: números pequenos (caí no caso-base) → O(1).
Caso médio: O(n^1.585).
Pior caso: O(n^1.585).

Espaço
Profundidade da recursão: O(log n).
Inteiros grandes: O(n) dígitos.
Total: O(n + log n) ≈ O(n).

## 4) Testes
Os testes internos cobrem:
Casos pequenos, negativos e números muito grandes.
Validações: tipos inválidos e threshold_digits < 1 devem lançar exceção.
Para rodar:
python main.py

## 5) Conclusão
O algoritmo de Karatsuba foi implementado corretamente em Python, com testes que verificam tanto a correção quanto as regras de entrada. A documentação apresenta a lógica do código, o cálculo da complexidade ciclomática (com grafo) e a análise assintótica de tempo e espaço, atendendo integralmente ao que o professor solicitou.
