import subprocess
import sys
import importlib

def require(module_name, pip_name=None):
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

webview = require("webview","pywebview")

# app.py
#import webview

class API:
    def say_hello(self, name):
        print(f"Hello from frontend: {name}")
        return f"Hello {name}, from Python backend!"

api = API()

html = """
<!DOCTYPE html>
<html>
  <body>
    <h1>Front-end</h1>
    <input id="nameInput" placeholder="Type your name" />
    <button onclick="sayHi()">Say Hi</button>
    <p id="response"></p>
    <script>
      function sayHi() {
        let name = document.getElementById("nameInput").value;
        window.pywebview.api.say_hello(name).then(function(response) {
          document.getElementById("response").innerText = response;
        });
      }
    </script>
  </body>
</html>
"""

webview.create_window("My App", html=html, js_api=api)
webview.start()
