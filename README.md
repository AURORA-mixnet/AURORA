# AURORA

This repository contains the artifact for the paper titled “AURORA: Throughput- and Congestion-Aware Low-Latency Mixnets with Adversarial Robustness,” accepted at NDSS 2027.

## Overview

Mixnets are overlay networks designed to provide strong anonymity for Internet users against network adversaries. However, this anonymity often comes at the cost of high communication latency and inefficient resource utilization. These limitations can arise from inefficient distribution of mixnodes within the mixnet and routing strategies that do not adequately account for differences among nodes. AURORA addresses these issues by jointly optimizing performance and anonymity.

We evaluate AURORA using two complementary approaches: (1) theoretical analysis and (2) simulation-based analysis.

In the theoretical setting, each proposed technique is evaluated under probability distributions for route selection in mixnets and relevant system characteristics, including inter-node latency and mixnode processing capacity.

In contrast, the simulation-based analysis is implemented in Python using the SimPy discrete-event simulation framework. In simulations, a dynamic set of clients generates packets destined for a set of receivers. These packets traverse mixnodes according to the routing strategies considered in the paper, including RLP, REP, and RBR. Along each route, mixnodes perform mixing operations to anonymize and forward packets.

The artifact contains approximately 10K lines of Python code and provides scripts for reproducing the experiments, figures, and tables presented in the paper. For practical artifact evaluation, the default artifact configuration reduces the number of iterations over independent network snapshots to one, whereas the experiments reported in the paper use up to 500 iterations. All other parameters remain consistent with those used in the paper.


## How to Access

The artifact is available through both a persistent **Zenodo archive** and the corresponding **GitHub repository**:

| Source | Link | Contents |
|---|---|---|
| **Zenodo** | https://doi.org/10.5281/zenodo.21874304 | Full artifact + short and extended datasets |
| **GitHub** | https://github.com/AURORA-mixnet/AURORA | Full artifact + short dataset |

The GitHub repository and Zenodo archive contain the same artifact code. The main difference is the size of the included AURORA dataset.

### 📦 GitHub Dataset

The GitHub repository includes the reduced dataset:

`Nym_RIPE_dataset_short_version.pkl`

**Size:** approximately 20 MB  
**Supported network snapshots:** 4 (`It1`--`It4`)

This dataset is sufficient for reproducing the artifact results. With this dataset, the number of iterations can be increased up to **4** by modifying **`self.Iterations`** in: `Experiments.py`

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
## Benchmark: AURORA Dataset

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

in: `Experiments.py`

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


# Project Structure


```text
AURORA/
│
├── Figures/                                      # Automatically created output directory for generated figures.
│
├── README.md                                     # Main documentation for installing, configuring, and running the artifact.
│
├── ARTIFACT_APPENDIX.pdf                         # Artifact appendix accompanying the AURORA paper.
│
├── requirements.txt                              # Python dependencies required to run the artifact.
│
├── Nym_RIPE_dataset_short_version.pkl            # Reduced Nym/RIPE dataset containing four network snapshots
│                                                 # used for standard artifact reproduction.
│
├── Baseline_functions.py                         # Core baseline, simulation, and analysis routines used to reproduce
│                                                 # the experimental results.
│
├── Experiments.py                                # Defines the artifact experiments and maps input IDs to the
│                                                 # corresponding experiments, figures, and tables.
│
├── FCP_Functions.py                              # Helper functions for fairness-constrained path selection
│                                                 # and related routing computations.
│
├── main.py                                       # Main entry point of the artifact. Allows users to select and run
│                                                 # experiments, figures, and tables.
│
├── Message_.py                                   # Defines simulated packets and stores their target probabilities,
│                                                 # timing information, and client information.
│
├── Message_Genartion_and_mix_net_processing_.py  # Generates packets and submits them to the mixnet during
│                                                 # discrete-event simulations.
│
├── Mix_Node_.py                                  # Models individual mixnodes, including processing capacity,
│                                                 # mixing delays, and probability updates.
│
├── Node_replacement.py                           # Provides stochastic-matrix normalization utilities used when
│                                                 # updating routing matrices.
│
├── NYM.py                                        # Models packet traversal through the Nym mixnet and records
│                                                 # latency and anonymity-related simulation statistics.
│
├── Optimization.py                               # Implements linear-programming routines for constructing
│                                                 # constrained routing matrices.
│
├── PLOTTER.py                                    # Plotting utilities used to generate the figures reported
│                                                 # in the paper.
│
├── Routings.py                                   # Implements routing-distribution construction, latency processing,
│                                                 # and supporting routing operations.
│
└── Sim.py                                        # Constructs and executes the SimPy-based discrete-event
                                                  # mixnet simulations.
```

> [!NOTE]
> The `Figures/` directory is created automatically when the artifact is executed and contains the generated experimental figures.

> [!NOTE]
> The extended dataset `Nym_RIPE_dataset_long_version.pkl` is available separately through the Zenodo archive and is not included in the standard GitHub repository because of its size.

# Evaluation Workflow

## Major Claims

- **(C1):** The first claim concerns the trend illustrated in **Figure 3**. Across all settings and scenarios, we observe that as the tuning parameter **α** or the threshold `T` increases, the mixnet propagation latency increases. This claim is substantiated by **Experiment E1**, which generates Figure 3.

- **(C2):** The second claim concerns the trend illustrated in **Figure 4**. Across all settings and scenarios, we observe that as the tuning parameter **α** or the threshold `T` increases, **M_RL**, the maximum processing load on mixnodes, decreases. This claim is supported by **Experiment E1**, which also generates Figure 4.

- **(C3):** The third claim concerns the trend illustrated in **Figure 5**. Across all settings and scenarios, we observe that as the tuning parameter **α** or the threshold `T` increases, the route-selection predictability metric **RSD** decreases. This claim is supported by **Experiment E1**, which also generates Figure 5.

- **(C4):** The fourth claim concerns the trend illustrated in **Figure 11(a)**. Across the evaluated settings, we observe that as the tuning parameter **α** increases, the total end-to-end mixnet communication latency gradually increases. This claim is supported by **Experiment E2**, which generates Figure 11(a).

- **(C5):** The fifth claim concerns the trend illustrated in **Figure 11(b)**. Across the evaluated settings, we observe that as the tuning parameter **α** increases, the session anonymity attack metric **SAA** decreases, thereby increasing the anonymity of client-destination sessions. This claim is supported by **Experiment E2**, which also generates Figure 11(b).


## Experiments

### E1: Reproducing Figures 3, 4, and 5; Verifying Claims C1, C2, and C3 [< 45 min]

- **Configuration Parameters:** The configuration parameters match those used for Figures 3, 4, and 5. Specifically:
  - `L = 3`
  - `W = 200`
  - `T = 12` for the RBR experiments in which anonymity and performance are evaluated as a function of `α`
  - `α = 0.6` for the RBR experiments in which anonymity and performance are evaluated as a function of `T`
  - `self.Iterations = 1` in `Experiments.py` by default for artifact evaluation

- **Execution:** To run this experiment, either execute:

  ```bash
  python3 main.py
  ```

  and enter `1` when prompted, or directly execute:

  ```bash
  python3 main.py 1
  ```

- **Results:** Upon completion, the following files will be generated in the `AURORA/Figures/` directory:

  ```text
  Fig_3a.png
  Fig_3b.png
  Fig_3c.png
  Fig_3d.png

  Fig_4a.png
  Fig_4b.png
  Fig_4c.png
  Fig_4d.png

  Fig_5a.png
  Fig_5b.png
  Fig_5c.png
  Fig_5d.png
  ```

- **Verification:** Compare the generated figures with Figures 3, 4, and 5 in the paper, shown below. Because the artifact uses a reduced number of iterations for practical execution on personal machines or Google Colab, the reproduced figures may not exactly match the values reported in the paper. For verification purposes, focus on the consistency of the observed trends, particularly whether the corresponding values increase or decrease as expected along the x-axis.

<img width="1571" height="403" alt="image" src="https://github.com/user-attachments/assets/5edf5b69-f14c-42a8-be61-491b55ec048d" />

<img width="1577" height="377" alt="image" src="https://github.com/user-attachments/assets/de33756e-5428-441e-a523-fde95547aa65" />

<img width="1541" height="347" alt="image" src="https://github.com/user-attachments/assets/2ffe7a68-91b1-4aca-92ea-e51ab9d0d512" />



### E2: Reproducing Figures 11(a) and 11(b); Verifying Claims C4 and C5 [< 20 min]

- **Configuration Parameters:** The configuration parameters match those used for Figure 11. Specifically:
  - `L = 3`
  - `W = 80`
  - Routing strategy: `REP`
  - Average mixing delay: `μ = 50 ms`
  - `self.Iterations = 1` in `Experiments.py` by default for artifact evaluation

- **Execution:** To run this experiment, either execute:

  ```bash
  python3 main.py
  ```

  and enter `2` when prompted, or directly execute:

  ```bash
  python3 main.py 2
  ```

- **Results:** Upon completion, the following files will be generated in the `AURORA/Figures/` directory:

  ```text
  Fig_11a.png
  Fig_11b.png
  ```
- **Verification:** Compare the generated figures with Figures 11(a) and 11(b) in the paper, shown below. Because the artifact uses a reduced number of iterations for practical execution on personal machines or Google Colab, the reproduced figures may not exactly match the values reported in the paper. For verification purposes, focus on the consistency of the observed trends, particularly whether the corresponding values increase or decrease as expected along the x-axis.

  
<img width="716" height="265" alt="image" src="https://github.com/user-attachments/assets/702dc9c5-6de2-46a2-aebe-54c0b2ab75d4" />



### E*: Additional Figures and Tables [< 2 h]

If you are interested in running additional experiments that generate specific figures or tables not necessarily associated with the main claims, first execute:

```bash
python3 main.py
```

Then enter the appropriate experiment ID from the table below when prompted.

Alternatively, execute a specific target directly using:

```bash
python3 main.py ID
```

where `ID` is the numerical identifier corresponding to the desired figure or table.

| Target | ID | Target | ID |
|---|---:|---|---:|
| Fig. 3 | `3` | Fig. 4 | `4` |
| Fig. 5 | `5` | Fig. 8 | `8` |
| Fig. 9 | `9` | Fig. 11 | `11` |
| Fig. 12 | `12` | Table 1 | `100` |
| Table 2 | `200` | Table 3 | `300` |
| Experiment E1 | `1` | Experiment E2 | `2` |

> [!NOTE]
> Some results in the paper were originally generated using substantially more iterations and therefore required extended execution times, in some cases up to approximately three weeks. Exact point-by-point reproduction may therefore not be feasible on standard personal machines using the reduced artifact configuration. Running the experiments with fewer iterations should nevertheless reproduce the same overall trends.


## Customizations: Parameter Settings and Execution Time

The network and simulation parameters are initialized in `Experiments.py` and do not require manual modification to reproduce the standard artifact.

For artifact evaluation, the main parameter reduced relative to the full paper evaluation is:

```python
self.Iterations = 1
```

The experiments reported in the paper use up to **500 iterations**.

Users interested in additional experiments may safely adjust the following parameters in `Experiments.py`:

- **`Iterations`**  
  Controls the number of independent network snapshots used in the experiment.
  - The GitHub dataset supports up to **4 iterations**.
  - The extended Zenodo dataset supports up to **500 iterations**.

  To use more than four iterations, download:

  `Nym_RIPE_dataset_long_version.pkl`

  from Zenodo and change the dataset path as described in the Benchmark section.

- **`num_targets`**  
  Controls the number of target packets considered in the simulation.  
  Recommended customizable range: **20–200**.

- **`run`**  
  Controls the duration of each simulation run.  
  Recommended customizable range: **0.3–1.0**.

- **`delay1`**  
  Controls the average delay introduced at each mixnode.  
  Recommended customizable range: **0.01–0.08**.

> [!NOTE]
> **Execution Time and Configuration**
>
> The computational cost grows approximately linearly with the number of iterations because each iteration evaluates an additional network snapshot.
>
> Consequently, an experiment requiring approximately **one hour for one iteration** may require approximately **three weeks when repeated 500 times**.
>
> The reduced artifact configuration is therefore intended to verify the implementation and reproduce the trends underlying the paper's main claims within a practical artifact-evaluation time.
>
> Close numerical agreement with the results reported in the paper requires using the same number of iterations as in the paper.
> Note that the execution times reported here are based on tests conducted in the specified workstation environment. The actual execution time may be shorter or longer depending on the hardware and system environment.
> 
> [!WARNING]
> Other parameters in `Experiments.py` should not be modified unless the evaluator is familiar with the dependencies among mixnet topology, routing algorithms, and simulation parameters.
>
> Arbitrary modifications may generate configurations that no longer correspond to those evaluated in the paper or may lead to invalid simulation behavior or execution errors.
>
> Because the configuration space is large, evaluators are encouraged to contact the authors for guidance regarding substantial changes.
