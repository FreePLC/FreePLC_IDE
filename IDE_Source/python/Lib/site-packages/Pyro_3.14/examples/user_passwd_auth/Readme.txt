Example of username + password connection Authentication.

This example uses a custom connection validator that
checks username + password before a client can connect.
Notice that you don't have to restrict yourself to a single
string that is passed as identification, it can be any 
python object (in this case, a login/password tuple, 
where the password is munged to avoid storing it in plaintext).

The connection validator is used both by client and server.

