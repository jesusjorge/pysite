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

print("Python Exodo - 2025.08.20 ")
print("Nothing to do here\n\n")

print(Jan.platform)

print(Jan.dirLocalConfig("foundations"))
print(Jan.DirExists(Jan.dirLocalConfig("foundations")))

print(Jan.dirCache("foundations"))
print(Jan.DirExists(Jan.dirCache("foundations")))

print(Jan.dirTemp("foundations"))
print(Jan.DirExists(Jan.dirTemp("foundations")))










input("\n\n<Press Enter to exit>\n")
