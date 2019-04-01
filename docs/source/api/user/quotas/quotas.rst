Quotas
======


All Quotas operations are performed through the **/quotas** endpoint.

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


The Quotas APIs allow user to fetch informations about its resources.


**URL: /quotas/**\ *(optional string: hpc)*\ **/**\ *(optional string: project_name)*\ **/**


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Get all quotas for all project and all HPC systems*

        **Example Request**

        .. code::

            GET /quotas/                HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json

            [
                {
                    u'id':              2,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       19887678,
                    u'user':            u'306328'
                },
                {
                    u'id':              1,
                    u'project':         2,
                    u'project_hpc':     u'PIZDAINT',
                    u'project_name':    u'bsp_pizdaint_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17994600,
                    u'user':            u'306328'
                }
            ]   



    * *Get all quotas for all project for a specific HPC systems*

        **Example Request**

        .. code::

            GET /quotas/nsg/            HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json

            [
                {
                    u'id':              2,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       19887678,
                    u'user':            u'306328'
                },
            ]


    * *Get quota for the specific HPC system's project*

        **Example Request**

        .. code::

            GET /quotas/nsg/bsp_nsg_01/ HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json

            {
                u'id':                  2,
                u'project':             1,
                u'project_hpc':         u'NSG',
                u'project_name':        u'bsp_nsg_01',
                u'space_left':          10000000.0,
                u'time_left':           19887678,
                u'user':                u'306328'
            }
