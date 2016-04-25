# pyjmx-discovery

Based on https://github.com/RiotGamesMinions/zabbix_jmxdiscovery/.

I write this project for two reasons:
 1. I Don't know java to contribute with RiotGamesMinions project.
 2. I needed more customs macros to use in prototypes for LLD 

Works with [ActivemQ Artemis](https://activemq.apache.org/artemis/) > 1.2.0.
For [HornetQ](http://hornetq.jboss.org/) see hornetq branch

Requirements
------------
#### jython
- Tested on jython version 2.7
- Minimal installation: core and mod 

Usage
------------
- Set ```{$JMX_DISCOVERY_CONFIG}``` macro with the ```config.ini``` path file, on each host of the cluster(or on hostgroup).

    Example:
```
{$JMX_DISCOVERY_CONFIG} = /etc/zabbix/pyjmx-discovery.ini
```
- Import the template file on zabbix server.
- Move the ```artemis.conf``` to ```/etc/zabbix/zabbix_agent.d/``` and restart the zabbix-agent service.
- Link the "Template ActiveMQ Artemis" on each host of the Artemis cluster.

List of LLD discovery macros:
------------
<table>
  <tr>
    <th>Macro</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><tt>{#QUEUE_NAME}</tt></td>
    <td>The name of the queue. (case sensitive)</td>
  </tr>
  <tr>
    <td><tt>{#CONS_THRESHOLD}</tt></td>
    <td>Threshold for the minimum consumer connected.</td>
  </tr>
  <tr>
    <td><tt>{#QUEUE_MAX}</tt></td>
    <td>Threshold for the maximum message queued.</td>
  </tr>
  <tr>
    <td><tt>{#QUEUE_MIN}</tt></td>
    <td>Threshold for the minimum message queued.</td>
  </tr>
  <tr>
    <td><tt>{#ARTEMIS_BROKER}</tt></td>
    <td>The name of artemis broker.</td>
  </tr>
  <tr>
    <td><tt>{#PROC_URL}</tt></td>
    <td>For the urls on triggers. (This field started to support discovery macros on zabbix 3.0)<br>disable by default on template<br></td>
  </tr>
</table>

Minimal configuration
------------

    [main]
    host = localhost
    port = 8100
    search_query =org.apache.activemq.artemis:brokerName=*,module=JMS,name=*,serviceType=Queue,type=Broker

    [DEFAULTS]
    queue_max_messages = 5000
    queue_min_messages = 0
    consumers_threshold = 5000
    proc_url = http://www.google.com.br

Output Format
------------

```
{
	"data": [{
		"{#CONS_THRESHOLD}": "10",
		"{#QUEUE_MAX}": "5000",
		"{#QUEUE_MIN}": "0",
		"{#QUEUE_NAME}": "DLQ",
        "{#ARTEMIS_BROKER}": "localhost",
		"{#PROC_URL}": "http://www.google.com.br"
	}, {
		"{#CONS_THRESHOLD}": "10",
		"{#QUEUE_MAX}": "5000",
		"{#QUEUE_MIN}": "0",
		"{#QUEUE_NAME}": "ExampleQueue",
        "{#ARTEMIS_BROKER}": "localhost",
		"{#PROC_URL}": "http://www.google.com.br"
	}, {
		"{#CONS_THRESHOLD}": "10",
		"{#QUEUE_MAX}": "5000",
		"{#QUEUE_MIN}": "0",
		"{#QUEUE_NAME}": "ExpiryQueue",
        "{#ARTEMIS_BROKER}": "localhost",
		"{#PROC_URL}": "http://www.google.com.br"
	}]
}
```
