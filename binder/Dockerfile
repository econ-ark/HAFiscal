# MyBinder Dockerfile for HAFiscal
#
# This Dockerfile tells MyBinder to use a pre-built Docker image from DockerHub
# instead of building from scratch, which dramatically speeds up launch times.
#
# The image llorracc/hafiscal-public:latest contains:
# - Full TeX Live installation
# - Python 3.11 with all dependencies
# - Jupyter, Voila, and all required packages
# - Complete HAFiscal codebase
#
# MyBinder will pull this image (fast) instead of rebuilding (slow)

FROM llorracc/hafiscal-public:latest

# Set the working directory to match the repository structure
WORKDIR /workspace

# Ensure Jupyter is properly configured for MyBinder
# MyBinder expects to be able to start jupyter notebook/lab
USER root
RUN pip install --no-cache-dir notebook jupyterlab voila || true

# Switch back to the default user (if your image uses a non-root user)
# Adjust this if your base image uses a different user (e.g., vscode)
USER ${NB_USER:-vscode}

# Set the default command for MyBinder
# This will be overridden by MyBinder's own startup commands
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
