from prometheus_client import Gauge

cpu_count = Gauge('cpu_count', 'Number of CPU cores')
cpu_utilisation = Gauge('cpu_utilisation', 'CPU utilisation percentage')
memory_total = Gauge('memory_total_bytes', 'Total memory in bytes')
memory_utilisation = Gauge('memory_utilisation_percentage', 'Used memory in percentage')
disk_read_bytes = Gauge('disk_read_bytes', 'Disk read bytes')
disk_write_bytes = Gauge('disk_write_bytes', 'Disk write bytes')
network_bytes_sent = Gauge('network_bytes_sent', 'Network bytes sent')
network_bytes_recv = Gauge('network_bytes_recv', 'Network bytes received')
disk_total_bytes = Gauge('disk_total_bytes', 'Total disk space in bytes', ['mountpoint'])
disk_utilisation_percentage = Gauge('disk_utilisation_percentage', 'Disk utilisation percentage', ['mountpoint'])
