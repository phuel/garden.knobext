import kivy.graphics as kg
from kivy.core.text import Label as CoreLabel

class Tick(object):
    """Class describing a tick drawn on a :class:`KnobWithTick`."""
    default_size = (3,10)
    default_color = (1,1,1,1)
    default_distance = 2
    
    def __init__(self, **kwargs):
        '''
        The configuration values are passed into the constructor as key value pairs (``**kwargs``)

        ``angle``
            The angle at which to position the tick, in degree from the knob's :attr:`start_angle``.

        ``value``
            The knob value at which to position the tick. (Ignored if ``angle`` is specified.)

        ``color``
            The color as rgba value in which the tick is rendered (default: ``(1,1,1,1)``).

        ``distance``
            The distance (in pixel) of the tick from the knob (default: ``2``).

        ``size``
            The size of the rectangle drawn as the tick mark as a (width,height) tuple (default: ``(3,10)``)

        ``text``
            The text shown as the tick mark. If text is specified no rectangle tick mark is drawn.
        '''
        self.angle = self._get_value('angle', None, **kwargs)
        self.value = self._get_value('value', None, **kwargs)
        self.text = self._get_value('text', None, **kwargs)
        self.size = self._get_value('size', self.default_size, **kwargs)
        self.color = self._get_value('color', self.default_color, **kwargs)
        self.distance = self._get_value('distance', self.default_distance, **kwargs)
        
    def _get_value(self, key, default_value, **kwargs):
        """Get the value for the specified key from the kwargs or return default_value if no value is available."""
        return kwargs[key] if key in kwargs else default_value

    def get_color(self):
        """Creates a Color graphics instruction."""
        return kg.Color(rgba=self.color)

    def get_angle(self, knob):
        """Gets the angle for the tick. Returns either the :attr:`angle` or the angle calculated from :attr:``value`."""
        if self.angle is not None:
            return knob.start_angle + self.angle
        return knob.start_angle + knob.get_angle(self.value)

    def get_rotation(self, knob):
        """Creates the Rotate instruction for the tick."""
        return kg.Rotate(angle=360 - self.get_angle(knob), origin=knob.center)

    def get_element(self, knob):
        """Creates the Rectangle instruction for the tick."""
        x = knob.center[0] - self.size[0] / 2
        y = knob.center[1] + (knob.height * knob.knobimg_size) / 2 + self.distance
        return kg.Rectangle(pos=(x, y), size=self.size)

    def render(self, canvas, knob):
        """Renders the ticks by adding graphics instructions to the ``canvas.before``."""
        canvas.add(self.get_color())
        if self.text is not None:
            label = CoreLabel(text=self.text)
            label.refresh()
            texture = label.texture
            x = knob.center[0]
            y = knob.center[1] + (knob.height * knob.knobimg_size) / 2 + self.distance
            canvas.add(self.get_rotation(knob))
            canvas.add(kg.Rotate(angle=-(360-self.get_angle(knob)), origin=(x,y)))
            canvas.add(kg.Rectangle(pos=(x-texture.width/2, y-texture.height/2), size=texture.size, texture=texture))
        else:
            canvas.add(self.get_rotation(knob))
            canvas.add(self.get_element(knob))
