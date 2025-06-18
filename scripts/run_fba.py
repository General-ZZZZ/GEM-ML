import cobra
import pandas as pd
import numpy as np

model = cobra.io.read_sbml_model("../models/iML1515_muconic.xml")

model.objective = "BIOMASS_Ec_iML1515_WT_53p95M"
mu_ex = model.reactions.get_by_id("EX_muconate_e")
mu_ex.lower_bound = 0
mu_ex.upper_bound = 1000

results = []
for glc in np.linspace(-5, -20, 16):
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = glc
    sol = model.optimize()
    results.append({
        "glc_uptake": -glc,
        "growth_rate": sol.objective_value,
        "moconate_rate": sol.fluxes[mu_ex.id]
    })

pd.DataFrame(results).to_csv("../data/fba_data.csv", index=False)
print("FBA 数据已保存：data/fba_data.csv")
