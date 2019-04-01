List All Users Jobs
===================

All queries related to all users' jobs are performed through the **/admin/jobs** endpoint. 

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


The List All Users Jobs APIs allow admin to fetch information abount all submitted jobs on the HPC systems using the Service Account. 


**URL: /admin/jobs/**\ *(optional string: hpc)*\ **/**\ *(optional string: project_name)*\ **/**\ *(optional string: job_id)**\ **/**


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Get info on all jobs for all users*

        **Example Request**

        .. code::

            GET /admin/jobs/            HTTP/1.1
            Authorization:              Bearer Token


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Disposition:        application/json

            [
                {
                    u'end_date':        u'2019-03-21T13:15:03Z',
                    u'failed':          False,
                    u'id':              4,
                    u'init_date':       u'2019-03-21T13:13:59Z',
                    u'job_id':          u'42AA3163-F8F7-4502-9640-431ED649DF54',
                    u'owner':           u'301330',
                    u'project':         2,
                    u'project_hpc':     u'PIZDAINT',
                    u'project_name':    u'bsp_pizdaint_01',
                    u'runtime':         0.5,
                    u'stage':           u'SUCCESSFUL',
                    u'terminal_stage':  True,
                    u'title':           u''
                },
                {
                    u'end_date':        u'2019-03-21T13:30:13Z',
                    u'failed':          False,
                    u'id':              6,
                    u'init_date':       u'2019-03-21T13:29:28Z',
                    u'job_id':          u'06E62677-255F-4E13-9E25-F978749540F1',
                    u'owner':           u'301330',
                    u'project':         2,
                    u'project_hpc':     u'PIZDAINT',
                    u'project_name':    u'bsp_pizdaint_01',
                    u'runtime':         0.5,
                    u'stage':           u'SUCCESSFUL',
                    u'terminal_stage':  True,
                    u'title':           u''
                },
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                {
                    u'end_date':        None,
                    u'failed':          False,
                    u'id':              21,
                    u'init_date':       u'2019-03-25T11:08:56Z',
                    u'job_id':          u'NGBW-JOB-NEURON75_TG-3BAAA5A35EA440958BB7406F4DBDC653',
                    u'owner':           u'251951',
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'runtime':         2.0,
                    u'stage':           u'QUEUE',
                    u'terminal_stage':  False,
                    u'title':           u'test-25-mar-19'
                }
            ]


    * *Get info on all jobs submitted on a specific HPC system for all users*

        **Example Request**

        .. code::

            GET /admin/jobs/nsg/        HTTP/1.1
            Authorization:              Bearer Token


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Disposition:        application/json
            
            [
                {
                    u'end_date':        None,
                    u'failed':          False,
                    u'id':              3,
                    u'init_date':       u'2019-03-21T13:11:21Z',
                    u'job_id':          u'NGBW-JOB-NEURON75_TG-E60ADB33CD774FFD9B7EE5805ED03E17',
                    u'owner':           u'301330',
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'runtime':         0.5,
                    u'stage':           u'QUEUE',
                    u'terminal_stage':  False,
                    u'title':           u''
                },
                {
                    u'end_date':        None,
                    u'failed':          False,
                    u'id':              10,
                    u'init_date':       u'2019-03-21T15:23:20Z',
                    u'job_id':          u'NGBW-JOB-NEURON75_TG-03B10581DD5340BC8FCE5BB17566F49B',
                    u'owner':           u'301330',
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'runtime':         0.5,
                    u'stage':           u'QUEUE',
                    u'terminal_stage':  False,
                    u'title':           u''
                },
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                {
                    u'end_date':        None,
                    u'failed':          False,
                    u'id':              64,
                    u'init_date':       u'2019-03-21T21:43:51Z',
                    u'job_id':          u'NGBW-JOB-NEURON75_TG-EAFE7B11DC104805A566AD5E2277A3A5',
                    u'owner':           u'301330',
                    u'project':         2,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'runtime':         0.5,
                    u'stage':           u'QUEUE',
                    u'terminal_stage':  False,
                    u'title':           u''
                }
            ]



    * *Get info all jobs submitted on a specific HPC system's project for all users*

        **Example Request**

        .. code::

            GET /admin/jobs/nsg/bsp_nsg_01/            HTTP/1.1
            Authorization:              Bearer Token


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Disposition:        application/json
            
            [
                {
                    u'end_date':        None,
                    u'failed':          False,
                    u'id':              3,
                    u'init_date':       u'2019-03-21T13:11:21Z',
                    u'job_id':          u'NGBW-JOB-NEURON75_TG-E60ADB33CD774FFD9B7EE5805ED03E17',
                    u'owner':           u'301330',
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'runtime':         0.5,
                    u'stage':           u'QUEUE',
                    u'terminal_stage':  False,
                    u'title':           u''
                },
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                {
                    u'end_date':        None,
                    u'failed':          False,
                    u'id':              10,
                    u'init_date':       u'2019-03-21T15:23:20Z',
                    u'job_id':          u'NGBW-JOB-NEURON75_TG-03B10581DD5340BC8FCE5BB17566F49B',
                    u'owner':           u'301330',
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'runtime':         0.5,
                    u'stage':           u'QUEUE',
                    u'terminal_stage':  False,
                    u'title':           u''
                }
           ]    


    * *Get info on a single job submitted on a specific HPC system's project*

        **Example Request**

        .. code::

            GET /admin/jobs/nsg/bsp_nsg_01/NGBW-JOB-NEURON75_TG-419E34839B144E15A06F9473814926F7            HTTP/1.1
            Authorization:              Bearer Token


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Disposition:        application/json

            {
                u'end_date':            None,
                u'failed':              False,
                u'id':                  16,
                u'init_date':           u'2019-03-21T22:02:39Z',
                u'job_id':              u'NGBW-JOB-NEURON75_TG-419E34839B144E15A06F9473814926F7',
                u'owner':               u'301330',
                u'project':             1,
                u'project_hpc':         u'NSG',
                u'project_name':        u'bsp_nsg_01',
                u'runtime':             0.5,
                u'stage':               u'QUEUE',
                u'terminal_stage':      False,
                u'title':               u'TestJob_SA_NSG'
            }
