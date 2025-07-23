import json
import base64
import subprocess
import sys
import importlib
import urllib.request

class init:
  @classmethod
  def run(cls,code,filehint):
    if not isinstance(code, str):
      code = code.decode('utf-8')
    #e34bbc0f-fae2-490a-9219-d2c8ff8d8875# <- Reverse Token
    parts = code.split("#e34bbc0f-fae2-490a-9219-d2c8ff8d8875#")
    if len(parts) > 1:
      code = parts[1] + "\n" + parts[0]
      filehint = f"{filehint}      SCRAMBLED FILE, (-{len(parts[1].split('\n'))}|+{len(parts[0].split('\n'))-1} LINE OFFSET)"
    try:
      exec(compile(code, filehint, 'exec'), globals())
    except Exception as e:
      raise RuntimeError(f"[{filehint}] Error while executing remote script") from e
  
  @classmethod
  def httpGet(cls,path):
    return urllib.request.urlopen(path).read()

  @classmethod
  def githubGet(cls,owner,repo,path):
    try:
      tResponse = cls.httpGet(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")
      tJson = json.loads(tResponse)
      tContent = tJson["content"]
      tBase64 = base64.b64decode(tContent)
      return tBase64
    except urllib.error.HTTPError as e:
      if e.code == 403:
        tRequest = urllib.request.urlopen(f"https://raw.githubusercontent.com/{owner}/{repo}/main/{path}")
        tResponse = tRequest.read()
        return tResponse
      else:
          raise

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

init.run(init.githubGet("jesusjorge","pysite","index.py"),"https://github.com/jesusjorge/pysite/blob/main/index.py")
