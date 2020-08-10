import matplotlib.pyplot as plt
import matplotlib.style as style
from results import get_batch_metrics
from options.visualization_options import get_arguments


def plot_metric_dataprop(prop, metric, methods, prop_supervised, metric_supervised, methods_supervised):
    """
    plot the accuracy vs data proportion being used, graph
    credits to: Alex Olteanu (https://www.dataquest.io/blog/making-538-plots/) for the plot style
    :return: None
    """
    plt.figure(figsize=(14, 10))
    style.use('fivethirtyeight')

    lenet = ['Margin Sampling', 'Least Confidence', 'Ratio Sampling', 'Entropy Based', 'Density Weighted',
             'MC dropout (BALD)', 'Random Sampling', 'Pseudo Labeling', 'Auto Encoder']

    resnet = ['SimCLR']

    colors = [[0, 0, 0, 1], [230 / 255, 159 / 255, 0, 1], [86 / 255, 180 / 255, 233 / 255, 1],
              [0, 158 / 255, 115 / 255, 1], [213 / 255, 94 / 255, 0, 1], [0, 114 / 255, 178 / 255, 1],
              [93 / 255, 58 / 255, 155 / 255, 1], [153 / 255, 79 / 255, 0, 1], [211 / 255, 95 / 255, 183 / 255, 1],
              [238 / 255, 136 / 255, 102 / 255, 1]]
    color_grey = [0 / 255, 0 / 255, 0 / 255, 1]

    for i, j in enumerate(range(1, len(metric), 3)):
        linestyle = '-' if methods[i] in resnet else '-'
        plt.plot(prop[i], metric[j], color=colors[i % len(colors)], label=methods[i], linewidth=2, linestyle=linestyle)
        plt.fill_between(prop[i], metric[j - 1], metric[j + 1], color=colors[i % len(colors)], alpha=0.05)

    # for i, j in enumerate(range(1, len(metric_supervised), 3)):
    #    plt.plot(prop_supervised[i], metric_supervised[j], color=color_grey, linewidth=2, linestyle=':', alpha=0.5)

    plt.title("Proof of concept - AL on Cifar-10",
              fontsize=20, weight='bold', alpha=.75)
    plt.xlabel("Labeled ratio of the dataset", fontsize=20, weight='bold', alpha=.75)
    plt.ylabel("Top-1 Accuracy (%)", fontsize=20, weight='bold', alpha=.75)
    # plt.text(x=0.1, y=91, s='Resnet Fully Supervised', color=color_grey, fontsize=18, rotation=0,
    #         backgroundcolor='#f0f0f0')
    plt.legend(loc='lower right', fontsize=18)
    plt.show()


if __name__ == "__main__":
    args = get_arguments()
    met, ratios = get_batch_metrics(met=args.metric, class_specific=args.class_specific, class_id=args.class_id)

    plot_metric_dataprop(
        prop=ratios,
        metric=met,
        methods=[
            'Random Sampling',
            'FixMatch',
            'Least Confidence',
            'Ratio Sampling',
            'Entropy Based',
            'Density Weighted',
            'MC dropout (BALD)',
            'Pseudo Labeling',
            'Auto Encoder',
            'SimCLR'
        ], prop_supervised=[
            [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        ], metric_supervised=[
            [94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52, 94.52],
            [93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24, 93.24],
            [91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63, 91.63],
        ], methods_supervised=[
            'Resnet Supervised',
        ]
    )

'''
Adam Optimizer results:
prop=[
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66]
    ], acc=[
        [30.49, 40.45, 47.68, 51.8, 55.25, 57.44, 59.31, 61.45, 63.31, 64.42, 65.54, 66.61, 67.46, 67.74],
        [31.47, 41.22, 48.33, 52.7, 56.22, 58.51, 60.47, 62.53, 64.2, 65.52, 66.48, 67.37, 68.2, 68.6],
        [32.45, 41.99, 48.98, 53.6, 57.19, 59.58, 61.63, 63.61, 65.09, 66.62, 67.42, 68.13, 68.94, 69.46],

        [30.49, 41.01, 47.92, 52.0, 55.58, 58.2, 59.87, 61.6, 63.39, 64.96, 65.89, 67.21, 68.04, 68.61],
        [31.47, 41.88, 48.84, 52.86, 56.71, 59.11, 61.16, 63.08, 64.63, 65.86, 66.95, 67.84, 68.56, 69.23],
        [32.45, 42.75, 49.76, 53.72, 57.84, 60.02, 62.45, 64.56, 65.87, 66.76, 68.01, 68.47, 69.08, 69.85],

        [30.49, 41.19, 47.81, 51.8, 55.31, 58.24, 59.98, 61.34, 63.28, 64.67, 65.95, 66.77, 67.81, 68.75],
        [31.47, 41.75, 48.66, 52.65, 56.14, 58.99, 61.0, 62.62, 64.35, 65.76, 66.92, 67.77, 68.61, 69.4],
        [32.45, 42.31, 49.51, 53.5, 56.97, 59.74, 62.02, 63.9, 65.42, 66.85, 67.89, 68.77, 69.41, 70.05],

        [30.49, 40.89, 48.73, 52.57, 55.82, 58.27, 59.67, 62.1, 63.64, 64.69, 66.21, 67.25, 68.0, 68.74],
        [31.47, 41.62, 49.12, 53.02, 56.22, 59.01, 61.1, 63.25, 64.69, 65.79, 67.01, 67.95, 68.75, 69.22],
        [32.45, 42.35, 49.51, 53.47, 56.62, 59.75, 62.53, 64.4, 65.74, 66.89, 67.81, 68.65, 69.5, 69.7],

        [30.49, 41.08, 47.81, 51.75, 55.05, 58.15, 59.54, 62.1, 63.61, 65.08, 65.88, 66.96, 67.84, 68.29],
        [31.47, 41.96, 48.44, 52.69, 56.22, 59.32, 60.76, 63.25, 64.6, 65.88, 66.69, 67.63, 68.4, 68.92],
        [32.45, 42.84, 49.07, 53.63, 57.39, 60.49, 61.98, 64.4, 65.59, 66.68, 67.5, 68.3, 68.96, 69.55],

        [30.49, 41.11, 48.18, 52.08, 55.15, 57.88, 59.85, 61.73, 63.54, 64.75, 65.81, 67.0, 67.78, 68.19],
        [31.47, 41.7, 48.66, 52.98, 56.32, 59.06, 61.2, 62.88, 64.54, 65.84, 66.74, 67.97, 68.56, 69.05],
        [32.45, 42.29, 49.14, 53.88, 57.49, 60.24, 62.55, 64.03, 65.54, 66.93, 67.67, 68.94, 69.34, 69.91],

        [29.16, 38.86, 47.65, 53.07, 57.37, 61.59, 64.6, 66.66, 68.69, 70.21, 71.52, 72.07, 73.16, 73.56],
        [30.63, 40.62, 48.69, 53.83, 58.05, 61.87, 64.83, 67.06, 68.97, 70.38, 71.63, 72.31, 73.34, 73.84],
        [32.1, 42.38, 49.73, 54.59, 58.73, 62.15, 65.06, 67.46, 69.25, 70.55, 71.74, 72.55, 73.52, 74.12],

        [30.18, 41.45, 48.57, 52.21, 55.91, 58.32, 59.88, 62.69, 63.84, 65.52, 66.67, 67.6, 68.08, 68.7],
        [30.66, 41.96, 48.99, 52.82, 56.21, 58.74, 60.17, 62.87, 64.04, 65.72, 66.9, 67.84, 68.28, 68.98],
        [31.14, 42.47, 49.41, 53.43, 56.51, 59.16, 60.46, 63.05, 64.24, 65.92, 67.13, 68.08, 68.48, 69.26],
    ]
'''

'''
SGD optimizer:
prop=[
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
    ], acc=[
        [30.82, 34.15, 42.01, 48.20, 49.97, 51.64, 52.44, 54.69, 56.51, 57.46, 58.7, 59.7, 59.98, 60.21],
        [32.74, 35.90, 44.03, 50.37, 52.3, 53.92, 55.32, 57.12, 58.9, 59.97, 61.34, 62.35, 62.6, 62.86],
        [34.66, 37.65, 46.05, 52.53, 54.62, 56.2, 58.2, 59.55, 61.28, 62.48, 63.98, 65.0, 65.22, 65.51],

        [30.82, 32.64, 40.66, 48.81, 50.78, 52.43, 53.44, 55.81, 57.6, 58.89, 59.9, 60.6, 60.77, 60.98],
        [32.74, 36.61, 43.72, 50.79, 52.74, 54.38, 55.5, 57.36, 58.9, 60.39, 61.32, 62.0, 62.27, 62.41],
        [34.66, 40.58, 46.78, 52.77, 54.7, 56.33, 57.56, 58.91, 60.20, 61.89, 62.74, 63.4, 63.77, 63.84],

        [30.82, 33.83, 41.9, 48.44, 50.51, 52.66, 53.84, 55.13, 56.72, 57.96, 58.99, 60.0, 60.28, 60.43],
        [32.74, 36.6, 44.19, 50.43, 52.38, 54.35, 55.64, 57.28, 58.8, 60.2, 61.42, 62.44, 62.73, 62.88],
        [34.66, 39.37, 46.48, 52.42, 54.25, 56.04, 57.44, 59.43, 60.88, 62.44, 63.85, 64.88, 65.18, 65.33],

        [30.82, 33.02, 43.12, 49.92, 51.29, 53.35, 53.84, 55.43, 56.79, 57.97, 59.2, 60.02, 60.29, 60.53],
        [32.74, 35.52, 44.72, 52.23, 54.12, 56.01, 57.26, 58.83, 60.06, 61.28, 62.21, 63.16, 63.34, 63.56],
        [34.66, 38.02, 46.32, 54.54, 56.95, 58.67, 60.68, 62.23, 63.33, 64.59, 65.22, 66.3, 66.39, 66.59],

        [30.82, 33.96, 43.37, 49.62, 52.2, 53.87, 54.53, 56.53, 57.98, 59.18, 60.37, 61.13, 61.39, 61.65],
        [32.74, 36.07, 45.07, 51.27, 53.6, 55.2, 56.78, 58.54, 59.96, 61.27, 62.26, 63.21, 63.43, 63.62],
        [34.66, 38.18, 46.77, 52.92, 55.0, 56.53, 59.03, 60.55, 61.94, 63.36, 64.15, 65.29, 65.47, 65.59],

        [30.82, 33.82, 40.98, 48.25, 50.25, 51.88, 53.12, 54.68, 56.22, 57.61, 58.7, 59.36, 59.55, 59.96],
        [32.74, 36.3, 44.25, 50.48, 52.41, 53.89, 55.13, 56.74, 58.25, 59.47, 60.67, 61.62, 61.84, 62.16],
        [34.66, 38.78, 47.52, 52.71, 54.57, 55.9, 57.14, 58.80, 60.28, 61.33, 62.64, 63.88, 64.13, 64.36],

        [30.82, 33.16, 40.6, 46.66, 48.41, 49.78, 50.73, 52.17, 54.42, 55.83, 57.26, 57.98, 58.39, 58.46],
        [32.74, 34.53, 43.8, 50.17, 51.78, 53.3, 54.6, 56.32, 58.02, 59.21, 60.37, 61.28, 61.62, 61.75],
        [34.66, 35.9, 47.0, 53.68, 55.15, 56.82, 58.47, 60.47, 61.62, 62.59, 63.48, 64.58, 64.85, 65.04],

        [26.66, 29.13, 38.98, 43.99, 49.36, 52.86, 56.04, 58.7, 61.3, 63.66, 65.99, 67.43, 68.52, 69.1],
        [28.82, 31.75, 41.17, 45.52, 50.03, 53.53, 57.08, 60.02, 62.85, 65.1, 67.11, 68.31, 69.57, 70.37],
        [30.98, 34.37, 43.36, 47.05, 50.7, 54.2, 58.12, 61.34, 64.4, 66.54, 68.23, 69.19, 70.62, 71.64],
    ]
'''

'''
SGD optimizer w/ nesterov, affine augmentations and auto LR
prop=[
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
    ], acc=[
        [22.44, 38.96, 49.52, 54.35, 57.46, 60.06, 64.05, 65.66, 66.71, 67.68, 68.36, 69.03, 69.64, 69.91],
        [27.03, 42.01, 51.18, 56.02, 59.47, 61.54, 65.5, 67.07, 67.98, 69.04, 69.84, 70.32, 70.95, 71.22],
        [31.62, 45.06, 52.84, 57.69, 61.48, 63.02, 66.95, 68.48, 69.25, 70.4, 71.32, 71.61, 72.26, 72.53],

        [22.44, 38.58, 45.55, 50.48, 55.07, 57.28, 62.51, 63.71, 65.21, 66.35, 67.3, 68.24, 68.73, 69.0],
        [27.03, 41.02, 48.14, 53.05, 56.6, 58.83, 62.77, 64.19, 65.5, 66.76, 67.48, 68.41, 68.81, 69.19],
        [31.62, 43.46, 50.73, 55.62, 58.13, 60.38, 63.03, 64.67, 65.79, 67.17, 67.66, 68.58, 68.89, 69.38],

        [22.44, 38.4, 47.69, 53.6, 57.86, 59.77, 62.73, 64.48, 65.63, 66.71, 67.32, 67.95, 68.61, 69.37],
        [27.03, 42.17, 49.27, 54.61, 58.09, 59.92, 63.13, 64.81, 66.23, 67.4, 68.35, 68.85, 69.59, 70.12],
        [31.62, 45.94, 50.85, 55.62, 58.32, 60.07, 63.53, 65.14, 66.83, 68.09, 69.38, 69.75, 70.57, 70.87],

        [22.44, 38.47, 46.98, 52.54, 56.15, 58.43, 61.65, 62.81, 63.75, 64.7, 65.44, 66.15, 66.94, 67.53],
        [27.03, 41.94, 49.38, 54.01, 57.69, 59.82, 63.11, 64.42, 65.57, 66.54, 67.27, 68.0, 68.58, 69.11],
        [31.62, 45.41, 51.78, 55.48, 59.23, 61.21, 64.57, 66.03, 67.39, 68.38, 69.1, 69.85, 70.22, 70.69],

        [22.44, 39.17, 48.86, 53.42, 56.41, 58.84, 62.38, 64.24, 65.21, 66.77, 68.0, 68.77, 69.28, 69.8],
        [27.03, 43.47, 51.45, 55.61, 58.46, 60.82, 64.1, 66.1, 67.18, 68.64, 69.43, 70.15, 70.7, 71.12],
        [31.62, 47.77, 54.04, 57.8, 60.51, 62.8, 65.82, 67.96, 69.15, 70.51, 70.86, 71.53, 72.12, 72.44],

        [22.44, 37.86, 49.52, 54.46, 57.09, 59.34, 62.85, 64.23, 65.52, 66.86, 68.03, 68.68, 69.4, 69.83],
        [27.03, 41.81, 50.25, 54.9, 57.61, 59.99, 63.33, 64.9, 66.25, 67.44, 68.4, 69.11, 69.76, 70.32],
        [31.62, 45.76, 50.98, 55.34, 58.13, 60.64, 63.81, 65.57, 66.98, 68.02, 68.77, 69.54, 70.12, 70.81],

        [22.44, 40.37, 49.27, 53.86, 57.65, 59.77, 63.52, 64.97, 66.78, 68.11, 69.07, 69.89, 70.52, 71.2],
        [27.03, 42.8, 51.13, 55.12, 58.9, 61.03, 64.71, 66.33, 67.85, 68.85, 69.8, 70.42, 71.01, 71.56],
        [31.62, 45.23, 52.99, 56.38, 60.15, 62.29, 65.9, 67.69, 68.92, 69.59, 70.53, 70.95, 71.5, 71.92],

        [29.16, 38.86, 47.65, 53.07, 57.37, 61.59, 64.6, 66.66, 68.69, 70.21, 71.52, 72.07, 73.16, 73.56],
        [30.63, 40.62, 48.69, 53.83, 58.05, 61.87, 64.83, 67.06, 68.97, 70.38, 71.63, 72.31, 73.34, 73.84],
        [32.1, 42.38, 49.73, 54.59, 58.73, 62.15, 65.06, 67.46, 69.25, 70.55, 71.74, 72.55, 73.52, 74.12],
'''

'''
Adam w/ augmentations:
prop=[
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
        [0.01, 0.06, 0.11, 0.16, 0.21, 0.26, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66],
    ], acc=[
        [29.16, 42.91, 51.23, 55.76, 59.17, 61.46, 63.78, 65.56, 66.8, 68.18, 69.17, 69.81, 70.31, 70.79],
        [30.82, 44.57, 51.92, 56.37, 60.03, 62.42, 64.62, 66.27, 67.3, 68.52, 69.34, 70.09, 70.71, 71.11],
        [32.48, 46.23, 52.61, 56.98, 60.89, 63.38, 65.46, 66.98, 67.8, 68.86, 69.51, 70.37, 71.11, 71.43],

        [29.16, 42.78, 50.91, 55.03, 58.41, 60.8, 62.92, 64.9, 66.19, 67.5, 68.32, 69.31, 69.81, 70.2],
        [30.82, 44.36, 51.73, 56.46, 59.76, 62.19, 64.39, 66.16, 67.39, 68.5, 69.31, 70.19, 70.55, 71.1],
        [32.48, 45.94, 52.55, 57.89, 61.11, 63.58, 65.86, 67.42, 68.59, 69.5, 70.3, 71.07, 71.29, 72.0],

        [29.16, 43.74, 51.46, 55.83, 58.73, 61.5, 63.77, 65.76, 67.17, 67.99, 69.1, 69.66, 70.55, 70.78],
        [30.82, 44.55, 52.36, 56.77, 60.16, 62.76, 64.81, 66.54, 67.69, 68.54, 69.66, 70.15, 70.84, 71.27],
        [32.48, 45.36, 53.26, 57.71, 61.59, 64.02, 65.85, 67.32, 68.21, 69.09, 70.22, 70.64, 71.13, 71.76],

        [29.16, 43.15, 51.22, 55.34, 58.57, 60.9, 63.37, 64.88, 66.46, 67.39, 68.76, 69.4, 70.11, 70.69],
        [30.82, 44.76, 52.18, 56.44, 60.03, 62.33, 64.55, 66.1, 67.51, 68.39, 69.36, 70.06, 70.72, 71.19],
        [32.48, 46.37, 53.14, 57.54, 61.49, 63.76, 65.73, 67.32, 68.56, 69.39, 69.96, 70.72, 71.33, 71.69],

        [29.16, 43.01, 50.85, 55.27, 58.33, 60.94, 63.13, 64.37, 65.87, 66.98, 67.82, 68.7, 69.31, 69.83],
        [30.82, 44.46, 51.74, 56.32, 59.84, 62.09, 64.27, 65.61, 67.01, 67.94, 68.9, 69.55, 70.34, 70.77],
        [32.48, 45.91, 52.63, 57.37, 61.35, 63.24, 65.41, 66.85, 68.15, 68.9, 69.98, 70.4, 71.37, 71.71],

        [29.16, 43.36, 51.41, 55.64, 58.6, 60.88, 63.05, 64.41, 65.86, 66.8, 67.79, 68.69, 69.09, 69.7],
        [30.82, 44.36, 52.1, 56.57, 59.86, 62.14, 64.23, 65.59, 66.98, 67.94, 68.84, 69.45, 70.1, 70.57],
        [32.48, 45.36, 52.79, 57.5, 61.12, 63.4, 65.41, 66.77, 68.1, 69.08, 69.89, 70.21, 71.11, 71.44],

        [29.16, 43.0, 50.33, 54.95, 58.08, 59.94, 62.42, 64.08, 65.49, 66.68, 67.59, 68.44, 69.33, 69.94],
        [30.82, 44.17, 51.53, 56.01, 59.3, 61.68, 63.93, 65.46, 66.73, 67.76, 68.64, 69.39, 70.03, 70.67],
        [32.48, 45.34, 52.73, 57.07, 60.52, 63.42, 65.44, 66.84, 67.97, 68.84, 69.69, 70.34, 70.73, 71.4],

        [29.16, 43.04, 50.91, 55.26, 57.9, 60.73, 62.89, 64.38, 65.61, 66.55, 67.62, 68.46, 69.36, 70.01],
        [30.82, 44.42, 51.76, 56.42, 59.55, 62.28, 64.24, 65.7, 66.99, 67.84, 68.87, 69.55, 70.37, 70.93],
        [32.48, 45.8, 52.61, 57.58, 61.2, 63.83, 65.59, 67.02, 68.37, 69.13, 70.12, 70.64, 71.38, 71.85],

        [24.62, 40.06, 48.15, 53.27, 58.09, 61.36, 64.51, 66.36, 67.81, 68.9, 69.81, 70.66, 71.32, 72.07],
        [26.4, 41.66, 49.54, 54.64, 59.02, 62.17, 65.1, 66.91, 68.34, 69.6, 70.46, 71.19, 71.82, 72.38],
        [28.18, 43.26, 50.93, 56.01, 59.95, 62.98, 65.69, 67.46, 68.87, 70.3, 71.11, 71.72, 72.32, 72.69],
    ]
'''
