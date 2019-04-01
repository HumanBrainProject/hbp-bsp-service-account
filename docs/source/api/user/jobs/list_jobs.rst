List Jobs
=========

The List Jobs APIs allow to fetch information for submitted jobs.

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


All queries related to jobs are performed through the **/jobs** endpoint.

There are some optional parameters which filter the requests through the HPC 
system used, the project related to the job and the job ids.

If a single job is fetched but the id is not valid a *404 NOT FOUND* is
returned.

**URL: /jobs/**\ *(optional string: hpc)*\ **/**\ *(optional string: project_name)*\ **/**\ *(optional string: job_id)*\ **/**

**Required Headers:**
	
    * Authorization:

        .. code::
        
            Authorization: Bearer <token>


**Examples:**

    * *Get a list of all jobs submitted on any hpc for any project*
        		
        **Example Request**

        .. code::

            GET	/jobs/	                HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

             HTTP/1.1                   200 OK
             Content-Type:              application/json

             [
                 {
	             u'end_date':       u'2019-01-27T15:34:52Z',
  	             u'failed':         False,
  		     u'id':             1,
	             u'init_date':      u'2019-01-27T15:33:15Z',
	             u'job_id':         u'9EF0C1F9-E7CB-4E80-A1A4-823BC59E807B',
		     u'owner':          u'306328',
  		     u'project':        2,
  		     u'project_hpc':    u'PIZDAINT',
  		     u'project_name':   u'bsp_pizdaint_01',
		     u'runtime':        2.0,
  		     u'stage':          u'SUCCESSFUL',
  		     u'terminal_stage': True,
                     u'title':          u'a job title'
		 },
 		 {
	             u'end_date':       u'2019-01-27T17:17:42Z',
  		     u'failed':         False,
  		     u'id':             2,
  		     u'init_date':      u'2019-01-27T17:15:46Z',
  		     u'job_id':         u'18A99969-54FC-40D7-8348-55060DAEDBC0',
  		     u'owner':          u'306328',
  		     u'project':        2,
  		     u'project_hpc':    u'PIZDAINT',
  		     u'project_name':   u'bsp_pizdaint_01',
  		     u'runtime':        2.0,
  		     u'stage':          u'SUCCESSFUL',
  		     u'terminal_stage': True,
                     u'title':          u'a job title'
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
	             u'end_date':       u'2019-02-10T23:21:51Z',
  		     u'failed':         False,
  		     u'id':             81,
  		     u'init_date':      u'2019-02-10T22:46:19Z',
  		     u'job_id':         u'NGBW-JOB-NEURON75_TG-85CB59F5CD5A4FBCBCBA5DABCC420280',
  		     u'owner':          u'306328',
  		     u'project':        1,
  		     u'project_hpc':    u'NSG',
  		     u'project_name':   u'bsp_nsg_01',
  		     u'runtime':        0.5,
  		     u'stage':          u'COMPLETED',
  		     u'terminal_stage': True,
                     u'title':          u'a job title'
		 }
	    ]    


    * *Get a list of all jobs submitted on a single HPC*

        **Example Request**

        .. code::

            GET	/jobs/nsg/	        HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json

            [
	        {
		    u'end_date':        u'2019-02-04T11:21:59Z',
  		    u'failed':          False,
  		    u'id':              9,
  		    u'init_date':       u'2019-02-04T10:47:44Z',
  		    u'job_id':          u'NGBW-JOB-NEURON75_TG-018095E597064F9FBEC486ED29BD2138',
  		    u'owner':           u'306328',
  		    u'project':         1,
  		    u'project_hpc':     u'NSG',
  		    u'project_name':    u'bsp_nsg_01',
  		    u'runtime':         0.5,
  		    u'stage':           u'COMPLETED',
  		    u'terminal_stage':  True,
                    u'title':           u'a job title'
		},
		{
		    u'end_date':        u'2019-02-04T11:31:18Z',
  		    u'failed':          False,
  		    u'id':              10,
  		    u'init_date':       u'2019-02-04T10:56:49Z',
  		    u'job_id':          u'NGBW-JOB-NEURON75_TG-2F471C35BFE64BDAAFF876EE88785BE6',
  		    u'owner':           u'306328',
  		    u'project':         1,
  		    u'project_hpc':     u'NSG',
  		    u'project_name':    u'bsp_nsg_01',
  		    u'runtime':         0.5,
  		    u'stage':           u'COMPLETED',
  		    u'terminal_stage':  True,
                    u'title':           u'a job title'
		},
		{
		    u'end_date':        u'2019-02-04T11:31:18Z',
  		    u'failed':          False,
  		    u'id':              11,
  		    u'init_date':       u'2019-02-04T10:57:27Z',
  		    u'job_id':          u'NGBW-JOB-NEURON75_TG-42EB47EE2B40482289F3DCD70A80E6AA',
  		    u'owner':           u'306328',
  		    u'project':         1,
  		    u'project_hpc':     u'NSG',
  		    u'project_name':    u'bsp_nsg_01',
  		    u'runtime':         0.5,
  		    u'stage':           u'COMPLETED',
  		    u'terminal_stage':  True,
                    u'title':           u'a job title'
		}
	   ]



    * *Get a list of all jobs submitted on a single HPC and a single project*

        **Example Request**
        
        .. code:: 

            GET	/jobs/pizdaint/bsp_pizdaint_01/	HTTP/1.1
            Authorization:              Bearer FakeToken    
        

        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type:               application/json
	
	    [
                {
	    	    u'end_date':        u'2019-01-27T15:34:52Z',
  		    u'failed':          False,
  		    u'id':              1,
		    u'init_date':       u'2019-01-27T15:33:15Z',
		    u'job_id':          u'9EF0C1F9-E7CB-4E80-A1A4-823BC59E807B',
		    u'owner':           u'306328',
  		    u'project':         2,
  		    u'project_hpc':     u'PIZDAINT',
  		    u'project_name':    u'bsp_pizdaint_01',
		    u'runtime':         2.0,
  		    u'stage':           u'SUCCESSFUL',
  		    u'terminal_stage':  True,
                    u'title':           u'a job title'
		},
 		{
		    u'end_date':        u'2019-01-27T17:17:42Z',
  		    u'failed':          False,
  		    u'id':              2,
  		    u'init_date':       u'2019-01-27T17:15:46Z',
  		    u'job_id':          u'18A99969-54FC-40D7-8348-55060DAEDBC0',
  		    u'owner':           u'306328',
  		    u'project':         2,
  		    u'project_hpc':     u'PIZDAINT',
     		    u'project_name':    u'bsp_pizdaint_01',
  		    u'runtime':         2.0,
  		    u'stage':           u'SUCCESSFUL',
  		    u'terminal_stage':  True,
                    u'title':           u'a job title'
		}
	    ]  


    * *Get info on a single job*

        **Example Request**

        .. code::
        
            GET	/jobs/nsg/bsp_nsg_01/NGBW-JOB-NEURON75_TG-85CB59F5CD5A4FBCBCBA5DABCC420280/	HTTP/1.1
            Authorization:              Bearer FakeToken ù

        
        **Example Response**

        .. code::

            HTTP/1.1 200 OK
            Content-Type: application/json
	   
	    {
	        u'end_date':            u'2019-02-10T23:21:51Z',
     		u'failed':              False,
 		u'id':                  81,
 		u'init_date':           u'2019-02-10T22:46:19Z',
 		u'job_id':              u'NGBW-JOB-NEURON75_TG-85CB59F5CD5A4FBCBCBA5DABCC420280',
 		u'owner':               u'306328',
 		u'project':             1,
 		u'project_hpc':         u'NSG',
 		u'project_name':        u'bsp_nsg_01',
 		u'runtime':             0.5,
 		u'stage':               u'COMPLETED',
 		u'terminal_stage':      True,
                u'title':               u'a job title'
            }
