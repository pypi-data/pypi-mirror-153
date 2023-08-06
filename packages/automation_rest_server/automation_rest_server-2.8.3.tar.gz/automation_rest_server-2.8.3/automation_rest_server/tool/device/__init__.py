import sys
from utils.system import nexus_or_nvme_device
if "win" in sys.platform:
    from .windows import NVME
else:
    device_type = nexus_or_nvme_device()
    if device_type == "nvme":
        from .linux_nvme import NVME
    elif device_type == "nexus":
        from .linux_nexus import NVME
    else:
        from .linux_nvme import NVME
