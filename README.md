###Some notes about my unorthodox coding practices


---
Most of the stuff that you see here will get you into real trouble, if you try to execute them in any serious and professional enviroment. They are risky, and I do not recomend it. I assume these are ok if you are running them for a project in a sandbox virtual machine that you can [ab]use.

I barely even ask or inform the user that a large script is about to be executed and installed. I don't recomend to follow this practices at all.

**It honestly feels illegal to do any of this**
This doesn’t feel like proper software, it acts more like an aggresive and invasive Trojan Horse, packed with hacks and virus like behavior. But instead of doing harm to your machine, it delivers software using extremely questionable and illegal methods.

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
I don't ask users if they wish to do a pip install. I do it myself automatically. Looks dangerous, I admit.

---

I pass the global() context to every exec() in my code. While some people may claim that this pollutes the context, this is exactly what I want. I want to be able to "agregate" objects to my execution enviroment. 
