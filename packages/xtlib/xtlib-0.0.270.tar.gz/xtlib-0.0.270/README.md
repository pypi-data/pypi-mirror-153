# XTlib: Experiment Tools Library

XTlib is an API and command line tool for scaling and managing ML experiments.  

The goal of XTLib is to enable you to effortlessly organize and scale your ML experiments.
Our tools offer an incremental approach to adoption, so you can begin realizing benifits immediatly.

XT Key Features
  - Scale ML experiments across multiple COMPUTE services:
      - local machine, VM's, Azure Batch, Singularity, and Azure ML
  - Provide a consistent STORAGE model:
      - workspaces, experiments, jobs, runs
      - blob shares
  - Provide related tooling:
      - live tensorboard, hyperparameter searching, reporting, plotting, utilities

XTLib provides an experiment STORE that enables you to easily track, compare, rerun, and share your ML experiments.  
The STORE consists of user-defined workspaces, each of which can contain a set of user-run experiments.  
XT currently supports 2 STORE services: local (folder-based) and azure (Azure Storage-based).

In addition, XTLb also provides easy access to scalable COMPUTE resources so you can 
easily run multiple experiments in parallel and on larger computers, as needed.  With this feature, 
you can scale from running  experiments on your local machine, to multiple VM's under your control, to compute 
services like Azure Batch and Azure ML.

Finally, XTLib offers a few other experiment-related features to help maximize your ML agility:
    - hyperparameter searching
    - run and job reports
    - ad-hoc plotting

For more information, run: xt --help

# Contributing

Check [CONTRIBUTING](CONTRIBUTING.md) page.

# Microsoft Open Source Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# License

This project is licensed under the terms of the MIT license. See [LICENSE.txt](LICENSE.txt) for additional details.
