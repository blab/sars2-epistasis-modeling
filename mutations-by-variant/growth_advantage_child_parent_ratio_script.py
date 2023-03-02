import pandas as pd
import numpy as np
import string

# growth advantage dataframe structure is:
  # count
  # strain_name
  # fitness
growth_advantages = pd.read_csv('mutational_growth_advantages.tsv', sep='\t')
parent_child_relationships = pd.read_csv('pango_variant-relationships.tsv', sep='\t')
rows_for_tsv = []
parent_child_relationships_children = parent_child_relationships['variant']
variants = growth_advantages['variant']

#For every variant in the growth advantages output
for ind in growth_advantages.index:
    child = growth_advantages['variant'][ind]
    child_ga = growth_advantages['median_ga'][ind]
    if child in parent_child_relationships_children.values:
        child_index_obj = parent_child_relationships.index[parent_child_relationships['variant'] == child]
        child_index = child_index_obj[0]
        parent = parent_child_relationships['parent'][child_index]
        if parent in variants.values:
            parent_index_obj = growth_advantages.index[growth_advantages['variant'] == parent]
            parent_index = parent_index_obj[0]
            parent_ga = growth_advantages['median_ga'][parent_index]
            ratio = float(child_ga)/float(parent_ga)
            rows_for_tsv.append({'variant': child, 'parent': parent, 'child-ga':child_ga, 'parent-ga': parent_ga, 'variant-parent-ratio': ratio})
df = pd.DataFrame(rows_for_tsv)
df.to_csv('child-parent-growth-advantages-2.tsv', sep='\t')
