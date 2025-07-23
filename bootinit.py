import json
import base64
import subprocess
import sys
import importlib
import urllib.request

class init:
  @classmethod
  def httpGet(cls,path):
    return urllib.request.urlopen(path).read()

  @classmethod
  def githubGet(cls,owner,repo,path):
    r = cls.httpGet(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")
    j = json.loads(r)
    c = j["contents"]
    d = base64.b64decode(c)
    return d
  
  @classmethod
  def require(cls,module_name, pip_name=None):
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

print("Hello World from boot init fresh 3")
print(init.httpget("http://checkip.dyndns.org"))
