This example shows the behavior of initTLS.
It should be called in the context of the new thread.
(so the thread id is checked to be the same).

It also checks if it is called for Oneway method calls.

If you run it on Windows, it will also use a tiny bit of COM
code to get usernames. This should work fine. If you fail to
initialize COM properly, you get errors such as "CoInitialize
has not been called"...
