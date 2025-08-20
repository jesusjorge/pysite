import importlib
import os
import sys

class classproperty(property):
    def __get__(self, obj, cls):
        return self.fget(cls)

class Jan:
    _internal = {}
    _localconfig = {"L":"$HOME/.local/share/*/", "W":"%LOCALAPPDATA%/*/"}
    _cache = {"L":"$HOME/.cache/*/", "W":"%LOCALAPPDATA%/*/Cache/"}
    _temp = {"L":"/tmp/$USER/*/", "W":"%TEMP%/*/"}

    @classmethod
    def moduleRequire(cls,module_name, pip_name=None):
      """
      Ensures a module is installed and imported.
      - module_name: name used in 'import'
      - pip_name: name used in 'pip install' (optional, defaults to module_name)
      Returns the imported module.
      """
      try:
          return importlib.import_module(module_name)
      except ImportError:
          pip_name = pip_name or module_name
          print(f"Installing '{pip_name}'...")
          subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pip_name])
          return importlib.import_module(module_name)
    
    @classproperty
    def platform(cls):
        if "sys.platform" in cls._internal:
            return cls._internal["sys.platform"]
        result = sys.platform
        value = ""
        if "linux" in result:
            value = "L"
        elif "win" in result:
            value = "W"
        else:
            value = result
        cls._internal["sys.platform"] = value
        return value

    @classmethod
    def dirLocalConfig(cls,folder):
        return os.path.expandvars(cls._localconfig[cls.platform].replace("*",folder))

    @classmethod
    def dirCache(cls,folder):
        return os.path.expandvars(cls._cache[cls.platform].replace("*",folder))

    @classmethod
    def dirTemp(cls,folder):
        return os.path.expandvars(cls._temp[cls.platform].replace("*",folder))

    @classmethod
    def DirMake(cls,path):
        os.makedirs(path, exist_ok=True)

    @classmethod
    def DirExists(cls,path):
        return os.path.isdir(path)

print("\n")
print("Exodo - 2025.08.20 ")
print("Nothing to do here\n\n")

Jan.moduleRequire("zeroconf","zeroconf")

print(Jan.platform)

print(Jan.dirLocalConfig("foundations"))
print(Jan.DirExists(Jan.dirLocalConfig("foundations")))

print(Jan.dirCache("foundations"))
print(Jan.DirExists(Jan.dirCache("foundations")))

print(Jan.dirTemp("foundations"))
print(Jan.DirExists(Jan.dirTemp("foundations")))
####
#!/usr/bin/env python3
# bonjour_scan.py
import argparse
import ipaddress
import sys
import threading
import time
from typing import Dict, List, Set

from zeroconf import ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf

def fmt_addrs(info: ServiceInfo) -> List[str]:
    addrs: List[str] = []
    # Prefer modern helpers; fall back if needed
    candidates = []
    if hasattr(info, "parsed_scoped_addresses"):
        candidates = info.parsed_scoped_addresses()
    elif hasattr(info, "parsed_addresses"):
        candidates = info.parsed_addresses()
    for addr in candidates:
        addr = addr.split("%")[0]  # strip scope (e.g., "%eth0")
        try:
            addrs.append(str(ipaddress.ip_address(addr)))
        except ValueError:
            pass
    return addrs

def decode_txt(props) -> dict:
    """DNS‑SD TXT: keys are bytes; values may be bytes, None (flag), or lists."""
    out = {}
    if not props:
        return out
    for k, v in props.items():
        key = k.decode(errors="replace") if isinstance(k, (bytes, bytearray)) else str(k)
        if v is None:
            out[key] = True  # key present => boolean flag
        elif isinstance(v, (bytes, bytearray)):
            out[key] = v.decode("utf-8", errors="replace")
        elif isinstance(v, (list, tuple)):
            out[key] = [
                x.decode("utf-8", errors="replace") if isinstance(x, (bytes, bytearray)) else str(x)
                for x in v
            ]
        else:
            out[key] = str(v)
    return out

class TypeCollector:
    """Collect DNS‑SD service types via _services._dns-sd._udp.local."""
    def __init__(self, zc: Zeroconf):
        self.zc = zc
        self.types: Set[str] = set()
        self._lock = threading.Lock()

    # Recent zeroconf uses keyword args
    def _on_change(self, *, zeroconf, service_type, name, state_change, **_):
        if state_change in (ServiceStateChange.Added, ServiceStateChange.Updated):
            with self._lock:
                # 'name' here is the discovered type (e.g., "_http._tcp.local.")
                self.types.add(name)

    def collect(self, seconds: float) -> List[str]:
        browser = ServiceBrowser(
            self.zc,
            "_services._dns-sd._udp.local.",
            handlers=[self._on_change],
        )
        time.sleep(seconds)
        browser.cancel()
        with self._lock:
            return sorted(self.types)

class ServiceCollector:
    """Collect instances for given service types."""
    def __init__(self, zc: Zeroconf, types: List[str]):
        self.zc = zc
        self.types = types
        self.services: Dict[str, Dict[str, ServiceInfo]] = {t: {} for t in types}
        self._lock = threading.Lock()
        self._browsers: List[ServiceBrowser] = []

    def _on_change(self, *, zeroconf, service_type, name, state_change, **_):
        if state_change in (ServiceStateChange.Added, ServiceStateChange.Updated):
            info = zeroconf.get_service_info(service_type, name, timeout=2000)
            if info:
                with self._lock:
                    self.services[service_type][name] = info
        elif state_change == ServiceStateChange.Removed:
            with self._lock:
                self.services.get(service_type, {}).pop(name, None)

    def browse(self, seconds: float):
        self._browsers = [ServiceBrowser(self.zc, t, handlers=[self._on_change]) for t in self.types]
        time.sleep(seconds)
        for b in self._browsers:
            b.cancel()

    def snapshot(self):
        with self._lock:
            return {t: dict(s) for t, s in self.services.items()}

def main():
    ap = argparse.ArgumentParser(description="List Bonjour (mDNS/DNS‑SD) devices on the LAN.")
    ap.add_argument("--discover-seconds", type=float, default=3.0,
                    help="Seconds to discover service TYPES (default: 3)")
    ap.add_argument("--browse-seconds", type=float, default=5.0,
                    help="Seconds to browse service INSTANCES (default: 5)")
    ap.add_argument("--types", nargs="*", default=None,
                    help="Service types to browse (e.g. _http._tcp.local. _ipp._tcp.local.). "
                         "If omitted, auto‑discovers types.")
    args = ap.parse_args()

    zc = Zeroconf()
    try:
        types = args.types
        if not types:
            tc = TypeCollector(zc)
            types = tc.collect(args.discover_seconds)
            if not types:
                print("No DNS‑SD service types discovered.", file=sys.stderr)

        if types:
            sc = ServiceCollector(zc, types)
            sc.browse(args.browse_seconds)
            data = sc.snapshot()

            printed_any = False
            for t in sorted(data.keys()):
                entries = data[t]
                if not entries:
                    continue
                printed_any = True
                print(f"\n=== Service Type: {t} ===")
                for name, info in sorted(entries.items()):
                    addrs = fmt_addrs(info)
                    host = info.server.rstrip(".") if getattr(info, "server", None) else "—"
                    txt = decode_txt(getattr(info, "properties", {}) or {})
                    print(f"- {name}")
                    print(f"    Host:  {host}")
                    print(f"    Port:  {info.port}")
                    print(f"    Addrs: {', '.join(addrs) if addrs else '—'}")
                    if txt:
                        print(f"    TXT:   {txt}")
            if not printed_any:
                print("No Bonjour services found.")
        else:
            print("Nothing to browse.")
    finally:
        zc.close()

if __name__ == "__main__":
    main()

####









input("\n\n<Press Enter to exit>\n")
