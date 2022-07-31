import os

from kivy.base  import  runTouchApp
from kivy.lang  import  Builder

if os.path.isfile('__init__.py'):
    from __init__ import Knob
else:
    from kivy.garde.knob import Knob

# LOAD KV UIX
runTouchApp(Builder.load_file('example.kv'))
