Video: http://youtu.be/Zz7c1OGv2U4

Knob
====

The `Knob` widget creates a component that looks like a
control Knob or Dial (from Wikipedia: "A control knob is a rotary
control used to provide input to a device when grasped by an
operator and turned, so that the degree of rotation corresponds to
the desired input."). To configure a knob a `max`/`min` and `step` value
should be provided (like in Slider). Additionally, `knobimg_source`
could be set to load a texture that visually represents the knob.

The `Knob` widget has a `start_angle` and `angle_range` property to
limit the allowed range of angles. Values of `start_angle` = 225 and
`angle_range` = 227 can be used to mimic a traditional volume knob.

The `value` of a `Knob` can be changed with the mouse wheel in the defined
`step` increments.

The `Knob` widget is focusable and the `value` can be changed with the
cursor keys in `step` increments as well.

To create a basic knob (in a kv file):

    Knob:
        size: 100, 100
        min: 0
        max: 100
        step: 1
        value: 0  # Default position of knob.
        knobimg_source: "img/knob_metal.png"  # Knob texture
        show_marker: False  # Do not show surrounding marker

To create a knob with a surrounding marker:

    Knob:
        size: 100, 100
        min: 0
        max: 100
        step: 1
        value: 0  # Default position of knob.
        knobimg_source: "img/knob_metal.png"  # Knob texture
        show_marker: True  # Show surrounding marker
        marker_img: "img/bline.png" # Marker texture image
        knob_size: 0.9  # Scales knob size to leave space for marker
        markeroff_color: 0, 0, 0, 0

License
=======
MIT license.

Credits
=======

- img/knob_metal.png by icondeposit.com (http://www.icondeposit.com/design:dial-version-3-includes-tutorial). Creative Commons Attribution 3.0.

- img/knob_black.ong by gliskard. http://gliskard.deviantart.com/art/UI-KNOB-free-PSD-324742538
