Pcap Analyzer Online
======

Pcap Analyzer
---

在线轻量Pcap流量文件分析工具

Web PCAP Storage and Analytic Tool

![img](img/pcap-analyzer-01.png)


Features
---

*	轻量,易读.但不适合大数据包分析.(可以基于此改进)
*	上传,存储,下载基本功能
*	数据包分析
	*	数据包列表
	*	数据包细节查询
	*	Filter过滤
	*	数据包分析(来源/目的:IP/端口)
	*	Web请求提取
	*	DNS请求提取
	*	Mail流量提取

Files
---

```
.
├── app.py(运行Server)
├── img(ScreenShot)
├── server
│   ├── __init__.py(Core)
│   ├── func.py(调用函数)
│   ├── views.py(视图)
│   ├── pcapfile(上传文件目录)
│   ├── db(数据库)
│   ├── static(静态文件)
│   └── templates(模板)
├── readme.md(项目说明)
├── requirements.txt(python库依赖)
├── run.sh(运行项目)
└── run.bat(Windows下运行项目)
```

Installation/Running
---

* `$ git clone https://github.com/le4f/pcap-analyzer.git`
* `$ cd pcap-analyzer`
* `$ pip install -r requirements.txt`
* `$ chmod +x run.sh`
* `$ ./run.sh`
* `View http://127.0.0.1:8080/ `

Screenshots
---

![img](img/pcap-analyzer-01.png)

![img](img/pcap-analyzer-02.png)

![img](img/pcap-analyzer-03.png)

![img](img/pcap-analyzer-04.png)

![img](img/pcap-analyzer-05.png)

![img](img/pcap-analyzer-06.png)

![img](img/pcap-analyzer-07.png)

![img](img/pcap-analyzer-08.png)


Build With
---

*	[Flask](http://flask.pocoo.org)
*	[Semanstic-UI](http://semantic-ui.com)
*	[JQuery](http://jquery.com/)
*	[PyShark](http://kiminewt.github.io/pyshark/)
*	[Chartkick](https://github.com/mher/chartkick.py)
*	[Highcharts](http://api.highcharts.com/highcharts)

More
---

For More Infomation.Visit My Blog:[le4f.net](http://le4f.net/post/post/pcap-online-analyzer)