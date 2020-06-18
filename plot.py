import argparse
import json
from os import path as osp

import matplotlib.pyplot as plt
import numpy as np


def main(args):
    params = json.load(open(args.param_file))
    metrics = np.load(args.log_file)
    exp_id = osp.splitext(osp.basename(args.log_file))[0]
    dataset_name = osp.basename(params[exp_id]['data_dir'])

    print('#######')
    print(dataset_name)
    to_plot = ['tng_loss', 'val_loss', 'val_acc']

    y = 100 * metrics['val_acc']
    y_mean = np.mean(y, axis=0)
    y_std = np.std(y, axis=0)
    y_max = np.argmax(y_mean)

    val_mean = y_mean[y_max]
    val_std = y_std[y_max]
    print(f'Val acc max {val_mean:.2f} (+/-{val_std:.2f})%')

    f, ax = plt.subplots(len(to_plot), 1, sharex=True, figsize=[10, 10])
    for i, m in enumerate(to_plot):
        y = metrics[m][:, :args.max_epochs]

        epochs = range(y.shape[1])
        y_mean = np.mean(y, axis=0)

        boundaries = []
        for b in range(4):
            boundaries.append([
                np.percentile(y, 10 * (b + 1), axis=0),
                np.percentile(y, 100 - 10 * (b + 1), axis=0)
            ])
        p_25 = np.percentile(y, 25, axis=0)
        p_75 = np.percentile(y, 75, axis=0)
        for r in y:
            ax[i].plot(epochs, r, ':')

        ax[i].plot(epochs, y_mean)
        for b in boundaries:
            ax[i].fill_between(epochs, b[0], b[1], color='b', alpha=.1)
        ax[i].fill_between(epochs, p_25, p_75, color='b', alpha=.1)
        ax[i].set_title(m)
        ax[i].grid(True)

    f.suptitle(f'Dataset: {dataset_name}\nMetrics averaged over {y.shape[0]} runs')
    plt.savefig(f'{dataset_name}.png')
    plt.show()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--log-file')
    PARSER.add_argument('--param-file')
    PARSER.add_argument('--max-epochs', type=int, default=25)

    ARGS = PARSER.parse_args()
    main(ARGS)