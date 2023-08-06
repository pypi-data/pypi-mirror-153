# Setup

Clone the repository:
```
git clone ssh://git@gitlab.cern.ch:7999/clcheng/quickstats.git
```

### 1. CERN User

To set up from lxplus, just do
```
source setup.sh
```

### 2. Genearl User

To set up locally, make sure you have pyROOT 6.22+ installed (using conda is recommended), and do
```
pip install quickstats
```
### Important: First-time compilation

To compile c++ dependencies, do this for first time use
```
quickstats compile
```
### Installing pyROOT

Simplest way to install pyROOT is via conda
```
conda install -c conda-forge ROOT
```

# Command Line Tools

## Run Pulls
```
quickstats run_pulls -i <input_ws_path> -d <dataset_name> -p <np_name/pattern> --poi <poi_name> --parallel -1 -o <output_dir>
```

The following options are available

| **Option** | **Description** | **Default** |
| ---------- | ---------- | ----------- | 
| `-i/--input_file` | Path to the input workspace file | - |
| `-w/--workspace` | Name of workspace. Auto-detect by default. | None |
| `-m/--model_config` | Name of model config. Auto-detect by default. | None |
| `-d/--data` | Name of dataset | "combData" |
| `-p/--parameter` | Nuisance parameter(s) to run pulls on. Multiple parameters are separated by commas. Wildcards are accepted. All NPs will be run over by default| "" |
| `-x/--poi` | POIs to measure. If empty, impact on POI will not be calculated. | "" |
| `-r/--profile` | Parameters to profile | "" |
| `-f/--fix` | Parameters to fix | "" |
| `-s/--snapshot` | Name of initial snapshot | "nominalNuis" |
| `-o/--outdir` | Output directory | "pulls" |
| `-t/--minimizer_type` | Minimizer type | "Minuit2" |
| `-a/--minimizer_algo` | Minimizer algorithm | "Migrad" |
| `-c/--num_cpu` | Number of CPUs to use per parameter | 1 |
| `--binned/--unbinned` | Whether to use binned likelihood | True |
| `-q/--precision` | Precision for scan | 0.001 |
| `-e/--eps` | Tolerance | 1.0 |
| `-l/--log_level` | Log level | "INFO" |
| `--eigen/--no-eigen` | Compute eigenvalues and vectors | False |
| `--strategy`  | Default fit strategy | 0 |
| `--fix-cache/--no-fix-cache` | Fix StarMomentMorph cache | True |
| `--fix-multi/--no-fix-multi` |  Fix MultiPdf level 2 | True |
| `--offset/--no-offset` | Offset likelihood | True |
| `--optimize/--no-optimize` | Optimize constant terms | True |
| `--max_calls` | Maximum number of function calls | -1 |
| `--max_iters` | Maximum number of Minuit iterations | -1 |
| `--parallel` | Parallelize job across different nuisanceparameters using N workers. Use -1 for N_CPU workers. | 0 |
| `--cache/--no-cache` | Cache existing result | True |
| `--exclude` | Exclude NPs (wildcard is accepted) | "" |

## Plot Pulls

```
quickstats plot_pulls --help
```

## Run Likelihood Scan

```
quickstats likelihood_scan --help
```

## Inspect Workspace

```
quickstats inspect_ws --help
```

## Asymptotic CLs Limit

```
quickstats cls_limit --help
```
