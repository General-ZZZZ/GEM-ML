import cobra
from cobra import Reaction, Metabolite

model = cobra.io.load_model("../models/iML1515.xml")

# 1) add DHSA_dehydratase
dhsa = Reaction("DHSA_dehydratase")
dhsa.name = "3-dehydroshikimate dehydratase"
dhsa.add_metabolites({
    model.metabolites.get_by_id("dhsa_c"): -1.0,
    model.metabolites.get_by_id("pca_c"): 1.0
})
dhsa.gene_reaction_rule = "hetero_DHSA_gene"
model.add_reactions([dhsa])

# 2) add PCA_decarboxylase
pca = Reaction("PCA_decarboxylase")
pca.name = "protocatechuate decarboxylase"
pca.add_metabolites({
    model.metabolites.get_by_id("pca_c"): -1.0,
    model.metabolites.get_by_id("catechol_c"): 1.0
})
pca.gene_reaction_rule = "hetero_PCA_gene"
model.add_reactions([pca])

# 3) add Catechol_dioxygenase
