List Users
==========


List Users API allow admin to fetch a list of all users.


**URL: /admin/users/**


**Required Headers:**

    * Authorization:

        .. code::
        
            Authorization: Bearer <token>


**Example:**

    * *Get all users*

        **Example Request**

        .. code::

            GET /admin/users/           HTTP/1.1
            Authorization:              Bearer FakeToken


        **Example Response**

        .. code::

            HTTP/1.1                    200 OK
            Content-Type                application/json

            [
                {
                    u'banned_from':     u'',
                    u'country':         u'IT',
                    u'email':           u'user1@example.com',
                    u'groups':          u'1,2,',
                    u'id':              u'306328',
                    u'institution':     u'An Institution Name',
                    u'is_admin':        True,
                    u'username':        u'fakenick1'
                },
                {
                    u'banned_from':     u'1,',
                    u'country':         u'EN',
                    u'email':           u'user2@example.en',
                    u'groups':          u'2,1,',
                    u'id':              u'301330',
                    u'institution':     u'An Institution Name',
                    u'is_admin':        False,
                    u'username':        u'fakenick2'
                },
                        .
                        .
                        .
                        .
                        .
                        .
                        .
                {
                    u'banned_from':     u'',
                    u'country':         u'CH',
                    u'email':           u'user17@example.ch',
                    u'groups':          u'2,',
                    u'id':              u'303506',
                    u'institution':     u'UNKNOWN',
                    u'is_admin':        False,
                    u'username':        u'fakenick116'
                }
            ]
