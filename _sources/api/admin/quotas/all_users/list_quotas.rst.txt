List Quotas For All Users
=========================


**URL: /admin/quotas/**\ *(optional string: hpc)*\ **/**\ *(optional string: project_name)*\ **/**


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Get all users quotas for every HPC systems and projects*

        **Example Request**

        .. code::

            GET /admin/quotas/          HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type                application/json

            [
                {
                    u'id':              5,
                    u'project':         2,
                    u'project_hpc':     u'PIZDAINT',
                    u'project_name':    u'bsp_pizdaint_01',
                    u'space_left':      10000000.0,
                    u'time_left':       18000000,
                    u'user':            u'263955'
                },
                {
                    u'id':              3,
                    u'project':         2,
                    u'project_hpc':     u'PIZDAINT',
                    u'project_name':    u'bsp_pizdaint_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17987553,
                    u'user':            u'301330'
                },
                {
                    u'id':              4,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17982000,
                    u'user':            u'301330'
                },
                        .
                        .
                        .
                        .
                        .
                        .
                {
                    u'id':              6,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17996400,
                    u'user':            u'263955'
                }
            ]



    * *Get all users quotas for every projects on a single HPC system*

        **Example Request**

        .. code::

            GET /admin/quotas/nsg/      HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type                application/json

            [
                {
                    u'id':              4,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17982000,
                    u'user':            u'301330'
                },
                {
                    u'id':              6,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17996400,
                    u'user':            u'263955'
                },
                        .
                        .
                        .
                        .
                        .
                        .
                {
                    u'id':              8,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17998200,
                    u'user':            u'305532'
                }
            ]


    * *Get all users quotas for a single project on a single HPC system*

        **Example Request**

        .. code::

            GET /admin/quotas/nsg/bsp_nsg_01/      HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type                application/json

            [
                {
                    u'id':              4,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17982000,
                    u'user':            u'301330'
                },
                {
                    u'id':              6,
                    u'project':         1,
                    u'project_hpc':     u'NSG',
                    u'project_name':    u'bsp_nsg_01',
                    u'space_left':      10000000.0,
                    u'time_left':       17996400,
                    u'user':            u'263955'
                }
            ]

