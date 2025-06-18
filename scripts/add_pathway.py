import cobra
from cobra import Reaction, Metabolite

model = cobra.io.load_model("iML1515")

cat = model.metabolites.get_by_id("catechol_c")
print(cat.id, cat.name, cat.formula, cat.compartment, cat.compartment_id)
# 1) add DHSA_dehydratase
dhsa = Reaction("DHSA_dehydratase")
dhsa.name = "3-dehydroshikimate dehydratase"
dhsa.add_metabolites({
    model.metabolites.get_by_id("3dhsk_c"): -1.0,
    model.metabolites.get_by_id("34dphacoa_c"): 1.0
})
dhsa.gene_reaction_rule = "hetero_DHSA_gene"
model.add_reactions([dhsa])

# 2) add PCA_decarboxylase
pca = Reaction("PCA_decarboxylase")
pca.name = "protocatechuate decarboxylase"
pca.add_metabolites({
    model.metabolites.get_by_id("34dphacoa_c"): -1.0,
    model.metabolites.get_by_id("catechol_c"): 1.0
})
pca.gene_reaction_rule = "hetero_PCA_gene"
model.add_reactions([pca])

# 3) add Catechol_dioxygenase
cat = Reaction("Catechol_dioxygenase")
cat.name = "catachol 1,2-dioxygenase"
cat.add_metabolites({
    model.metabolites.get_by_id("catechol_c"): -1.0,
    model.metabolites.get_by_id("o2_c"): -1.0,
    model.metabolites.get_by_id("muconate_c"): 1.0
})
cat.gene_reaction_rule = "hetero_CAT_gene"
model.add_reactions([cat])

# save model
model.write_sbml_model("../models/iML1515_muconic.xml")
print("已生成模型：models/iML1515_muconic.xml")
