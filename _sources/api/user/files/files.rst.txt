Files
=====


Files operations on the HPC systems are performed through the **/files** endpoint.

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


The APIs allow to get a list of files related to a specific job and to download
them individually. 


**URL: /files/**\ *(string: hpc)*\ **/**\ *(string: project_name)*\ **/**\ *(string: job_id)*\ **/**\ *(optional string: file_id)*\ **/**

**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Get the file list of a completed job on NSG system*

        **Example Request**

        .. code::

            GET	/files/nsg/bsp_nsg_01/NGBW-JOB-NEURON75_TG-018095E597064F9FBEC486ED29BD2138/	HTTP/1.1
            Authorization:              Bearer Token       


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json

            [
	        {
		    u'fileid':          u'29057', 
		    u'filename':        u'STDOUT', 
		    u'length':          u'244144'
	        },
 		{
		    u'fileid':          u'29059',
		    u'filename':        u'STDERR',
		    u'length':          u'372'
		}
	    ]   


    * *Download a file of a completed job on NSG system*

        **Example Request**

        .. code::

            GET	/files/nsg/bsp_nsg_01/NGBW-JOB-NEURON75_TG-018095E597064F9FBEC486ED29BD2138/29057/	HTTP/1.1
            Authorization:              Bearer Token

        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/unknown




    * *Get the file list of a completed job on CSCS-Pizdaint system*

        **Example Request**

        .. code::

            GET /files/pizdaint/bsp_pizdaint_01/DBC6A573-9D99-4376-983C-9A3536CDD753/    HTTP/1.1
            Authorization:              Bearer Token       


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json
        
            [
                u'/UNICORE_Job_1552071365450',
                u'/stderr',
                u'/UNICORE_SCRIPT_EXIT_CODE',
                u'/stdout',
                u'/bss_submit_1552071365450'
            ]


    * *Download a file of a completed job on CSCS-Pizdaint system*

        **Example Request**

        .. code::

            GET /files/pizdaint/bsp_pizdaint_01/DBC6A573-9D99-4376-983C-9A3536CDD753/stdout/      HTTP/1.1
            Authorization:              Bearer Token

        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               text/plain

