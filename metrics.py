from prometheus_client import Gauge

machine_cpu_count = Gauge('machine_cpu_count', 'Number of CPU cores')
machine_cpu_utilisation = Gauge('machine_cpu_utilisation', 'CPU utilisation percentage')
machine_memory_total = Gauge('machine_memory_total_bytes', 'Total memory in bytes')
machine_memory_utilisation = Gauge('machine_memory_utilisation_percentage', 'Used memory in percentage')
machine_disk_read_bytes = Gauge('machine_disk_read_bytes', 'Disk read bytes')
machine_disk_write_bytes = Gauge('machine_disk_write_bytes', 'Disk write bytes')
machine_network_bytes_sent = Gauge('machine_network_bytes_sent', 'Network bytes sent')
machine_network_bytes_recv = Gauge('machine_network_bytes_recv', 'Network bytes received')
disk_total_bytes = Gauge('disk_total_bytes', 'Total disk space in bytes', ['mountpoint'])
disk_utilisation_percentage = Gauge('disk_utilisation_percentage', 'Disk utilisation percentage', ['mountpoint'])
