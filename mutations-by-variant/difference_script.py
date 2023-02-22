import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

growth_advantages = pd.read_csv('child_parent_growth_advantages.tsv', sep='\t')
innovation_ga = pd.read_csv('mlr_innovation_growth_advantages.tsv', sep='\t')
rows_for_tsv = []
# Base Node is BA.2 in this case
BASE_NODE_GA = -0.07345003
innovation_variants = innovation_ga['variant']
ga_variants = growth_advantages['variant']

for variant in ga_variants:
  if variant in innovation_variants.values:
    s1 = innovation_ga.loc[innovation_variants == variant]['median_ga']
    innovation_num = s1.item()
    s2 = growth_advantages.loc[growth_advantages['variant'] == variant]['variant-parent-ratio']
    mutation_ga = s2.item()/BASE_NODE_GA
    division_result = mutation_ga/innovation_num
    difference_result = mutation_ga - innovation_num
    rows_for_tsv.append({'variant': variant, 'division': division_result, 'difference':difference_result})

# compiling total output
df = pd.DataFrame(rows_for_tsv)
df.to_csv('mutation_innovation_comparison.tsv', sep='\t')

# finding outliers
q1=df.quantile(0.25)
q3=df.quantile(0.75)
IQR=q3-q1

diff_iqr = IQR['difference']
div_iqr = IQR['division']

diff_outliers =df[((df['difference'] < (q1['difference']-1.5*diff_iqr)) | ( df['difference'] >(q3['difference']+1.5*diff_iqr)))]
div_outliers = df[((df['division'] < (q1['division']-1.5*div_iqr)) | ( df['division'] >(q3['division']+1.5*div_iqr)))]

diff_outliers.drop(columns = 'division').to_csv('difference-outliers.tsv', sep='\t')
div_outliers.drop(columns = 'difference').to_csv('division-outliers.tsv', sep='\t')


# plotting histogram of differences
subtract = list(df['difference'])
quotient = list(df['division'])
colors=['blue', 'green']
names=['DIFF_SUB', 'DIFF_DIV']
plt.hist([subtract, quotient], color=colors, label=names,  density = True, stacked = True)

# Set the legend and labels
plt.legend()
plt.title('Stacked Histogram for Growth Advantage Differences')
plt.xlabel('Variant Growth Advantages')
plt.savefig('ga-histogram.pdf')
