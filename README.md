### Some notes about my unortodox coding practices


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
  File "/home/user/Downloads/start.py", line 1, in <module>
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

I pass the global() context to every exec() in my code. While some people may claim that this pollutes the context, this is exactly what I want.
