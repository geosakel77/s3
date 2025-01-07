import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def prepare_data(data):
    org_mean_values={}
    org_values_per_landscape={}
    org_cti_products_mean_values={}
    org_cti_products_values_per_landscape={}
    for key in data:
        organization_data = data[key]
        org_mean_values[key]=[]
        org_values_per_landscape[key]=[]
        org_cti_products_mean_values[key] = {}
        org_cti_products_values_per_landscape[key] = {}
        for key1 in organization_data:
            org_mean_values[key].append(organization_data[key1][0])
            org_cti_products_mean_values[key][key1] = organization_data[key1][0]
            org_values_per_landscape[key].append(organization_data[key1][1])
            org_cti_products_values_per_landscape[key][key1] = organization_data[key1][1]
    for key in org_mean_values:
        print(f"{key}: {org_mean_values[key]}")
        print(f"{key}: {org_values_per_landscape[key]}")
        print(f"{key}: {org_cti_products_mean_values[key]}")
        print(f"{key}: {org_cti_products_values_per_landscape[key]}")
    return org_mean_values, org_values_per_landscape, org_cti_products_mean_values, org_cti_products_values_per_landscape


def plot_violin(data_dict, filename,title="Set Diagrams Title",):
    """
    Plots a violin plot for multiple groups given as a dictionary.

    Parameters:
    - data_dict: dict
        A dictionary where keys are group names and values are lists of data points.
    - title: str
        Title of the plot (default is "Violin Plot for Groups").
    """
    # Convert dictionary to a DataFrame
    data = pd.DataFrame({
        'Value': [value for group in data_dict.values() for value in group],
        'Organizations': [group for group, values in data_dict.items() for _ in values]
    })

    # Create violin plot
    plt.figure(figsize=(8, 6))
    sns.violinplot(x='Organizations', y='Value', data=data,legend=False)
    plt.title(title, fontsize=14)
    plt.xlabel('Organizations', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(filename)
    plt.show()
    plt.close()

