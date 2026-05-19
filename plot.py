import matplotlib.pyplot as plt
import numpy as np
from .functions import *
from .operations import *


def plotLinReg(xs,ys,xerr,yerr,title,xlabel,ylabel):
    plt.figure(figsize=(12,8))
    plt.errorbar(xs,ys, xerr=xerr, yerr=yerr, c="black", fmt="o")

    adjust = getAdjust(lin, xs, ys, xerr, yerr)
    x = np.linspace(min(xs), max(xs),100)
    y = lin(adjust.beta, x)
    plt.plot(x,y, c="orange", label=getPolynomialLabel2(adjust.beta,xlabel,ylabel))

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(fontsize='12')
    plt.grid()
    plt.show()
    return adjust

def plotQuadReg(xs,ys,xerr,yerr,title,xlabel,ylabel):
    plt.figure(figsize=(12,8))
    plt.errorbar(xs,ys, xerr=xerr, yerr=yerr, c="black", fmt="o")

    adjust = getAdjust(quadratic, xs, ys, xerr, yerr,[1,1,1])
    x = np.linspace(min(xs), max(xs),100)
    y = quadratic(adjust.beta, x)
    plt.plot(x,y, c="orange", label=getPolynomialLabel2(adjust.beta,xlabel,ylabel))

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(fontsize='12')
    plt.grid()
    plt.show()
    return adjust

def plotFinal(x1,y1,xres,yres,xerr1,yerr1,title,xlabel,ylabel,beta0=[1,1],xscale='linear',yscale='linear'):
    plt.figure(figsize=(12,8))
    plt.errorbar(x1,y1, xerr=xerr1, yerr=yerr1, c="black", fmt="o", label="Pontos Experimentais")
    adjust = getAdjust(lin, x1, y1, xerr1, yerr1,beta0)
    if len(xres) == 0:
        x = np.linspace(min(x1), max(x1),100)
    else:
        x = np.linspace(min(min(x1),min(xres)), max(max(x1),max(xres)),100)
    
    y = lin(adjust.beta, x)
    plt.plot(x,y, c="orange", label=getPolynomialLabel2(adjust.beta, xlabel,ylabel))
    if len(xres) != 0:
        plt.plot(xres,yres, c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados")

    plt.title(rf"${title}$")
    plt.xlabel(rf"${xlabel}$")
    plt.ylabel(rf"${ylabel}$")
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.legend()
    plt.grid()
    plt.show()
    return adjust

def finalResidues(xTrue,yTrue,xFalse,yFalse,adjust,stdy,xlabel, ylabel):
    resTrue = yTrue - xTrue*adjust.beta[0] - adjust.beta[1]
    resFalse = yFalse - xFalse*adjust.beta[0] - adjust.beta[1]

    plt.figure(figsize=(12,8))
    plt.axhline(0, c="black", alpha=0.5)
    plt.axhline(stdy, c="orange", label="Intervalo {} Desvio Padrão".format(stdy))
    plt.axhline(-stdy, c="orange")
    plt.plot(xTrue,resTrue,c="black", marker="o", ls="", label="Pontos Experimentais")
    plt.plot(xFalse,resFalse,c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados")
    plt.xlabel(rf'${xlabel}$')
    plt.ylabel(rf"$Res$ {ylabel}")
    plt.title("Resíduos E")
    plt.legend()
    plt.show()

def fullLinAnalysis(x,y,xerr,yerr,title,xlabel,ylabel,beta0=[1,1],tol=1,xscale='linear',yscale='linear'):
    if isinstance(xerr,(int,float)):
        xerr = np.full(len(x),xerr)
    if isinstance(yerr,(int,float)):
        yerr = np.full(len(y),yerr)
    adjust = getAdjust(lin,x,y,xerr,yerr,beta0)

    res = y - x*adjust.beta[0] - adjust.beta[1]

    stdy = np.std(res)*tol

    yTrue = y[abs(res) < stdy]
    yFalse = y[abs(res) > stdy]

    xTrue = x[abs(res) < stdy]
    xFalse = x[abs(res) > stdy]

    yerrTrue = yerr[abs(res) < stdy]
    xerrTrue = xerr[abs(res) < stdy]

    adjustFinal = plotFinal(xTrue,yTrue,xFalse,yFalse,xerrTrue,yerrTrue,title,xlabel,ylabel,beta0,xscale,yscale)
    finalResidues(xTrue,yTrue,xFalse,yFalse,adjust,stdy,xlabel, ylabel)
    return adjustFinal


def plotColumnFullLinReg(xs,ys,xerrs,yerrs,titles,xlabels,ylabels,beta0=[1,1],tol=1):

    fig, axs = plt.subplots(len(xs),2,figsize=(18,len(xs)*7))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    axsIter = iter(axs.flat)
    adjusts = []

    if isinstance(xlabels, str):
        xlabels = [xlabels] * len(xs)
    if isinstance(ylabels, str):
        ylabels = [ylabels] * len(xs)

    for i in range(0,len(xs)):
        x=xs[i]
        y=ys[i]
        xerr=xerrs[i]
        yerr=yerrs[i]
        title = titles[i]
        xlabel = xlabels[i]
        ylabel = ylabels[i]
        ax = next(axsIter)

        if isinstance(xerr,(int,float)):
            xerr = np.full(len(x),xerr)
        if isinstance(yerr,(int,float)):
            yerr = np.full(len(y),yerr)
        adjust = getAdjust(lin,x,y,xerr,yerr,beta0)

        res = y - x*adjust.beta[0] - adjust.beta[1]

        stdy = np.std(res)*tol

        yTrue = y[abs(res) < stdy]
        yFalse = y[abs(res) > stdy]

        xTrue = x[abs(res) < stdy]
        xFalse = x[abs(res) > stdy]

        yerrTrue = yerr[abs(res) < stdy]
        xerrTrue = xerr[abs(res) < stdy]

        ax.errorbar(xTrue,yTrue, xerr=xerrTrue, yerr=yerrTrue, c="black", fmt="o", label="Pontos Experimentais")
        adjustTrue = getAdjust(lin, xTrue, yTrue, xerrTrue, yerrTrue,beta0)
        adjusts.append(adjustTrue)
        if len(xFalse) == 0:
            x = np.linspace(min(xTrue), max(xTrue),100)
        else:
            x = np.linspace(min(min(xTrue),min(xFalse)), max(max(xTrue),max(xFalse)),100)

        y = lin(adjustTrue.beta, x)
        ax.plot(x,y, c="orange", label=getPolynomialLabel2(adjustTrue.beta,adjustTrue.sd_beta, xlabel,ylabel))
        if len(xFalse) != 0:
            ax.plot(xFalse,yFalse, c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados")

        ax.set_title(rf"${title}$")
        ax.set_xlabel(rf"${xlabel}$")
        ax.set_ylabel(rf"${ylabel}$")
        ax.legend()
        ax.grid()

        ax = next(axsIter)

        resTrue = yTrue - xTrue*adjust.beta[0] - adjust.beta[1]
        resFalse = yFalse - xFalse*adjust.beta[0] - adjust.beta[1]

        ax.axhline(0, c="black", alpha=0.5)
        ax.axhline(stdy, c="orange", label="Intervalo {}$\sigma$".format(tol))
        ax.axhline(-stdy, c="orange")
        ax.plot(xTrue,resTrue,c="black", marker="o", ls="", label="Pontos Experimentais")
        ax.plot(xFalse,resFalse,c="red", marker="o", ls="", label="Pontos Rejeitados")
        ax.set_xlabel(rf'${xlabel}$')
        ax.set_ylabel(rf"$Res \quad {ylabel}$")
        ax.set_title(fr"$Resíduos \quad {ylabel.split('(')[0]}$")
        ax.legend()
        ax.grid()
        
    return adjusts

def plotMultipleReg(xs,ys,xerrs,yerrs,title, xlabel,ylabel,colors,legends="Pontos Experimentais",regressions=False,beta0=[1,1],xscale='linear',yscale='linear', errorbars= True):
    plt.figure(figsize=(12,8))
    regs = np.zeros([len(xs)],dtype=object)

    if legends == "Pontos Experimentais":
        legends = ["Pontos Experimentais"] * len(xs)

    for i in range(0,len(xs)):
        x = xs[i]
        y = ys[i]
        color = colors[i]

        x = x[~np.isnan(x)]
        y = y[~np.isnan(y)]

        if isinstance(xerrs,(int,float)):
            xerr = np.full(len(x),xerrs)
        else:
            xerr = xerrs[i]
        if isinstance(yerrs,(int,float)):
            yerr = np.full(len(y),yerrs)
        else:
            yerr = yerrs[i]

        adjust = getAdjust(lin,x,y,xerr,yerr,beta0)
        regs[i] = adjust

        if errorbars:
            plt.errorbar(x,y, xerr=xerr, yerr=yerr, c=color, fmt="o", label=legends[i])
        else:
            plt.scatter(x,y, c=color, label=legends[i])
        xLin = np.linspace(np.min(x),np.max(x),50)
        yLin = lin(adjust.beta, xLin)
        if regressions:
            plt.plot(xLin,yLin, c=color, label=getPolynomialLabel2(adjust.beta,adjust.sd_beta, xlabel,ylabel))

    plt.title(title)
    plt.xlabel(rf"${xlabel}$")
    plt.ylabel(rf"${ylabel}$")
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.legend()
    plt.grid()
    plt.show()

    return regs


def plotColumnReg(xs,ys,xerrs,yerrs,titles,xlabels,ylabels,func,beta0=[1,1],tol=1):


    fig, axs = plt.subplots(len(xs),2,figsize=(18,len(xs)*7))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    axsIter = iter(axs.flat)
    adjusts = []

    if isinstance(xlabels, str):
        xlabels = [xlabels] * len(xs)
    if isinstance(ylabels, str):
        ylabels = [ylabels] * len(xs)


    for i in range(0,len(xs)):
        x=xs[i]
        y=ys[i]
        xerr=xerrs[i]
        yerr=yerrs[i]
        title = titles[i]
        xlabel = xlabels[i]
        ylabel = ylabels[i]
        ax = next(axsIter)


        if isinstance(xerr,(int,float)):
            xerr = np.full(len(x),xerr)
        if isinstance(yerr,(int,float)):
            yerr = np.full(len(y),yerr)

        adjust = getAdjust(func,x,y,xerr,yerr,beta0)

        res = y - x*adjust.beta[0] - adjust.beta[1]

        stdy = np.std(res)*tol

        yTrue = y[abs(res) < stdy]
        yFalse = y[abs(res) > stdy]

        xTrue = x[abs(res) < stdy]
        xFalse = x[abs(res) > stdy]

        yerrTrue = yerr[abs(res) < stdy]
        xerrTrue = xerr[abs(res) < stdy]

        ax.errorbar(xTrue,yTrue, xerr=xerrTrue, yerr=yerrTrue, c="black", fmt="o", label="Pontos Experimentais")
        adjustTrue = getAdjust(func, xTrue, yTrue, xerrTrue, yerrTrue,beta0)
        adjusts.append(adjustTrue)
        if len(xFalse) == 0:
            x = np.linspace(min(xTrue), max(xTrue),100)
        else:
            x = np.linspace(min(min(xTrue),min(xFalse)), max(max(xTrue),max(xFalse)),100)

        y = func(adjustTrue.beta, x)
        ax.plot(x,y, c="orange", label=getPolynomialLabel2(adjustTrue.beta,adjustTrue.sd_beta, xlabel,ylabel))
        if len(xFalse) != 0:
            ax.plot(xFalse,yFalse, c="red", marker="o", ls="", label="Pontos Experimentais Rejeitados")

        ax.set_title(rf"${title}$")
        ax.set_xlabel(rf"${xlabel}$")
        ax.set_ylabel(rf"${ylabel}$")
        ax.legend()
        ax.grid()

        ax = next(axsIter)

        resTrue = yTrue - xTrue*adjust.beta[0] - adjust.beta[1]
        resFalse = yFalse - xFalse*adjust.beta[0] - adjust.beta[1]

        ax.axhline(0, c="black", alpha=0.5)
        ax.axhline(stdy, c="orange", label="Intervalo {}$\sigma$".format(tol))
        ax.axhline(-stdy, c="orange")
        ax.plot(xTrue,resTrue,c="black", marker="o", ls="", label="Pontos Experimentais")
        ax.plot(xFalse,resFalse,c="red", marker="o", ls="", label="Pontos Rejeitados")
        ax.set_xlabel(rf'${xlabel}$')
        ax.set_ylabel(rf"$Res \quad {ylabel}$")
        ax.set_title(fr"$Resíduos \quad {ylabel.split('(')[0]}$")
        ax.legend()
        ax.grid()
        
    return adjusts

def plot(xs,ys,xerrs=None,yerrs=None,title="Título",xlabel="x",ylabel="y", label="Dados", color="black",hlines=None):
    plt.figure(figsize=(12,8))
    if (xerrs == None).all() and (yerrs == None).all():
        plt.scatter(xs,ys,c=color, label=label)
    else:
        plt.errorbar(xs,ys,xerr=xerrs,yerr=yerrs, fmt="o", c=color, label=label)

    if hlines != None:
        for i in hlines:
            plt.axhline(i[0],color="red",label=i[1])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()
    