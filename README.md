### Some notes about my unortodox coding practices

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
