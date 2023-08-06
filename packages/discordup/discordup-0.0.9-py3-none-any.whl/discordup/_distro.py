def findDistroType():
    try:
        open("/etc/debian_version").read()
        return "debian"
    except Exception:
        pass

    return "unknown"