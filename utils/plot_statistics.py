import os
import sys
# sys.path.insert(1, os.path.join(sys.path[0], '../pytorch'))
import numpy as np
import argparse
import h5py
import math
import time
import logging
import _pickle as cPickle
import matplotlib.pyplot as plt
 
from utilities import create_folder


def plot_statistics(args):

    # Arugments & parameters
    workspace = args.workspace
    select = args.select
    
    # Paths
    split = 'test'
    linewidth = 1
    save_out_path = 'results/{}_{}.pdf'.format(split, select)
    create_folder(os.path.dirname(save_out_path))

    fig, axes = plt.subplots(2, 2, figsize=(8, 8))

    def _load_metrics(filename, model_type, loss_type, 
        augmentation, batch_size):

        statistics_path = os.path.join(workspace, 'statistics', filename, 
            model_type, 'loss_type={}'.format(loss_type), 
            'augmentation={}'.format(augmentation), 'batch_size={}'.format(batch_size), 
            'statistics.pkl')

        statistics = cPickle.load(open(statistics_path, 'rb'))
        
        result_dict = {}
        for split in ['train', 'validation', 'test']:
            result_dict[split] = {}
            # for key in statistics[split][0].keys():
            #     result_dict[split][key] = [stat[key] for stat in statistics[split]]

            result_dict[split]['frame_f1'] = [stat['pitch_f1'] for stat in statistics[split]]

            if 'onset_f1' in statistics[split][0].keys():
                result_dict[split]['onset_f1'] = [stat['onset_f1'] for stat in statistics[split]]

            if 'offset_f1' in statistics[split][0].keys():
                result_dict[split]['offset_f1'] = [stat['offset_f1'] for stat in statistics[split]]

        return result_dict

    
    for metric_type, i, j, in zip(['frame_f1', 'onset_f1', 'offset_f1'], [0, 0, 1], [0, 1, 0]):
        lines = []

        if select == '1a':
            result_dict = _load_metrics('main','CnnGoogle_frameonly', 'frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_frameonly', linewidth=linewidth, color='b')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onset_frame', 'onset_frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onset_frame', linewidth=linewidth, color='r')
                lines.append(line)

            result_dict = _load_metrics('main','Cnn', 'frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='Cnn', linewidth=linewidth, color='c')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGRU', 'frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGRU', linewidth=linewidth, color='k')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGRU_onset', 'onset_frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGRU_onset_frame', linewidth=linewidth, color='g')
                lines.append(line)

        elif select == '1b':
            result_dict = _load_metrics('main','CnnGoogle_onset_frame', 'onset_frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onset_frame', linewidth=linewidth, color='r')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onset_frame_no_detach', 'onset_frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onset_frame_no_detach', linewidth=linewidth, color='g')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onset_offset_frame', 'onset_offset_frame_bce', 'none', 16)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onset_offset_frame', linewidth=linewidth, color='b')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onset_distance_frame', 'onset_offset_distance_bce', 'none', 16)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onset_distance_frame', linewidth=linewidth, color='k')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onset_frame', 'onsetfilter3_frame_bce', 'none', 16)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onset_frame_onsetfilter3', linewidth=linewidth, color='y')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onsetadaptive_frame', 'onsetadaptive_frame_bce', 'none', 16)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onsetadaptive_frame', linewidth=linewidth, color='m')
                lines.append(line)

        elif select == '1c':
            result_dict = _load_metrics('main','CnnGoogle_onset_frame', 'onset_frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='CnnGoogle_onset_frame', linewidth=linewidth, color='r')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onset_frame', 'soft_onset_frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='soft_onset_frame_bce', linewidth=linewidth, color='g')
                lines.append(line)

            result_dict = _load_metrics('main','CnnGoogle_onset_frame', 'hard_onset_frame_bce', 'none', 32)
            if metric_type in result_dict[split].keys():
                line, = axes[i, j].plot(result_dict[split][metric_type], label='hard_onset_frame_bce', linewidth=linewidth, color='b')
                lines.append(line)

 
        max_plot_iteration = 200001
        iterations = np.arange(0, max_plot_iteration, 2000)
        axes[i, j].set_ylim(0, 1)
        axes[i, j].set_xlim(0, len(iterations))
        axes[i, j].xaxis.set_ticks(np.arange(0, len(iterations), 20))
        axes[i, j].xaxis.set_ticklabels(np.arange(0, max_plot_iteration, 40000))
        axes[i, j].yaxis.set_ticks(np.arange(0, 1.01, 0.1))
        # ax.yaxis.set_ticklabels(np.arange(0, 1.01, 0.1))
        axes[i, j].grid(color='b', linestyle='solid', linewidth=0.3)
        
        axes[i, j].legend(handles=lines, loc=4, fontsize=8)

    plt.show()
    plt.savefig(save_out_path)
    print('Save figure to {}'.format(save_out_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example of parser. ')
    subparsers = parser.add_subparsers(dest='mode')

    # Plot statistics
    parser_plot = subparsers.add_parser('plot')
    parser_plot.add_argument('--workspace', type=str, required=True, help='Directory of your workspace.')
    parser_plot.add_argument('--select', type=str, required=True)
 
    # Parse arguments
    args = parser.parse_args()

    if args.mode == 'plot':
        plot_statistics(args)

    else:
        raise Exception('Error argument!')