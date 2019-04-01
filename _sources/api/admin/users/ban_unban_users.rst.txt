Ban/Unban Users
===============


Ban a user from a project mean that user is not able to submit jobs on that project anymore but its quotas and other informations about the user's activity on that project are still there. 


**URL: /admin/ban/**\ *(required string: user_id)*\ **/**\ *(required string: project_id)*\ **/**

Ban a user from a group.


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Ban a user from a project*

        **Example Request**

        .. code::

            GET /admin/ban/301330/1/    HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type                application/json

            {
                u'banned_from':         u'1,',
                u'country':             u'IT',
                u'email':               u'user@example.it',
                u'groups':              u'2,1,',
                u'id':                  u'301330',
                u'institution':         u'An Institution Name',
                u'is_admin':            False,
                u'username':            u'fakenick'
            }



**URL: /admin/unban/**\ *(required string: user_id)*\ **/**\ *(required string: project_id)*\ **/**

Unban user that has previously banned from that project. Restore the ability of the user to submit jobs again into that project.



**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Unban user from a project*

        **Example Request**

        .. code::

            GET /admin/unban/301330/1/  HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type                application/json

            {
                u'banned_from':         u'',
                u'country':             u'IT',
                u'email':               u'user@example.it',
                u'groups':              u'2,1,',
                u'id':                  u'301330',
                u'institution':         u'An Institution Name',
                u'is_admin':            False,
                u'username':            u'fakenick'
            }
