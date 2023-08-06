from typing import Callable, Tuple, List, Optional, Union
import numpy as np
import numpy.typing as npt
import pandas as pd

def generateCrossSection(
        func: Callable[[float], float],
        ranges: List[float],
        nbins: List[int],
        file: Optional[str] = None
        ) -> Tuple[npt.NDArray, npt.NDArray]:
    """Function used to generate tabulated functions for the use as 
    cross-section data. Data is tabulated for the x-axis.

    Args: 
        func (Callable) : Mathemathical callable in the form func(x) -> y,
            where x is in eV and y is returned as A^2.
        ranges (List[float]) : Ranges, starts from 0.
        nbins (List[int]) : Number of bins for every range.

    Returns:
        npt.NDArray : numpy.ndarray (x, y).
    """
     
    dx = np.zeros(len(ranges))
    xarr = []
    for i in range(len(ranges)):
        if i == 0:
            dx[i] = ranges[i]/nbins[i]
        else:
            dx[i] = (ranges[i] - ranges[i-1])/nbins[i]
        for j in range(nbins[i]):
            if i == 0:
                xarr.append(j*dx[i])
            else:
                xarr.append(j*dx[i] + ranges[i-1])
    nparr = np.zeros((2, len(xarr)), dtype=np.float64)
    for i in range(len(xarr)):
        nparr[0, i] = xarr[i]
        nparr[1, i] = func(xarr[i])

    if file != None:
        with open(file, 'w') as f:
            f.write(f"# ranges = {ranges}\n")
            f.write(f"# nbins = {nbins}\n")
        pd.DataFrame(nparr).transpose().to_csv(file, index=False, header=False, mode='a', float_format="%.16e")
    
    return nparr


