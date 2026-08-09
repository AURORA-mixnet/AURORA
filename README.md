# AURORA

This repository contains the artifact for the paper titled “AURORA: Throughput- and Congestion-Aware Low-Latency Mixnets with Adversarial Robustness,” accepted at NDSS 2027.

## Overview

Mixnets are overlay networks designed to provide strong anonymity for Internet users against network adversaries. However, this anonymity often comes at the cost of high communication latency and inefficient resource utilization. These limitations can arise from inefficient distribution of mixnodes within the mixnet and routing strategies that do not adequately account for differences among nodes. AURORA addresses these issues by jointly optimizing performance and anonymity.

We evaluate AURORA using two complementary approaches: (1) theoretical analysis and (2) simulation-based analysis.

In the theoretical setting, each proposed technique is evaluated under probability distributions for route selection in mixnets and relevant system characteristics, including inter-node latency and mixnode processing capacity.

In contrast, the simulation-based analysis is implemented in Python using the SimPy discrete-event simulation framework. A dynamic set of clients generates packets destined for a set of receivers. These packets traverse mixnodes according to the routing strategies considered in the paper, including RLP, REP, and RBR. Along each route, mixnodes perform mixing operations to anonymize and forward packets.

The artifact contains approximately 10K lines of Python code and provides scripts for reproducing the experiments, figures, and tables presented in the paper. For practical artifact evaluation, the default artifact configuration reduces the number of iterations over independent network snapshots to one, whereas the experiments reported in the paper use up to 500 iterations. All other parameters remain consistent with those used in the paper.


## How to Access

The artifact is available through both a persistent **Zenodo archive** and the corresponding **GitHub repository**:

| Source | Link | Contents |
|---|---|---|
| **Zenodo** | https://doi.org/10.5281/zenodo.xxxx | Full artifact + short and extended datasets |
| **GitHub** | https://github.com/AURORA-mixnet/AURORA | Full artifact + short dataset |

The GitHub repository and Zenodo archive contain the same artifact code. The main difference is the size of the included Nym dataset.

### 📦 GitHub Dataset

The GitHub repository includes the reduced dataset:

`Nym_RIPE_dataset_short_version.pkl`

**Size:** approximately 20 MB  
**Supported network snapshots:** 4 (`It1`--`It4`)

This dataset is sufficient for reproducing the artifact results. With this dataset, the number of iterations can be increased up to **4** by modifying **`self.Iterations`** in:

`Experiments.py`

For example:

```python
self.Iterations = 4
```

The extended dataset available on Zenodo supports up to **500 iterations**.

---

## Hardware and Software Dependencies

The artifact can run on standard systems with **16 GB RAM** and approximately **50 GB of available disk space**. It was tested successfully on **Google Colab** and additionally on the following two hardware/software environments.

### 🖥️ Environment A — Workstation

| Component | Specification |
|---|---|
| **Operating system** | Ubuntu 24.04.4 LTS |
| **CPU** | Intel Core i9-9920X @ 3.50 GHz |
| **CPU usage** | One core used |
| **Python** | 3.12.3 |

The corresponding Python package versions are:

| Package | Version |
|---|---:|
| `numpy` | 2.4.3 |
| `scipy` | 1.17.1 |
| `simpy` | 4.1.1 |
| `matplotlib` | 3.10.8 |
| `PuLP` | 3.3.0 |

### 💻 Environment B — Laptop

| Component | Specification |
|---|---|
| **Operating system** | Ubuntu 18.04 LTS |
| **CPU** | Intel Core i7-10850H @ 2.70 GHz |
| **CPU usage** | One core used |
| **Python** | 3.11.0 |

The corresponding dependency versions are:

| Package | Version |
|---|---:|
| `numpy` | 2.4.4 |
| `scipy` | 1.17.1 |
| `simpy` | 4.1.1 |
| `matplotlib` | 3.10.8 |
| `PuLP` | 3.3.0 |

All required dependencies are listed in:

`requirements.txt`

Other compatible versions may also work; however, reported execution times may vary depending on processor performance and system load.

To install all requirements compatible with **Environment B** automatically, run the following command once from the command line or within Google Colab before executing the project:

```bash
pip install -r requirements.txt
```

---

## Hardware Requirements

The code has been tested on standard hardware with:

- **16 GB RAM**
- **50 GB of available disk space**


Alternatively, the artifact can be executed on **Google Colab**. To do so, you need a Google account. Once signed in, clone the GitHub repository, install the required dependencies, and run the code by following the instructions provided below.

> [!TIP]
> Google Colab is a convenient option for evaluators who do not want to configure a local Python environment.
>
## Benchmark: Nym Network Dataset

Our evaluation relies on empirical latency, geographical-location, and node-processing-capacity information derived from the [Nym network](https://nym.com) and measurements from the **RIPE Atlas** dataset.

### 📦 Short Dataset — GitHub

The standard GitHub artifact contains the reduced dataset:

`Nym_RIPE_dataset_short_version.pkl`

This dataset contains four independent snapshots of the network:
- `It1` - `It2` - `It3` - `It4`

Consequently, the bundled GitHub artifact supports experiments over up to **4 distinct network configurations**. For practical artifact evaluation, the default configuration uses:

```python
self.Iterations = 1
```

in:

`Experiments.py`

This setting minimizes the artifact execution time while preserving the experimental configuration used in the paper. Evaluators may increase the number of iterations up to **4** without downloading any additional data. For example:

```python
self.Iterations = 4
```

> [!NOTE]
> The short dataset included in the GitHub repository is sufficient for standard artifact evaluation and for reproducing the main trends reported in the paper.

### 📦 Extended Dataset — Zenodo

For users interested in running experiments over a larger number of independent network configurations, we additionally provide: `Nym_RIPE_dataset_long_version.pkl` through the **Zenodo archive**. The extended dataset contains up to **500 network snapshots** and can therefore be used to reproduce longer experimental runs, including configurations closer to those used in the full evaluation reported in the paper.

Because of its approximately **3 GB** size, the extended dataset is not included directly in the GitHub repository.

> [!TIP]
> Use `Nym_RIPE_dataset_short_version.pkl` for standard artifact evaluation. Use `Nym_RIPE_dataset_long_version.pkl` when running experiments with more than four iterations.

### 🔧 Using the Extended Dataset

To use the extended dataset, first download: `Nym_RIPE_dataset_long_version.pkl` from the Zenodo archive. Then change the dataset-loading path in: `Baseline_functions.py` from the short dataset:
```python
Nym_RIPE_dataset_short_version.pkl
```
to:
```python
Nym_RIPE_dataset_long_version.pkl
```

After changing the dataset path, increase: `self.Iterations` in: `Experiments.py` to the desired number of iterations. For example:
```python
self.Iterations = 100
```
The extended dataset supports values up to:
```python
self.Iterations = 500
```
> [!WARNING]
> Increasing the number of iterations substantially increases the execution time. The computational cost grows approximately linearly with the number of network snapshots evaluated.
