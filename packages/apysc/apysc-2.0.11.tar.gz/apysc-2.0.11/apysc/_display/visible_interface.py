"""Class implementation for the `visible` interface.
"""

from typing import Dict

from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.attr_linking_interface import AttrLinkingInterface
from apysc._type.boolean import Boolean
from apysc._type.revert_interface import RevertInterface
from apysc._type.variable_name_interface import VariableNameInterface


class VisibleInterface(
        VariableNameInterface, RevertInterface, AttrLinkingInterface):

    _visible: Boolean

    def _initialize_visible_if_not_initialized(self) -> None:
        """
        Initialize _visible attribute if this instance does not
        initialize it yet.
        """
        if hasattr(self, '_visible'):
            return
        self._visible = Boolean(True)

        self._append_visible_attr_linking_setting()

    @add_debug_info_setting(
        module_name=__name__, class_name='VisibleInterface')
    def _append_visible_attr_linking_setting(self) -> None:
        """
        Append a visible attribute linking settings.
        """
        self._append_applying_new_attr_val_exp(
            new_attr=self._visible, attr_name='visible')
        self._append_attr_to_linking_stack(
            attr=self._visible, attr_name='visible')

    @property
    @add_debug_info_setting(
        module_name=__name__, class_name='VisibleInterface')
    def visible(self) -> Boolean:
        """
        Get a visibility value of this instance.

        Returns
        -------
        result : Boolean
            If this instance is visible, this interface returns True.

        Examples
        --------
        >>> import apysc as ap
        >>> stage: ap.Stage = ap.Stage()
        >>> sprite: ap.Sprite = ap.Sprite()
        >>> sprite.graphics.begin_fill(color='#0af')
        >>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(
        ...     x=50, y=50, width=50, height=50)
        >>> rectangle.visible = ap.Boolean(False)
        >>> rectangle.visible
        Boolean(False)
        """
        from apysc._type import value_util
        self._initialize_visible_if_not_initialized()
        return value_util.get_copy(value=self._visible)

    @visible.setter
    def visible(self, value: Boolean) -> None:
        """
        Update a visibility value of this instance.

        Parameters
        ----------
        value : Boolean
            Boolean value to set.
        """
        from apysc._html.debug_mode import DebugInfo
        with DebugInfo(
                callable_='visible', args=[value], kwargs={},
                module_name=__name__,
                class_name=VisibleInterface.__name__):
            import apysc as ap
            from apysc._validation import bool_validation
            bool_validation.validate_bool(value=value)
            if isinstance(value, bool):
                value = ap.Boolean(value)
            self._visible = value
            self._append_visible_update_expression()

            self._append_visible_attr_linking_setting()

    @add_debug_info_setting(
        module_name=__name__, class_name='VisibleInterface')
    def _append_visible_update_expression(self) -> None:
        """
        Append visible property updating expression.
        """
        import apysc as ap
        expression: str = (
            f'if ({self._visible.variable_name}) {{'
            f'\n  {self.variable_name}.show();'
            '\n}else {'
            f'\n  {self.variable_name}.hide();'
            '\n}'
        )
        ap.append_js_expression(expression=expression)

    _visible_snapshots: Dict[str, bool]

    def _make_snapshot(self, *, snapshot_name: str) -> None:
        """
        Make value's snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self._initialize_visible_if_not_initialized()
        self._set_single_snapshot_val_to_dict(
            dict_name='_visible_snapshots',
            value=self._visible._value, snapshot_name=snapshot_name)

    def _revert(self, *, snapshot_name: str) -> None:
        """
        Revert value is snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self._visible._value = self._visible_snapshots[snapshot_name]
