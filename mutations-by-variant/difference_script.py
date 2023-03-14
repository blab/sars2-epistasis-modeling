import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

growth_advantages = pd.read_csv('child-parent-growth-advantages.tsv', sep='\t')
innovation_ga = pd.read_csv('mlr_innovation_growth_advantages.tsv', sep='\t')
rows_for_tsv = []
# Base Node is BA.2.1 in this case
BASE_NODE_GA = 1.0614669
innovation_variants = innovation_ga['variant']
ga_variants = growth_advantages['variant']

for variant in ga_variants:
  if variant in innovation_variants.values:
    s1 = innovation_ga.loc[innovation_variants == variant]['median_ga']
    innovation_num = s1.item()
    s2 = growth_advantages.loc[growth_advantages['variant'] == variant]['variant-parent-ratio']
    mutation_ga = s2.item()/BASE_NODE_GA
    division_result = mutation_ga/innovation_num
    # outputing absolute value of difference
    difference_result = abs(mutation_ga - innovation_num)
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
new_df = df[['difference', 'variant']]
subtract_names =new_df.to_dict('records')
name = list(df['variant'])
subtract = list(df['difference'])
quotient = list(df['division'])
colors = ['blue']
names=['DIFF_SUB,DIFF_QUO']
x = [0] * len(subtract)
#plt.hist([subtract, quotient], color=colors, label=names,  density = True, stacked = True)
plt.scatter(subtract,quotient, color=colors, label=names)
plt.plot(np.unique(subtract), np.poly1d(np.polyfit(subtract, quotient, 1))(np.unique(subtract)))
for i in range(len(subtract)):
    plt.annotate(name[i], (subtract[i],quotient[i]))
# Set the legend and labels
plt.legend()
plt.title('Scatter for Mutational_GA by Innovation_GA')
plt.xlabel('Variant Growth Advantages')
plt.savefig('ga-histogram-both.pdf')

a,b = np.polyfit(subtract, quotient, 1)
yfit = []
delta_fit =[]

for i in range(len(subtract)):
    yfit.append(a*subtract[i] + b)
    delta_fit.append({'variant': name[i], "delta_y": abs(yfit[i]-subtract[i])})

rows_for_tsv_top_10 = []
for i in range(len(delta_fit)):
    row = delta_fit[i]
    rows_for_tsv_top_10.append({'variant': row['variant'], 'diff from line': row['delta_y']})

df = pd.DataFrame(rows_for_tsv_top_10)
top_10 = df.nlargest(10, 'diff from line')
top_10.to_csv('top_10_outliers.tsv', sep='\t')
