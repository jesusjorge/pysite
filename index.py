webview = init.require("webview","pywebview")

class API:
    def say_hello(self, name):
        print(f"JS → Python: say_hello({name})")
        x = 0
        x = x / x
        return f"🌟 Hello {name.upper()}! You're connected to the Python backend."

    def reverse_text(self, text):
        print(f"JS → Python: reverse_text({text})")
        return text[::-1]

api = API()

webview.create_window("🌌 PyFuturism Interface", html=html, js_api=api, width=600, height=500)
webview.start()




















































































######################################
# Resource Section ###################
#e34bbc0f-fae2-490a-9219-d2c8ff8d8875#


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
    color: #00ffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;

    /* Tron-inspired cool glow gradient */
    background: linear-gradient(-45deg,
      #0f0f1e 0%,
      #081b2f 25%,
      #0e2b3d 50%,
      #081b2f 75%,
      #0f0f1e 100%);
    background-size: 600% 600%;
    animation: gradientShift 12s ease-in-out infinite;
  }

  @keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  h1 {
    font-size: 2em;
    text-shadow: 0 0 15px #00ffff;
  }

  .input-box {
    margin: 20px;
  }

  input {
    padding: 10px;
    font-size: 1em;
    border: 2px solid #00ffff;
    border-radius: 5px;
    background: rgba(0, 0, 0, 0.4);
    color: #00ffff;
    width: 300px;
    outline: none;
  }

  button {
    padding: 12px 25px;
    background: #00ffff;
    color: #000;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s;
    margin: 5px;
    box-shadow: 0 0 10px #00ffff;
  }

  button:hover {
    background: #00b0b0;
    box-shadow: 0 0 20px #00ffff;
  }

  #response, #reverse {
    margin-top: 20px;
    font-size: 1.2em;
    min-height: 1em;
    text-shadow: 0 0 5px #00ffff;
  }

  .spinner {
    border: 3px solid #00ffff22;
    border-top: 3px solid #00ffff;
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
  <h1>🤖 It works! </h1>
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





















######################################
# And this is the ignore section #####
#e34bbc0f-fae2-490a-9219-d2c8ff8d8875#



You can write anything here, and it won't break any Python rules.
Just a free text section.

In fact, nothing in here is even going to be part of the executable Code, or the Resources.




