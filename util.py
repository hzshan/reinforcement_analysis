import numpy as np
from numpy.random import binomial


def load_data(first_row, last_row, first_column, last_column, sheet):

    assert last_row > first_row
    n_columns = ord(last_column) - ord(first_column) + 1
    _data_array = np.zeros((int(last_row - first_row + 1), n_columns))
    range_string = '%s%i:%s%i' % (first_column, first_row, last_column, last_row)
    _sheet_select = sheet[range_string]

    for i in range(last_row - first_row + 1):
        for j in range(n_columns):
            _data_array[i, j] = _sheet_select[i][j].value

    return _data_array


def count_consecutive(opening_data):

    (entries, days) = opening_data.shape
    _consec_counter = 0
    for i in range(entries):
        for j in range(days):
            if j == days - 1:
                continue
            elif opening_data[i, j] == 1 and opening_data[i, j + 1] == 1:
                _consec_counter += 1

    return _consec_counter


def get_prob_table(data):

    simed_prob = np.zeros_like(data)
    day_mean = np.mean(data, axis=0)
    rat_mean = np.mean(data, axis=1)

    for i in range(rat_mean.size):
        for j in range(day_mean.size):
            simed_prob[i, j] = day_mean[j] * rat_mean[i]

    simed_prob *= np.sum(data) / np.sum(simed_prob)
    simed_prob[simed_prob > 1] = 1

    return simed_prob


def simulate(simed_prob):
    simed_data = np.zeros_like(simed_prob)
    for i in range(simed_prob.shape[0]):
        for j in range(simed_prob.shape[1]):
            simed_data[i, j] = binomial(1, p=simed_prob[i, j])
    return simed_data






