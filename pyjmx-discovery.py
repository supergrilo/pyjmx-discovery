# -*- coding: utf-8 -*-
import javax.management.remote.JMXConnector;                                                                                                                            
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import javax.management.ObjectName as ObjectName;
import java.lang.management.ManagementFactory;

import re
import types
import sys
import json
from ConfigParser import ConfigParser

if len(sys.argv) < 2:
    print "Faltou o arquivo de configuração no parâmetro"
    sys.exit(1)

config = ConfigParser()
config.read(sys.argv[1])

host = config._sections["main"]["host"]
port = config._sections["main"]["port"]
query = config._sections["main"]["search_query"]

serviceURL = str()
serviceURL = "service:jmx:rmi:///jndi/rmi://"
serviceURL = serviceURL + host + ":" + str(port) + "/jmxrmi"
url =  javax.management.remote.JMXServiceURL(serviceURL);
connector = javax.management.remote.JMXConnectorFactory.connect(url);
remote = connector.getMBeanServerConnection();

serverMbName = ObjectName(query)
beans = remote.queryMBeans(serverMbName, None)

queue_results = []

for i in beans:
    line = str(i.getObjectName())
    print line
    regex = r'(?P<org>[.\w]+):type=(?P<type>\w+),brokerName="(?P<brokername>[\w\d_-]+)",module=(?P<module>\w+),serviceType=(?P<servicetype>\w+),name="(?P<name>[\w\d._-]+)"'
    
    r = re.compile(regex).search(line)
    if not isinstance(r, types.NoneType):
        key = r.group('name') if r.group('name') in config._sections else "DEFAULTS"
        cons_threshold = config._sections[key]["consumers_threshold"]
        queue_max_messages = config._sections[key]["queue_max_messages"]
        queue_min_messages = config._sections[key]["queue_min_messages"]
        proc_url = config._sections[key]["proc_url"]
        queue = { "{#QUEUE_NAME}": r.group('name'), "{#CONS_THRESHOLD}": cons_threshold, "{#QUEUE_MAX}": queue_max_messages, "{#QUEUE_MIN}": queue_min_messages, "{#PROC_URL}": proc_url, "{#ARTEMIS_BROKER}": r.group('brokername') }
        queue_results.append(queue)

#print "{ \"data\": %s }" % json.dumps({"data":queue_results})
print json.dumps({"data":queue_results})
