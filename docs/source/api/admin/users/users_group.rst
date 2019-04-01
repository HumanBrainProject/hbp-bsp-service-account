Users Group
===========

Groups are a user's property.

The groups are, substantially, a permissions where the user can submit a job. They are represent with the project's id in which user has able to submit.  



**URL: /admin/groups/add/**\ *(required string: user_id)*\ **/**\ *(required string: project_id)*\ **/**

Add user to a group. Allow user to submit on that project.


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Add a user to a group*

        **Example Request**

        .. code::

            GET /admin/groups/add/301330/1/                  HTTP/1.1
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



**URL: /admin/groups/remove/**\ *(required string: user_id)*\ **/**\ *(required string: project_id)*\ **/**

Remove user from a group. User won't be able to submit on that project. If user is not present on that project, the request raise an error.


**Required Headers:**

    * Authorization:

        .. code::

            Authorization: Bearer <token>


**Example:**

    * *Remove a user to a group*

        **Example Request**

        .. code::

            GET /admin/groups/remove/301330/1/                  HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type                application/json

            {
                u'banned_from':         u'',
                u'country':             u'IT',
                u'email':               u'user@example.it',
                u'groups':              u'2,',
                u'id':                  u'301330',
                u'institution':         u'An Institution Name',
                u'is_admin':            False,
                u'username':            u'fakenick'
            }
