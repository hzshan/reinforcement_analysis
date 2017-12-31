import numpy as np

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



