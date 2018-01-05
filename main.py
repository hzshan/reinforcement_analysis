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

n_cat = 6  # number of categories
n_rats = 16  # total number of rats per category
n_days = 12
n_simulations = 5000 # number of simulations to run
filename = 'trapped_open.xlsx'  # name of Excel spreadsheet

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

# Make figures
summary_hist = plt.figure()
color_dict = ['b', 'r', 'y', 'g', 'salmon', 'c']
for i in range(n_cat):
    label = 'Category ' + str(i)
    plt.hist(sim_count[i, :], color=color_dict[i], bins=np.linspace(0, n_days * n_rats, n_days * n_rats), label=label)
    plt.axvline(x=cat_count[i], label=label, color=color_dict[i])

plt.xlabel('Consecutive openings')
plt.ylabel('Count')
plt.show()
plt.grid()
plt.legend()
