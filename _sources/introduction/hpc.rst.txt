HPC Systems And Projects
========================

The service currently allows submission to the following HPC platforms:

* |CSCS-PIZDAINT|: Swiss National Supercomputing Center-PIZDAINT

* |NSG|: NeuroScience Gateway


.. |CSCS-PIZDAINT| raw:: html

    <a href="https://www.cscs.ch/computers/piz-daint/" target="_blank">CSCS-PIZDAINT</a>

.. |NSG| raw:: html

    <a href="https://www.nsgportal.org/" target="_blank">NSG</a>
    
Currently, all the resources are allocated on the following projects:

* **bsp_pizdaint_01** on CSCS-PIZDAINT

* **bsp_nsg_01** on NSG.


When the users query the service for the first time, via any rest API call, 
they are first identified via the provided access token. 
Successively, they are granted the default quotas on the chosen project. 
Quotas are updated any time a job is launched, finalized, canceled or deleted.
