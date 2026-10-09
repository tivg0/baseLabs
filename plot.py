import matplotlib.pyplot as plt
import numpy as np

try:
    from .functions import *
    from .operations import *
    from .dataset import DataSet
except ImportError:
    from functions import *
    from operations import *
    from dataset import DataSet

plt.rcParams['errorbar.capsize'] = 4


def plotLinReg(dataset):
    plt.figure(figsize=(12,8))
    plt.errorbar(dataset.x, dataset.y, xerr=dataset.ux, yerr=dataset.uy, c="black", fmt="o")

    adjust = dataset.adjust
    x = np.linspace(min(dataset.x), max(dataset.x), 100)
    y = dataset.fit_type(adjust.beta, x)
    plt.plot(x, y, c="orange", label=getPolynomialLabel2(adjust.beta, adjust.sd_beta, dataset.labelx, dataset.labely))

    plt.title(dataset.titulo)
    plt.xlabel(dataset.labelx)
    plt.ylabel(dataset.labely)
    plt.legend(fontsize='12')
    plt.grid()
    plt.show()
    return adjust


def plotQuadReg(dataset):
    plt.figure(figsize=(12,8))
    plt.errorbar(dataset.x, dataset.y, xerr=dataset.ux, yerr=dataset.uy, c="black", fmt="o")

    adjust = dataset.adjust
    x = np.linspace(min(dataset.x), max(dataset.x), 100)
    y = dataset.fit_type(adjust.beta, x)
    plt.plot(x, y, c="orange", label=getPolynomialLabel2(adjust.beta, adjust.sd_beta, dataset.labelx, dataset.labely))

    plt.title(dataset.titulo)
    plt.xlabel(dataset.labelx)
    plt.ylabel(dataset.labely)
    plt.legend(fontsize='12')
    plt.grid()
    plt.show()
    return adjust


def plotFinal(dataset, xres=[], yres=[], xscale='linear', yscale='linear', s=5):
    plt.figure(figsize=(12,8))
    adjust = dataset.adjust
    x1, y1 = dataset.x, dataset.y
    xerr1, yerr1 = dataset.ux, dataset.uy
    title, xlabel, ylabel = dataset.titulo, dataset.labelx, dataset.labely

    if len(xres) == 0:
        x = np.linspace(min(x1), max(x1), 100)
    else:
        x = np.linspace(min(min(x1), min(xres)), max(max(x1), max(xres)), 100)
    
    y = dataset.fit_type(adjust.beta, x)
    plt.plot(x, y, c="orange", label=getPolynomialLabel2(adjust.beta, adjust.sd_beta, xlabel, ylabel), zorder=3)
    plt.errorbar(x1, y1, xerr=xerr1, yerr=yerr1, c="black", fmt="o", label="Pontos Experimentais", zorder=2, markersize=s)

    if len(xres) != 0:
        plt.plot(xres, yres, c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados", zorder=1, markersize=s)

    plt.title(rf"${title}$")
    plt.xlabel(rf"${xlabel}$")
    plt.ylabel(rf"${ylabel}$")
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.legend()
    plt.grid()
    plt.show()
    return adjust


def plotFinalwResidues(dataset, xres=[], yres=[], adjust1=None, stdy=0, xscale='linear', yscale='linear', s=5, tol=1):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    adjust = dataset.adjust
    if adjust1 is None:
        adjust1 = adjust

    x1, y1 = dataset.x, dataset.y
    xerr1, yerr1 = dataset.ux, dataset.uy
    title, xlabel, ylabel = dataset.titulo, dataset.labelx, dataset.labely

    if len(xres) == 0:
        x = np.linspace(min(x1), max(x1), 100)
    else:
        x = np.linspace(min(min(x1), min(xres)), max(max(x1), max(xres)), 100)
    
    y = dataset.fit_type(adjust.beta, x)
    ax1.plot(x, y, c="orange", label=getPolynomialLabel2(adjust.beta, adjust.sd_beta, xlabel, ylabel), zorder=3)
    ax1.errorbar(x1, y1, xerr=xerr1, yerr=yerr1, c="black", fmt="o", label="Pontos Experimentais", zorder=2, markersize=s)

    if len(xres) != 0:
        ax1.plot(xres, yres, c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados", zorder=1, markersize=s)

    ax1.set_title(rf"${title}$")
    ax1.set_ylabel(rf"${ylabel}$")
    ax1.set_xscale(xscale)
    ax1.set_yscale(yscale)
    ax1.legend()
    ax1.grid()

    resTrue = y1 - x1 * adjust1.beta[0] - adjust1.beta[1]
    resFalse = np.array(yres) - np.array(xres) * adjust1.beta[0] - adjust1.beta[1] if len(xres) > 0 else []
    ax2.axhline(0, c="red")
    ax2.axhline(stdy, c="orange", label=f"Intervalo de {tol}σ")
    ax2.axhline(-stdy, c="orange")
    ax2.scatter(x1, resTrue, c="black", s=s)
    ax2.grid(axis="x")
    ax2.legend()
    if len(xres) != 0:
        ax2.scatter(xres, resFalse, c="red", s=s)

    ax2.set_xlabel(rf"${xlabel}$")
    ax2.set_ylabel(rf"Resíduos ${ylabel}$")

    plt.subplots_adjust(hspace=0)
    plt.show()
    return adjust


def finalResidues(dataset, xFalse=[], yFalse=[], stdy=0, s=5):
    xTrue, yTrue = dataset.x, dataset.y
    adjust = dataset.adjust
    xlabel, ylabel = dataset.labelx, dataset.labely

    resTrue = yTrue - xTrue * adjust.beta[0] - adjust.beta[1]
    resFalse = np.array(yFalse) - np.array(xFalse) * adjust.beta[0] - adjust.beta[1] if len(xFalse) > 0 else []

    plt.figure(figsize=(12,8))
    plt.axhline(0, c="black", alpha=0.5)
    plt.axhline(stdy, c="orange", label="Intervalo {} Desvio Padrão".format(stdy))
    plt.axhline(-stdy, c="orange")
    plt.scatter(xTrue, resTrue, c="black", label="Pontos Experimentais", s=s)
    if len(xFalse) > 0:
        plt.scatter(xFalse, resFalse, c="red", label="Pontos Experimentais Rejeitados", s=s)
    plt.xlabel(rf'${xlabel}$')
    plt.ylabel(rf"$Res$ {ylabel}")
    plt.title("Resíduos E")
    plt.legend()
    plt.show()


def fullLinAnalysis(dataset, separate=True, tol=1, xscale='linear', yscale='linear', s=5):
    x, y = dataset.x, dataset.y
    xerr, yerr = dataset.ux, dataset.uy
    title, xlabel, ylabel = dataset.titulo, dataset.labelx, dataset.labely
    
    adjust = dataset.adjust

    res = y - x * adjust.beta[0] - adjust.beta[1]
    stdy = np.std(res) * tol

    stdy_thresh = max(stdy, 1e-12)
    yTrue = y[abs(res) <= stdy_thresh]
    yFalse = y[abs(res) > stdy_thresh]

    xTrue = x[abs(res) <= stdy_thresh]
    xFalse = x[abs(res) > stdy_thresh]

    yerrTrue = yerr[abs(res) <= stdy_thresh]
    xerrTrue = xerr[abs(res) <= stdy_thresh]


    dataset_true = DataSet(xTrue, yTrue, xerrTrue, yerrTrue, title, xlabel, ylabel, dataset.fit_type)

    if separate:
        adjustFinal = plotFinal(dataset_true, xFalse, yFalse, xscale=xscale, yscale=yscale, s=s)
        finalResidues(dataset_true, xFalse, yFalse, stdy, s=s)
        return adjustFinal
    else:
        adjustFinal = plotFinalwResidues(dataset_true, xFalse, yFalse, adjust1=adjust, stdy=stdy, xscale=xscale, yscale=yscale, s=s, tol=tol)
        return adjustFinal


def plotColumnFullLinReg(datasets, tol=1):
    fig, axs = plt.subplots(len(datasets), 2, figsize=(18, len(datasets) * 7))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    axsIter = iter(axs.flat) if hasattr(axs, 'flat') else iter([axs[0], axs[1]])
    adjusts = []

    for ds in datasets:
        x, y = ds.x, ds.y
        xerr, yerr = ds.ux, ds.uy
        title, xlabel, ylabel = ds.titulo, ds.labelx, ds.labely
        
        ax = next(axsIter)
        adjust = ds.adjust

        res = y - x * adjust.beta[0] - adjust.beta[1]
        stdy = np.std(res) * tol

        stdy_thresh = max(stdy, 1e-12)
        yTrue = y[abs(res) <= stdy_thresh]
        yFalse = y[abs(res) > stdy_thresh]

        xTrue = x[abs(res) <= stdy_thresh]
        xFalse = x[abs(res) > stdy_thresh]

        yerrTrue = yerr[abs(res) <= stdy_thresh]
        xerrTrue = xerr[abs(res) <= stdy_thresh]

        ax.errorbar(xTrue, yTrue, xerr=xerrTrue, yerr=yerrTrue, c="black", fmt="o", label="Pontos Experimentais")
        ds_true = DataSet(xTrue, yTrue, xerrTrue, yerrTrue, title, xlabel, ylabel, ds.fit_type)
        adjustTrue = ds_true.adjust
        adjusts.append(adjustTrue)

        if len(xFalse) == 0:
            x_plot = np.linspace(min(xTrue), max(xTrue), 100)
        else:
            x_plot = np.linspace(min(min(xTrue), min(xFalse)), max(max(xTrue), max(xFalse)), 100)

        y_plot = ds.fit_type(adjustTrue.beta, x_plot)
        ax.plot(x_plot, y_plot, c="orange", label=getPolynomialLabel2(adjustTrue.beta, adjustTrue.sd_beta, xlabel, ylabel))
        if len(xFalse) != 0:
            ax.plot(xFalse, yFalse, c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados")

        ax.set_title(rf"${title}$")
        ax.set_xlabel(rf"${xlabel}$")
        ax.set_ylabel(rf"${ylabel}$")
        ax.legend()
        ax.grid()

        ax = next(axsIter)

        resTrue = yTrue - xTrue * adjust.beta[0] - adjust.beta[1]
        resFalse = yFalse - xFalse * adjust.beta[0] - adjust.beta[1]

        ax.axhline(0, c="black", alpha=0.5)
        ax.axhline(stdy, c="orange", label=f"Intervalo {tol}$\\sigma$")
        ax.axhline(-stdy, c="orange")
        ax.plot(xTrue, resTrue, c="black", marker="o", ls="", label="Pontos Experimentais")
        ax.plot(xFalse, resFalse, c="red", marker="o", ls="", label="Pontos Rejeitados")
        ax.set_xlabel(rf'${xlabel}$')
        ax.set_ylabel(rf"$Res \quad {ylabel}$")
        ax.set_title(fr"$Resíduos \quad {ylabel.split('(')[0]}$")
        ax.legend()
        ax.grid()
        
    return adjusts


def plotMultipleReg(datasets, colors, legends="Pontos Experimentais", regressions=False, tol=1, xscale='linear', yscale='linear', errorbars=True):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    regs = np.zeros([len(datasets)], dtype=object)

    if legends == "Pontos Experimentais":
        legends = ["Pontos Experimentais"] * len(datasets)

    first_ds = datasets[0]
    title, xlabel, ylabel = first_ds.titulo, first_ds.labelx, first_ds.labely

    ax2.axhline(0, c="red")

    for i in range(len(datasets)):
        ds = datasets[i]
        x = ds.x[~np.isnan(ds.x)]
        y = ds.y[~np.isnan(ds.y)]
        xerr = ds.ux[~np.isnan(ds.x)]
        yerr = ds.uy[~np.isnan(ds.y)]
        color = colors[i]

        adjust = ds.adjust
        regs[i] = adjust

        if errorbars:
            ax1.errorbar(x, y, xerr=xerr, yerr=yerr, c=color, fmt="o", label=legends[i])
        else:
            ax1.scatter(x, y, c=color, label=legends[i])

        xLin = np.linspace(np.min(x), np.max(x), 50)
        yLin = ds.fit_type(adjust.beta, xLin)
        if regressions:
            ax1.plot(xLin, yLin, c=color, label=getPolynomialLabel2(adjust.beta, adjust.sd_beta, xlabel, ylabel))

        res = y - ds.fit_type(adjust.beta, x)
        if errorbars:
            ax2.errorbar(x, res, yerr=yerr, c=color, fmt="o")
        else:
            ax2.scatter(x, res, c=color)

        if tol is not None and tol > 0:
            stdy = np.std(res) * tol
            label_sig = f"Intervalo de {tol}σ ({legends[i]})" if len(datasets) > 1 else f"Intervalo de {tol}σ"
            ax2.axhline(stdy, c=color, label=label_sig, alpha=0.5)
            ax2.axhline(-stdy, c=color, alpha=0.5)

    ax1.set_title(rf"${title}$")
    ax1.set_ylabel(rf"${ylabel}$")
    ax1.set_xscale(xscale)
    ax1.set_yscale(yscale)
    ax1.legend()
    ax1.grid()

    ax2.set_xlabel(rf"${xlabel}$")
    ax2.set_ylabel(rf"Resíduos ${ylabel}$")
    ax2.grid()
    if tol is not None and tol > 0:
        ax2.legend()

    plt.subplots_adjust(hspace=0)
    plt.show()

    return regs


def plotColumnReg(datasets, tol=1):
    fig, axs = plt.subplots(len(datasets), 2, figsize=(18, len(datasets) * 7))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    axsIter = iter(axs.flat) if hasattr(axs, 'flat') else iter([axs[0], axs[1]])
    adjusts = []

    for ds in datasets:
        x, y = ds.x, ds.y
        xerr, yerr = ds.ux, ds.uy
        title, xlabel, ylabel = ds.titulo, ds.labelx, ds.labely
        func = ds.fit_type
        ax = next(axsIter)

        adjust = ds.adjust
        res = y - x * adjust.beta[0] - adjust.beta[1]
        stdy = np.std(res) * tol

        stdy_thresh = max(stdy, 1e-12)
        yTrue = y[abs(res) <= stdy_thresh]
        yFalse = y[abs(res) > stdy_thresh]

        xTrue = x[abs(res) <= stdy_thresh]
        xFalse = x[abs(res) > stdy_thresh]

        yerrTrue = yerr[abs(res) <= stdy_thresh]
        xerrTrue = xerr[abs(res) <= stdy_thresh]

        ax.errorbar(xTrue, yTrue, xerr=xerrTrue, yerr=yerrTrue, c="black", fmt="o", label="Pontos Experimentais")
        ds_true = DataSet(xTrue, yTrue, xerrTrue, yerrTrue, title, xlabel, ylabel, func)
        adjustTrue = ds_true.adjust
        adjusts.append(adjustTrue)

        if len(xFalse) == 0:
            x_plot = np.linspace(min(xTrue), max(xTrue), 100)
        else:
            x_plot = np.linspace(min(min(xTrue), min(xFalse)), max(max(xTrue), max(xFalse)), 100)

        y_plot = func(adjustTrue.beta, x_plot)
        ax.plot(x_plot, y_plot, c="orange", label=getPolynomialLabel2(adjustTrue.beta, adjustTrue.sd_beta, xlabel, ylabel))
        if len(xFalse) != 0:
            ax.plot(xFalse, yFalse, c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados")

        ax.set_title(rf"${title}$")
        ax.set_xlabel(rf"${xlabel}$")
        ax.set_ylabel(rf"${ylabel}$")
        ax.legend()
        ax.grid()

        ax = next(axsIter)

        resTrue = yTrue - xTrue * adjust.beta[0] - adjust.beta[1]
        resFalse = yFalse - xFalse * adjust.beta[0] - adjust.beta[1]

        ax.axhline(0, c="black", alpha=0.5)
        ax.axhline(stdy, c="orange", label=f"Intervalo {tol}$\\sigma$")
        ax.axhline(-stdy, c="orange")
        ax.plot(xTrue, resTrue, c="black", marker="o", ls="", label="Pontos Experimentais")
        ax.plot(xFalse, resFalse, c="red", marker="o", ls="", label="Pontos Rejeitados")
        ax.set_xlabel(rf'${xlabel}$')
        ax.set_ylabel(rf"$Res \quad {ylabel}$")
        ax.set_title(fr"$Resíduos \quad {ylabel.split('(')[0]}$")
        ax.legend()
        ax.grid()
        
    return adjusts


def plot(dataset, label="Dados", color="black", hlines=None):
    plt.figure(figsize=(12,8))
    if dataset.ux is None and dataset.uy is None:
        plt.scatter(dataset.x, dataset.y, c=color, label=label)
    else:
        plt.errorbar(dataset.x, dataset.y, xerr=dataset.ux, yerr=dataset.uy, fmt="o", c=color, label=label, capsize=4)

    if hlines is not None:
        for i in hlines:
            plt.axhline(i[0], color="red", label=i[1])

    plt.title(fr"${dataset.titulo}$")
    plt.xlabel(fr"${dataset.labelx}$")
    plt.ylabel(fr"${dataset.labely}$")
    plt.legend()
    plt.grid()
    plt.show()

#fodasse