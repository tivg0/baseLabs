# 🧪 baseLabs

Uma biblioteca em Python desenvolvida para apoiar a análise de dados experimentais em laboratório, oferecendo ferramentas de gestão de dados, regressão (ODR), visualização de gráficos e análise de resíduos. Desenhada para uso direto em **Jupyter Notebooks**.

---

## 🚀 Importação nos Notebooks

Coloca a pasta `baseLabs` no mesmo diretório que o teu notebook `.ipynb` e importa a biblioteca:

```python
from baseLabs import *
```

*(Nota: Os ficheiros adicionais do módulo, como `functions.py` e `operations.py`, contêm funções matemáticas e auxiliares de suporte).*

---

## 📦 Mecânica da Classe `DataSet` (`dataset.py`)

A classe `DataSet` (com o alias `Dataset`) é a estrutura central de dados. Encapsula os dados experimentais, incertezas, títulos, rótulos de eixos e o modelo de ajuste a aplicar.

### ⚙️ Cálculo Automático de Ajuste
Ao instanciar um objeto `DataSet`, o ajuste por **SciPy ODR (Orthogonal Distance Regression)** é executado **automaticamente** considerando as incertezas em $x$ (`ux`) e em $y$ (`uy`). O resultado fica imediatamente acessível através do atributo `.adjust`.

### Assinatura do Construtor

```python
DataSet(x, y, ux, uy, titulo, labelx, labely, fit_type=lin, beta0=None)
```

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `x`, `y` | `list` ou `array` | Valores experimentais das variáveis |
| `ux`, `uy` | `float` ou `array` | Incertezas experimentais em $x$ e $y$ (escalares são expandidos automaticamente) |
| `titulo` | `str` | Título principal do gráfico |
| `labelx` | `str` | Rótulo do eixo X (ex: `"t (s)"`) |
| `labely` | `str` | Rótulo do eixo Y (ex: `"x (m)"`) |
| `fit_type` | `function` | Função modelo de ajuste (padrão: `lin` de `functions.py`) |
| `beta0` | `list` (opcional) | Estimativa inicial de parâmetros para o ODR |

### Principais Atributos
- `ds.x`, `ds.y`: Arrays NumPy com os dados experimentais.
- `ds.ux`, `ds.uy`: Arrays NumPy com as incertezas experimentais.
- `ds.titulo`, `ds.labelx`, `ds.labely`: Rótulos e títulos.
- `ds.fit_type`: Função modelo usada no ajuste.
- `ds.adjust`: Objeto retornado por `odr.run()`, contendo os coeficientes ajustados (`ds.adjust.beta`) e respetivos desvios padrão (`ds.adjust.sd_beta`).

---

## 📊 Funções Principais de Visualização (`plot.py`)

O ficheiro `plot.py` centraliza todas as funções de geração de gráficos e análise de regressão.

---

### 1. `plot(dataset, label="Dados", color="black", hlines=None)`
Gera um gráfico simples dos pontos experimentais com barras de erro. Permite adicionar linhas horizontais de referência.

---

### 2. `plotLinReg(dataset)` / `plotQuadReg(dataset)`
Exibe o gráfico com os pontos experimentais e a curva da regressão linear ou quadrática calculada para o `DataSet`. Retorna o objeto `adjust`.

---

### 3. `plotFinal(dataset, xres=[], yres=[], xscale='linear', yscale='linear', s=5)`
Desenha a curva de regressão e diferencia visualmente os pontos experimentais aceites dos pontos rejeitados (`xres`, `yres`).

---

### 4. `plotFinalwResidues(dataset, xres=[], yres=[], adjust1=None, stdy=0, xscale='linear', yscale='linear', s=5, tol=1)`
Plota o gráfico de regressão no subplot superior e os resíduos no subplot inferior, partilhando o eixo X.

---

### 5. `finalResidues(dataset, xFalse=[], yFalse=[], stdy=0, s=5)`
Gera um gráfico independente focado apenas na distribuição dos resíduos do ajuste com o intervalo de desvio padrão.

---

### 6. `fullLinAnalysis(dataset, separate=True, tol=1, xscale='linear', yscale='linear', s=5)`
Realiza uma análise linear completa com filtragem automática de pontos fora do intervalo de tolerância de resíduos (`tol` desvios padrão).
- `separate=True`: Mostra o gráfico de ajuste e o gráfico de resíduos em janelas separadas.
- `separate=False`: Mostra a regressão e os resíduos combinados num gráfico integrado com subplots.

```python
adjust_final = fullLinAnalysis(ds, separate=False, tol=1.5)
```

---

### 7. `plotMultipleReg(datasets, colors, legends="Pontos Experimentais", regressions=False, xscale='linear', yscale='linear', errorbars=True, tol=1)`
Sobrepõe múltiplos objetos `DataSet` no subplot superior com cores e legendas personalizadas. No subplot inferior, apresenta automaticamente os **resíduos correspondentes a cada conjunto de dados** e as respetivas **linhas de intervalo de $\sigma$ (`tol*std`)**, com as cores alinhadas a cada dataset.

```python
regs = plotMultipleReg(
    datasets=[ds1, ds2],
    colors=["black", "blue"],
    legends=["Amostra 1", "Amostra 2"],
    regressions=True
)
```

---

### 8. `plotColumnReg(datasets, tol=1)` / `plotColumnFullLinReg(datasets, tol=1)`
Plota uma lista de objetos `DataSet` dispostos em 2 colunas por linha (lado esquerdo: regressão; lado direito: resíduos), recalculando os ajustes após a rejeição de pontos atípicos com base na tolerância `tol`.

---

## 🛠️ Outros Ficheiros Auxiliares

- `functions.py`: Define os modelos matemáticos de ajuste (`lin`, `quadratic`, `polinomial`, `sin`, `exp`, etc.).
- `operations.py`: Contém utilitários auxiliares para cálculo de derivadas, algarismos significativos (`getSignAlg`), tabelas formatadas (`getTable`) e gestão do SciPy ODR.
