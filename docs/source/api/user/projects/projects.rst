Projects
========


Projects operations on the HPC systems are performed through the **/projects** endpoint.

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


The APIs allow to get a list of projects that they can be filtered by the HPC system in which they are hosted.



**URL: /projects/**\ *(optional string: hpc)*\ **/**


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Get all projects for all HPC systems*

        **Example Request**

        .. code::

            GET /projects/              HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json
        
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

    * *Get all projects for a specific HPC systems*

        **Example Request**

        .. code::

            GET /projects/nsg/          HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json
        
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
                      .
                      .
                      .
                      .
                      .
                {
                    u'hpc':             u'NSG',
                    u'id':              7,
                    u'init_space':      10000000.0,
                    u'init_time':       10000000,
                    u'name':            u'nsg_project',
                    u'space_left':      10000000.0,
                    u'time_left':       10000000,
                    u'user_space':      10000000.0,
                    u'user_time':       18000000
                }
            ]


    * *Get info about a specific HPC system's project*

        **Example Request**

        .. code::

            GET /projects/nsg/bsp_nsg_01/              HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json
        
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
