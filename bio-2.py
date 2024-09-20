
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Generate synthetic data with more pronounced differences
def generate_synthetic_data(n_genes=1000, n_samples=6):
    np.random.seed(42)
    gene_names = [f'gene_{i}' for i in range(n_genes)]
    sample_names = ['control1', 'controlz', 'control3', 'treatment1', 'treatment2', 'treatment3']
    data = np.random.negative_binomial (20, 0.3, size=(n_genes, n_samples))
    # Introduce more pronounced differential expression
    effect_size = 5 # Increased from 2 to 5
    for i in range(n_genes // 5): # 20% of genes are differentially expressed (increased from 10%) 
        if i % 2 == 0:
            data[i, 3:] *= effect_size # up-regulated in treatment
        else:
            data[i, 3:]= np.maximum (data[i, 3:] // effect_size, 1) # down-regulated in treatment, ensure minimum count of 1
    return pd.DataFrame(data, index=gene_names, columns=sample_names)

# Generate synthetic data
data = generate_synthetic_data()

# Step 2: Normalize the data
def cpm(counts):
    return counts (counts.sum() / 1e6)

normalized_data = data.apply(cpm, axis=0)

# Step 3: Log transform the data
log_data = np.log2 (normalized_data + 1) # Add 1 to avoid log(0)

# Step 4: Define groups
control_samples = ['control1', 'control2', 'control3']
treatment_samples = ['treatment1', 'treatment2', 'treatment3']

# Step 5: Perform differential expression analysis
def differential_expression (data, group1, group2):
    results = []
    for gene in data.index:
        t_stat, p_value = stats.ttest_ind(data.loc[gene, group1], data.loc[gene, group2])
        log2_fold_change = np.log2((data.loc[gene, group2].mean() + 1) / (data.loc[gene, group1].mean() + 1)) 
        results.append([gene, log2_fold_change, p_value])
    return pd.DataFrame (results, columns=['Gene', 'Log2FoldChange', 'PValue'])

de_results = differential_expression(log_data, control_samples, treatment_samples)

# Step 6: Adjust p-values for multiple testing using Benjamini-Hochberg procedure 
def benjamini_hochberg_correction(p_values):
    n = len(p_values)
    ranked_p_values = stats.rankdata(p_values)
    adjusted_p_values = p_values * n / ranked_p_values
    return np.minimum(adjusted_p_values, 1.0) # ensure no adjusted p-value exceeds 1

de_results['AdjustedPValue'] = benjamini_hochberg_correction (de_results[ 'PValue'])

# Step 7: Calculate log10(PValue) for plotting
de_results['-log10(PValue)'] = np.log10(de_results['PValue'])

# Step 8: Filter significant genes (adjusted criteria)
significant_genes
de_results[(de_results['AdjustedPValue'] < 0.1) & (abs(de_results['Log2FoldChange']) > 0.5)]

# Step 9: Visualize results
plt.figure(figsize=(10, 6))
sns.scatterplot(data=de_results, x='Log2FoldChange', y='-log10(PValue)',
hue=(de_results['AdjustedPValue'] < 0.1) & (abs (de_results['Log2FoldChange']) > 0.5))
plt.title('Volcano Plot of Differential Expression')
plt.savefig('volcano_plot.png')
plt.close()

# Print top differentially expressed genes
print(significant_genes.sort_values('AdjustedPValue').head (10))

# Save results to file
de_results.to_csv('differential_expression_results.csv')

# Print summary statistics
print("\nTotal number of genes: [len (de_results)}")
print (f"Number of significant genes: (len(significant_genes)")
print("Percentage of significant genes: (len(significant_genes) / len(de_results) * 100:.2f}%")
