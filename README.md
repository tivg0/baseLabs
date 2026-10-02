# 🧪 labs2-starter-pack

Uma biblioteca Python desenvolvida para apoiar a análise de dados experimentais em laboratório, com ferramentas de regressão, visualização de gráficos e formatação de tabelas. Criada para ser usada em **Jupyter Notebooks**.

---

## 📁 Estrutura do Repositório

```
labs2-starter-pack/
│
├── __init__.py      # Módulo principal (re-exporta DataSet, functions.py, operations.py e plot.py)
├── dataset.py       # Classe DataSet para gestão de dados, rótulos e ajustes automáticos
├── functions.py     # Funções matemáticas para ajustes/regressões
├── operations.py    # Operações de dados, ajustes ODR e utilitários
├── plot.py          # Funções de visualização e análise gráfica
```

---

## 🚀 Como importar nos teus Notebooks Jupyter

Coloca os ficheiros do repositório na mesma pasta que o teu notebook `.ipynb`. Depois importa o módulo principal:

```python
from baseLabs import *
```

---

## 📦 `dataset.py` — Classe `DataSet`

A classe `DataSet` encapsula os dados experimentais, incertezas, títulos, rótulos de eixos e o tipo de ajuste a realizar. Ao ser instanciada, **os parâmetros do ajuste são automaticamente calculados** através de SciPy ODR e guardados no atributo `adjust`.

### Assinatura do Construtor

```python
DataSet(x, y, ux, uy, titulo, labelx, labely, fit_type=lin)
```

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x`, `y`  | `list` ou `array` | Dados experimentais (variáveis independente e dependente) |
| `ux`, `uy` | `float` ou `array` | Incertezas experimentais em x e y |
| `titulo`  | `str` | Título do gráfico |
| `labelx`  | `str` | Rótulo do eixo X |
| `labely`  | `str` | Rótulo do eixo Y |
| `fit_type`| `function` | Função modelo de ajuste (default: `lin` de `functions.py`) |

### Atributos Principais

- `ds.x`, `ds.y`: Arrays NumPy dos dados.
- `ds.ux`, `ds.uy`: Arrays NumPy das incertezas (escalares são expandidos automaticamente).
- `ds.titulo`, `ds.labelx`, `ds.labely`: Rótulos e título.
- `ds.fit_type`: Função utilizada no ajuste (ex: `lin`, `quadratic`).
- `ds.adjust`: Objeto de output retornado pelo SciPy ODR (`odr.run()`), contendo `ds.adjust.beta` e `ds.adjust.sd_beta`.

### Exemplo de Criação

```python
ds = DataSet(
    x=[1, 2, 3, 4, 5],
    y=[2.1, 3.9, 6.1, 8.2, 9.8],
    ux=0.1,
    uy=0.2,
    titulo="Posição em Função do Tempo",
    labelx="t (s)",
    labely="x (m)",
    fit_type=lin
)

# Acesso direto ao ajuste pré-calculado:
print("Declive e ordenada na origem:", ds.adjust.beta)
```

---

## 📐 `functions.py` — Funções Matemáticas

Este ficheiro define as funções matemáticas utilizadas como modelos nos ajustes por regressão.

### `lin(coefs, x)`
Calcula uma função **linear** (`coefs[0]*x + coefs[1]`).

### `quadratic(coefs, x)`
Calcula uma função **quadrática** (`coefs[0]*x² + coefs[1]*x + coefs[2]`).

---

## ⚙️ `operations.py` — Operações e Utilitários

Ficheiro contendo ferramentas de tratamento de dados e utilitários ODR:

- `getAdjust(dataset)` — Retorna o ajuste do objeto `DataSet` (ou executa ODR para dados genéricos).
- `getSignAlg(dataset)` — Tratamento de algarismos significativos e arredondamento de dados/incertezas.
- `getTable(columns, data, title, firstcolumnShade, size)` — Exibe tabelas formatadas com `matplotlib`.

---

## 📊 `plot.py` — Visualização e Análise Gráfica

Todas as funções de gráfico recebem agora objetos `DataSet` (ou listas de `DataSet`).

### `plot(dataset, label="Dados", color="black", hlines=None)`
Gera um gráfico simples com pontos e barras de erro a partir de um `DataSet`.

### `plotLinReg(dataset)` / `plotQuadReg(dataset)`
Exibe o gráfico dos pontos experimentais e a curva de regressão associada ao `DataSet`.

### `fullLinAnalysis(dataset, separate=True, tol=1, xscale='linear', yscale='linear', s=5)`
Realiza uma análise completa: exibe a regressão, filtra resíduos com base na tolerância `tol` (desvios padrão) e apresenta o gráfico de resíduos.

```python
adjust_final = fullLinAnalysis(ds, separate=False, tol=1.5)
```

### `plotColumnFullLinReg(datasets, tol=1)`
Plota múltiplos conjuntos de dados (uma lista de `DataSet`) em formato de colunas (regressão + resíduos por linha).

```python
adjusts = plotColumnFullLinReg([ds1, ds2], tol=1)
```

### `plotMultipleReg(datasets, colors, legends="Pontos Experimentais", regressions=False, errorbars=True)`
Sobrepõe múltiplos `DataSet` no mesmo gráfico com cores e legendas personalizadas.

```python
regs = plotMultipleReg(
    datasets=[ds1, ds2],
    colors=["black", "blue"],
    legends=["Amostra 1", "Amostra 2"],
    regressions=True
)
```
