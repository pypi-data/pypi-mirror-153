.. _sql_database:

==============================================
Configuring XT to use Azure SQL Server
==============================================

The default database for XT is MongoDB, but SQL Server scales better 
for XT users that need to train lots of runs simultaneously.

Here are the suggested steps for setting up XT to use Azure SQL Server
for its database (first at a high level, followed by the detail for each step):

    1. Create an Azure SQL Server service and database
    2. Configure the Firewall for your SQL database
    3. Create a new Azure Storage account (to be paired with the SQL database)
    4. Add a new store to your XT config file
    5. Add keys for your 2 new services to your XT vault secret
    6. Add support the install of the ODBC driver on your compute node
    7. Add support the install/build of pyodbc (python package)
    8. Test your new SQL-based store

-------------------------------------------------
1. Create an Azure SQL Server and Database
-------------------------------------------------

From the Azure Portal (https://azure.microsoft.com/en-us/features/azure-portal/):

    1. Sign in 
    2. Click on: Create a Resource
    3. Search for: Sql Database
    4. Click on: SQL Database (from Microsoft)
    5. Click on: Create
    6. For "Database name", enter a name "xt_db"
    7. For "Server", click "Create new" (and a panel will open)
    8. In the "New Server" panel:

        - Server name: enter a unique name (we suggest your team name or a variant of it)
        - Server admin login: enter a login name (we suggest "admin")
        - Server password: select a password for the admin login
        - Location: make sure this matches the region of your Azure Storage account
        - Click OK

    9. Leave the other settings in the default state
    10. Click: Review + Create
    11. Click: Create
    12. It will take about 15 minutes to deploy the Server and the Database
    13. Once the deployment has completed, click on "go to new resource"

-----------------------------------------------------
2. Configure the Firewall for your SQL database
-----------------------------------------------------

From the overview page for the "xt_db" database:
    
    1. click on "Set Server Firewall" at the top of the page
    2. Click on "Add Client IP" and give the rule a name ("my rule" will work)
    3. To enable just your own access, enter your machine's IP address for both "Start IP" and "End IP"
    4. To enable anyone to connect to the SQL database, enter "0.0.0.0" for the Start IP, and "255.255.255.255" for the End IP
    5. To sure to click the "Save" button at the top of the page (to save your settings)

-------------------------------------------------
3. Create an Azure Storage Account
-------------------------------------------------

From the Azure Portal (https://azure.microsoft.com/en-us/features/azure-portal/):

    1. Sign in 
    2. Click on: Create a Resource
    3. Search for: Azure Storage
    4. Click on: Storage account (Microsoft)
    5. Click: Create
    6. Fill in needed fields, leaving default settings for everything else.
    7. Click: Review + Create
    8. Click: Create
    9. It will take about 5 minutes to deploy the Storage account

-------------------------------------------------
4. Add a new Store to your XT config file
-------------------------------------------------

To add a new SQL-enabled Store to your config file:

    1. Open your local (project) xt_config.yaml file in an editor
    2. Under "stores", add an entry like the following::
       
        my_sql_store: {storage: "xxx", database: "yyy",  vault: zzz, target: "local"}

    3. In the above entry, replace "xxx" with the name of your new Azure Storage account
    4. Replace "yyy" with the name of your new SQL Server service
    5. Replace "zzz" with the name of your existing Azure Key Vault service
    6. In the "external-services" section, add an entry like the following::

        xxx: {type: "storage", provider: "azure-blob-21", key: "$vault"}

    7. In the above entry, replace "xxx" with the name of your new Azure Storage account
    8. In the "external-services" section, add an entry like the following::

        yyy: {type: "odbc", connection-string: "$vault"}

    9. Replace "yyy" with the name of your new SQL Server service

    10. when you are ready to use the new store, set the value of the "store" outer 
        property of your config file to "my_sql_store" (or whatever you decided to call
        your new store entry from step #2).

--------------------------------------------------------------
5. Add keys for your 2 new services to your XT vault secret
--------------------------------------------------------------

From the Azure Portal (https://azure.microsoft.com/en-us/features/azure-portal/):

    1. Sign in 
    2. In the Search bar at the top, search for "Key Vaults"
    3. Click on: your key vault name
    4. Click on: Secrets
    5. Click on: "xt-keys" (or the name you used to store your XT secret, if different)
    6. Click on: Current Version
    7. Click on: the "copy to clipboard" button to the right of the "Secret" entry
    8. Paste the current secret into an editor
    9. Add something like the following after the opening JSON "{"::

        "xxx": "xxx-key", "yyy": 
          "DRIVER={ODBC Driver 17 for SQL Server};SERVER=sss.database.windows.net;PORT=1433;DATABASE=xt_db;UID=uuu;PWD=ppp"

    10. replace "xxx" with the name of your new Storage acount
    11. replace "xxx-key" with the KEY for your new Storage account
    12. replace "yyy" with the name of your new SQL Server service
    13. replace "sss" with the name of your new SQL Server service
    14. replace "uuu" with your SQL admin login name
    15. replace "ppp" with the SQL admin log password
    16. at the top of the Azure Portal page, click on the "xt-keys" entry in the breadcrumb UI at the top 
    17. Click on: "+ New version"
    18. In the "Value" textbox, paste in the COMPLETE new JSON text for the secret (from step 9 in this section)
    19. Click on "Create"

----------------------------------------------------------------------------
6. Add support for the install of the ODBC driver on your compute node
----------------------------------------------------------------------------

If you are using Azure Batch without a docker image, the ODBC driver should already be installed and 
you are done with this step.

If you are using 1 of XT's latest docker images on your compute node, the ODBC driver is pre-installed 
and you are done with this step.  The XT docker images are (as pre-defined in the default/factory config file):

    - pytorch-xtlib: {image: "rfernand/pytorch-xtlib:torch_1.6_cuda_10.1_xtlib_230_odbc17"}

    - pytorch-xtlib-cuda9: {image: "rfernand/pytorch-xtlib-cuda9:torch_1.6_cuda_9.2_xtlib_230_odbc17"}

The "cuda9" version of these docker images should be used on systems with older GPUs (K80, RTX 1080 TI, etc.).

If none of the above apply to you, you will need to install the ODBC driver either in your docker image 
(if you are using docker) or as a set of "pre-cmds" in the "setup" entry used by your compute target in the XT config file.

The commands to install the ODBC driver for a docker image based on Ubuntu 16 are::

    RUN apt-get update
    RUN apt-get install -y curl
    RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
    RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
    RUN apt-get update
    RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
    RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
    RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
    RUN apt-get install -y unixodbc-dev


The commands to use in "pre-cmds", if you are not using docker, are the same as shown above, but with the "RUN" prefix removed.

If you are using Ubuntu 18.04, you should replace the "16.04" with "18.04" in the above commands.

--------------------------------------------------------------------------------------------
7. Add support for the install/build of pyodbc (python package)
--------------------------------------------------------------------------------------------

If you are using one of the XT docker images, pyodbc is preinstalled and you are done with this step.

The pyodbc PIP installable package has 2 special requirements:

    - it must be built from source (and therefore requires the LINUX "build-essential" tools)
    - it requires a sql.h header file (which requires the "unixodbc-dev" package)

The following pre-cmds (in your target's 'setup' entry) can be used to correctly install the pydobc package::

    pre-cmds: ['sudo apt-get -y update', 'sudo apt-get -y install build-essential unixodbc-dev']

These "pre-cmds" are run before we run conda and pip commands as specified by your setup entry, so they will
install the build tools and the SQL header file before the pip install of xtlib tries to install its odbc dependency.

---------------------------------------------------------------------------------------------
8. Test your new SQL-based store
---------------------------------------------------------------------------------------------

Steps:
    1. set the outer property "store" in your XT config file to the name of your new store
    2. run: xt clear credentials  (will force XT to load your updated Key Vault secret)
    3. run: xt list runs     (this will create the workspace from your config file and should show no runs)

Congratulations - you did it!
