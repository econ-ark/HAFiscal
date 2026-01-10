# Binder Configuration

This directory contains configuration files for [MyBinder.org](https://mybinder.org), which allows users to launch interactive Jupyter notebooks in the cloud.

## Fast Launch with Pre-built Docker Image

**Important:** This repository uses a pre-built Docker image (`llorracc/hafiscal-public:latest`) to dramatically speed up MyBinder launch times.

- **Without pre-built image:** 10-15 minutes to build
- **With pre-built image:** 30-60 seconds to launch

The `Dockerfile` in this directory tells MyBinder to pull the pre-built image from DockerHub instead of building from scratch.

## Files

- **`Dockerfile`** - References pre-built Docker image from DockerHub (primary configuration)
- **`environment.yml`** → symlink to `../environment.yml` (Single Source of Truth, used for local testing)
- **`apt.txt`** - System packages to install via apt-get (legacy, superseded by Dockerfile)
- **`postBuild`** - Post-installation script (legacy, superseded by Dockerfile)
- **`requirements.txt`** - Additional pip requirements (legacy, superseded by Dockerfile)

## How It Works

1. MyBinder detects `binder/Dockerfile` and uses it as the primary build configuration
2. The Dockerfile pulls `llorracc/hafiscal-public:latest` from DockerHub
3. This image already contains:
   - Full TeX Live installation
   - Python 3.11 with all dependencies
   - Jupyter, Voila, and all required packages
   - Complete HAFiscal codebase
4. MyBinder launches the container (fast!) instead of building from scratch (slow)

## Updating the Docker Image

When you make changes to the repository that require rebuilding the Docker image:

1. Build and push the updated image to DockerHub:
   ```bash
   cd /path/to/HAFiscal-Public
   docker build -t llorracc/hafiscal-public:latest .
   docker push llorracc/hafiscal-public:latest
   ```

2. MyBinder will automatically pull the new image on the next launch

## Single Source of Truth

The `environment.yml` file is a **symlink** to the root-level `environment.yml`. This ensures:

- Only one environment specification to maintain
- Binder environment matches local development environment
- Changes to root `environment.yml` automatically apply to binder

When synced to HAFiscal-Public via `makePublic-master.sh`, the symlink is materialized (converted to a regular file) by rsync's `-L` flag, which is the correct behavior for distribution.

## Testing Binder Locally

To test the binder configuration locally:

```bash
# Activate the environment
conda env create -f ../environment.yml
conda activate hafiscal

# Or with uv
uv sync --group=standalone
```

## Launching on MyBinder

Click the binder badge in the main README to launch the repository on MyBinder.org.
