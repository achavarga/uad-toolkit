
import argparse, os, pandas as pd, matplotlib.pyplot as plt
from .uad import preprocess_table, make_uad_spline_1nm, find_unique_hues
from .metrics import wavelength_discrimination

def cmd_from_csv(args):
    df = pd.read_csv(args.input)
    wl, RG, YB = preprocess_table(df)
    wl1, RG1, YB1 = make_uad_spline_1nm(wl, RG, YB, args.min, args.max)
    unique = find_unique_hues(wl1, RG1, YB1)
    disc = wavelength_discrimination(wl1, RG1, YB1, criterion=args.criterion)

    os.makedirs(os.path.dirname(args.out), exist_ok=True) if os.path.dirname(args.out) else None
    pd.DataFrame({'wavelength_nm': wl1, 'RG': RG1, 'YB': YB1}).to_csv(args.out+'_uad_1nm.csv', index=False)
    disc.to_csv(args.out+'_discrimination.csv', index=False)

    plt.figure()
    plt.plot(RG1, YB1); plt.axhline(0, ls='--'); plt.axvline(0, ls='--')
    for k,v in unique.items():
        j = abs(wl1 - v).argmin()
        plt.scatter(RG1[j], YB1[j]); plt.text(RG1[j], YB1[j], k.replace('_nm',''), fontsize=8)
    plt.xlabel('RG'); plt.ylabel('YB'); plt.title('UAD (1-nm spline)'); plt.tight_layout()
    plt.savefig(args.out+'_uad_trajectory.png', dpi=150)

    plt.figure()
    plt.plot(disc['wavelength_nm'], disc['delta_lambda_nm'])
    plt.xlabel('Wavelength (nm)'); plt.ylabel(f'Δλ (city-block ≥ {args.criterion:.2f})')
    plt.title('Wavelength discrimination'); plt.tight_layout()
    plt.savefig(args.out+'_discrimination.png', dpi=150)

    print("Unique hues (nm):", {k: round(v,2) for k,v in unique.items()})
    print("Saved files with prefix:", args.out)

def main():
    ap = argparse.ArgumentParser(prog="uad", description="Uniform Appearance Diagram toolkit")
    sub = ap.add_subparsers(dest="cmd")

    ap_csv = sub.add_parser("from-csv", help="Process a hue-scaling CSV")
    ap_csv.add_argument("input", help="Path to CSV file")
    ap_csv.add_argument("--out", default="out/uad", help="Output prefix (dir/prefix)")
    ap_csv.add_argument("--criterion", type=float, default=4.0, help="City-block threshold for Δλ")
    ap_csv.add_argument("--min", type=float, default=None, help="Minimum wavelength to evaluate (nm)")
    ap_csv.add_argument("--max", type=float, default=None, help="Maximum wavelength to evaluate (nm)")
    ap_csv.set_defaults(func=cmd_from_csv)

    args = ap.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        ap.print_help()
