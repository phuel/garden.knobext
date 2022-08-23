import os

from kivy.base  import  runTouchApp
from kivy.lang  import  Builder

if os.path.isfile('__init__.py'):
    from knob import Knob, KnobWithTicks
    from tick import Tick
else:
    from kivy.garde.knob import Knob, KnobWithTicks, Tick

from kivy.config import Config
Config.set('graphics', 'width', '650')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class DecimalTickKnob(KnobWithTicks):
    def __init__(self, *args, **kwargs):
        ticks = []
        for i in range(0,11,2):
            ticks.append(Tick(value=i))
            ticks.append(Tick(value=i, text=str(i), distance=25))
        for i in range(1,10,2):
            ticks.append(Tick(value=i, size=(3,5)))
        super().__init__(ticks, *args, **kwargs)

class SymmetricTickKnob(KnobWithTicks):
    def __init__(self, *args, **kwargs):
        ticks = [
            Tick(value=-50),
            Tick(value=-50, text="-50", distance=25),
            Tick(value=-25),
            Tick(value=-25, text="-25", distance=25),
            Tick(value=0),
            Tick(value=0, text="0", distance=25),
            Tick(value=25),
            Tick(value=25, text="25", distance=25),
            Tick(value=50),
            Tick(value=50, text="50", distance=25),
        ]
        super().__init__(ticks, *args, **kwargs)

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
