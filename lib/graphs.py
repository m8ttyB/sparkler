#!/usr/bin/env python
"""

A CLI tool like spark, that produces sparklines from
whitespace-delimited lists of numbers passed by other command line
arguments. See https://github.com/holman/spark

There are three valid use cases:

1. space-delimited list of values (no labels, all values on one line):

    git log --since 'september' --format='%ad' --date-order | \
        awk '{print $1" "$2" "$3}' | uniq -c | tac | awk '{print $1}' | \
        xargs python graphs.py

2. newline-delimited list of values (no labels, newline-delimited):

     git log --since 'september' --format='%ad' --date-order | \
         awk '{print $1" "$2" "$3}' | uniq -c | tac | awk '{print $1}' | \
         python graphs.py

3. newline-delimited list where each line is a value followed by label text:

    git log --since 'september' --format='%ad' --date-order | \
        awk '{print $1" "$2" "$3}' | uniq -c | tac | \
        python graphs.py

"""

import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_plot(values):
    if len(values) > 100:
        make_scatter_plot(values)
    else:
        make_line_graph(values)

def make_line_graph(values):
    plt.plot(values, '-', color='#333333', linewidth=2.0)

def make_scatter_plot(values):
    plt.plot(values, '.', color='#333333', linewidth=2.0)

def plot_integers(raw_values):
    values = [float(s) for s in raw_values]
    make_plot(values)

def get_inputs():
    if len(sys.argv) > 1:
        sys.argv.pop(0)

        if len(sys.argv) == 1:
            return sys.argv[0].strip().split('\n')
        else:
            return sys.argv
    else:
        raw_input = sys.stdin.readlines()
        if len(raw_input) == 1:
            return raw_input[0].strip().split(' ')
        else:
            return raw_input

"""
Only so many labels fit comfortably along the y-axis. After that,
downsample the labels so that we only print as many as will fit. Don't
attempt to be smart about which labels to filter, just use the overall
count of labels as a guide.
"""
def sample_from_labels(labels):
    labels_that_can_fit_on_the_y_axis = 50
    filtered_labels = []
    if (len(labels) > labels_that_can_fit_on_the_y_axis):
        filtered_labels = filter_for_labels(labels_that_can_fit_on_the_y_axis, labels)
    else:
        filtered_labels = labels
    return filtered_labels

def filter_for_labels(labels_that_can_fit_on_the_y_axis, labels):
    filtered_labels = []
    every_nth_label = len(labels) / (labels_that_can_fit_on_the_y_axis / 2)
    for index, label in enumerate(labels):
        if ((index + 1) == len(labels)):
            filtered_labels.append(label)
        elif (index % every_nth_label != 0):
            filtered_labels.append(' ')
        else:
            filtered_labels.append(label)

    return filtered_labels

raw_values = get_inputs()

if len(raw_values) > 1 and len(raw_values[0].strip().split(' ')) > 1:
    values = []
    labels = []

    for s in raw_values:
        tokens = s.strip().split()
        cons = tokens.pop(0)
        cdr = ' '.join(tokens)
        values.append(float(cons))
        labels.append(cdr)

    labels = sample_from_labels(labels)

    make_plot(values)
    plt.xticks(range(len(values)), labels, size='small', rotation=75)



elif len(raw_values) > 1:
    plot_integers(raw_values)

else:
     plot_integers(raw_values[0].strip().split(' '))

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10, 8)
fig.savefig('./my_graph.png', dpi=300, bbox_inches='tight')