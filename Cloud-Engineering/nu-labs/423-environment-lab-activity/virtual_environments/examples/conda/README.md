# Conda Tutorial

You have likely used conda to install packages. However, conda is also used to create and manage virtual environments. When you install conda to your computer, you are given a "base" environment. This is activated by default based on a snippet the conda installer places in your `~/.bashrc`. If you need to activate the base environment yourself, you can simply run `conda activate`.

Docs: <https://docs.conda.io/projects/conda/en/stable/user-guide/getting-started.html>

Install Guide: <https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html>

## Create a new environment

```bash
conda create --name tutorial python=3.7
```

## Activate your new environment

```bash
conda activate tutorial
```

## Deactivate your new environment

```bash
conda deactivate
```

## Installing packages in your new environment

### Installing packages

```bash
conda install numpy
```

### Installing packages from other `conda` channels

What if `conda install` doesn't work?! For example, the following will not work:

```bash
conda install geopy
```

This is because `geopy` is not part of the default `conda` channel. A `conda` channel is an online package repository for conda packages.

However, there exist numerous other channels that you can `conda install` from. You can search the [`conda` website](https://anaconda.org/) for channels that contain the package you are looking for.

[Search `geopy` in the conda website](https://anaconda.org/search?q=geopy). You will see that there are a number of channels you can install the package from, ordered by number of installs.

The channel with the highest number of installs is `conda-forge`, which is a popular and well-used channel. To install `geopy` via the `conda-forge` channel, run the following:

```bash
conda install -c conda-forge geopy
```

This command tells `conda` to install `geopy` from the channel (`-c`), `conda-forge`.

### Installing packages not in a `conda` channel

If you cannot locate a `conda` channel or the only channels that exist do not look well tested (i.e. have few installs), you can still use `pip`:

```bash
pip install geopy
```

> NOTE: Make sure that your active conda environment has `pip` installed, or else you may accidentally use a system-level pip which will install the package outside your virtual environment leading to much confusion

If the package does exist in a channel, however, it is preferable because `conda` takes care of the interactions of dependencies between the new package and packages already installed in the environment.

### Uninstall packages in your new environment

```bash
conda remove numpy scipy
```

## Reproducing your environment

You can reproduce your environment with a `environment.yml` file, which will list your version of Python, the conda channels to be used and the order in which to try them (i.e. install from the default channel and if the package does not exist in the default channel, install from `conda-forge`), and the list of packages with their versions. It will also include a list of the packages which were `pip install`ed rather than `conda install`ed (see more under _Listing project dependencies with `requirements.txt`_ for more on this).

### Creating `environment.yml`

To create your `environment.yml` file from a current environment, run:

```bash
conda env export > environment.yml
```

### Creating an environment using `environment.yml`

To reproduce an environment from an `environment.yml` file, run the following:

```bash
conda env create -n reproduced_env -f environment.yml
```

_Note_: this command will overwrite an `environment.yml` file already in the directory.

### Cloning an already existing environment

An `environment.yml` is useful for reproducing environments across servers, much like `requirements.txt` (discussed in a later section). However, to reproduce an environment already on the machine, you can `clone` an environment as follows:

```bash
conda create --name tutorial-clone --clone tutorial
```

> It can be nice to have a common environment with packages that you always use (such as `numpy` and `pandas`) that you can then clone and install packages into for each new project.

## Interacting with your environments

### Viewing a list of your environments

```bash
conda env list
```

### Removing an environment

```bash
conda env remove --name tutorial
```
