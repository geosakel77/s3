import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from openai import organization
from stix2validator import print_results


def prepare_data_rel(data):
    org_mean_values={}
    org_values_per_landscape={}
    org_cti_products_mean_values={}
    org_cti_products_values_per_landscape={}
    for key in data.keys():
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
    return org_mean_values, org_values_per_landscape, org_cti_products_mean_values, org_cti_products_values_per_landscape

def prepare_data_act(data):
    org_mean_values_per_product = {}
    org_values_per_def_mechanism = {}
    org_cti_products_mean_values = {}
    org_cti_products_values_per_def_mechanism = {}
    for key in data.keys():
        organization_data = data[key]
        org_mean_values_per_product[key] = []
        org_values_per_def_mechanism[key] = []
        org_cti_products_mean_values[key] = {}
        org_cti_products_values_per_def_mechanism[key] = {}
        for key1 in organization_data.keys():
            org_mean_values_per_product[key].append(organization_data[key1][0])
            org_cti_products_mean_values[key][key1] = organization_data[key1][0]
            org_values_per_def_mechanism[key].append(organization_data[key1][1])
            org_cti_products_values_per_def_mechanism[key][key1] = organization_data[key1][1]

    return org_mean_values_per_product, org_values_per_def_mechanism, org_cti_products_mean_values, org_cti_products_values_per_def_mechanism

def clean_data(data):
    products=[]
    for key in data.keys():
        products= data[key].keys()
        break
    data_cleaned={}
    counter=0
    for key in data.keys():
        data_cleaned[key] = {}

    for pr in products:
        flag=False
        occur=0
        for key in data.keys():
            if data[key][pr]>0.00525:
                flag=True
                occur=occur+1
        if flag and occur>9:
            counter=counter+1
            for key1 in data.keys():
                data_cleaned[key1][f"P{counter}"]=data[key1][pr]
    print(len(products))
    print(counter)
    return data_cleaned


def plot_products_rel_comparison(data_dict_init,filename='default',title="Set Diagrams Title"):
    data_dict=clean_data(data_dict_init)
    data = pd.DataFrame({
        'Organization':[org for org, values in data_dict.items() for _ in values.items()],
        'Products':[prd for org,values in data_dict.items() for prd,val in values.items()],
        'Relevance':[val for org,values in data_dict.items() for prd,val in values.items()],
    })

    graph=sns.FacetGrid(data, col="Organization", aspect=1.5,col_wrap=3)
    graph.map(sns.scatterplot, "Products", "Relevance")
    plt.tight_layout()
    plt.show()





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

