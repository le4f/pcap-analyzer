#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: le4f.net
from server import app
#如应用于生产环境 app.run(host='0.0.0.0', port=80) 并注意可能存在的安全隐患.
#有些情况下 localhost 会出问题，本地需要添加一个 hosts 。
if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)