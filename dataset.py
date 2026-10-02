import numpy as np
from scipy.odr import RealData, Model, ODR

try:
    from .functions import lin, quadratic
except ImportError:
    from functions import lin, quadratic

class DataSet:
    """
    Classe que representa um conjunto de dados experimentais, com incertezas,
    rótulos para gráficos e ajuste ODR (scipy) calculado automaticamente.
    """
    def __init__(self, x, y, ux, uy, titulo, labelx, labely, fit_type=lin, beta0=None):
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        
        if isinstance(ux, (int, float)):
            self.ux = np.full(len(self.x), float(ux))
        else:
            self.ux = np.array(ux, dtype=float)
            
        if isinstance(uy, (int, float)):
            self.uy = np.full(len(self.y), float(uy))
        else:
            self.uy = np.array(uy, dtype=float)
            
        self.titulo = titulo
        self.labelx = labelx
        self.labely = labely
        self.fit_type = fit_type
        
        self.adjust = self.calculate_adjust(beta0)
        
    def calculate_adjust(self, beta0=None):
        if beta0 is None:
            if self.fit_type == quadratic:
                beta0 = [1, 1, 1]
            else:
                beta0 = [1, 1]
        mod = Model(self.fit_type)
        data1 = RealData(self.x, self.y, self.ux, self.uy)
        odr = ODR(data1, mod, beta0)
        return odr.run()

    def __repr__(self):
        return f"<DataSet '{self.titulo}': len={len(self.x)}, fit={self.fit_type.__name__}>"

# Alias para flexibilidade de escrita
Dataset = DataSet
