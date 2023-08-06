.. _getting_started:

========================================
Getting Started with XT
========================================

XT is a command line tool to manage and scale Machine learning (ML) experiments, with a uniform model of workspaces and runs, across a variety of cloud compute services. It supports ML features such as :ref:`live and post Tensorboard viewing <tensorboard>`, :ref:`hyperparameter searching <hyperparameter_search>`, and :ref:`ad-hoc plotting <plot>`.

XT also supports the Experiment Tools Library (XTlib), which is an API for managing and scaling your ML experiments. See :ref:`XT Command Piping <pipes>` for more information.

XT and XTLib's experiment store, based on Azure Storage and Azure Cosmos DB, enables tracking, run compares, reruns, and sharing of your ML experiments. It consists of user-defined workspaces, that can contain sets of user-run experiments. You can upload data/models to storage before job runs and start new experiments on specified machine(s). XT and XTlib support hyperparameter tuning runs using Grid search, Random search, and DGD search. You can monitor job status with Tensorboard and XT's event logs, and generate reports during or after job runs and selective use of filtering, sorts and data columns. 

XT provides access to scalable compute resources, so you can run multiple experiments in parallel and on larger computers or arrays of computers. You can run experiments on your local machine, on other local computers or provisioned VMs, or on cloud computers and Docker containers, allocated on demand through Azure Batch.

-----------------------------------
Where can you run XT?
-----------------------------------

You can use XT on both Windows and Linux platforms. 

XT works with most Python virtual environments. XT is verified to work with the following:

    - Anaconda
    - Virtualenv

We recommend using Python Version 3.6.

This topic introduces you to XT and its various components, and describes how to install and run the XTlib package and its demonstration Python script (called **xt demo**). We also provide a list of additional resources for reference and inspiration at the end of this topic.

---------------------------
Introduction to XT
---------------------------

Your XT installation leverages the following Azure cloud services to help you develop, test and deploy new Machine Learning experiments:

    - Azure Batch
    - Azure Container Registry
    - Azure Cosmos DB - MongoDB
    - Azure Storage
    - Azure Key Vault
    - Azure Virtual Machine / Virtual Machine Scale Set
    - Generic Remote Server
    - Azure Machine Learning Services

.. only:: internal

    - Philly

You conduct your own experiments using the :ref:`**xt run** command <run>` to submit jobs to XT.

-----------------------
XT Requirements
-----------------------

Requirements for installing and running XT are:
    - Windows or Linux OS
    - Python 3.5 or later   (recommended: Python 3.6)
    - Anaconda or other virtual Python environment (recommended: Anaconda)
    - User must have an Azure account (required for authenticated access to Azure computing storage and resources)

.. only:: internal

    - For Linux users who will be using the Microsoft internal Philly services, you should install **curl**. Go to https://www.cyberciti.biz/faq/how-to-install-curl-command-on-a-ubuntu-linux/ to do so.

.. Note:: XT supports all popular Machine Learning frameworks. The following procedure installs PyTorch because it supports the XT demo. XT also supports important ML tools such as TensorFlow. You can also use :ref:`hyperparameter searching <hyperparameter_search>` to tune and improve your machine learning models.

------------------
Installing XT
------------------

XT package installation is straightforward. Follow these steps to set up XT on your computer. You may need to `install Anaconda <https://www.anaconda.com/distribution/>`_ on your system in order to follow these steps:

    **1. PREPARE a conda virtual environment for PyTorch:**
        
        .. code-block::

            > conda create -n MyEnvName python=3.6
            > conda activate MyEnvName
            > conda install pytorch torchvision cudatoolkit=10.1 -c pytorch

    **2. INSTALL XT:**

        .. code-block::

            > pip install -U xtlib

After installing XT, decide on the direction you need to follow to run the XT demo, based on whether or not you have an active set of Azure cloud services to support machine learning:

    - If you already have the needed Azure cloud services, set them up to work with your new XT installation (see :ref:`Setting up your XT Installation <xt_config_file>` for more information);
    - If you need to set up some or all of the Azure cloud services to support XT and to support running the demo, you run an XT utility to generate an Azure template and then use it to set up your cloud services through the Azure portal (see :ref:`Creating Azure Cloud Services for XT <creating_xt_services>` for more information).

**************************************
XT: Basic Mode vs. Advanced Mode
**************************************

.. note:: You can run the XT Demo, and the XT CLI, in two different modes: Basic mode and Advanced mode. 

You can run the XT Demo, and the XT CLI, in two different modes: Basic mode and Advanced mode. The demo and the CLI default to Basic mode, which contains a series of 20 steps that rely on a limited set of cloud services, creating a single workspace, running a single experiment, a single container, a single compute target that is based on Azure Batch, and several other limitations. 

Users can switch from Basic to Advanced mode by editing the **general.advanced-mode** parameter to the value **true** (its default is **false**)::

    general:
        advanced-mode: false    #sets XT CLI to Basic mode

XT Basic Mode supports the following Azure cloud services:

    - Azure Batch

.. only:: internal

    - Philly

**************************************
Running the XT Demo
**************************************

XT offers a self-contained demo that walks you through several usage scenarios, using multiple Machine Learning backends. Each step of the demo, which you run from your Python virtual environment's command line interface, provides descriptions explaining what that step does during the course of a sample experiment.

    **1. Start XT on your system:**
        
        .. code-block::

            > activate xt  # activates the conda virtual environment called XT 

    **2. CREATE a set of demo files:**

        .. code-block::

            > xt create demo xt_demo

            This creates 2 files and 1 subdirectory in the *xt_demo* directory:
                - xt_config_overrides.yaml     (xt config settings)
                - xt_demo.py                   (the demo script)
                - code                         (a subdirectory of code for the demo)

    **3. Start the XT demo:**

        .. code-block::

            > cd xt_demo
            > python xt_demo.py

        Once started, you can navigate thru the demo with the following keys:
            - ENTER (to execute the current command)
            - 's'   (to skip to the next command)
            - 'b'   (to move to the previous command)
            - 'q'   (to quit the demo)

While you run the demo, you may hit a point where it stops running. This typically happens when a numbered demo step relies on a cloud service that may not yet be configured. To continue the demo, note the step where the demo stopped, and enter *python xt_demo.py* once again. Then, press the 's' key to step through the demo past the numbered step where you previously stopped. 

------------
Next Steps
------------

After installation and running the XT demo, you can set up your Azure cloud services to work with XT. You do so by editing the properties inside an important configuration file called the local *xt_config* file. See :ref:`Setting up your XT Installation <xt_config_file>` for more information.

For those just beginning to explore ML on the Microsoft Azure cloud platform, see the `What is Azure Machine Learning? <https://docs.microsoft.com/en-us/azure/machine-learning/>`_ page, and `What is Azure Batch? <https://docs.microsoft.com/en-us/azure/batch/batch-technical-overview/>`_, which gives a full description of the Azure Batch service.

To get a closer look at running jobs using the **xt run** command, see :ref:`XT run command <run>`.