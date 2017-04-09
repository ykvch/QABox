QABox
======

[prettyrpc.py] (prettyrpc.py) -- a better RPC :) A pair of classes that allow positional parameters in XMLRPC method calls. They also allow passing python objects as parameters to XMLRPC calls. They also help to avoid unintentional parameters modifications by XMLRPC (like removing newlines etc.).

[bitbox.py] (bitbox.py) -- just playing with bit operations.

[multitest.py] (multitest.py)  -- metaclass/base class to generate multiple tests with the similar steps but different parameters in each test. Uses parameterized methods as input. Produces multiple unittest-compatible methods inside the same class as output (please see the file docstring for more information).

[registry_plugin.py] (registry_plugin.py) / [registry_server.py] (registry_server.py) -- A simple nose plugin for distributed parallel tests run (same or multiple hosts, doesn't matter). Server part makes sure that only unique files are chosen for the run at each "nosetests" process.
