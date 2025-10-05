
import numpy as np, pandas as pd
from .transforms import arcsin_sqrt, running_average
from .spline import NaturalCubicSpline

def preprocess_table(df):
    lc = {c.lower(): c for c in df.columns}
    def get(*names):
        for n in names:
            if n in lc: return lc[n]
        return None
    col_wl = get("lambda (nm)","wavelength_nm","wavelength","nm","λ","lambda")
    col_r  = get("% red","frac_red","red","r")
    col_y  = get("% yellow","frac_yellow","yellow","y")
    col_g  = get("% green","frac_green","green","g")
    col_b  = get("% blue","frac_blue","blue","b")
    col_s  = get("% saturation","saturation","sat","chroma","%saturation")
    if not all([col_wl, col_r, col_y, col_g, col_b]):
        raise ValueError("Missing required columns")
    wl = df[col_wl].astype(float).to_numpy()
    R = df[col_r].astype(float).to_numpy()
    Y = df[col_y].astype(float).to_numpy()
    G = df[col_g].astype(float).to_numpy()
    B = df[col_b].astype(float).to_numpy()
    if max(R.max(),Y.max(),G.max(),B.max()) > 1.5:
        R/=100.0; Y/=100.0; G/=100.0; B/=100.0
    if col_s:
        S = df[col_s].astype(float).to_numpy()
        if S.max() > 1.5: S/=100.0
        S = np.clip(S, 0.0, 1.0)
    else:
        S = np.ones_like(wl)
    Rt, Yt, Gt, Bt = [arcsin_sqrt(v) for v in (R,Y,G,B)]
    Rt*=S; Yt*=S; Gt*=S; Bt*=S
    denom = Rt+Yt+Gt+Bt; denom[denom==0]=1.0
    Rt, Yt, Gt, Bt = Rt/denom, Yt/denom, Gt/denom, Bt/denom
    RG = Rt - Gt
    YB = Yt - Bt
    idx = np.argsort(wl)
    return wl[idx], RG[idx], YB[idx]

def make_uad_spline_1nm(wl_10nm, RG_10nm, YB_10nm, wl_min=None, wl_max=None):
    RG_sm = running_average(RG_10nm); YB_sm = running_average(YB_10nm)
    sRG = NaturalCubicSpline(wl_10nm, RG_sm); sYB = NaturalCubicSpline(wl_10nm, YB_sm)
    lo = wl_10nm.min() if wl_min is None else wl_min
    hi = wl_10nm.max() if wl_max is None else wl_max
    wl_1nm = np.arange(int(round(lo)), int(round(hi))+1, 1)
    RG_1nm = sRG.evaluate(wl_1nm); YB_1nm = sYB.evaluate(wl_1nm)
    return wl_1nm, RG_1nm, YB_1nm

def find_unique_hues(wl_1nm, RG_1nm, YB_1nm):
    out = {}
    def zeros(x, y):
        s = np.sign(y); idx = np.where(s[:-1]*s[1:] < 0)[0]; roots=[]
        for i in idx:
            x0,x1,y0,y1 = x[i],x[i+1],y[i],y[i+1]
            t = -y0/(y1-y0); roots.append(x0 + t*(x1-x0))
        return roots
    for z in zeros(wl_1nm, RG_1nm):
        yb = np.interp(z, wl_1nm, YB_1nm)
        if yb > 0: out["unique_yellow_nm"] = z
        elif yb < 0: out["unique_blue_nm"] = z
    for z in zeros(wl_1nm, YB_1nm):
        rg = np.interp(z, wl_1nm, RG_1nm)
        if rg > 0: out["unique_red_nm"] = z
        elif rg < 0: out["unique_green_nm"] = z
    return out
