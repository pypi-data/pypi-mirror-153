.. _creating_xt_services:

=========================================
Creating Azure Cloud Services for XT
=========================================

XT uses a set of Azure cloud services to run jobs on cloud computers, log statistics, and to store experiment artifacts. 

If you need to create a new set of Azure cloud services to support and run your XT machine learning experiments, follow the instructions in this topic.

.. note:: If you already have a set of Azure cloud services that you want to use with XT, see :ref:`Setting up your XT Installation <xt_config_file>` and for more information.

After you install XT, run the **xt create services template** command to create the template for the new cloud services you'll use with XT. 

Using the **xt create services template** command, setup should take the following times:
    - Create the 6 Azure services (20 mins);
    - Add the service secure keys and XT certificate to the key value (15 mins);
    - Edit the local XT config file (15 mins).

------------------------------
Solo and Team Setups
------------------------------

Multiple XT users can share a set of XT services.

If you're in a development team that wants to share a set of Azure services, choose a team member to be the XT admin. The XT admin manages creation of the XT services and maintains a list of your service users.

If you are setting up XT for your own use, you create the XT services as the solo user.

.. note:: Your organization may have a set of sandbox cloud services on Azure, which are designed for trying out and learning how to use XT. When you are ready to do work, you will want to create the complete set of services for your team.

--------------------------
The Azure Services for XT
--------------------------

Every XT installation uses 6 Azure services:

    - **Storage**            Provides cloud storage for your experiments
    - **Mongo DB**           Database for statistics and metrics of your experiments
    - **Key Vault**          Secure credential storage for Azure services
    - **Azure Batch**        A general compute service for on-demand Virtual Machine deployment
    - **Azure ML**           Compute services designed for Machine Learning on VMs. **This is an Advanced XT application**
    - **Container Registry** Storage for Docker images

The following steps illustrate how to create these services from the Azure Portal (https://portal.azure.com). We use default settings for service creation except where noted. 

.. note:: Your service names will differ from those shown below; ensure consistency with your service names, and note them down in case of mistakes. Even a single character being off in a service name entry is enough to keep the process from a successful conclusion. 

--------------------------------
Create services template command
--------------------------------

As noted, you start by running the **xt create services template** command. It generates an Azure template that you upload to the Azure Portal.  

.. code-block::

   (xt) C:\ExperimentTools\docs\xt> **xt create services template**
   
   template generated: create_xt_service_template.json
   To create the resources for your XT team:

    1. Browse to the :ref:`Azure Portal Custom Template Deployment page: 
    https://ms.portal.azure.com/#create/Microsoft.Template`_.
    2. Select 'Build your own template in the editor'.
    3. Copy/paste the contents of the generated file into the template editor or select Load file from the menu.
    4. Click 'Save'.
    5. Select the billing subscription for the resources.
    6. For a resource group, choose 'Create new' and enter a simple, short, and unique team name (no special characters).
    7. Check the 'I Agree' checkbox and choose 'Purchase'. 
    8. If you receive a 'Preflight validation error', you may need to choose another (unique) team name.
    9. After 5-15 minutes, you should receive a 'Deployment succeeded' message in the Azure Portal.
    10. At this point, you can create a new local XT config file for your team.

The template is a schema file in JSON. By default, the **xt create services template** command places this file in your home directory, which is c:\\<username> (for Windows) or /home/<username> (for Linux). 

.. note:: You can copy and paste the contents of the template JSON file as the command suggests, or load it into the custom template page. (After selecting **Build your own template in the editor**, choose **Load file**.) In either case, you will note that your Azure tenant ID appears throughout the template. Avoid changing any values in the template file at this phase.

After clicking **Save**, select the Azure billing **Subscription**. 

If you already have a **Resource group**, choose that from its drop-down as well, or choose **Create new** to create a new one. 

After you check the **I Agree** checkbox, choose **Purchase**. Azure goes to work building your resource group and its component resources.

---------------------------------------------------
Creating the Vault Secret
---------------------------------------------------

After you establish the Azure services and your resource group, you will need to install your Key Vault secrets for your Azure services. You do this by creating a single secret that contains the keys for 4 of your services) and add it to your vault.  Part of the task involves accessing your newly created Azure services.  

To access services in the Azure Portal, we suggest using the Azure web UI:

    - Log in to your Azure account.
    - Choose **Resource groups** in the left panel. 
    - Choose your team's resource group.
    - Find and choose the desired service (you can ignore the service names with extra text appended to them).

#. Using a code or text editor, paste the following JSON dictionary string into an empty file::

    { 
        "phoenixstorage": "key": 
        "mongodb: "key",  
        "phoenixbatch": "key", 
        "phoenixregistry": "key"
    }

#. Replace each of the service names in the above with your Azure service names (suggestion: do an editor search & replace "phoenix" to your team name).

#. For each "key" string, replace with the associated service key or connection string values. For this step, go to each service in the Azure Portal, choose the **Access Keys** tab or **Connection string** tab in the left panel, and copy the primary key or connection string value.

   For the **Storage** service:

      #. Navigate to your Azure storage service.
      #. Choose the **Access Keys** tab in the service's left panel.
      #. Select the **Key 1** field's copy-to-clipboard button.
      #. Paste the storage services key into your editor for the Azure Storage Service key.

   For the **Mongo DB** service:

      #. Navigate to your Mongodb service.
      #. Choose the **Connection string** tab in the service's left panel.
      #. Click the **PRIMARY CONNECTION STRING** field's copy-to-clipboard button.
      #. Paste the mongodb key string into your editor for the MongoDB service key.

   For the **Azure Batch** service:

      #. Navigate to your Azure Batch service.
      #. Choose the **Keys** tab in the service's left panel.
      #. Choose the **Primary access key** field's copy-to-clipboard button.
      #. Paste the batch key value into your editor for the Batch service key.

   For the **Container Registry** service:

      #. Navigate to your registry service.
      #. Choose the **Access Keys** tab in the service's left panel.
      #. Set the Admin User button to **Enable** if it isn't already enabled.
      #. Choose the **Password** field's copy-to-clipboard button.
      #. Paste the copied password value into your editor for the Registry service key. 

   The result should resemble the following::

      { 
          "phoenixstorage": "qfXOrW7bHQwVOSQ20ViTlsh4GRSmn4UwzbdMTkqqGlVt9sqtwHuWVyBR1XRGti3K1lVMIk4k0S1xgOz58eT4ag==",   
          "phoenixmongodb": "mongodb://xtxtdocsmongodb:mBoJtNrGtkAhwnzRzbT664H3wAFZvwz9l3ARygXzlHBUQerwZwv7QpbU5Nw9pnV9YyNA9wUnrmLGbfFLB7WH3g==@xtxtdocsmongodb.documents.azure.com:10255/?ssl=true&replicaSet=globaldb",  
          "phoenixbatch": "/suVqpCkEoC8n1VA0XRhjR24YNKdisfwIVwoyNtIBsdCsqKgm6QDBoaB6kHxACB7a4sHr0WSbkic59o67WCB7w==", 
          "phoenixregistry": "qHHBRO8okQdwOqBYnp=a9XMIceNUuoDl"
      }

#. From your code/text editor, copy the entire JSON dictionary string that you modified in Step 3 (both service names and keys) into your clipboard.

#. In the Azure Portal, do the following:

   a. Navigate to your team's (or your own) Key Vault service. 
   b. Choose the **Secrets** tab in the left panel.
   c. Choose **+ Generate/Import**.
   d. For **Name**, enter "xt-keys".
   e. For the **Value**, paste in the copied JSON dictionary (Ctrl+v).
   f. Click **Create**.

#. When you're finished, delete any files or open editor instances containing any key information.

*******************************************
Adding the XT certificates to the Key Vault
*******************************************

You also need to separately add your XT certificates to the Azure Portal. Do the following:

#. Navigate to the Key Vault service associated with your Azure tenant. 
#. Choose the "Certificates" tab in the left pane. 
#. Create the CLIENT CERT:

   a. Click **+ Generate/Import**.
   b. For the **Method of Certificate Creation**, select "Generate".
   c. For the **Certificate Name**, enter "xt-clientcert".
   d. For the **Subject**, enter "CN-xtclient.com".
   e. For the **Content Type**, change it to "PEM".
   f. Click **Create**.

#. Create the SERVER CERT:

   a. Click **+ Generate/Import**.
   b. For the **Method of Certificate Creation**, select "Generate".
   c. For the **Certificate Name**, enter "xt-servercert".
   d. For the **Subject**, enter "CN-xtserver.com".
   e. For the **Content Type**, change it to "PEM".
   f. Click **Create**.

-----------------------------------------------------------
Create a Compute Instance for your AML service
-----------------------------------------------------------

#. Navigate to your Azure ML service.
#. Choose the **Compute** tab in the left panel.
#. Click **+ New**.
#. For **Compute Name**, we suggest the team name followed by "compute" (such as phoenixcompute).
#. For **Virtual Machine Size**, select the CPU/GPU configuration for the VMs your service will use. 

   .. note:: You can incur expenses by choosing a VM size that uses substantial resources.

#. Click **Create**.

-----------------------------------------------------------
Editing your local XT config file 
-----------------------------------------------------------

To edit your local XT config file ('xt config' cmd), do the following:

#. Open your local xt_config.yaml file. By default, this file is located in the c:\\<username> folder (for Windows) or /home/<username> (for Linux).

#. Copy/paste the following sections (or merge them with existing sections of the same name):

.. code-block:: none 

  external-services: 
    phoenixbatch: {type: "batch", key: "$vault", url: "xxx"} 
    phoenixaml: {type: "aml", subscription-id: "xxx", resource-group: "phoenix"} 
    phoenixstorage: {type: "storage", provider: "azure-blob-21", key: "$vault"} 
    phoenixmongodb: {type: "mongo", mongo-connection-string: "$vault"} 
    phoenixkeyvault: {type: "vault", url: "xxx"} 
    phoenixregistry: {type: "registry", login-server: "xxx", username: "xxx", password: "$vault", login: "true"} 

  xt-services:
    storage: "phoenixstorage"        # storage for all services 
    mongo: "phoenixmongodb"          # database used for all runs across services 
    vault: "phoenixkeyvault"         # where to keep sensitive data (service credentials) 
.. only:: not internal 
  
  .. code-block:: none 

    compute-targets:
      batch: {service: "phoenixbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm", docker: "none"} 
      aml: {service: "phoenixaml", compute: "xxx", vm-size: "Standard_NC6", nodes: 1, low-pri: false}
.. only:: internal 

  .. code-block:: none 

    compute-targets:
      batch: {service: "phoenixbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm", docker: "none"} 
      philly: {service: "philly", vc: "msrlabs", cluster: "rr2", sku: "G1", nodes: 1, low-pri: true} 
      aml: {service: "phoenixaml", compute: "xxx", vm-size: "Standard_NC6", nodes: 1, low-pri: false}      
.. code-block:: none 

    general:
      workspace: "xxx"
      experiment: "xxx"
      primary-metric: "test-acc"             # name of metric to optimize in roll-ups, hyperparameter search, and early stopping
      maximize-metric: true                  # how primary metric is aggregated for hp search, hp explorer, early stopping 
      xt-team-name: "phoenix"                # for use with XT Grok
      bigbatch: {service: "labcoatbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm"}
      pip-packages: ["torch==1.2.0", "torchvision==0.4.1", "Pillow==6.2.0", "watchdog==0.9.0", "seaborn", "pandas", "xtlib==*"]       # packages to be installed by pip (xtlib, etc.)

    setups:
      local: {activate: "$call conda activate $current_conda_env", conda-packages: [], pip-packages: ["xtlib==*"]}
      py36: {activate: "$call conda activate py36", conda-packages: [], pip-packages: ["xtlib==*"]}
      aml: {pip-packages: ["torch==1.2.0", "torchvision==0.4.1", "Pillow==6.2.0", "watchdog==0.9.0", "xtlib==*"] }

#. Replace all occurences of "phoenix" with the name of your team.

#. Replace all "xxx" values with the associated property of the specified service, using information from the Azure Portal.

#. For the "compute-targets" and "general" sections, review the settings and edit as needed.  See the XT Config File help topic for additional information about these properties.

-----------------------------------------------------------
Test your new XT services
-----------------------------------------------------------

Test your new XT services configuration by running XT in the directory that contains your local XT config file. Try the following commands in the specified order:

    #. **xt list workspaces**
        - Tests that your Key Value and Storage services are configured correctly.
        - If an error occurs, double check the Key Vault service properties and XT configuration file properties for those services.

    #. **xt create workspace ws-test** 
        - Checks to see that your Storage account is writable. 
        - If you see a "Block blobs are not supported" error, you probably selected the wrong version of the storage **kind** property in the Azure storage configuration.  If this is the case, you will need to recreate the storage services.

    #. **xt run <script>**
        - Checks for the correct configuration of the Mongo DB service.
        - If you see a **getaddrinfo failed** error, you may have specified the wrong connection string for mongodb.  if so, update the xt-keys secret in the vault.

    #. xt run --target=batch <script>
        - This will ensure that the Batch service is configured correctly

    #. xt run --target=aml <script>
        - this will ensure that the Batch service is configured correctly

If you need to recreate one or more of the cloud services, do the following:

    #. Delete the old service in the Azure console.
    #. Create the new service using the same name.  Be aware that some services may take 5-10 minutes before the name can be reused.
    #. Get the keys string from the "xt-keys" secret in the Key Vault.
    #. Use an editor to update the keys for any new services.
    #. Create a new version of the xt-keys secret with the updated JSON dictionary string.
    #. On your local machine, be sure to run **xt kill cache** before trying further testing.

.. seealso:: 

    After creating your XT services, you need to set up your XT project to do your first job runs. See :ref:`Setting up your XT project <prepare_new_project>` for more information.
 
