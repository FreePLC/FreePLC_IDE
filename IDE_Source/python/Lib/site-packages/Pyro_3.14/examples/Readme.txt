This directory contains some assorted unstructured test programs.
Just examine the source to get enlightened.

Read on for usage tips.

AllInOne          - shows a single application with NS, ES, servers, clients
agent2            - a true mobile agent application (code downloading)
agent3            - another mobile agent example where the agent travels to other servers
attributes        - uses the attribute access feature
authenticate      - shows how connection authentication works
autoreconnect     - shows the auto reconnect/rebind feature 
BankExample       - a simple electronic banking example
Bank2             - a more advanced bank example
benchmark         - Pyro benchmark
callback          - shows callbacks from server to client, and oneway call		
chatbox-ES        - a chat server and client using the Event Server
chatbox-non-ES    - a chat server and client not using the Event Server
circle            - shows circular and conversation communication.
countingcars      - a more advanced Event Service example
denyhosts         - shows how to use a custom newConnectionValidator, to block or grant connection access to certain hosts.
disconnect        - shows the different ways in which you can disconnect objects from the daemon
distributed-computing  - a computational task (md5 cracking or merge sorting) is distributed among concurrently operating processors (push-style). Uses ES for progress monitoring
distributed-computing2 - a computational task (prime factorization) is distributed among concurrently operating processors (pull-style).
exceptions        - remote exceptions test
factory           - uses the object creation feature
filetransfer      - example of a simple ftp-like file transfer mechanism using Pyro.
hugetransfer      - test transfer of huge data structures
inheritance       - inheritance of remote objects
logging           - test the logging facility
maxclients        - example to test limit on simultaneous connections
multithread       - shows need of multithreading server
mobilehierarchy   - shows that mobile code can process a hierarchy of needed modules	
naming            - shows naming functions
NS_sec_plugins    - shows the connection validator plugin feature of the NS
noNS              - how to use Pyro without a Name Server (not recommended)
oneway            - shows how oneway calls work in the background
pickle            - check pickleability of various Pyro objects.
proxysharing      - shows the sharing of proxies over different threads
quickstart        - shows the use of the Pyro.ext.remote module which makes using Pyro extremely easy, and a 'pyrorun' script which makes it even easier (no more server code needed!)
quickstart-noNS   - like "quickstart" but doesn't use the Name Server
sessions          - show use of TLS and user-session resource objects.
simple            - a simple generic test
ssl               - shows how to use the Secure Socket Layer (SSL) features
stockquotes       - shows the use of the Event Service for stock quotes
stresstest        - stress testing for Pyro, the NS, and the ES.
testmobile        - various tests of the mobile code features
timeout           - shows socket timeout handling
tlstest           - test program to check if TLS is being initialized properly (including COM)
threadmobile      - technical multithreading test of Pyro's mobile code import logic
user_passwd_auth  - shows how to do username + password type connection validation.


testserver.py is the base implementation for most of the test servers.
testclient.py is the base implementation for most of the test clients.

Examples that use very specific features have their own server or client
code, they don't use the testserver/testclient.


If your network doesn't support broadcast lookup of the Pyro NameServer,
please set the environment variable PYRO_NS_HOSTNAME to the name of
the host that the NS is running on.
