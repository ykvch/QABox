#!/usr/bin/env
# -*- coding: utf-8 -*-

import nose
from registry_plugin import RegistryClient

if __name__ == '__main__':
        nose.main(addplugins=[RegistryClient()])
