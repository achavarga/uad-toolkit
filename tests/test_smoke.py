
import pandas as pd
from uadtoolkit.uad import preprocess_table, make_uad_spline_1nm, find_unique_hues
from uadtoolkit.metrics import wavelength_discrimination

def test_pipeline_smoke():
    df = pd.DataFrame({
        "Lambda (nm)": [430, 440, 450, 460],
        "% Red": [20, 22, 18, 15],
        "% Yellow": [0, 0, 5, 10],
        "% Green": [10, 20, 30, 40],
        "% Blue": [70, 58, 47, 35],
        "% Saturation": [100, 95, 90, 85]
    })
    wl, RG, YB = preprocess_table(df)
    wl1, RG1, YB1 = make_uad_spline_1nm(wl, RG, YB, 430, 460)
    uniq = find_unique_hues(wl1, RG1, YB1)
    disc = wavelength_discrimination(wl1, RG1, YB1, criterion=4.0)
    assert len(wl1) == (460-430+1)
    assert 'wavelength_nm' in disc.columns
