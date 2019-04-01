Job Delete/Cancel
=================

==========================

All the requests reported below must be appended to the service endpoint:

**https://bspsa.cineca.it**

The allowed HPC string values are:

* pizdaint
* nsg

The allowed Project string values are:

* bsp_pizdaint_01
* bsp_nsg_01

==========================

Deleting a job from a HPC system is perfomed through a **DELETE** request
removes all the output files and related info concerning that job, on the HPC.

Canceling a job is also performed throuh a **DELETE** request and allows to 
cancel a job before it is terminated. In this case, the user's resources which
have not been used will be restored.

**URL: /jobs/**\ *(string: hpc)*\ **/**\ *(string: project_name)*\ **/**\ *(string: job_id)*\ **/** 

**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Delete a job*

        **Example Request**

        .. code::

            DELETE /jobs/nsg/bsp_nsg_01/NGBW-JOB-NEURON75_TG-E1B7ADD55CB54F1B9468EEEDFE9F6A64                  HTTP/1.1
            Authorization:              Bearer Token


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            {
                u'end_date':            u'2019-03-26T16:45:24Z',
                u'failed':              False,
                u'id':                  2,
                u'init_date':           u'2019-03-20T16:44:36Z',
                u'job_id':              u'NGBW-JOB-NEURON75_TG-E1B7ADD55CB54F1B9468EEEDFE9F6A64',
                u'owner':               u'306328',
                u'project':             1,
                u'project_hpc':         u'NSG',
                u'project_name':        u'bsp_nsg_01',
                u'runtime':             0.5,
                u'stage':               u'DELETED',
                u'terminal_stage':      True,
                u'title':               u'a job title'
            }

**Example:**

    * *Cancel a job*

        **Example Request**

        .. code::

            DELETE /jobs/nsg/bsp_nsg_01/NGBW-JOB-NEURON75_TG-E1B7ADD55CB54F1B9468EEEDFENEHCJ7                  HTTP/1.1
            Authorization:              Bearer Token


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            {
                u'end_date':            u'2019-03-26T16:45:24Z',
                u'failed':              False,
                u'id':                  54,
                u'init_date':           u'2019-03-20T16:44:36Z',
                u'job_id':              u'NGBW-JOB-NEURON75_TG-E1B7ADD55CB54F1B9468EEEDFENEHCJ7',
                u'owner':               u'306328',
                u'project':             1,
                u'project_hpc':         u'NSG',
                u'project_name':        u'bsp_nsg_01',
                u'runtime':             0.5,
                u'stage':               u'CANCELED',
                u'terminal_stage':      True,
                u'title':               u'a job title'
            }

