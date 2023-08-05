"""This module is for SVG's `continual 3D bezier curve` (S)
path data class implementations.
"""

from typing import Any
from typing import Union

from apysc._geom.path_control_x_interface import PathControlXInterface
from apysc._geom.path_control_y_interface import PathControlYInterface
from apysc._geom.path_data_base import PathDataBase
from apysc._geom.path_dest_x_interface import PathDestXInterface
from apysc._geom.path_dest_y_interface import PathDestYInterface
from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.boolean import Boolean
from apysc._type.int import Int
from apysc._type.string import String


class PathBezier3DContinual(
        PathDataBase, PathControlXInterface, PathControlYInterface,
        PathDestXInterface, PathDestYInterface):
    """
    Path data class for SVG's `continual 3D bezier curve` (S).

    Examples
    --------
    >>> import apysc as ap
    >>> stage: ap.Stage = ap.Stage()
    >>> sprite: ap.Sprite = ap.Sprite()
    >>> sprite.graphics.line_style(color='#fff', thickness=3)
    >>> path: ap.Path = sprite.graphics.draw_path(
    ...     path_data_list=[
    ...         ap.PathMoveTo(x=0, y=50),
    ...         ap.PathBezier3D(
    ...             control_x1=0, control_y1=0,
    ...             control_x2=50, control_y2=0,
    ...             dest_x=50, dest_y=50),
    ...         ap.PathBezier3DContinual(
    ...             control_x=100, control_y=100,
    ...             dest_x=100, dest_y=50),
    ...     ])
    """

    @add_debug_info_setting(
        module_name=__name__, class_name='PathBezier3DContinual')
    def __init__(
            self,
            control_x: Union[int, Int],
            control_y: Union[int, Int],
            dest_x: Union[int, Int],
            dest_y: Union[int, Int],
            *,
            relative: Union[bool, Boolean] = False) -> None:
        """
        Path data class for SVG's `continual 3D bezier curve` (S).

        Parameters
        ----------
        control_x : Int or int
            X-coordinate of the bezier's control point.
        control_y : Int or int
            Y-coordinate of the bezier's control point.
        dest_x : Int or int
            X-coordinate of the destination point.
        dest_y : Int or int
            Y-coordinate of the destination point.
        relative : bool or Boolean, default False
            A boolean value indicates whether the path coordinates
            are relative or not (absolute).

        Examples
        --------
        >>> import apysc as ap
        >>> stage: ap.Stage = ap.Stage()
        >>> sprite: ap.Sprite = ap.Sprite()
        >>> sprite.graphics.line_style(color='#fff', thickness=3)
        >>> path: ap.Path = sprite.graphics.draw_path(
        ...     path_data_list=[
        ...         ap.PathMoveTo(x=0, y=50),
        ...         ap.PathBezier3D(
        ...             control_x1=0, control_y1=0,
        ...             control_x2=50, control_y2=0,
        ...             dest_x=50, dest_y=50),
        ...         ap.PathBezier3DContinual(
        ...             control_x=100, control_y=100,
        ...             dest_x=100, dest_y=50),
        ...     ])
        """
        from apysc._converter.to_apysc_val_from_builtin import \
            get_copied_int_from_builtin_val
        from apysc._geom.path_label import PathLabel
        super(PathBezier3DContinual, self).__init__(
            path_label=PathLabel.BEZIER_3D_CONTINUAL,
            relative=relative)
        self.control_x = get_copied_int_from_builtin_val(
            integer=control_x)
        self.control_y = get_copied_int_from_builtin_val(
            integer=control_y)
        self.dest_x = get_copied_int_from_builtin_val(integer=dest_x)
        self.dest_y = get_copied_int_from_builtin_val(integer=dest_y)

    @add_debug_info_setting(
        module_name=__name__, class_name='PathBezier3DContinual')
    def _get_svg_str(self) -> str:
        """
        Get a path's SVG string created with the current setting.

        Returns
        -------
        svg_str : str
            An SVG path string was created with the
            current setting.
        """
        from apysc._type.value_util import get_value_str_for_expression
        svg_char: String = self._get_svg_char()
        svg_char_str: str = get_value_str_for_expression(
            value=svg_char)
        control_x_str: str = get_value_str_for_expression(
            value=self._control_x)
        control_y_str: str = get_value_str_for_expression(
            value=self._control_y)
        dest_x_str: str = get_value_str_for_expression(value=self._dest_x)
        dest_y_str: str = get_value_str_for_expression(value=self._dest_y)
        svg_str: str = (
            f'{svg_char_str} + String({control_x_str}) '
            f'+ " " + String({control_y_str}) '
            f'+ " " + String({dest_x_str}) '
            f'+ " " + String({dest_y_str})'
        )
        return svg_str

    @add_debug_info_setting(
        module_name=__name__, class_name='PathBezier3DContinual')
    def update_path_data(
            self,
            control_x: Union[int, Int],
            control_y: Union[int, Int],
            dest_x: Union[int, Int],
            dest_y: Union[int, Int],
            *,
            relative: Union[bool, Boolean] = False) -> None:
        """
        Update the path's data settings.

        Parameters
        ----------
        control_x : Int or int
            X-coordinate of the bezier's control point.
        control_y : Int or int
            Y-coordinate of the bezier's control point.
        dest_x : Int or int
            X-coordinate of the destination point.
        dest_y : Int or int
            Y-coordinate of the destination point.
        relative : bool or Boolean, default False
            A boolean value indicates whether the path
            coordinates are relative or not (absolute).

        Examples
        --------
        >>> import apysc as ap
        >>> bezier_3d_continual = ap.PathBezier3DContinual(
        ...     control_x=100, control_y=100,
        ...     dest_x=100, dest_y=50)
        >>> bezier_3d_continual.update_path_data(
        ...     control_x=150, control_y=150,
        ...     dest_x=150, dest_y=100)
        >>> bezier_3d_continual.control_x
        Int(150)

        >>> bezier_3d_continual.control_y
        Int(150)

        >>> bezier_3d_continual.dest_x
        Int(150)

        >>> bezier_3d_continual.dest_y
        Int(100)
        """
        from apysc._converter.to_apysc_val_from_builtin import \
            get_copied_boolean_from_builtin_val
        from apysc._converter.to_apysc_val_from_builtin import \
            get_copied_int_from_builtin_val
        self.control_x = get_copied_int_from_builtin_val(
            integer=control_x)
        self.control_y = get_copied_int_from_builtin_val(
            integer=control_y)
        self.dest_x = get_copied_int_from_builtin_val(integer=dest_x)
        self.dest_y = get_copied_int_from_builtin_val(integer=dest_y)
        self.relative = get_copied_boolean_from_builtin_val(
            bool_val=relative)

    @add_debug_info_setting(
        module_name=__name__, class_name='PathBezier3DContinual')
    def __eq__(self, other: Any) -> Any:
        """
        Equal comparison method.

        Parameters
        ----------
        other : Any
            The other value to compare.

        Returns
        -------
        result : Boolean
            Comparison result.
        """
        import apysc as ap
        if not isinstance(other, PathBezier3DContinual):
            result: ap.Boolean = ap.Boolean(False)
            return result
        return (
            self.control_x == other.control_x
            and self.control_y == other.control_y
            and self.dest_x == other.dest_x
            and self.dest_y == other.dest_y
            and self.relative == other.relative)

    @add_debug_info_setting(
        module_name=__name__, class_name='PathBezier3DContinual')
    def __ne__(self, other: Any) -> Any:
        """
        Not equal comparison method.

        Parameters
        ----------
        other : Any
            The other value to compare.

        Returns
        -------
        result : Boolean
            Comparison result.
        """
        import apysc as ap
        result: ap.Boolean = self == other
        result = result.not_
        return result
