Some examples to show the use of the Thread Local Storage, its caller attribute,
and the use of user-session specific resource objects.

There is a basic example to show TLS usage: basic_server, basic_client/basic_client2.

There is an example to show use of user-session resource objects (in this example only
simple data files where a user can append lines to): storage_server_caller/storage_server_tls,
storage_client.

There is also an example to show how you might make use of the connection authentication
mechanism to obtain session user data (username): auth_server, auth_client.

