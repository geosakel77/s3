"""
<Cyber Threat Intelligence Relevance and Actionability Quality Metrics Implementation.>
    Copyright (C) 2025  Georgios Sakellariou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import random
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean


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

def clean_data(data,min_value=0.005):
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
            if data[key][pr]>=min_value:
                flag=True
                occur=occur+1
        if flag and occur>9:
            counter=counter+1
            for key1 in data.keys():
                data_cleaned[key1][f"P{counter}"]=data[key1][pr]
    print(len(products))
    print(counter)
    return data_cleaned, len(data.keys())

def data_to_dataframe(data_dict_init,metric, min_value,frame_type=1):
    data=None
    wrap_val=None
    if frame_type == 1:
        data_dict, wrap_val = clean_data(data_dict_init, min_value)
        data = pd.DataFrame({
            'Organization': [org for org, values in data_dict.items() for _ in values.items()],
            'Products': [prd for org, values in data_dict.items() for prd, val in values.items()],
            metric: [val for org, values in data_dict.items() for prd, val in values.items()],
        })
    elif frame_type == 2:
        if metric == 'Relevance':
            landscapes=['L1','L2','L3']
            data_dict, wrap_val = clean_data_ext(data_dict_init, min_value)
            data = pd.DataFrame({
                'Organization': [org for org, values in data_dict.items() for prd, val in values.items() for _ in range(len(val))],
                'Products': [prd for org, values in data_dict.items() for prd, val in values.items() for _ in range(len(val))],
                'Landscape':[landscapes[i] for org, values in data_dict.items() for prd, val in values.items() for i in range(len(val))],
                metric: [val[i] for org, values in data_dict.items() for prd, val in values.items() for i in range(len(val))],
            })
        elif metric == 'Actionability':
            data_dict, wrap_val = clean_data_ext(data_dict_init, min_value)
            key = random.choice(list(data_dict.keys()))
            print("Selected organisation {}".format(key))
            data_dict_chosen = data_dict[key]
            dm_num=None
            for prd in data_dict[key].keys():
                dm_num = len(data_dict[key][prd])
                break
            def_mec=[]
            for i in range(dm_num):
                def_mec.append(f"DF{i}")

            data = pd.DataFrame({
                'Defence Mechanism': [def_mec[i] for prd, values in data_dict_chosen.items() for i in range(len(values))],
                'Products': [prd for prd, values in data_dict_chosen.items() for _ in range(len(values))],
                metric: [values[i] for prd, values in data_dict_chosen.items() for i in range(len(values))]
            })
            wrap_val=dm_num
    return data,wrap_val

def plot_grid(data,col,metric,x_ax,col_wrap,title,filename,aspect=1.5):
    graph = sns.FacetGrid(data, col=col, hue=metric, aspect=aspect, col_wrap=col_wrap)
    graph.map(sns.scatterplot, x_ax, metric)
    graph.set_xticklabels("")
    #plt.title(title)
    plt.savefig(filename)
    plt.tight_layout()
    plt.show()

def plot_grid_1(data,col,metric,landscape,x_ax,col_wrap,filename,aspect=1.5):
    graph = sns.FacetGrid(data, col=col, hue=landscape, aspect=aspect, col_wrap=col_wrap)
    graph.map(sns.barplot, x_ax, metric,order=['L1','L2','L3'])
    graph.set_xticklabels("")
    plt.savefig(filename)
    plt.tight_layout()
    plt.show()

def plot_products_metric_comparison(data_dict_init,min_value,metric,filename='default',title="Set Diagrams Title"):
    data,wrap_val = data_to_dataframe(data_dict_init,metric,min_value=min_value)
    plot_grid(data,col="Organization",metric=metric,col_wrap=int(wrap_val / 2),title=title,filename=filename,x_ax="Products")

def plot_distributions_violin(data_dict_init,metric,min_value,filename='default',size=1.5,title="Set Diagrams Title"):
    data, wrap_val =data_to_dataframe(data_dict_init,metric,min_value=min_value)
    graph = sns.catplot(data,x='Organization', y=metric, kind='violin',inner='box')
    sns.swarmplot(data,x='Organization', y=metric, color='r',size=size, ax=graph.ax)
    #plt.title(title)
    plt.savefig(filename)
    plt.tight_layout()
    plt.show()

def clean_data_ext(data,min_value=0.005):
    products = []
    for key in data.keys():
        products = data[key].keys()
        break

    data_cleaned = {}
    counter = 0
    for key in data.keys():
        data_cleaned[key] = {}

    for pr in products:
        flag = False
        occur = 0
        for key in data.keys():
            if mean(data[key][pr]) >= min_value:
                flag = True
                occur = occur + 1
        if flag and occur > 9:
            counter = counter + 1
            for key1 in data.keys():
                data_cleaned[key1][f"P{counter}"] = data[key1][pr]
    print(len(products))
    print(counter)
    return data_cleaned, len(data.keys())


def plot_bar_distribution(data_dict_init,metric,min_value,frame_type,filename='default',size=1.5,title="Set Diagrams Title",):
    data, wrap_val =data_to_dataframe(data_dict_init,metric,min_value=min_value,frame_type=frame_type)
    if metric == 'Relevance':
        plot_grid_1(data,col="Organization",metric=metric,landscape='Landscape',x_ax='Landscape',col_wrap=int(wrap_val/2),filename=filename)
    elif metric == 'Actionability':
        plot_grid(data,col="Defence Mechanism",metric=metric,col_wrap=int(wrap_val / 2),title=title,filename=filename,x_ax="Products")
