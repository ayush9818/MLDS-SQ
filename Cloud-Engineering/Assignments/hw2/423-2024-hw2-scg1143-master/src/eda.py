import os
import logging
import matplotlib.pyplot as plt

# Setup logging
logger = logging.getLogger("cloudlogger." + __name__)


def save_figures(features, output_directory):
    """
    Generates and saves histogram plots for each feature in the dataset,
    comparing distributions for two classes defined by the "target".

    The figures are saved into the specified output directory. Each figure file
    is named after the feature it represents.

    Args:
        features (pd.DataFrame): A DataFrame where each column is a feature to plot.
        target (pd.Series): A binary target variable used to separate the data into two groups.
        output_directory (pathlib.Path or str): The directory where the figures will be saved.

    Notes:
        The output directory will be created if it does not exist.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    target = features["target"]
    # Generate and save figures
    for feat in features.columns:
        fig, ax = plt.subplots(figsize=(12, 8))
        # Plot histograms for both classes
        ax.hist(
            [features[target == 0][feat].values, features[target == 1][feat].values],
            label=["Class 0", "Class 1"],
            color=["blue", "orange"],
            alpha=0.75,
        )
        # Setting labels and title
        ax.set_xlabel(" ".join(feat.split("_")).capitalize())
        ax.set_ylabel("Number of observations")
        ax.set_title(f"Distribution of {feat} by target class")
        ax.legend()

        # Save the figure
        fig_path = os.path.join(output_directory, f"{feat}.png")
        fig.savefig(fig_path)
        plt.close(fig)  # Close the figure to free up memory

        # Logging the action
        logger.info("Saved figure for %s to %s", feat, fig_path)
