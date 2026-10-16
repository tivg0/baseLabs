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


def plot(dataset, label="Dados", color="black", hlines=None, meanAndStd=False):
    plt.figure(figsize=(12,8))
    if dataset.ux is None and dataset.uy is None:
        plt.scatter(dataset.x, dataset.y, c=color, label=label)
    else:
        plt.errorbar(dataset.x, dataset.y, xerr=dataset.ux, yerr=dataset.uy, fmt="o", c=color, label=label, capsize=4)

    if hlines is not None:
        for i in hlines:
            plt.axhline(i[0], color=i[2], label=i[1])
    
    if meanAndStd:
        plt.axhline(np.mean(dataset.y), color="red", label=f"Média {np.mean(dataset.y):.2e}")
        plt.axhline(np.mean(dataset.y) + np.std(dataset.y), color="orange", label=f"Desvio Padrão {np.std(dataset.y):.2e}")
        plt.axhline(np.mean(dataset.y) - np.std(dataset.y), color="orange")

    plt.title(fr"${dataset.titulo}$")
    plt.xlabel(fr"${dataset.labelx}$")
    plt.ylabel(fr"${dataset.labely}$")
    plt.legend()
    plt.grid()
    plt.show()


def _calculate_hist_bins(data, bins="auto", intcentered=False, AllN=False):
    if AllN:
        try:
            arr_np = np.asarray(data)
            if (
                arr_np.size == 0
                or not np.issubdtype(arr_np.dtype, np.number)
                or not np.all(np.isfinite(arr_np))
                or not bool(np.all(arr_np == np.floor(arr_np)))
            ):
                raise ValueError("Not all values are integers")
        except Exception as e:
            if str(e) == "Not all values are integers":
                raise
            raise ValueError("Not all values are integers")

        min_val = int(np.min(data))
        max_val = int(np.max(data))
        if min_val == max_val:
            return np.array([min_val - 0.5, min_val + 0.5]) if intcentered else np.array([min_val, min_val + 1])
        if intcentered:
            return np.arange(min_val - 0.5, max_val + 1.5, 1)
        else:
            return np.arange(min_val, max_val + 2, 1)

    if intcentered:
        if isinstance(bins, (list, tuple, np.ndarray)):
            b_arr = np.asarray(bins, dtype=float)
            centers = (b_arr[:-1] + b_arr[1:]) / 2.0
            if np.all(centers == np.floor(centers)):
                return b_arr
            shift = np.round(centers[0]) - centers[0]
            shifted = b_arr + shift
            w = np.diff(b_arr)[0] if len(b_arr) > 1 else 1.0
            while np.min(data) < shifted[0]:
                shifted = np.insert(shifted, 0, shifted[0] - w)
            while np.max(data) > shifted[-1]:
                shifted = np.append(shifted, shifted[-1] + w)
            return shifted
        else:
            b_edges = np.histogram_bin_edges(data, bins=bins)
            raw_w = (b_edges[-1] - b_edges[0]) / max(1, len(b_edges) - 1)
            step = max(1, int(round(raw_w)))
            min_val = np.min(data)
            max_val = np.max(data)
            c_start = int(round(min_val))
            while c_start - 0.5 * step > min_val:
                c_start -= step
            c_end = int(round(max_val))
            while c_end + 0.5 * step < max_val:
                c_end += step
            centers = np.arange(c_start, c_end + step, step)
            actual = np.append(centers - 0.5 * step, centers[-1] + 0.5 * step)
            return actual

    return np.histogram_bin_edges(data, bins=bins) if isinstance(bins, str) else bins


def plotHist(dataset, bins="auto", axis="y", label="Histograma", color="#4C7BB8", edgecolor="black", alpha=0.7, density=False, normalize=False, meanAndStd=False, gaussian=False, poisson=False, intcentered=False, AllN=False, vlines=None, title=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(12, 8))
    
    if hasattr(dataset, "y") and hasattr(dataset, "x"):
        data = dataset.y if axis == "y" else dataset.x
    else:
        data = np.asarray(dataset)
    
    weights = np.ones(len(data)) / len(data) if normalize else None
    d = False if normalize else density
    actual_bins = _calculate_hist_bins(data, bins=bins, intcentered=intcentered, AllN=AllN)
    counts, bin_edges, patches = plt.hist(data, bins=actual_bins, weights=weights, color=color, edgecolor=edgecolor, alpha=alpha, density=d, label=label)

    if vlines is not None:
        for i in vlines:
            c = i[2] if len(i) > 2 else "red"
            plt.axvline(i[0], color=c, label=i[1])

    if meanAndStd:
        mean_val = np.mean(data)
        std_val = np.std(data)
        plt.axvline(mean_val, color="red", linewidth=2, label=f"Média {mean_val:.2e}")
        plt.axvline(mean_val + std_val, color="orange", linestyle="--", linewidth=1.5, label=f"Desvio Padrão {std_val:.2e}")
        plt.axvline(mean_val - std_val, color="orange", linestyle="--", linewidth=1.5)

    if gaussian:
        mu = np.mean(data)
        sigma = np.std(data)
        if sigma > 0:
            xg = np.linspace(min(data), max(data), 200)
            yg = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xg - mu) / sigma) ** 2)
            bin_width = np.diff(bin_edges)[0] if len(bin_edges) > 1 else 1.0
            if normalize:
                yg *= bin_width
            elif not density:
                yg *= len(data) * bin_width
            plt.plot(xg, yg, color="red", linewidth=2, label=f"Gaussiana ($\\mu={mu:.2e}$, $\\sigma={sigma:.2e}$)")

    if poisson:
        mu = np.mean(data)
        if mu > 0:
            k_min = max(0, int(np.floor(np.min(data))))
            k_max = int(np.ceil(np.max(data)))
            k_min = min(k_min, max(0, int(np.floor(mu - 3 * np.sqrt(mu)))))
            k_max = max(k_max, int(np.ceil(mu + 3 * np.sqrt(mu))))
            k = np.arange(k_min, k_max + 1)

            try:
                from scipy.stats import poisson as sp_poisson
                yp = sp_poisson.pmf(k, mu)
            except Exception:
                from scipy.special import gammaln
                yp = np.exp(k * np.log(mu) - mu - gammaln(k + 1))

            bin_width = np.diff(bin_edges)[0] if len(bin_edges) > 1 else 1.0
            if normalize:
                yp_plot = yp * bin_width
            elif not density:
                yp_plot = yp * len(data) * bin_width
            else:
                yp_plot = yp / bin_width if bin_width > 0 else yp

            plt.plot(k, yp_plot, color="orange", marker="o" if len(k) <= 50 else "", markersize=4, linewidth=1.8, label=f"Poisson ($\\lambda={mu:.2e}$)")

    t = title if title is not None else getattr(dataset, "titulo", "Histograma")
    lx = xlabel if xlabel is not None else (getattr(dataset, "labely", "y") if axis == "y" else getattr(dataset, "labelx", "x"))
    if ylabel is not None:
        ly = ylabel
    elif normalize:
        ly = "Probabilidade"
    elif density:
        ly = "Densidade de Probabilidade"
    else:
        ly = "Frequência"

    plt.title(fr"${t}$" if not str(t).startswith("$") else t)
    plt.xlabel(fr"${lx}$" if not str(lx).startswith("$") else lx)
    plt.ylabel(ly)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    return counts, bin_edges, patches


plotHistogram = plotHist
plotHistograma = plotHist


def plotMultiHist(datasets, nrows=None, ncols=None, bins="auto", axis="y", color="#4C7BB8", edgecolor="black", alpha=0.7, density=False, normalize=False, meanAndStd=False, gaussian=False, poisson=False, intcentered=False, AllN=False, figsize=None, titles=None, xlabels=None, ylabels=None):
    N = len(datasets)
    if N == 0:
        return None, None

    if nrows is None and ncols is None:
        if N == 1:
            nrows, ncols = 1, 1
        else:
            ncols = 2
            nrows = int(np.ceil(N / ncols))
    elif nrows is not None and ncols is None:
        ncols = int(np.ceil(N / nrows))
    elif ncols is not None and nrows is None:
        nrows = int(np.ceil(N / ncols))

    if figsize is None:
        figsize = (ncols * 7, nrows * 4.5)

    fig, axs = plt.subplots(nrows, ncols, figsize=figsize)
    
    if isinstance(axs, np.ndarray):
        axes_list = list(axs.flat)
    else:
        axes_list = [axs]

    for i, ax in enumerate(axes_list):
        if i >= N:
            ax.set_visible(False)
            continue

        ds = datasets[i]
        if hasattr(ds, "y") and hasattr(ds, "x"):
            data = ds.y if axis == "y" else ds.x
        else:
            data = np.asarray(ds)

        b = bins[i] if isinstance(bins, list) and len(bins) > i else bins
        c = color[i] if isinstance(color, list) and len(color) > i else color
        int_c = intcentered[i] if isinstance(intcentered, list) and len(intcentered) > i else intcentered
        all_n = AllN[i] if isinstance(AllN, list) and len(AllN) > i else AllN
        lbl = getattr(ds, "titulo", None)
        if not lbl:
            lbl = f"Dataset {i+1}"

        weights = np.ones(len(data)) / len(data) if normalize else None
        d = False if normalize else density
        actual_b = _calculate_hist_bins(data, bins=b, intcentered=int_c, AllN=all_n)
        counts, bin_edges, patches = ax.hist(data, bins=actual_b, weights=weights, color=c, edgecolor=edgecolor, alpha=alpha, density=d, label=fr"${lbl}$")

        if meanAndStd:
            mean_val = np.mean(data)
            std_val = np.std(data)
            ax.axvline(mean_val, color="red", linewidth=2, label=f"Média {mean_val:.2e}")
            ax.axvline(mean_val + std_val, color="orange", linestyle="--", linewidth=1.5, label=f"Desvio {std_val:.2e}")
            ax.axvline(mean_val - std_val, color="orange", linestyle="--", linewidth=1.5)

        if gaussian:
            mu = np.mean(data)
            sigma = np.std(data)
            if sigma > 0:
                xg = np.linspace(min(data), max(data), 200)
                yg = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xg - mu) / sigma) ** 2)
                bin_width = np.diff(bin_edges)[0] if len(bin_edges) > 1 else 1.0
                if normalize:
                    yg *= bin_width
                elif not density:
                    yg *= len(data) * bin_width
                ax.plot(xg, yg, color="red", linewidth=2, label=f"Gaussiana ($\\mu={mu:.2e}$, $\\sigma={sigma:.2e}$)")

        if poisson:
            mu = np.mean(data)
            if mu > 0:
                k_min = max(0, int(np.floor(np.min(data))))
                k_max = int(np.ceil(np.max(data)))
                k_min = min(k_min, max(0, int(np.floor(mu - 3 * np.sqrt(mu)))))
                k_max = max(k_max, int(np.ceil(mu + 3 * np.sqrt(mu))))
                k = np.arange(k_min, k_max + 1)

                try:
                    from scipy.stats import poisson as sp_poisson
                    yp = sp_poisson.pmf(k, mu)
                except Exception:
                    from scipy.special import gammaln
                    yp = np.exp(k * np.log(mu) - mu - gammaln(k + 1))

                bin_width = np.diff(bin_edges)[0] if len(bin_edges) > 1 else 1.0
                if normalize:
                    yp_plot = yp * bin_width
                elif not density:
                    yp_plot = yp * len(data) * bin_width
                else:
                    yp_plot = yp / bin_width if bin_width > 0 else yp

                ax.plot(k, yp_plot, color="orange", marker="o" if len(k) <= 50 else "", markersize=4, linewidth=1.8, label=f"Poisson ($\\lambda={mu:.2e}$)")

        t = titles[i] if (isinstance(titles, list) and len(titles) > i) else (titles if titles is not None else getattr(ds, "titulo", f"Dataset {i+1}"))
        lx = xlabels[i] if (isinstance(xlabels, list) and len(xlabels) > i) else (xlabels if xlabels is not None else (getattr(ds, "labely", "y") if axis == "y" else getattr(ds, "labelx", "x")))
        if ylabels is not None:
            ly = ylabels[i] if isinstance(ylabels, list) and len(ylabels) > i else ylabels
        elif normalize:
            ly = "Probabilidade"
        elif density:
            ly = "Densidade"
        else:
            ly = "Frequência"

        ax.set_title(fr"${t}$" if not str(t).startswith("$") else t)
        ax.set_xlabel(fr"${lx}$" if not str(lx).startswith("$") else lx)
        ax.set_ylabel(fr"{ly}")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return fig, axs


plotMultiHistogram = plotMultiHist
plotMultiHistograma = plotMultiHist
plotHistogramas = plotMultiHist

