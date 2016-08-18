#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
After server.start() server will be running in background
This would be a test server to verify test runs
It serves randomly status 200, 300, 400 responses with sample json content
After server.stop() server will stop

Please write test class (derived from TestCase) containing
test methods to cover the following cases:

TEST-0
    Steps:
    1. Client sends GET request to server (any path)
    Expected:
    1. Server responds with status 200
    1. Response body should contain `e` character

TEST-1
    Steps:
    1. Client sends PUT request to server (any path)
    Expected:
    1. Server responds with status 200
    1. Response `Content-Length` header value should be greater than 50
'''

from unittest import TestCase
from http_server import server # please find server address in http_server.py

# Please add your class below
# The suite is expected to handle server.start() and server.stop()
# You are free to import and use any helper (eg HTTP-client) modules You prefer