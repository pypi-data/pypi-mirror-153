import logging
import os
import resource

import psutil


def limit_memory_to_cgroup_limits():
    if os.path.isfile('/sys/fs/cgroup/memory/memory.limit_in_bytes'):
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes') as limit:
            total_memory_from_host_os = psutil.virtual_memory().total
            total_memory_limit_from_cgroup = int(limit.read())
            if total_memory_limit_from_cgroup < total_memory_from_host_os:
                logging.info(f"Limiting memory to {total_memory_limit_from_cgroup} byte")
                resource.setrlimit(resource.RLIMIT_AS, (total_memory_limit_from_cgroup, total_memory_limit_from_cgroup))
