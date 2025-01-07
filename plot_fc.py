import pickle
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from mne_connectivity.viz import plot_connectivity_circle

# import mne
# from matplotlib.colors import Normalize
# from mne_connectivity.viz import plot_connectivity_circle

# Dataset
with open('./selected_data/selected_ANOVA_FC.pkl', 'rb') as f:
    anova_fc = pickle.load(f)  # (95, 19)

with open('./selected_data/selected_Scheffe_FC_revised.pkl', 'rb') as f:
    scheffe_fc = pickle.load(f)  # (285, 19) = (19*3*5, 19)   # AD vs CN, CN vs FTD, AD vs FTD



# Info
ch_names = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'Fz',
            'Cz', 'Pz']


# Prepare for plotting
cmap = 'seismic'
# anova_fc[anova_fc == 0] = 0.5  # Make color similar to white


# Create an empty circular graph
G = nx.Graph()

positions = {ch: (np.cos(2 * np.pi * i / len(ch_names)), np.sin(2 * np.pi * i / len(ch_names)))
             for i, ch in enumerate(ch_names)}


# Add nodes to the graph
for ch, pos in positions.items():
    G.add_node(ch, pos=pos)


# Define edges
def print_edge(data):
    edges = []
    for i in range(len(ch_names)):
        for j in range(len(ch_names)):
            if data[i, j] == 1:
                edges.append((ch_names[i], ch_names[j]))

    return edges


edges = print_edge(scheffe_fc[19*14:19*15, :])
data = anova_fc[19*4:19*5, :]

# # Add edges to the graph
# G.add_edges_from(edges)
#
# # Assign colors to nodes (all nodes in the same color for EEG)
# node_colors = ['RdBu'] * len(G.nodes())
#
# # Draw the graph
# plt.figure(figsize=(5, 5))
# # nx.draw(G, positions, node_color=range(19), node_size=500, edge_color='k', cmap=plt.cm.Blues)
# nx.draw_networkx_nodes(G, positions,
#                        # node_color=node_colors,
#                        node_size=500, edgecolors='k', node_color=range(19), cmap=plt.cm.RdBu_r)
# nx.draw_networkx_labels(G, positions, font_size=10, font_color='black')
# nx.draw_networkx_edges(G, positions, edgelist=edges, edge_color='gray', width=1)


# Save graph in eps
plt.axis('off')
# plt.show()
# plt.savefig('selected_fc_scheffe_1_0.eps', dpi=300)


# Save connectivity graph in eps
plt.figure(figsize=(5, 5))
cmap = 'seismic'
plot_connectivity_circle(data, ch_names, vmin=0, vmax=1,
                          n_lines=20, colormap=cmap, facecolor='white', textcolor='black', linewidth=1.5, colorbar=False, show=False)

# plt.show()
plt.savefig('selected_fc_anova_0_4.eps', dpi=300)



'''
# Scheffe-FC slicing

band 0
group 0 1 2

0.0 = 19*0 : 19*1
0.1 = 19*1 : 19*2
0.2 = 19*2: 19*3

1.0 = 19*3 : 19*4
1.1 = 19*4 : 19*5
1.2 = 19*5 : 19*6

...

4.0 = 19*12 : 19*13
4.1 = 19*13 : 19*14
4.2 = 19*14 : 19*15

=> 19* (band*3+ group) : 19* (band*3 + group+1)




# Plot for ANOVA-FC
def connectivity(data, vmin, vmax, n_lines, ax):
    return plot_connectivity_circle(data, ch_names, vmin=vmin, vmax=vmax, n_lines=n_lines, colormap=cmap, ax=axes[ax],
                                    facecolor='white', textcolor='black', linewidth=1.5, colorbar=False, show=False)


fig, axes = plt.subplots(1, 5,  facecolor='white', figsize=(10, 5), subplot_kw=dict(polar=True))
for band in range(5):
    connectivity(anova_fc[19*band:19*(band+1), :], 0, 1, 15, band)
    
    
    
    



# scheffe_fc[scheffe_fc == 0] = 0.5

# Plot for Scheffe-FC
def connectivity2(data, vmin, vmax, n_lines):
    return plot_connectivity_circle(data, ch_names, vmin=vmin, vmax=vmax, n_lines=n_lines, colormap=cmap,
                                    facecolor='white', textcolor='black', linewidth=1.5, colorbar=False, show=False)


fig, axes = plt.subplots(5, 3, figsize=(8, 15))

for band in range(5):
    for group in range(3):
        idx_start = 19*(band*3 + group)
        idx_stop = 19*(band*3 + group + 1)
        connectivity2(scheffe_fc[idx_start:idx_stop, :], 0, 1, 15)



############################# scheffe_fc_revised (triangular upper part 0으로 바꾸기)
def slicing(data):
    matrix = np.zeros((19, 19), dtype=int)
    for i in range(19):
        for j in range(i):
            matrix[i, j] = data[i,j]

    return matrix

scheffe = []
for i in range(15):
    under = slicing(scheffe_fc[19*i:19*(i+1), :])
    scheffe.append(under)

scheffe = np.concatenate(scheffe, axis=0)

with open('selected_Scheffe_FC_revised.pkl', 'wb') as f:
    pickle.dump(scheffe, f)

'''


# def print_edge(data):
#     edges = []
#     for i in range(len(ch_names)):
#         for j in range(len(ch_names)):
#             if data[i, j] == 1:
#                 edges.append((ch_names[i], ch_names[j]))
#
#     return edges
#
#
# for band in range(5):
#     edges = print_edge(anova_fc[19*band:19*(band+1), :])
#     print("ANOVA_FC : Selected edges are {}".format(edges))
#
#
# for band in range(5):
#     for group in range(3):
#         edges=[]
#         if group==0:
#             group_name = 'AD vs CN'
#         elif group==1:
#             group_name = 'CN vs FTD'
#         else:
#             group_name = 'AD vs FTD'
#
#         idx_start = 19*(band*3 + group)
#         idx_stop = 19*(band*3 + group + 1)
#         edges = print_edge(scheffe_fc[idx_start:idx_stop, :])
#
#         print("Scheffe_FC in {}: {}".format(group_name, edges))