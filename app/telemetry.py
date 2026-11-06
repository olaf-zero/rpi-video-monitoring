import psutil

psutil.cpu_percent(interval=None)

def get_system_stats():
    cpu_percent = round(psutil.cpu_percent(interval=None), 1)
    ram_percent = round(psutil.virtual_memory().percent, 1)
    disk_percent = round(psutil.disk_usage('/').percent, 1)

    ret = {
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "disk_percent": disk_percent
    }

    return ret
