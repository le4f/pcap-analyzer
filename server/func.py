#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: le4f.net

from server import *

#连接数据库
def connect_db():
    return sqlite3.connect(DATABASE)

#获取数据库连接
def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

#获取数据条目
def show_entries():
    db = get_connection()
    cur = db.execute('select * from pcap')
    entries = [dict(id=row[0], filename=row[1] ,filepcap=row[2], filesize=row[3]) for row in cur.fetchall()]
    return entries

#获取包信息
def get_pcap_entries(id):
    db = get_connection()
    cur = db.execute('select * from pcap where id ='+ str(int(id)) + ';')
    entries = [dict(id=row[0], filename=row[1] ,filepcap=row[2], filesize=row[3]) for row in cur.fetchall()]
    return entries

#执行sql命令
def sql_exec(sql):
    db = get_connection()
    db.execute(sql)
    print "[*]execute sql: " + sql
    db.commit()

#列出文件
def list_file(CapFiles):
    files = os.listdir(UPLOAD_FOLDER)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    dbfiles = [entry['filename'] for entry in show_entries()]
    for file in files:
        if file in dbfiles:
            pass
        else:
            filesize = convertBytes(os.path.getsize(UPLOAD_FOLDER+file))
            pcapnum = get_capture_count(UPLOAD_FOLDER+file)
            sql_exec('insert into pcap (file,pcapnum,size) values ("'+file+'",'+str(pcapnum)+',"'+filesize+'");')
    for dbfile in dbfiles:
        if dbfile not in files:
            sql_exec('delete from pcap where file = "'+dbfile+'";')
        else:
            pass

#获取数据包数目
def get_capture_count(filename):
    p = pyshark.FileCapture(filename, only_summaries=True, keep_packets=False)
    p.load_packets()
    return len(p)

#文件大小表示
def convertBytes(bytes, lst=['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']):
    i = int(math.floor(math.log(bytes, 1024)))
    if i >= len(lst):
        i = len(lst) - 1
    return ('%.2f' + " " + lst[i]) % (bytes/math.pow(1024, i))

#判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#获取包内容
def decode_capture_file(pcapfile, filter=None):
    if filter:
        cap = pyshark.FileCapture(os.path.join(UPLOAD_FOLDER, pcapfile), keep_packets=False, only_summaries=True, display_filter=filter)
    else:   
        cap = pyshark.FileCapture(os.path.join(UPLOAD_FOLDER, pcapfile), keep_packets=False, only_summaries=True)

    cap.load_packets(timeout=5)
    if len(cap) == 0:
        return 0, 'No packets found.'
    details = {
        'stats': {
            'breakdown': {},
            'length_buckets': {'0-200': 0, '201-450': 0, '451-800':0, '801-1200':0, '1201-1500': 0}
        },
        'packets': [],
        # 'linechart': []
    }
    avg_length = []
    #解包
    def decode_packet(packet):
        pkt_details = {
            'number' : packet.no,
            'length' : packet.length,
            'time' : packet.time
        }
        pkt_details['src_ip'] = packet.source
        pkt_details['dst_ip'] = packet.destination
        pkt_details['protocol'] = packet.protocol
        pkt_details['desc'] = packet.info
        # delta and stream aren't supported by earlier versions (1.99.1) of tshark
        try:
            pkt_details['delta'] = packet.delta
            pkt_details['stream'] = packet.stream
        except AttributeError:
            pass

        details['packets'].append(pkt_details)
        avg_length.append(int(packet.length))

        if 0 <= int(packet.length) <= 200:
            details['stats']['length_buckets']['0-200'] += 1
        elif 201 <= int(packet.length) <= 450:
            details['stats']['length_buckets']['201-450'] += 1
        elif 451 <= int(packet.length) <= 800:
            details['stats']['length_buckets']['451-800'] += 1
        elif 801 <= int(packet.length) <= 1200:
            details['stats']['length_buckets']['801-1200'] += 1
        elif 1201 <= int(packet.length):
            details['stats']['length_buckets']['1201-1500'] += 1

        try:
            details['stats']['breakdown'][packet.protocol] += 1
        except KeyError:
            details['stats']['breakdown'][packet.protocol] = 1

    try:
        cap.apply_on_packets(decode_packet, timeout=10)
    except:
        return 0, 'Capture File Too Large!'

    details['stats']['avg_length'] = sum(avg_length) / len(avg_length)
    return details

#获取包细节
def get_packet_detail(pcapfile, num):
    cap = pyshark.FileCapture(os.path.join(UPLOAD_FOLDER, pcapfile))

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    cap[int(num)-1].pretty_print()
    sys.stdout = old_stdout
    detail = '''
<script type="text/javascript">
$(document).ready(function(){
    $('.ui.accordion').accordion();
});
</script>
<i class="close icon"></i>
<div class="header">
    Packet Details
</div>
<div class="content">'''
    for line in mystdout.getvalue().split('\n'):
        if line == 'self._packet_string':
            continue
        elif 'Layer ETH' in line:
            detail += '''
    <div class="ui black segment" style="height:29rem;overflow:auto">
        <div class="ui styled fluid accordion">
            <div class="active title">
                <i class="dropdown icon"></i>
                <a class="packetHeader" data-target="#%(link)s">%(name)s</a>
            </div>
            <div id="%(link)s" class="active content">
                <div class="ui black segment">
            ''' % {'name': line[:-1], 'link': line.replace(' ', '-').strip(':')}
        elif 'Layer' in line:
            detail += '''
                </div>
            </div>
        </div>
        <div class="ui styled fluid accordion">
            <div class="title">
                <i class="dropdown icon"></i>
                <a class="packetHeader" data-target="#%(link)s">%(name)s</a>
            </div>
            <div id="%(link)s" class="content">
                <div class="ui black segment">
            ''' % {'name': line[:-1], 'link': line.replace(' ', '-').strip(':')}
        else:   
            keyword = line.split(': ')[0] + ': '

            try:
                value = line.split(': ')[1]
            except IndexError:
                keyword = ''
                value = line
            
            try:
                keyword = keyword.split('= ')[1]
            except IndexError:
                pass

            detail += '<p><strong>%s</strong>%s</p>\n' % (keyword, value)
    detail += '''
                </div>
            </div>
        </div>
    </div>
'''
    return detail

#获取包信息
def get_statistics(file):
    tcp = 0
    udp = 0
    arp = 0
    icmp = 0
    other = 0
    pcapstat = {}
    pcap = rdpcap(UPLOAD_FOLDER+file)
    for packet in pcap:
        if TCP in packet:
            tcp = tcp + 1
        elif UDP in packet:
            udp = udp + 1
        elif ARP in packet:
            arp = arp + 1
        elif ICMP in packet:
            icmp = icmp + 1
        else:
            other = other + 1
    pcapstat['tcp'] = str(tcp)
    pcapstat['udp'] = str(udp)
    pcapstat['arp'] = str(arp)
    pcapstat['icmp'] = str(icmp)
    pcapstat['other'] = str(icmp)
    pcapstat['total'] = str(tcp + udp + arp + icmp + other)
    return pcapstat

#获取包来源地址
def get_ip_src(file):
    ipsrc = []
    pcap = rdpcap(UPLOAD_FOLDER+file)
    for packet in pcap:
        if TCP in packet:
            # if packet.getlayer('TCP').flags == 2:
                ipsrc.append(packet.getlayer('IP').src)
    ipsrclist = Counter(ipsrc).most_common()
    return ipsrclist

#获取包去向地址
def get_ip_dst(file):
    ipdst = []
    pcap = rdpcap(UPLOAD_FOLDER+file)
    for packet in pcap:
        if TCP in packet:
            # if packet.getlayer('TCP').flags == 2:
                ipdst.append(packet.getlayer('IP').dst)
    ipdstlist = Counter(ipdst).most_common()
    return ipdstlist

#获取包去向端口
def get_port_dst(file):
    dstport = []
    pcap = rdpcap(UPLOAD_FOLDER+file)
    for packet in pcap:
        if TCP in packet:
            dstport.append(packet.getlayer('TCP').dport)
    dstportlist = Counter(dstport).most_common()
    return dstportlist

#获取DNS请求
def get_dns(file):
    dns = []
    pcap = rdpcap(UPLOAD_FOLDER+file)
    for packet in pcap:
        if DNS in packet:
                res = packet.getlayer('DNS').qd.qname
                if res[len(res) - 1] == '.':
                    res = res[:-1]
                dns.append(res)
    dns = Counter(dns).most_common()
    dnstable ='''
<table class="ui table">
    <thead>
        <tr>
        <th class="twelve wide">DNS Request</th>
        <th class="four wide">Request Num</th>
        </tr>
    </thead>
    <tbody>
''' 
    for dnsreq in dns:
        dnstable += '''
        <tr>
            <td>
            %(dns)s
            </td>
            <td>
            %(num)s
            </td>
        </tr>
''' % { 'dns':dnsreq[0],'num':str(dnsreq[1])} 
    dnstable += '''
    </tbody>
  </table>
'''
    return dns,dnstable

#邮件数据包提取
def get_mail(file):
    mailpkts = []
    result = "<p>"
    pcap = rdpcap(UPLOAD_FOLDER+file)
    for packet in pcap:
        if TCP in packet:
            if packet.getlayer('TCP').dport == 110 or packet.getlayer('TCP').sport == 110 or packet.getlayer('TCP').dport == 143 or packet.getlayer('TCP').sport == 143 :
                mailpkts.append(packet)
    for packet in mailpkts:
        if packet.getlayer('TCP').flags == 24:
            result = result + packet.getlayer('Raw').load.replace(' ','&nbsp;').replace('\n','<br/>')
    if result == "<p>":
        result = result + "No Mail Packets!"
    result = result + "</p>"
    result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\\x80-\\xff]').sub('', result)
    return result

#Web数据包提取
def get_web(file):
    webpkts = []
    result = ""
    pcap = rdpcap(UPLOAD_FOLDER+file)
    for packet in pcap:
        if TCP in packet:
            if packet.getlayer('TCP').dport == 80 or packet.getlayer('TCP').dport == 8080:
                webpkts.append(packet)
    for packet in webpkts:
        if packet.getlayer('TCP').flags == 24:
            result = result + '''<div class="ui vertical segment"><p>'''
            result = result + packet.getlayer('Raw').load.replace(' ','&nbsp;').replace('\n','<br/>')
            result = result + '''</p></div>'''
    if result == "":
        result = '''<div class="ui vertical segment"><p>No WebView Packets!</p></div>'''
    result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\\x80-\\xff]').sub('', result)
    return result