from openpyxl import load_workbook
import os.path
from util import load_data, count_consecutive, get_prob_table, simulate
import numpy as np
from numpy.random import binomial
import matplotlib.pyplot as plt

"""
REINFORCEMENT ANALYSIS
Based on the idea presented in Fig. 3 in 

Bartal, I. B. A., Shan, H., Molasky, N. M., Murray, T. M.,
Williams, J. Z., Decety, J., & Mason, P. (2016).
Anxiolytic treatment impairs helping behavior in rats. Frontiers in psychology, 7.

Uses Python 3, openpyxl

by Haozhe Shan
12/31/2017
"""
# ################################################
# ################################################
# ################################################

n_cat = 6  # number of categories
n_rats = 16  # total number of rats per category
n_days = 12  # number of days
n_simulations = 10000 # number of simulations to run
filename = 'trapped_open.xlsx'  # name of Excel spreadsheet

''' Put in names of the conditions in order. Surround each condition with quotation marks and separate with commas'''

conditions = ['saline', 'uninjected', 'highMDZ', 'LowMDZ', 'anesthesia', 'SedMDZ']

# ################################################
# ################################################
# ################################################

# See if the spreadsheet can be found
if os.path.isfile(filename) is False:
    print('File not found. Check file name and working directory.')

# Load the first sheet of the selected spreadsheet
workbook = load_workbook(filename)
sheet = workbook.worksheets[0]

# Load the column containing category information
categories = load_data(first_row=2,
                       last_row=2 + n_rats * n_cat - 1,
                       first_column='B',
                       last_column='B',
                       sheet=sheet)

# Load the column containing rats information
rats = load_data(first_row=2,
               last_row=2 + n_rats * n_cat - 1,
               first_column='A',
               last_column='A',
               sheet=sheet)

# Load the area containing opening data (in '1's and '0's)

opening_data = load_data(first_row=2,
               last_row=2 + n_rats * n_cat - 1,
               first_column='C',
               last_column=chr(67 + n_days - 1),
               sheet=sheet)

cat_mask = np.repeat(categories, repeats=n_days, axis=1)
rat_mask = np.repeat(rats, repeats=n_days, axis=1)

# Calculate mean opening probability for each category
cat_p = np.zeros(n_cat)  # set up storage vector
for i in range(n_cat):
    cat_p[i] = np.mean(opening_data[cat_mask == i])

# Count consecutive openings
cat_count = np.zeros_like(cat_p)
for i in range(n_cat):
    cat_count[i] = count_consecutive(opening_data[cat_mask == i].reshape((n_rats, n_days)))

# Calculate probability tables
tables = np.zeros((n_rats, n_days, n_cat))
for i in range(n_cat):
    tables[:, :, i] = get_prob_table(opening_data[cat_mask == i].reshape((n_rats, n_days)))

# Generated simulated data
sim_count = np.zeros((n_cat, n_simulations))
for trial in range(n_simulations):
    sim_data = np.zeros_like(opening_data)
    for i in range(n_cat):
        sim_count[i, trial] = count_consecutive(simulate(tables[:, :, i]))

    p_values = np.zeros(n_cat)
    for i in range(n_cat):
        p_values[i] = sim_count[i, :][sim_count[i, :] > cat_count[i]].size / n_simulations

# Make figures
summary_hist = plt.figure()
for i in range(n_cat):
    subplot_str = str(n_cat) + '1' + str(i+1)
    summary_hist.add_subplot(subplot_str)
    plt.hist(sim_count[i, :],
             bins=np.linspace(0, n_days * n_rats, n_days * n_rats))
    plt.axvline(x=cat_count[i])
    plt.title(conditions[i] + ' one-tail p-value: ' + str(p_values[i]), fontsize=10)
    if i == n_cat - 1:
        plt.xlabel('Consecutive openings')
        plt.ylabel('Count')
    else:
        plt.xticks(fontsize=4)
    plt.grid()


print(p_values)
