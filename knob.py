
"""
    Based on: https://github.com/kivy-garden/garden.knob

    Knob
    ====

    The :class:`Knob` widget creates a component that looks like a
    control Knob or Dial (from Wikipedia : "A control knob is a rotary
    control used to provide input to a device when grasped by an
    operator and turned, so that the degree of rotation corresponds to
    the desired input." http://en.wikipedia.org/wiki/Control_knob).
    To configure a knob a max/min, slope and step values should be provided.
    Additionally, knobimg_source could be set to load
    a texture that visually represents the knob.
"""

__all__     = ('Knob',)
__version__ = '0.3'

import math

from kivy.lang          import  Builder
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.widget    import  Widget
from kivy.properties    import  NumericProperty, StringProperty,\
                                BooleanProperty, BoundedNumericProperty,\
                                ListProperty
import kivy.graphics as kg

Builder.load_string('''
#
#    Knob
#    ====
#     To create a basic knob (in a kv file):
#
#     Knob:
#       size:               100, 100
#       min:                0
#       max:                100
#       step:               1
#       slope:              1
#       value:              0                       # Default position of knob.
#       knobimg_source:     "img/knob_metal.png"    # Knob texture
#       show_marker:        False                   # Do not show surrounding marker
#
#     To create a knob with a surrounding marker:
#
#     Knob:
#       size:               100, 100
#       min:                0
#       max:                100
#       step:               1
#       slope:              1
#       value:              0                       # Default position of knob.
#       knobimg_source:     "img/knob_metal.png"    # Knob texture
#       show_marker:        True                    # Show surrounding marker
#       marker_img:         "img/bline.png"         # Marker texture image
#       knob_size:          0.9                     # Scales knob size to leave space for marker
#       markeroff_color:    0, 0, 0, 0

<Knob>
    size_hint: None, None

    canvas:
        Color:
            rgba: self.markeroff_color
        Ellipse:
            pos: self.pos
            size: self.size
            angle_start: 0
            angle_end: 360
            source: self.markeroff_img

        Color:
            rgba: self.marker_color
        Ellipse:
            pos: self.pos
            size: self.size
            angle_start: self.start_angle
            angle_end: self._angle + self.marker_ahead if self._angle > self.start_angle else self.start_angle
            source: self.marker_img

        Color:
            rgba: self.knobimg_bgcolor
        Ellipse:
            pos: self.pos[0] + (self.size[0] * (1 - self.knobimg_size))/2, self.pos[1] + (self.size[1] * (1 - self.knobimg_size)) / 2
            size: self.size[0] * (self.knobimg_size), self.size[1] * (self.knobimg_size)

        Color:
            rgba: self.knobimg_color
        PushMatrix
        Rotate:
            angle: 360 - self._angle
            origin: self.center
        Rectangle:
            pos: self.pos[0] + (self.size[0] * (1 - self.knobimg_size)) /2, self.pos[1] + (self.size[1] * (1 - self.knobimg_size)) / 2
            size: self.size[0] * (self.knobimg_size), self.size[1] * (self.knobimg_size)
            source: self.knobimg_source
        PopMatrix
''')

class Knob(FocusBehavior, Widget):
    """Class for creating a Knob widget."""

    min = NumericProperty(0)
    '''Minimum value for value :attr:`value`.
    :attr:`min` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    max = NumericProperty(100)
    '''Maximum value for value :attr:`value`.
    :attr:`max` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 100.
    '''

    value = NumericProperty(0)
    '''Current value of the knob. Set :attr:`value` when creating a knob to
    set its initial position. An internal :attr:`_angle` is calculated to set
    the position of the knob.
    :attr:`value` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    step = BoundedNumericProperty(1, min=0)
    '''Step interval of knob to go from min to max. An internal
    :attr:`_angle_step` is calculated to set knob step in degrees.
    :attr:`step` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 1 (min=0).
    '''

    curve = BoundedNumericProperty(1, min=1)
    '''This parameter determines the shape of the map function. It represent the
    reciprocal of a power function's exponent used to map the input value.
    So, for higher values of curve the contol is more reactive, and conversely.
    '''

    knobimg_source = StringProperty("")
    '''Path of texture image that visually represents the knob. Use PNG for
    transparency support. The texture is rendered on a centered rectangle of
    size = :attr:`size` * :attr:`knobimg_size`.
    :attr:`knobimg_source` is a :class:`~kivy.properties.StringProperty`
    and defaults to empty string.
    '''

    knobimg_color = ListProperty([1, 1, 1, 1])
    '''Color to apply to :attr:`knobimg_source` texture when loaded.
    :attr:`knobimg_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1,1,1,1].
    '''

    knobimg_size = BoundedNumericProperty(0.9, max=1.0, min=0.1)
    ''' Internal proportional size of rectangle that holds
    :attr:`knobimg_source` texture.
    :attr:`knobimg_size` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 0.9.
    '''

    show_marker = BooleanProperty(True)
    ''' Shows/hides marker surrounding knob. use :attr:`knob_size` < 1.0 to
    leave space to marker.
    :attr:`show_marker` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    '''

    marker_img = StringProperty("")
    '''Path of texture image that visually represents the knob marker. The
    marker is rendered in a centered Ellipse (Circle) with the same size of
    the widget and goes from angle_start=:attr:`marker_startangle` to
    angle_end=:attr:`_angle`.
    :attr:`marker_img` is a :class:`~kivy.properties.StringProperty` and
    defaults to "".
    '''

    marker_color = ListProperty([1, 1, 1, 1])
    '''Color to apply to :attr:`marker_img` texture when loaded.
    :attr:`marker_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1,1,1,1].
    '''

    knobimg_bgcolor = ListProperty([0, 0, 0, 1])
    ''' Background color behind :attr:`knobimg_source` texture.
    :attr:`value` is a :class:`~kivy.properties.ListProperty` and defaults
    to [0,0,0,1].
    '''

    markeroff_img = StringProperty("")
    '''Path of texture image that visually represents the knob marker where
    it's off, that is, parts of the marker that haven't been reached yet by
    the knob (:attr:`value`).
    :attr:`markeroff_img` is a :class:`~kivy.properties.StringProperty`
    and defaults to "".
    '''

    markeroff_color = ListProperty([0, 0, 0, 0])
    '''Color applied to :attr:`markeroff_img` int the Canvas.
    :attr:`markeroff_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [0,0,0,0].
    '''

    marker_startangle = NumericProperty(0)
    '''Starting angle of Ellipse where :attr:`marker_img` is rendered.
    :attr:`value` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    marker_ahead = NumericProperty(0)
    ''' Adds degrees to angle_end of marker (except when :attr:`value` == 0).
    :attr:`marker_ahead` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.
    '''

    start_angle = BoundedNumericProperty(0, max=360, min=0)
    ''' The start of the allowed range of angles. For a traditional volume
    knob this would be 225°.
    :attr:`start_angle` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 0 (min=0, max=360).
    '''
    angle_range = BoundedNumericProperty(360, max=360, min=0)
    ''' The allowed range this knob can be turned. 270° for a normal volume knob.
    :attr:`angle_range` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 360 (min=0, max=360).
    '''
    
    _angle = NumericProperty(0)            # Internal angle calculated from value.

    def __init__(self, *args, **kwargs):
        self.is_focusable = kwargs.get('is_focusable', True)
        super(Knob, self).__init__(*args, **kwargs)
        self.bind(show_marker = self._show_marker)
        self.bind(value       = self._value)
        self.bind(start_angle = lambda _,__: self._value(self, self.value))
        self.bind(angle_range = lambda _,__: self._value(self, self.value))
        self.selected = False

    def _value(self, instance, value):
        angle = self.get_angle(value)
        self.set_angle(angle)
        self.on_knob(value)

    def _show_marker(self, instance, flag):
        # "show/hide" marker.
        if flag:
            self.knobimg_bgcolor[3] = 1
            self.marker_color[3] = 1
            self.markeroff_color[3] = 1
        else:
            self.knobimg_bgcolor[3] = 0
            self.marker_color[3] = 0
            self.markeroff_color[3] = 0


    def get_angle(self, value):
        return pow( (value - self.min)/(self.max - self.min), 1./self.curve) * self.angle_range

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'scrollup':
                self.value -= self.step
                self.focus = True
            elif touch.button == 'scrolldown':
                self.value += self.step
                self.focus = True
            else:    
                self.selected = True
                self.update_angle(touch)
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.selected = False
        super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if self.selected:
            self.update_angle(touch)
        super().on_touch_move(touch)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if (keycode[1] == 'up' or keycode[1] == 'right') and self.value < self.max:
            self.value += self.step
        elif (keycode[1] == 'down' or keycode[1] == 'left') and self.value > self.min:
            self.value -= self.step
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def update_angle(self, touch):
        posx, posy = touch.pos
        cx, cy     = self.center
        relx, rely = posx - cx, posy - cy
        # Don't change the angle after clicks in the middle third of the
        # knob so that the knob can be focused with a center click.
        if abs(relx) < self.width / 6 and abs(rely) < self.height / 6:
            return
        coss = math.cos(self.start_angle / 180.0 * math.pi)
        sins = math.sin(self.start_angle / 180.0 * math.pi)
        rx = relx * coss - rely * sins
        ry = relx * sins + rely * coss

        if ry >= 0:                                 # Quadrants are clockwise.
            quadrant = 1 if rx >= 0 else 4
        else:
            quadrant = 3 if rx <= 0 else 2

        try:
            angle = math.atan(rx / ry) * (180.0 / math.pi)
            if quadrant == 2 or quadrant == 3:
                angle = 180 + angle
            elif quadrant == 4:
                angle = 360 + angle
        except:                                   # atan not def for angle 90 and 270
            angle = 90 if quadrant <= 2 else 270
        self.set_angle(angle)

    def set_angle(self, angle):
        angle_step = (self.step * self.angle_range)/(self.max - self.min)
        angle = int(angle / angle_step + 0.5) * angle_step

        bottom_angle = 360 - (360 - self.angle_range) / 2
        if angle < 0 or angle > bottom_angle:
            angle = 0
        if angle > self.angle_range:
            angle = self.angle_range
        self._angle = self.start_angle + angle

        relativeValue = pow((angle / self.angle_range), 1.0 / self.curve)
        self.value = (relativeValue * (self.max - self.min)) + self.min

        self.marker_startangle = self.start_angle


    #TO OVERRIDE
    def on_knob(self, value):
        pass #Knob values listenerr


class KnobWithTicks(Knob):
    """Knob widget that shows markers around the knob."""

    def __init__(self, ticks, *args, **kwargs):
        """
        """
        self.ticks = ticks
        self.bind(size=self.position_ticks)
        self.bind(pos=self.position_ticks)
        super().__init__(*args, **kwargs)

    def position_ticks(self, *args):
        self.canvas.before.clear()
        for tick in self.ticks:
            self.canvas.before.add(kg.PushMatrix())
            tick.render(self.canvas.before, self)
            self.canvas.before.add(kg.PopMatrix())
