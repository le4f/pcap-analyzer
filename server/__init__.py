#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: le4f.net

from flask import Flask, request, redirect, url_for, send_file, render_template, g
from werkzeug.utils import secure_filename
from cStringIO import StringIO
from collections import Counter
from scapy.all import *
import os,sys,time,math,re
import simplejson,sqlite3
import pyshark
import chartkick

UPLOAD_FOLDER = 'server/pcapfile/'
ALLOWED_EXTENSIONS = set(['pcap','pcapng','cap'])
DATABASE = 'server/db/db.sqlite'

app = Flask(__name__)
app.jinja_env.add_extension("chartkick.ext.charts")

import views
import func