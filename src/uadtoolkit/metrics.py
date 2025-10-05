
import numpy as np, pandas as pd

def wavelength_discrimination(wl_1nm, RG_1nm, YB_1nm, criterion=4.0, max_step=60):
    def L1(i,j): return abs(RG_1nm[j]-RG_1nm[i]) + abs(YB_1nm[j]-YB_1nm[i])
    n=len(wl_1nm); d=np.full(n, np.nan)
    for i in range(n-1):
        hi=min(i+5, n-1)
        while L1(i,hi)<criterion and hi<min(i+max_step, n-1):
            hi=min(hi+5, n-1)
        if L1(i,hi)<criterion: continue
        lo=i
        while hi-lo>1:
            mid=(lo+hi)//2
            if L1(i,mid)>=criterion: hi=mid
            else: lo=mid
        d[i]=wl_1nm[hi]-wl_1nm[i]
    return pd.DataFrame({'wavelength_nm': wl_1nm, 'delta_lambda_nm': d})
