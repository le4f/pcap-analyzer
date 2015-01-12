#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: le4f.net
from server import app

if __name__ == '__main__':
	app.run(host='localhost', port=8080, debug=True)