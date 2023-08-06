.. _xt_and_singularity:

========================================
Running jobs on Singularity with XT 
========================================

XT now supports running jobs on the Microsoft Singularity platform.  The following information is current as of XT build 0.0.264 (Mar-20-2022).

An overview of the Singularity platforms, along with a table of available VC Clusters, can be found here:
    `Singularity Overview <https://dev.azure.com/msresearch/GCR/_wiki/wikis/GCR.wiki/4712/Singularity-Overview>`_ 

A more detailed description of Singularity in provided in their official docs: 
    `Singularity Docs <https://singularitydocs.azurewebsites.net/>`_ 

In this document, we will discuss:
    - using Docker images on Singularity
    - creating Singularity-compliant Docker images
    - how to submit a job to Singularity with XT
    - how to monitor your job
    - how to cancel your job
    - where to find your code files and logs
    - generating reports and plots

------------------------------------
Using Docker Images on Singularity
------------------------------------

On the Singularity platform, all jobs run within a Docker Container/Image.  You have 3 basic choices:
    - run in a Singularity standard container
    - run in your custom container, auto-wrapped on job-submission in a new Singularity-compatible container 
    - run in your custom container that has been made Singularity-compatible

If your XT target does not specify a named docker record, you job will run in the default Singularity container.

A Singularity docker record (in the XT config file) specifies values for the following properties:

    :image:             the name of your image in its container registry 
    :registry:          (optional) a named registry record in the external-services section (specifies the container registry from which your image can be pulled) 
    :sha256:            (optional) the sha256 string used to exactly match a version of your docker image (for auto-wrapping)
    :post_sing_steps:   (optional) a list of docker file commands that will used to build your wrapped docker image (for auto-wrapping) 
    :sing_wrap:         (optional) a bool value specifying if your image should be auto-wrapped to be Singularity compatible when your job is submitted

A list of pre-defined Singularity docker images can be found: 
    - `Singulairy Job Container Images: <https://singularitydocs.azurewebsites.net/docs/container_images/>`_ 

Each Singularity Workspace also defines an Environments page, which define their own set of pre-defined docker images.  This can be found in the "Environments" page 
of the website for your Singularity Workspace.  For examples, here is the Environments page for the "msrresrchws" Workspace: 

    `msrresrchws Environments <https://ml.azure.com/environments?wsid=/subscriptions/22da88f6-1210-4de2-a5a3-da4c7c2a1213/resourcegroups/gcr-singularity-resrch/workspaces/msrresrchws&tid=72f988bf-86f1-41af-91ab-2d7cd011db47#curatedEnvironments>`_ 

If no registry is defined for a docker record, the docker hub registry (docker.io) will be assumed.

To ensure that your image doesn't get auto-wrapped each time you submit a new job, you should:
    - specify the sha256 string for your docker image; this can normally be found in the webpage for your container registry
    - specify the login username and password for your container registry account (in the external-services registry record of your XT config file)

Beware that when Singularity wraps your docker image, it will overwrite your global python environment, meaning your job may run with a different version of
python, PyTorch, etc.  In order to correct this overwrite, you can reinstall things as the last steps in the wrapping of your docker image, 
using the above mentioned **post_sing_steps** property.

-----------------------------------------------
Creating Singularity-Compliant Docker Images
-----------------------------------------------

A simple way to make your docker image Singularity compliant is to create a second docker image as follows:
    - using your original image as the base image
    - add the needed Singularity components
    - run the Singularity compliance tests
    - finally, add any needed commands to reestablish your python environment (pytorch, XT, etc.)

An example Dockerfile for doing the above steps:

.. code-block:: dockerfile
    :linenos:

    # build Singularity-compliant docker image by wrapping your docker image 
    FROM your-registry/your-image-name:your-image-tag as base

    FROM singularitybase.azurecr.io/installer/base/singularity-installer:20220218T112740648 as installer
    FROM singularitybase.azurecr.io/validations/base/singularity-tests:20220309T233405410 as validator
    FROM base

    # get the installation scripts
    COPY --from=installer /installer /opt/microsoft/_singularity/installations/

    # get the validation scripts
    COPY --from=validator /validations /opt/microsoft/_singularity/validations/

    # set validation arguments for expected use of this image
    ENV SINGULARITY_IMAGE_ACCELERATOR=NVIDIA

    RUN \
        # install Singularity-required components 
        /opt/microsoft/_singularity/installations/singularity/installer.sh \

        # run Singularity validation tests
        && /opt/microsoft/_singularity/validations/validator.sh \

        # run your needed post-singularity commands to restore anything overwritten by singularity components
        # for example, here we show 2 cmds that install the latest pytorch/cuda and xtlib
        && conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch  \
        && pip install xtlib==0.0.265 \

        # cleanup files to reduce final docker image size
        && rm -rf /var/lib/apt/lists/* \
        && conda clean -y --all \
        && pip install --upgrade pip \
        && rm -rf  $(pip cache dir) 

To make a Singularity-compliant docker image:
    - copy the above commands to a file named Dockerfile
    - replace the full docker image name on line 2 with the full name of your original docker image
    - modify the lines 26-27 as needed, to restore your python environment
    - run this command (modify -t (target) name as appropriate):
    .. code-block:: dockerfile

        docker build  -t myappname-sing-ready .


A more robust and detailed technique for building Singularity-compliant docker images can be found here:

    `Build Docker images from a non-Singularity base image for Singularity <https://dev.azure.com/msresearch/GCR/_wiki/wikis/GCR.wiki/4742/Build-Docker-images-from-a-non-Singularity-base-image-for-Singularity>`_ 

------------------------------------------------
How to submit your job to Singularity with XT
------------------------------------------------

To run your job on Singularity under XT, you need specify a Singularity target defined in your XT config file (or the factory config file).

A Singularity target record (in the XT config file) specifies values for the following properties:
    :service:   this is the name of the Azure workspace that contains the Virtual Cluster on which you will run
    :compute:   this is the name of the Virtual Cluster
    :vm-size:   this is the instance type name (similiar to Azure SKU names, but slightly different in their spellings)
    :location:  the location in which in want to run (e.g., eastus or westus3)
    :nodes:     the default number of nodes to run your job on
    :sla:       the amount of protection from your job being preempted: premium, standard, basic     
    :setup:     a named record in the setups section of the config file (specifies additional setup commands for your job)
    :docker:    a named record in the dockers section of the config file (specifies the docker image to run your job within)

A table of available VC Clusters, can be found here:
    `Singularity Overview <https://dev.azure.com/msresearch/GCR/_wiki/wikis/GCR.wiki/4712/Singularity-Overview>`_ 

Once you have a defined target (in your own XT config file, or a pre-defined target in the XT factory config file), you can submit a job to 
Singularity as you normally do with the run command, for example:

    xt run --target=eus-v100 myscript.py

--------------------------------------------
How to monitor your Singularity job
--------------------------------------------

You can monitor your Singularity job either in a console window, or thru the Singularity web UI.  For console window monitoring, use the XT monitor command:

    xt monitor job123456

For monitoring your job thru the Singularity web portal, you can click on the job URL that was displayed on the console when you submitted your job, 
or you can navigate to your job by invoking the web portal associated with your target, for example:

    xt view portal eus-v100 --browse

--------------------------------------------
How to cancel your Singularity job
--------------------------------------------

You can cancel your job from the console, using XT:

    xt cancel job job123456

You can also cancel it from the web portal.  See the above section on monitoring your job thru the web portal.

---------------------------------------------
Where to find your code files and job logs
---------------------------------------------

Both XT and Singularity keep their own copies of your submitted code files and user/system generated log files.  The Singularity files are accessible
thru the Singularity web portal or thru the Azure ML/Singularity API. 

The XT files are accessible thru the XT "extract" and "download" commands, the Microsoft Storage Explorer desktop app, or the Azure console.  

---------------------------------------------------------
Generating Reports and Plots for Singularity Jobs
---------------------------------------------------------

The normal XT commands for viewing hyperparameters, metrics, and other log data from jobs also work for Singularity jobs:

    - :ref:`xt list runs <list_runs>`
    - :ref:`xt list nodes <list_nodes>`
    - :ref:`xt list jobs <list_jobs>`

    - :ref:`xt plot <plot>`
    - :ref:`xt plot summary <plot_summary>`
    - :ref:`xt explore <explore>`

    - :ref:`xt view database <view_database>`
    - :ref:`xt view errors <view_errors>`
    - :ref:`xt view events <view_events>`
    - :ref:`xt view log <view_log>`
    - :ref:`xt view metrics <view_metrics>`
    