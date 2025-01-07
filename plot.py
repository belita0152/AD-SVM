import pickle
import matplotlib.pyplot as plt
import mne
from matplotlib.colors import Normalize
import matplotlib

# Dataset
with open('./selected_data/selected_ANOVA_PSD.pkl', 'rb') as f:
    anova_psd = pickle.load(f)

with open('./selected_data/selected_Scheffe_PSD.pkl', 'rb') as f:
    scheffe_psd = pickle.load(f)



# Info
ch_names = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'Fz',
            'Cz', 'Pz']
fname = "./AD-GNN/preproc/data/derivatives/sub-001/eeg/sub-001_task-eyesclosed_eeg.set"
info_data = mne.io.read_raw_eeglab(fname, preload=False)



# Prepare for plotting
cmap = 'seismic'
# delta = [0.5 for i in range(19)]
norm = Normalize(vmin=0, vmax=1)
anova_psd[anova_psd == 0] = 0.5  # Make color similar to white
scheffe_psd[scheffe_psd == 0] = 0.5


# Plot for ANOVA-PSD
def topomap(data, ax, cmap, norm):
    return mne.viz.plot_topomap(data, info_data.info, ch_type='eeg', cmap=cmap, cnorm=norm, axes=axes[ax], show=False)


fig, axes = plt.subplots(1, 5, figsize=(10, 5))
# topomap(delta, 0, cmap, norm)
for band in range(5):
    topomap(anova_psd[19*band:19*(band+1)], band,  cmap, norm)

# plt.savefig('selected_psd_anova.eps', dpi=300)


# Plot for Scheffe-PSD
def topomap2(data, x, y, cmap, norm):
    return mne.viz.plot_topomap(data, info_data.info, ch_type='eeg', cmap=cmap, cnorm=norm, axes=axes[x, y], show=False)


fig, axes = plt.subplots(5, 3, figsize=(8, 15))
# for col in range(3):
#     for row in range(5):
#         topomap2(scheffe_psd[19*row:19*(row+1), col], row, col, cmap, norm)

# plt.show()
# plt.savefig('selected_psd_scheffe.eps', dpi=300)


colormapping = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)

# create space on the right side. add a small custom axis
cax = fig.add_axes([0.94, 0.3, 0.005, 0.5])
fig.colorbar(colormapping, cax=cax, shrink=0.5)
# plt.savefig('selected_colorbar.eps', dpi=300)
plt.show()