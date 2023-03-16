import pandas as pd
import numpy as np

# load in outliers dataframe
outliers = pd.read_csv("growth-advantage-comparisons.tsv", sep="\t")
outlier_variants = outliers['variant'].values
# load in accumulated mutations dataframe
mutations = pd.read_csv("accumulated_mutations_output.tsv", sep="\t")
mutation_variants = mutations['variant'].values
mutation_count = {}
# for every outlier
for variant in outlier_variants:
    # if outlier is variant in mutation
    if variant in mutation_variants:
        # mutation = mutation + region
        rows = mutations.loc[mutations['variant'] == variant]
        rows = rows.reset_index()
        for index, r in rows.iterrows():
            mutation = r['mutation'] + "_" + r['region']
            # else update value to get(key) + 1
            if mutation in mutation_count:
                mutation_count[mutation] = mutation_count[mutation] + 1
            #if key does not exist, add (mutation, 1)
            else:
                mutation_count.update({mutation:1})

# save dictionary as df
df = pd.DataFrame.from_dict(mutation_count, orient='index', columns = ['count'])
#grab top 10 mutations in dataframe
top_10 = df.nlargest(10, 'count')
top_10.to_csv('top_10_mutations.tsv', sep='\t')
df.to_csv('all_outlier_mutations.tsv', sep='\t')
