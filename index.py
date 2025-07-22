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

# Backend API
class API:
    def say_hello(self, name):
        print(f"JS → Python: say_hello({name})")
        return f"🌟 Hello {name.upper()}! You're connected to the Python backend."

    def reverse_text(self, text):
        print(f"JS → Python: reverse_text({text})")
        return text[::-1]

api = API()

# Fancy HTML + CSS + JS
html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🚀 PyFuturism Interface</title>
  <style>
  body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    color: #00ffe1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;

    /* 👇 New animated gradient with strong contrast */
    background: linear-gradient(-60deg,
      #0ff 0%,
      #f0f 25%,
      #0f0 50%,
      #00f 75%,
      #ff0 100%);
    background-size: 800% 800%;
    animation: gradientMove 5s ease-in-out infinite;
  }

  @keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  h1 {
    font-size: 2em;
    text-shadow: 0 0 10px #00ffe1;
  }

  .input-box {
    margin: 20px;
  }

  input {
    padding: 10px;
    font-size: 1em;
    border: 2px solid #00ffe1;
    border-radius: 5px;
    background: transparent;
    color: #00ffe1;
    width: 300px;
    outline: none;
  }

  button {
    padding: 12px 25px;
    background: #00ffe1;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
    margin: 5px;
  }

  button:hover {
    background: #007a74;
  }

  #response, #reverse {
    margin-top: 20px;
    font-size: 1.2em;
    min-height: 1em;
    text-shadow: 0 0 5px #00ffe1;
  }

  .spinner {
    border: 3px solid #00ffe122;
    border-top: 3px solid #00ffe1;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
    display: none;
    margin-top: 10px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>

</head>
<body>
  <h1>🤖 Welcome to PyFuturism</h1>
  <div class="input-box">
    <input id="nameInput" placeholder="Type your name..." />
  </div>
  <div>
    <button onclick="sayHi()">Greet</button>
    <button onclick="reverse()">Reverse</button>
  </div>
  <div class="spinner" id="loader"></div>
  <p id="response"></p>
  <p id="reverse"></p>

  <script>
    function setLoading(show) {
      document.getElementById("loader").style.display = show ? "block" : "none";
    }

    async function sayHi() {
      const name = document.getElementById("nameInput").value;
      setLoading(true);
      const response = await window.pywebview.api.say_hello(name);
      document.getElementById("response").innerText = response;
      setLoading(false);
    }

    async function reverse() {
      const text = document.getElementById("nameInput").value;
      setLoading(true);
      const reversed = await window.pywebview.api.reverse_text(text);
      document.getElementById("reverse").innerText = "🔁 Reversed: " + reversed;
      setLoading(false);
    }
  </script>
</body>
</html>
"""


webview.create_window("🌌 PyFuturism Interface", html=html, js_api=api, width=600, height=500)
webview.start()
