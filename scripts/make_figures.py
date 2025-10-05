
import os, pandas as pd, matplotlib.pyplot as plt
from uadtoolkit.uad import preprocess_table, make_uad_spline_1nm, find_unique_hues
from uadtoolkit.metrics import wavelength_discrimination

infile = "examples/huescalingdata.csv"
outprefix = "out/obs01"
os.makedirs("out", exist_ok=True)

df = pd.read_csv(infile)
wl, RG, YB = preprocess_table(df)
wl1, RG1, YB1 = make_uad_spline_1nm(wl, RG, YB, 330, 660)
uniq = find_unique_hues(wl1, RG1, YB1)
disc = wavelength_discrimination(wl1, RG1, YB1, criterion=4.0)

pd.DataFrame({'wavelength_nm': wl1, 'RG': RG1, 'YB': YB1}).to_csv(outprefix+'_uad_1nm.csv', index=False)
disc.to_csv(outprefix+'_discrimination.csv', index=False)

plt.figure()
plt.plot(RG1, YB1); plt.axhline(0, ls='--'); plt.axvline(0, ls='--')
for k,v in uniq.items():
    j = abs(wl1 - v).argmin()
    plt.scatter(RG1[j], YB1[j]); plt.text(RG1[j], YB1[j], k.replace('_nm',''), fontsize=8)
plt.xlabel('RG'); plt.ylabel('YB'); plt.title('UAD (1-nm spline)'); plt.tight_layout()
plt.savefig(outprefix+'_uad_trajectory.png', dpi=150)

plt.figure()
plt.plot(disc['wavelength_nm'], disc['delta_lambda_nm'])
plt.xlabel('Wavelength (nm)'); plt.ylabel('Δλ (city-block ≥ 4)')
plt.title('Wavelength discrimination'); plt.tight_layout()
plt.savefig(outprefix+'_discrimination.png', dpi=150)

print("Done. Outputs in:", os.path.abspath("out"))
