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
total_variants = growth_advantages.iloc[1]
first = True
#For every variant in the growth advantages output
for column in growth_advantages:
    # skip the first column because that is the index
    if first != True:
        series = growth_advantages[column]
        variant = series[1]
        #grab the child growth advantage in the growth advantage df
        child_growth_advantage = series[2]
        #look for its parent in the parent_relationships DataFrame
        if variant in parent_child_relationships['variant'].values:
            object = parent_child_relationships.index[parent_child_relationships['variant'] == variant]
            index = object[0]
            si = parent_child_relationships['parent']
            parent = si[index]
            if parent in total_variants.values:
                i = total_variants.values.tolist().index(parent)-1
                s = growth_advantages[str(i)]
                #grab the parent growth advantage in the growth advantage df
                parent_growth_advantage = s[2]
                #divide child/parent and append it to the output df
                ratio = float(child_growth_advantage)/float(parent_growth_advantage)
                rows_for_tsv.append({'variant': variant, 'parent': parent, 'child-ga':child_growth_advantage, 'parent-ga': parent_growth_advantage, 'variant-parent-ratio': ratio})
    first = False
df = pd.DataFrame(rows_for_tsv)
df.to_csv('child-parent-growth-advantages.tsv', sep='\t')
