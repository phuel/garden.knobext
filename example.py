import os

from kivy.base  import  runTouchApp
from kivy.lang  import  Builder

if os.path.isfile('__init__.py'):
    from knob import Knob, KnobWithTicks
    from tick import Tick
else:
    from kivy.garde.knob import Knob, KnobWithTicks, Tick


class RangeTickKnob(KnobWithTicks):
    def __init__(self, *args, **kwargs):
        ticks = [
            Tick(value=0),
            Tick(value=0, text="Low", distance=25),
            Tick(value=1),
            Tick(value=1, text="Med", distance=25),
            Tick(value=2),
            Tick(value=2, text="High", distance=25),
        ]
        super().__init__(ticks, *args, **kwargs)

# LOAD KV UIX
runTouchApp(Builder.load_file('example.kv'))
