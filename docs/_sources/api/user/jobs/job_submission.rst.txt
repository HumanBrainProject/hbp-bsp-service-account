Job Submission
==============

The Job Submission APIs allow to submit a job to an HPC system.

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

To submit a Job through the Service Account you must specify the HPC and 
optionally the project name. If no project is specified, the default project 
is selected.


**URL: /jobs/**\ *(string: hpc)*\ **/**\ *(optional string: project_name)*\ **/**

**Required Headers:**
    
    * Authorization:
    
        .. code::
                
                Authorization: Bearer <token>

    
    * Content-Disposition
        
        .. code::
                
                Content-Disposition: attachment; filename=<file.zip> 

    * Payload: 
      
        .. code::

                Payload {   
                    "command":          "<some slurm command>",         only for Pizdaint
                    "tool":             "<some tool>",                  only for NSG
                    "node_number":      "<int>",
                    "core_number":      "<int>",
                    "runtime":          "<float>",
                    "title":            "<string>"
                }  
    
 
**Examples:**

    * *Submit job into HPC's default project*

        **Example Request**
            
        .. code::
        
            POST /jobs/pizdaint/        HTTP/1.1
            Authorization:              Bearer Token
            Content-Disposition:        attachment; filename=job_file.zip
            Payload: {
                "command":              "ls -lisa",
                "node_number":          "2",
                "core_number":          "6",
                "runtime":              "2.0",
                "title":                "a job title"
            }


        **Example Response**
                
        .. code::

            HTTP/1.1                    201 Created
            Content-Type:               application/json
            {
                "end_date":             None,
                "failed":               False,
                "id":                   80,
                "init_date":            "2019-02-10T22:40:01Z",
                "job_id":               "AF17D39A-9E15-4FE3-9F84-0EAEB4CC94AA",
                "owner":                "306328",
                "project":              2,
                "project_hpc":          "PIZDAINT",
                "project_name":         "bsp_pizdaint_01",
                "runtime":              2.0,
                "stage":                "QUEUED",
                "terminal_stage":       False
                "title":                "a job title"
            }


    * *Submit a job into a specific HPC's project*

        **Example Request**

        .. code::

            POST /jobs/nsg/bsp_nsg_01/	HTTP/1.1
            Authorization:              Bearer Token
            Content-Dispostion:         attachment; filename=nsg_job.zip
            Payload: {
                "tool":                 "NEURON74_TG",
                "node_number":          "2",
                "core_number":          "6",
                "runtime":              "2.0",
                "title":                "a job title"
            }


        **Example Response**

        .. code::

            HTTP/1.1                    201 Created
            Content-Type:               application/json

            {
                "end_date":             None,
                "failed":               False,
                "id":                   81,
                "init_date":            "2019-02-10T22:46:19Z",
                "job_id":               "NGBW-JOB-NEURON75_TG-85CB59F5CD5A4FBCBCBA5DABCC420280",
                "owner":                "306328",
                "project":              1,
                "project_hpc":          "NSG",
                "project_name":         "bsp_nsg_01",
                "runtime":              0.5,
                "stage":                "QUEUE",
                "terminal_stage":       False,
                "title":                "a job title"
            }
