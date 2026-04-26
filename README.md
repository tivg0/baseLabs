# 🧪 labs2-starter-pack

Uma biblioteca Python desenvolvida para apoiar a análise de dados experimentais em laboratório, com ferramentas de regressão, visualização de gráficos e formatação de tabelas. Criada para ser usada em **Jupyter Notebooks**.

---

## 📁 Estrutura do Repositório

```
labs2-starter-pack/
│
├── base.py           # Módulo principal (re-exporta funções de functions.py, operations.py e plot.py)
├── functions.py      # Funções matemáticas para ajustes/regressões
├── operations.py     # Operações de dados, ajustes ODR e utilitários
├── plot.py           # Funções de visualização e análise gráfica
```

---

## 🚀 Como importar nos teus Notebooks Jupyter

Coloca os ficheiros do repositório na mesma pasta que o teu notebook `.ipynb`. Depois importa o módulo principal:

```python
import base as b
```

O módulo `base` agrega automaticamente todas as funções de `functions.py`, `operations.py` e `plot.py`, pelo que é o único import necessário para aceder a tudo.

Se quiseres importar os módulos individualmente:

```python
import functions as f
import operations as op
import plot as p
```

> **Nota:** Certifica-te de que tens instaladas as dependências necessárias:
> ```bash
> pip install numpy matplotlib scipy
> ```

---

## 📐 `functions.py` — Funções Matemáticas

Este ficheiro define as funções matemáticas utilizadas como modelos nos ajustes por regressão. São passadas como argumento a funções como `getAdjust`.

---

### `lin(coefs, x)`

Calcula uma função **linear**.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `coefs`   | `list` | Lista com 2 coeficientes: `[m, b]` |
| `x`       | `float` ou `array` | Valor(es) da variável independente |

**Output:** `coefs[0]*x + coefs[1]`

```python
b.lin([2, 1], 3)  # → 7
```

---

### `quadratic(coefs, x)`

Calcula uma função **quadrática**.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `coefs`   | `list` | Lista com 3 coeficientes: `[a, b, c]` |
| `x`       | `float` ou `array` | Valor(es) da variável independente |

**Output:** `coefs[0]*x² + coefs[1]*x + coefs[2]`

```python
b.quadratic([1, 0, -1], 3)  # → 8
```

---

### `polinomial(coefs, x)`

Calcula um **polinómio de grau arbitrário**.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `coefs`   | `list` | Lista com N coeficientes, do maior grau para o menor |
| `x`       | `float` ou `array` | Valor(es) da variável independente |

**Output:** Valor do polinómio em `x`.

> ⚠️ Nota: o grau mais alto calculado é `len(coefs)`, não `len(coefs)-1`. Confirma a convenção ao usar.

---

### `sin(x, A=1., omega=1., phi=0, c=0)`

Calcula uma função **sinusoidal** parametrizada.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x`       | `float` ou `array` | Variável independente |
| `A`       | `float` | Amplitude (default: 1) |
| `omega`   | `float` | Frequência angular (default: 1) |
| `phi`     | `float` | Fase (default: 0) |
| `c`       | `float` | Deslocamento vertical (default: 0) |

**Output:** `A * sin(omega*x + phi)`

---

### `cos(x, A=1., omega=1., phi=0, c=0)`

Calcula uma função **co-sinusoidal** parametrizada.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x`       | `float` ou `array` | Variável independente |
| `A`       | `float` | Amplitude (default: 1) |
| `omega`   | `float` | Frequência angular (default: 1) |
| `phi`     | `float` | Fase (default: 0) |
| `c`       | `float` | Deslocamento vertical (default: 0) |

**Output:** `A * cos(omega*x + phi)`

---

### `log(x, A=1, fac=0, c1=0, c2=0)`

Calcula uma função **logarítmica** parametrizada.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x`       | `float` ou `array` | Variável independente |
| `A`       | `float` | Fator multiplicativo (default: 1) |
| `fac`     | `float` | Fator interno do logaritmo (default: 0) |
| `c1`      | `float` | Constante aditiva interna (default: 0) |
| `c2`      | `float` | Constante aditiva externa (default: 0) |

**Output:** `A * log(fac*x + c1) + c2`

---

### `exp(x, A=1, fac=1, c1=0, c2=0)`

Calcula uma função **exponencial** parametrizada.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x`       | `float` ou `array` | Variável independente |
| `A`       | `float` | Fator multiplicativo (default: 1) |
| `fac`     | `float` | Fator do expoente (default: 1) |
| `c1`      | `float` | Constante aditiva no expoente (default: 0) |
| `c2`      | `float` | Constante aditiva externa (default: 0) |

**Output:** `A * exp(fac*x + c1) + c2`

---

## ⚙️ `operations.py` — Operações e Utilitários

Este ficheiro contém as funções de tratamento de dados, ajuste por ODR e formatação de resultados.

---

### `getTable(columns, data, title, firstcolumnShade, size)`

Gera e exibe uma **tabela formatada** visualmente usando `matplotlib`, com cabeçalhos a azul, linhas alternadas e opção de sombreado na primeira coluna.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `columns` | `list[str]` | Nomes das colunas (cabeçalhos) |
| `data`    | `list[list]` | Dados da tabela: lista de linhas, cada uma com valores correspondentes às colunas |
| `title`   | `str` | Título a apresentar por cima da tabela |
| `firstcolumnShade` | `bool` | Se `True`, a primeira coluna é sombreada a cinza e negrito |
| `size`    | `tuple` | Tamanho da figura em polegadas, ex: `(10, 4)` |

**Output:** Exibe a tabela diretamente (sem valor de retorno).

```python
b.getTable(
    columns=["Grandeza", "Valor", "Incerteza"],
    data=[
        ["Massa (kg)", "1.234", "0.002"],
        ["Comprimento (m)", "0.567", "0.001"],
    ],
    title="Medições Experimentais",
    firstcolumnShade=True,
    size=(10, 3)
)
```

**Estilo gerado:**
- Cabeçalhos com fundo **azul** e texto branco a bold
- Linhas alternadas entre **branco** e **cinza claro**
- Primeira coluna opcional em **cinza escuro** e bold
- Fonte de tamanho 12, células escaladas para boa legibilidade

---

## 📊 `plot.py` — Visualização e Análise Gráfica

Este ficheiro contém as funções de alto nível para gerar gráficos de regressão, análise de resíduos e comparação de múltiplos datasets. Todas usam internamente `b.getAdjust` para o ajuste ODR.

---

### `plotLinReg(xs, ys, xerr, yerr, title, xlabel, ylabel)`

Plota um **gráfico de regressão linear simples** com barras de erro.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `xs`      | `array` | Valores de x |
| `ys`      | `array` | Valores de y |
| `xerr`    | `float` ou `array` | Incerteza(s) em x |
| `yerr`    | `float` ou `array` | Incerteza(s) em y |
| `title`   | `str` | Título do gráfico |
| `xlabel`  | `str` | Rótulo do eixo x (suporta LaTeX) |
| `ylabel`  | `str` | Rótulo do eixo y (suporta LaTeX) |

**Output:** Exibe o gráfico e devolve o objeto `adjust` (resultado do ajuste ODR com `adjust.beta` e `adjust.sd_beta`).

```python
adjust = b.plotLinReg(xs, ys, xerr, yerr, "Título", "x (m)", "y (s)")
print(adjust.beta)      # [m, b] — coeficientes do ajuste
print(adjust.sd_beta)   # incertezas associadas
```

---

### `plotQuadReg(xs, ys, xerr, yerr, title, xlabel, ylabel)`

Plota um **gráfico de regressão quadrática** com barras de erro.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `xs`      | `array` | Valores de x |
| `ys`      | `array` | Valores de y |
| `xerr`    | `float` ou `array` | Incerteza(s) em x |
| `yerr`    | `float` ou `array` | Incerteza(s) em y |
| `title`   | `str` | Título do gráfico |
| `xlabel`  | `str` | Rótulo do eixo x |
| `ylabel`  | `str` | Rótulo do eixo y |

**Output:** Exibe o gráfico e devolve o objeto `adjust`.

```python
adjust = b.plotQuadReg(xs, ys, xerr, yerr, "Título", "x (m)", "y (m/s²)")
```

---

### `plotFinal(x1, y1, xres, yres, xerr1, yerr1, title, xlabel, ylabel, beta0=[1,1], xscale='linear', yscale='linear')`

Plota um **gráfico de regressão linear** distinguindo visualmente os **pontos aceites** (preto) dos **pontos rejeitados** (vermelho). Usado internamente por `fullLinAnalysis`.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x1`, `y1` | `array` | Pontos experimentais aceites |
| `xres`, `yres` | `array` | Pontos experimentais rejeitados (pode ser vazio `[]`) |
| `xerr1`, `yerr1` | `array` | Incertezas dos pontos aceites |
| `title`   | `str` | Título (renderizado como LaTeX) |
| `xlabel`, `ylabel` | `str` | Rótulos dos eixos (renderizados como LaTeX) |
| `beta0`   | `list` | Estimativa inicial dos coeficientes (default: `[1,1]`) |
| `xscale`, `yscale` | `str` | Escala dos eixos: `'linear'` ou `'log'` |

**Output:** Exibe o gráfico e devolve o objeto `adjust`.

---

### `finalResidues(xTrue, yTrue, xFalse, yFalse, adjust, stdy, xlabel, ylabel)`

Plota o **gráfico de resíduos** de uma regressão linear, com linhas horizontais a delimitar o intervalo de aceitação.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `xTrue`, `yTrue` | `array` | Pontos aceites |
| `xFalse`, `yFalse` | `array` | Pontos rejeitados |
| `adjust`  | objeto ODR | Resultado do ajuste (com `adjust.beta`) |
| `stdy`    | `float` | Limite do desvio padrão para aceitação |
| `xlabel`, `ylabel` | `str` | Rótulos dos eixos (renderizados como LaTeX) |

**Output:** Exibe o gráfico de resíduos (sem valor de retorno).

---

### `fullLinAnalysis(x, y, xerr, yerr, title, xlabel, ylabel, beta0=[1,1], tol=1, xscale='linear', yscale='linear')`

Realiza uma **análise linear completa** de forma automática: faz o ajuste, calcula os resíduos, rejeita pontos fora do intervalo de tolerância e exibe tanto o gráfico de regressão como o de resíduos.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x`, `y`  | `array` | Dados experimentais |
| `xerr`, `yerr` | `float` ou `array` | Incertezas (valor único ou array) |
| `title`   | `str` | Título do gráfico |
| `xlabel`, `ylabel` | `str` | Rótulos dos eixos |
| `beta0`   | `list` | Estimativa inicial dos coeficientes (default: `[1,1]`) |
| `tol`     | `float` | Tolerância em número de desvios padrão para rejeição de pontos (default: `1`) |
| `xscale`, `yscale` | `str` | Escala dos eixos: `'linear'` ou `'log'` |

**Output:** Exibe gráfico de regressão + gráfico de resíduos e devolve o objeto `adjust` final (apenas com pontos aceites).

```python
adjust = b.fullLinAnalysis(
    x, y, 0.01, yerr,
    title=r"Posição\ vs\ Tempo",
    xlabel=r"t\ (s)",
    ylabel=r"x\ (m)",
    tol=1.5
)
```

---

### `plotColumnFullLinReg(xs, ys, xerrs, yerrs, titles, xlabels, ylabels, beta0=[1,1], tol=1)`

Plota **múltiplos gráficos em coluna** (regressão + resíduos por linha), um conjunto de dados por linha. Ideal para comparar várias experiências de forma compacta.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `xs`, `ys` | `list[array]` | Lista de arrays de dados |
| `xerrs`, `yerrs` | `list` | Lista de incertezas (float ou array por dataset) |
| `titles`  | `list[str]` | Títulos de cada gráfico |
| `xlabels`, `ylabels` | `str` ou `list[str]` | Rótulos (um único aplicado a todos, ou lista) |
| `beta0`   | `list` | Estimativa inicial dos coeficientes |
| `tol`     | `float` | Tolerância para rejeição de pontos |

**Output:** Exibe a figura com todos os gráficos e devolve uma `list` com os objetos `adjust` de cada dataset.

```python
adjusts = b.plotColumnFullLinReg(
    xs=[x1, x2], ys=[y1, y2],
    xerrs=[xerr1, xerr2], yerrs=[yerr1, yerr2],
    titles=["Exp 1", "Exp 2"],
    xlabels=r"t\ (s)", ylabels=r"x\ (m)"
)
```

---

### `plotMultipleReg(xs, ys, xerrs, yerrs, title, xlabel, ylabel, colors, legends="Pontos Experimentais", tol=1, beta0=[1,1], xscale='linear', yscale='linear')`

Plota **múltiplos datasets no mesmo gráfico**, cada um com a sua regressão linear e cor distinta.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `xs`, `ys` | `list[array]` | Lista de arrays de dados |
| `xerrs`, `yerrs` | `float` ou `list` | Incertezas (valor único para todos ou lista) |
| `title`   | `str` | Título do gráfico |
| `xlabel`, `ylabel` | `str` | Rótulos dos eixos |
| `colors`  | `list[str]` | Lista de cores (uma por dataset), ex: `["blue","red"]` |
| `legends` | `list[str]` | Legenda de cada dataset (default: `"Pontos Experimentais"` para todos) |
| `tol`     | `float` | Tolerância para rejeição de pontos (default: `1`) |
| `beta0`   | `list` | Estimativa inicial dos coeficientes |
| `xscale`, `yscale` | `str` | Escala dos eixos |

**Output:** Exibe o gráfico e devolve um `array` com os objetos `adjust` de cada dataset.

```python
regs = b.plotMultipleReg(
    xs=[x1, x2], ys=[y1, y2],
    xerrs=0.01, yerrs=0.05,
    title="Comparação",
    xlabel=r"T\ (K)", ylabel=r"P\ (Pa)",
    colors=["blue", "red"],
    legends=["Amostra A", "Amostra B"]
)
```

---

### `plotColumnReg(xs, ys, xerrs, yerrs, titles, xlabels, ylabels, func, beta0=[1,1], tol=1)`

Semelhante a `plotColumnFullLinReg`, mas aceita **qualquer função de ajuste** (não apenas linear). Usa `func` como modelo de regressão.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `xs`, `ys` | `list[array]` | Lista de arrays de dados |
| `xerrs`, `yerrs` | `list` | Incertezas por dataset |
| `titles`  | `list[str]` | Títulos de cada gráfico |
| `xlabels`, `ylabels` | `str` ou `list[str]` | Rótulos dos eixos |
| `func`    | `callable` | Função de ajuste a usar como modelo (ex: `b.quadratic`) |
| `beta0`   | `list` | Estimativa inicial dos coeficientes |
| `tol`     | `float` | Tolerância para rejeição de pontos |

**Output:** Exibe a figura em coluna e devolve uma `list` com os objetos `adjust` de cada dataset.

```python
adjusts = b.plotColumnReg(
    xs=[x1, x2], ys=[y1, y2],
    xerrs=[xerr1, xerr2], yerrs=[yerr1, yerr2],
    titles=["Exp 1", "Exp 2"],
    xlabels=r"x\ (m)", ylabels=r"E\ (J)",
    func=b.quadratic,
    beta0=[1, 1, 0]
)
```

---

## 🔩 Funções Auxiliares

Para além das funções principais descritas acima, existem várias **funções auxiliares** utilizadas internamente que podem ser exploradas diretamente para casos de uso mais avançados. Encontram-se em `operations.py` e incluem, entre outras:

- `getAdjust` — ajuste ODR genérico com qualquer modelo
- `getData` — leitura de ficheiros de dados com separador tab
- `getPolynomialLabel` / `getPolynomialLabel2` — formatação de equações em LaTeX para legendas
- `round_un` — arredondamento de valores à ordem da incerteza
- `getUncertainty` / `getSignAlg` — tratamento de algarismos significativos e incertezas
- `handleCientNot` — formatação de notação científica para LaTeX
- `derivativePolinomialCoefs` — derivada de um polinómio pelos seus coeficientes

Estas funções estão disponíveis via `import base as b` e podem ser consultadas diretamente no código fonte de `operations.py`.

---

## 📝 Notas Gerais

- Os rótulos `xlabel` e `ylabel` suportam **LaTeX** (são renderizados com `rf"$...$"`). Usa `\` para comandos LaTeX, ex: `r"t\ (s)"`, `r"\lambda\ (nm)"`.
- O parâmetro `beta0` deve ter tantos elementos quantos os coeficientes da função usada (`[1,1]` para linear, `[1,1,1]` para quadrática, etc.).
- Os objetos `adjust` devolvidos pelas funções de plot são resultados do **SciPy ODR** e contêm, entre outros:
  - `adjust.beta` — coeficientes ajustados
  - `adjust.sd_beta` — incertezas dos coeficientes
