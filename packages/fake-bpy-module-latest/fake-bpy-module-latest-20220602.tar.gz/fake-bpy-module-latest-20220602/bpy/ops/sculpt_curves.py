import sys
import typing
import bpy.types


def brush_stroke(stroke: typing.Union[
        typing.Dict[str, 'bpy.types.OperatorStrokeElement'], typing.
        List['bpy.types.OperatorStrokeElement'], 'bpy_prop_collection'] = None,
                 mode: typing.Union[str, int] = 'NORMAL'):
    ''' Sculpt curves using a brush

    :param stroke: Stroke
    :type stroke: typing.Union[typing.Dict[str, 'bpy.types.OperatorStrokeElement'], typing.List['bpy.types.OperatorStrokeElement'], 'bpy_prop_collection']
    :param mode: Stroke Mode, Action taken when a paint stroke is made * NORMAL Regular -- Apply brush normally. * INVERT Invert -- Invert action of brush for duration of stroke. * SMOOTH Smooth -- Switch brush to smooth mode for duration of stroke.
    :type mode: typing.Union[str, int]
    '''

    pass


def select_all(action: typing.Union[str, int] = 'TOGGLE'):
    ''' (De)select all control points

    :param action: Action, Selection action to execute * TOGGLE Toggle -- Toggle selection for all elements. * SELECT Select -- Select all elements. * DESELECT Deselect -- Deselect all elements. * INVERT Invert -- Invert selection of all elements.
    :type action: typing.Union[str, int]
    '''

    pass
