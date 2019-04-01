List Projects
=============

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

**URL: /admin/projects/**\ *(optional string: hcp)*\ **/**\ *(optional string: project_name)*\ **/**


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Get info on all projects for all HPC systems*

        **Example Request**

        .. code::

            GET /admin/projects/        HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::
       
            HTTP/1.1                    200 OK
            Content-Disposition:        application/json

            [
                {
                    u'hpc':             u'NSG',
                    u'id':              1,
                    u'init_space':      10000000.0,
                    u'init_time':       10000000,
                    u'name':            u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       10000000,
                    u'user_space':      10000000.0,
                    u'user_time':       18000000
                },
                {
                    u'hpc':             u'PIZDAINT',
                    u'id':              2,
                    u'init_space':      10000000.0,
                    u'init_time':       10000000,
                    u'name':            u'bsp_pizdaint_01',
                    u'space_left':      10000000.0,
                    u'time_left':       10000000,
                    u'user_space':      10000000.0,
                    u'user_time':       18000000
                }
            ] 


    * *Get info on all projects for a single HPC system*

        **Example Request**

        .. code::

            GET /admin/projects/nsg/    HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::
       
            HTTP/1.1                    200 OK
            Content-Disposition:        application/json

            [
                {
                    u'hpc':             u'NSG',
                    u'id':              1,
                    u'init_space':      10000000.0,
                    u'init_time':       10000000,
                    u'name':            u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       10000000,
                    u'user_space':      10000000.0,
                    u'user_time':       18000000
                },
            ]


    * *Get info on a single projects for a single HPC system*

        **Example Request**

        .. code::

            GET /admin/projects/nsg/bsp_nsg_01/    HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Disposition:        application/json

            {
                u'hpc':                 u'NSG',
                u'id':                  1,
                u'init_space':          10000000.0,
                u'init_time':           10000000,
                u'name':                u'bsp_nsg_01',
                u'space_left':          10000000.0,
                u'time_left':           10000000,
                u'user_space':          10000000.0,
                u'user_time':           18000000
            }
