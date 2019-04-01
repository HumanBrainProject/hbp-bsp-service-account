Introduction
============

The Service Account allows to submit job, delete jobs, fetch results and, 
if queried by admin, manage user groups, ban/unban users, etc.

The endpoint of the service, to be used for any request, is:

**https://bspsa.cineca.it/**

Any request to the rest API service must contain the oidc access token granted 
to the users once they have entered the |HBP_Collab_link|.

.. |HBP_Collab_link| raw:: html

    <a href="https://collab.humanbrainproject.eu/#/collab/19/nav/6342" target="_blank">HBP Collaboratory</a>


The request to the service account is fullfilled after the validity of the 
token is verified. Job ids, user ids and  requested resources are 
stored in the service backend database.

In order to get started with the development of web applications in the HBP 
Collaboratory and know more on authentication on the platform, 
please refer to |HBP_Collab_dev_link|.

.. |HBP_Collab_dev_link| raw:: html

    <a href="https://collab.humanbrainproject.eu/#/collab/54/nav/368" target="_blank">How to develop apps</a>

Furthermore, and most importantly, the users are not required to own any 
resources on any HPC systems.

If you do not have access to the HBP Collaboratory and want to request an 
account, please send an email to: **bsp-support [AT] humanbrainproject.eu**

.. toctree::
   :maxdepth: 2

   hpc
   token
