import numpy as np
from scipy.odr import RealData, Model, ODR
import matplotlib.pyplot as plt

def derivativePolinomialCoefs(coefs):
    N = len(coefs)
    for i in range(0,N):
        coefs[i] *= (N-i)
    return coefs[1:]

def getData(filename, skip=1):
    return np.genfromtxt(filename, delimiter="\t", unpack=True, skip_header=skip)

def getAdjust(func_or_dataset, x=None, y=None, ux=None, uy=None, beta0=None):
    if hasattr(func_or_dataset, 'x') and hasattr(func_or_dataset, 'y'):
        dataset = func_or_dataset
        if beta0 is not None:
            return dataset.calculate_adjust(beta0)
        return dataset.adjust
    func = func_or_dataset
    if beta0 is None:
        beta0 = [1, 1]
    mod = Model(func)
    data1 = RealData(x, y, ux, uy)
    odr = ODR(data1, mod, beta0)
    output = odr.run()
    return output

def getPolynomialLabel(beta, x, y):
    x = x.split('(')[0]
    y = y.split('(')[0]
    s = rf"${y}({x}) = "
    
    for i in range(len(beta)):
        coef_power = len(beta) - i - 1
        coef_value = beta[i]
        
        # Add + sign if positive and not the first term
        sign = "+" if coef_value >= 0 and i != 0 else ""

        formattedCoefValue = f'{coef_value:.3e}'.split('e')[0] 

        if ('e' in f'{coef_value:.3e}' and '00' not in f'{coef_value:.3e}'.split('e')[1]):
            formattedCoefValue += r'\times10^' + '{' + str(int(f'{coef_value:.3e}'.split('e')[1])) + '}'
        
        if coef_power > 1:
            term = rf"{sign}{formattedCoefValue}{x}^{coef_power}"
        elif coef_power == 1:
            term = rf"{sign}{formattedCoefValue}{x}"
        else:
            term = rf"{sign}{formattedCoefValue}"
        
        s += term
    
    s += "$"
    return s

def getTable(columns,data,title, firstcolumnShade, size):

    # Criar figura
    fig, ax = plt.subplots(figsize=size)  # ajusta o tamanho
    ax.axis('off')  # remove eixos

    # Criar tabela
    table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')

    # Ajustar estilo
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.5, 3)  # escala horizontal e vertical

    # Colorir os headers (linha 0)
    for j in range(len(columns)):
        cell = table[(0, j)]
        cell.set_facecolor("#4C7BB8")   # verde
        cell.set_text_props(color="white", weight='bold')

    for i in range(1, len(data) + 1):  # começa em 1 por causa do header
        color = "#e0e0e0" if i % 2 == 0 else "white"
        for j in range(len(columns)):
            table[(i, j)].set_facecolor(color)

    # Colorir a primeira coluna (coluna 0, excluindo o header)
    if firstcolumnShade:
        for i_row in range(1, len(data)+1):
            cell = table[(i_row, 0)]
            cell.set_facecolor("#d8d8d8")   # cinza claro
            cell.set_text_props(weight='bold')

    # Título
    plt.title(title, fontsize=14, pad=20)

    plt.show()

def handleCientNot(x):
    new = f"{x:.3e}"
    if (new.endswith("00")):
        return new.split("e")[0]
    elif (new.endswith("-01") or new.endswith('-1')):
        new = f"{x:.4f}"
        return new
    elif (new.endswith("-02") or new.endswith('-2')):
        new = f"{x:.5f}"
        return new
    elif (new.endswith("01")):
        new = f"{x:.3f}"
        return new
    elif (new.endswith("02")):
        new = f"{x:.1f}"
        return new
    else:
        return new.split("e")[0] + r'\times10^' + '{' + str(int(f'{x:.3e}'.split('e')[1])) + '}'

def round_un(x, u):
    if u == 0 or np.isnan(u) or np.isnan(x):
        return np.array([x if not np.isnan(x) else 0.0, u if not np.isnan(u) else 0.0, 0])
    order = int(np.floor(np.log10(abs(u))))
    decimals = -(order - 1)
    
    u_rounded = round(u, decimals)
    x_rounded = round(x, decimals)
    
    return np.array([x_rounded, u_rounded, decimals])

def getPolynomialLabel2(beta, betastd, x, y):
    x = x.split('(')[0]
    y = y.split('(')[0]
    s = rf"${y}({x}) = "
    
    for i in range(len(beta)):
        coef_power = len(beta) - i - 1
        c = round_un(beta[i], betastd[i])
        coef_value = c[0]
        sci_str = f"{coef_value:e}"
        exp = sci_str.split('e')[1] if 'e' in sci_str else '0'
        if abs(coef_value) < 9:
            n = int((c[2] - abs(int(exp))))
        else:
            n = int(c[2] + int(exp))
        n = max(0, n)
        
        sign = "+" if coef_value >= 0 and i != 0 else ""
        formattedCoefValue = f'{coef_value:.{n}e}'.split('e')[0] 
        if ('e' in f'{coef_value:.{n}e}' and '00' not in f'{coef_value:.{n}e}'.split('e')[1]):
            formattedCoefValue += r'\times10^' + '{' + str(int(f'{coef_value:.{n}e}'.split('e')[1])) + '}'
        
        if coef_power > 1:
            term = rf"{sign}{formattedCoefValue}{x}^{coef_power}"
        elif coef_power == 1:
            term = rf"{sign}{formattedCoefValue}{x}"
        else:
            term = rf"{sign}{formattedCoefValue}"
        
        s += term
    
    s += "$"
    return s

def getUncertainty(uxs):
    Is = []
    for ux in uxs:
        i = 0
        if ux < 1:
            while ux < 1:
                ux *= 10
                i += 1
        else:
            while ux > 1:
                ux /= 10
                i += 1
        Is.append(i)
    return np.array(Is, int)

def getSignAlg(xs, uxs=None):
    if hasattr(xs, 'x') and hasattr(xs, 'ux'):
        dataset = xs
        xs_arr = np.copy(dataset.x)
        uxs_arr = np.copy(dataset.ux)
    else:
        xs_arr = np.copy(xs)
        uxs_arr = np.copy(uxs)

    uncuxs = getUncertainty(uxs_arr)
    uncxs = getUncertainty(xs_arr)

    for i in range(len(xs_arr)):
        uxs_arr[i] = round(uxs_arr[i], uncuxs[i])
        if uxs_arr[i] < xs_arr[i]:
            xs_arr[i] = round(xs_arr[i], uncuxs[i])
        else:
            e = getUncertainty([xs_arr[i]])[0]
            xs_arr[i] = round(xs_arr[i], e)

    return [xs_arr, uxs_arr]