[G](https://github.com/jesusjorge/jesusjorge.github.io/) [B](https://github.com/jesusjorge/pysite) [U](https://jesusjorge.github.io/)

### Some notes about my unorthodox coding practices

![trojan](trojan.avif)

---
Most of the stuff that you see [here](https://github.com/jesusjorge) will get you into real trouble, if you try to execute them in any serious and professional enviroment. They are risky, and I do not recomend it. I assume these are ok if you are running them for a project in a sandbox virtual machine that you can [ab]use.

I barely even ask or inform the user that a large script is about to be executed and installed. I don't recomend to follow this practices at all.

This doesn’t feel like proper software. It acts more like an aggressive and invasive Trojan Horse, packed with hacks and virus like behavior. But instead of harming your machine, it delivers software using extremely questionable, borderline-illegal methods.

|                 | **Software** 🧠   | **Virus** 🦠            | **Trojan** 🐴              | **Hacker** 🧑‍💻                   |
| --------------- | ----------------- | ----------------------- | -------------------------- | ---------------------------------- |
| **What is it?** | Code              | Self-replicating code   | Deceptive code             | Human using code as weapon         |
| **Intent**      | To serve or solve | To spread and disrupt   | To trick and infiltrate    | To subvert or repurpose            |
| **Entry**       | You install it    | It sneaks in or hijacks | You run it unknowingly     | Finds a hole and gets in           |
| **Trust**       | Transparent       | None                    | Pretends to be trusted     | Exploits misplaced trust           |
| **Autonomy**    | Runs when asked   | Runs when it can        | Runs when you trigger it   | Makes software run how *they* want |
| **Goal**        | Functionality     | Propagation / damage    | Delivery of hidden payload | Control, knowledge, chaos          |

I still question myself if this is actual software, or something else

| **Intent**     | **Delivery**                 | **Perception**                 |
| -------------- | ---------------------------- | ------------------------------ |
| Legit software | Automates setup for the user | "Wow, so easy!"                |
| Trojan/Virus   | Automates setup *for itself* | "Wait... what did I just run?" |

---
I don't ask users if they wish to do a pip install. I do it myself automatically. **Don't do this**

---
I like to move my important code to the top of my source file.
That means that "resources" inside such file will be put at the bottom.
And because of that, I will do weird things like flipping the code over.

https://github.com/jesusjorge/pysite/blob/main/index.py

---
You may notice that I break the file naming convention, by injecting lines like:

```
Traceback (most recent call last):
  File "https://github.com/jesusjorge/pysite/blob/main/init.py", line 20, in run
  File "https://github.com/jesusjorge/pysite/blob/main/index.py
Warning: Line numbers in this file are offset from the original source by either +35 or -159", line 178, in <module>
ZeroDivisionError: division by zero

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "start.py", line 1, in <module>
    exec(__import__('urllib.request').request.urlopen('http://jesusjorge.github.io/boot.py').read())
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 13, in <module>
  File "https://github.com/jesusjorge/pysite/blob/main/init.py", line 60, in <module>
  File "https://github.com/jesusjorge/pysite/blob/main/init.py", line 22, in run
RuntimeError: [https://github.com/jesusjorge/pysite/blob/main/index.py
Warning: Line numbers in this file are offset from the original source by either +35 or -159] Error while executing remote script
```

I do this for clarity. I want to be able to find the actual real line that is raising such Exception. 

---
I pass the global() context to every exec() in my code. While some people may claim that this pollutes the context, this is exactly what I want. I want to be able to "agregate" objects to my execution enviroment. 

---
### ☯️ Well, if all this sounds wrong, why are we doing it at all?

You can read about that here 

https://github.com/jesusjorge/jesusjorge.github.io
