#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_batch.py: support for running a XT job on a 1-N Azure Batch Compute boxes.

import os
import datetime
import numpy as np
from interface import implements
from threading import Lock
from datetime import timedelta

from xtlib import utils
from xtlib import errors
from xtlib import scriptor
from xtlib import constants
from xtlib import job_helper
from xtlib import file_utils
from xtlib import store_utils
from xtlib.console import console
from xtlib.helpers.xt_config import XTConfig
from xtlib.report_builder import ReportBuilder
from xtlib.helpers.feedbackParts import feedback as fb
from xtlib.helpers.key_press_checker import KeyPressChecker

from .backend_interface import BackendInterface
from .backend_base import BackendBase

# azure library, loaded on demand
batch = None   
azureblob = None
azuremodels = None
batchmodels = None

class AzureBatch(BackendBase):
    ''' 
    This class submits and controls Azure Batch jobs.  Submit process consists of:
        - building a "node_record" that describes how to launch each node
        - call the appropriate Batch SDK API's to build a batch job and launch it.

    Building a node record:
        - create a Batch ResourceFile for each input file and the expected output files
        - wraps the command(s) for the node by prefixing these commands:

            unzip CODE_ZIP_FN               (the user's source tree)
            conda activate py36             (activate py36 known good ML environment)
            pip install xtlib               (for controller and/or user's script)
            export XT_NODE_ID=nodeNN        (for controller to get his run info from the MRC file)
    '''

    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        super(AzureBatch, self).__init__(compute, compute_def, core, config, username, arg_dict)

        # import azure libraries on demand
        global azureblob, batchmodels, batch
        import azure.storage.blob as azureblob
        import azure.batch.models as batchmodels
        import azure.batch as batch
        # CAUTION: "batchmodels" is NOT the same as batch.models

        if not compute_def:
            compute_def = config.get_target_def(compute)

        self.compute = compute
        self.compute_def = compute_def
        self.core = core
        self.config = config
        self.username = username
        self.custom_image_name = None

        # first, ensure we have a config file
        if config:
            self.config = config
        else:
            self.config = self.core.config

        self.store = self.core.store if core else None
        self.batch_job = None

        store_creds = self.config.get_storage_creds()
        store_name = store_creds["name"]
        store_key = store_creds["key"]
        self.store_name = store_name

        blob_client = azureblob.BlockBlobService(account_name=store_name, account_key=store_key)
        blob_client.retry = utils.make_retry_func()
        self.blob_client = blob_client
        self.batch_client = None
        #console.print("blob_client=", blob_client)

        expire_days = self.config.get("general", "storage-cert-days")
        self.cert_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=expire_days*24)

    def get_name(self):
        return "batch"

    def get_ssh_creds(self, config, job_id, node_index, workspace_id):
        import azure.batch as batch
        import azure.batch.batch_auth as batch_auth

        # get batch credentials
        service_name = "xtsandboxbatch"
        batch_creds = config.get_service(service_name)
        batch_name = service_name
        batch_key = batch_creds["key"]
        batch_url = batch_creds["url"]

        credentials = batch_auth.SharedKeyCredentials(batch_name, batch_key)
        batch_client = batch.BatchServiceClient(credentials, batch_url= batch_url)
        compute_node_ops = batch_client.compute_node

        # get compute node
        store_id = config.get("store")
        batch_job_id = "{}__{}__{}".format(store_id, workspace_id, job_id)

        node_index = 0
        task_id = "task" + str(node_index)
        task = batch_client.task.get(batch_job_id, task_id)

        node_info = task.node_info
        pool_id = node_info.pool_id
        node_id = node_info.node_id

        node = batch_client.compute_node.get(pool_id, node_id)
        #ip_address = node.ip_address

        result = compute_node_ops.get_remote_login_settings(pool_id, node_id)
        ip_addr = result.remote_login_ip_address
        port = result.remote_login_port

        # create the xt-user for this node
        user_name = "xt-user"
        pw = "kt#abc!@XTwasHere"
        is_admin = True
        user = compute_node_ops.models.ComputeNodeUser(name=user_name, password=pw, is_admin=is_admin)

        try:
            compute_node_ops.add_user(pool_id, node_id, user)
        except:
            # ignore if user already exists
            pass

        return {"user": user_name, "pw": pw, "ip_addr": ip_addr, "port": port}


