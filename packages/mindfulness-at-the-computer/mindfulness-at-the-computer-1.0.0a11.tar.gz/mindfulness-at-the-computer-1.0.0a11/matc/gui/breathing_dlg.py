import enum
import logging
import math
import random
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
import matc.constants
import matc.globa
import matc.settings

WINDOW_FLAGS = (QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
"""
Other flags:
* QtCore.Qt.WindowDoesNotAcceptFocus - With this it seems we don't capture keyboard events
* QtCore.Qt.BypassWindowManagerHint - With this we won't see a placement in the activity panel
"""
DLG_WIDTH = 570
DLG_HEIGHT = 290
DLG_CORNER_RADIUS = 40
DLG_BOTTOM_MARGINAL = 50

CLOSE_DIALOG_DURATION = 2500
CLOSE_DIALOG_RANGE = 250
TIME_NOT_SET_FT = 0.0
TIME_LINE_IB_DURATION_INT = 8000
TIME_LINE_OB_DURATION_INT = 16000
TIME_LINE_DOT_DURATION_INT = 1000
TIME_LINE_IB_FRAME_RANGE_INT = 1000
TIME_LINE_OB_FRAME_RANGE_INT = 2000
TIME_LINE_IB_DOT_FRAME_RANGE_INT = 255

DOT_RADIUS_FT = 7
DOT_SPACING = 3

HELP_TEXTS=[
    "You can press and hold the (left or right) shift key while breathing in and letting it be while breathing out",
    "Please practice natural breathing and accept your breathing as it is: Do not force it to be longer",
    "Your breath is a bridge between your mind and body",
]
"""
"Stomach breathing",
"body awareness",
"present moment",
"""


class CursorPosition(enum.Enum):
    inner = enum.auto()
    outside = enum.auto()


class BreathingState(enum.Enum):
    inactive = 0
    breathing_in = 1
    breathing_out = 2


class BreathingGraphicsView(QtWidgets.QGraphicsView):
    """
    Explanation of the how coordinates work:
    https://forum.qt.io/topic/106003/how-to-seamlessly-place-item-into-scene-at-specific-location-adding-qgraphicsitem-to-scene-always-places-it-at-0-0/2
    """
    close_signal = QtCore.Signal()
    first_breathing_gi_signal = QtCore.Signal()

    # Also contains the graphics scene
    def __init__(self, i_can_be_closed: bool = True) -> None:
        super().__init__()
        self.is_first_time_opened = True
        self.active_bv_go = None
        self.is_first_time_shown: bool = True
        self.breathing_state = BreathingState.inactive
        self._can_be_closed_bool = i_can_be_closed
        self._keyboard_active_bool = True

        # Window setup
        self.setWindowFlags(WINDOW_FLAGS)
        self.setWindowTitle(f"Breathing Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")
        self.setWindowIcon(QtGui.QIcon(matc.globa.get_app_icon_path("icon.png")))
        self.setStyleSheet(f"background-color: {matc.globa.BLACK_COLOR};")
        """
        Border:
        self.setStyleSheet(f"background-color: {matc.globa.BLACK_COLOR}; border: 8px solid {matc.globa.GRAY_COLOR}; border-radius: {CORNER_RADIUS+0}")
        Reference: https://doc.qt.io/qt-5/stylesheet-reference.html#border-prop
        Reference: https://doc.qt.io/qt-5/qframe.html#frameWidth-prop
        """
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setFixedWidth(DLG_WIDTH)
        self.setFixedHeight(DLG_HEIGHT)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # ..set position
        screen_qrect = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self._xpos_int = screen_qrect.left() + (screen_qrect.width() - DLG_WIDTH) // 2
        self._ypos_int = screen_qrect.bottom() - DLG_HEIGHT - 60
        # -self.sizeHint().height() gives only 52 here, unknown why, so we use WIN_HEIGHT instead
        self.move(self._xpos_int, self._ypos_int)
        # ..rounding corners
        painter_path_mask = QtGui.QPainterPath()
        painter_path_mask.addRoundedRect(self.rect(), DLG_CORNER_RADIUS, DLG_CORNER_RADIUS)
        polygon_mask = painter_path_mask.toFillPolygon().toPolygon()
        # -.toPolygon converts from QPolygonF to QPolygon
        region_mask = QtGui.QRegion(polygon_mask)
        self.setMask(region_mask)
        # ..close dialog fade out animation
        self.close_dialog_qtimeline = QtCore.QTimeLine(duration=CLOSE_DIALOG_DURATION)
        self.close_dialog_qtimeline.setFrameRange(1, CLOSE_DIALOG_RANGE)
        self.close_dialog_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.close_dialog_qtimeline.frameChanged.connect(self.on_close_dialog_frame_changed)
        self.close_dialog_qtimeline.finished.connect(self.on_close_dialog_qtimeline_finished)

        # Graphics and layout setup..
        # ..graphics scene
        self._graphics_scene = QtWidgets.QGraphicsScene()
        self._graphics_scene.setSceneRect(QtCore.QRectF(0, 0, DLG_WIDTH, DLG_HEIGHT))
        self.setScene(self._graphics_scene)
        # ..dots
        # self.breathing_count = 0
        self.br_dots_gi_list = []
        self.dot_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_DOT_DURATION_INT)
        self.dot_qtimeline.setFrameRange(1, TIME_LINE_IB_DOT_FRAME_RANGE_INT)
        # self.dot_qtimeline.setCurveShape(QtCore.QTimeLine.EaseOutCurve)
        # self.dot_qtimeline.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        self.dot_qtimeline.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.dot_qtimeline.frameChanged.connect(self.on_dot_frame_change)
        # ..help text
        self.help_text_gi = GraphicsTextItem()
        self._graphics_scene.addItem(self.help_text_gi)
        # ..text
        self.breathing_phrase = None
        self.br_text_gi = GraphicsTextItem()
        # self.br_text_gi.position_signal.connect(self.on_br_text_position_changed)
        # self.br_text_gi.setAcceptHoverEvents(False)
        self._graphics_scene.addItem(self.br_text_gi)
        # ..central line
        self.central_line_gi = CentralLineQgi()
        self.central_line_gi.hide()
        self._graphics_scene.addItem(self.central_line_gi)

        # Animation time for the custom dynamic breathing graphics
        self.ib_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_IB_DURATION_INT)
        self.ib_qtimeline.setFrameRange(1, TIME_LINE_IB_FRAME_RANGE_INT)
        self.ib_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.ib_qtimeline.frameChanged.connect(self.on_frame_change_breathing_in)
        self.ob_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_OB_DURATION_INT)
        self.ob_qtimeline.setFrameRange(1, TIME_LINE_OB_FRAME_RANGE_INT)
        self.ob_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.ob_qtimeline.frameChanged.connect(self.on_frame_change_breathing_out)

    def minimumSizeHint(self) -> QtCore.QSize:
        size_ = QtCore.QSize(DLG_WIDTH, DLG_HEIGHT)
        return size_

    def minimumHeight(self) -> int:
        return DLG_HEIGHT

    def sizeHint(self) -> QtCore.QSize:
        size_ = QtCore.QSize(DLG_WIDTH, DLG_HEIGHT)
        return size_

    def close_dlg(self):
        # self.showNormal()
        # -for MacOS. showNormal is used here rather than showMinimized to avoid animation
        self.close_dialog_qtimeline.stop()
        self.ib_qtimeline.stop()
        self.ob_qtimeline.stop()
        self.hide()
        self.close_signal.emit()

    def on_close_dialog_qtimeline_finished(self):
        self.close_dlg()

    def on_close_dialog_frame_changed(self, i_frame_nr: int):
        opacity = 1.0 - i_frame_nr / CLOSE_DIALOG_RANGE
        self.setWindowOpacity(opacity)
        self.update()

    def show(self):
        raise Exception("Call not supported, please call the function in super class instead, or use initiate")

    def show_breathing_dlg(self):
        screen_qrect = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        _xpos_int = screen_qrect.left() + (screen_qrect.width() - DLG_WIDTH) // 2
        _ypos_int = screen_qrect.bottom() - DLG_HEIGHT - DLG_BOTTOM_MARGINAL
        # -self.sizeHint().height() gives only 52 here, unknown why, so we use VIEW_HEIGHT_INT instead
        self.move(_xpos_int, _ypos_int)
        self.close_dlg()
        self.showNormal()
        self.initiate_breathing_gv()  # -continuing the setup

    def initiate_breathing_gv(self, i_br_vis: int = -1):
        """
        If the user opens the breathing dialog, this function is called from show_breathing_dlg. It is also be called
        when generating preview images for the settings dialog, and when showing the (interactive) breathing dialog
        inside the intro dialog
        """
        super().show()
        self.setWindowOpacity(1)
        self.breathing_state = BreathingState.inactive
        move_mouse_cursor: bool = matc.settings.settings[matc.settings.SK_MOVE_MOUSE_CURSOR]
        if move_mouse_cursor and not self.is_first_time_shown and i_br_vis == -1:
            screen_point = self.mapToGlobal(QtCore.QPoint(DLG_WIDTH - 75, DLG_HEIGHT // 2 + 20))
            screen = QtGui.QGuiApplication.primaryScreen()
            mouse_cursor = QtGui.QCursor()
            mouse_cursor.setPos(screen, screen_point)
            # https://doc.qt.io/qt-5/qcursor.html#setPos-1

        # self.breathing_count = 0
        for br_dot in self.br_dots_gi_list:
            self._graphics_scene.removeItem(br_dot)
        self.br_dots_gi_list.clear()

        ####################################################################################

        if i_br_vis == -1:
            self.br_vis_id: int = matc.settings.settings[matc.settings.SK_BREATHING_VISUALIZATION]
            # -important that this setting is read here and stored, because we want to maintain the behaviour
            # if the user should happen to change the settings while the breathing dialog is visible
        else:
            self.br_vis_id = i_br_vis

        if self.active_bv_go:
            self._graphics_scene.removeItem(self.active_bv_go)

        if self.br_vis_id == matc.globa.BreathingVisalization.bar.value:
            self.active_bv_go = BreathingBarQgo()
        elif self.br_vis_id == matc.globa.BreathingVisalization.circle.value:
            self.active_bv_go = BreathingCircleQgo()
        elif self.br_vis_id == matc.globa.BreathingVisalization.line.value:
            self.active_bv_go = BreathingLineQgo()
        elif self.br_vis_id == matc.globa.BreathingVisalization.columns.value:
            self.active_bv_go = BreathingColumnRootQgo()
        else:
            raise Exception("Case not covered")
        self._graphics_scene.addItem(self.active_bv_go)
        self.active_bv_go.show()
        self.active_bv_go.update_pos_and_origin_point()
        self.active_bv_go.position_signal.connect(self._breathing_gi_position_changed)

        if matc.globa.active_phrase_id == matc.globa.BREATHING_PHRASE_NOT_SET:
            self.breathing_phrase = matc.settings.get_topmost_breathing_phrase()
            matc.globa.active_phrase_id = self.breathing_phrase.id
        self.breathing_phrase = matc.settings.get_breathing_phrase(matc.globa.active_phrase_id)

        help_text_x = DLG_WIDTH / 2 - self.help_text_gi.boundingRect().width() / 2
        help_text_pointf = QtCore.QPointF(help_text_x, 10)
        self.help_text_gi.setPos(help_text_pointf)
        self.help_text_gi.show()

        if self.is_first_time_shown:
            help_text_str = self.active_bv_go.get_help_text()
        else:
            help_text_str = random.choice(HELP_TEXTS)
        self.help_text_gi.set_text(help_text_str)

        self.br_text_gi.setHtml(self._get_ib_ob_html())
        text_pointf = QtCore.QPointF(
            DLG_WIDTH / 2 - self.br_text_gi.boundingRect().width() / 2,
            DLG_HEIGHT - self.br_text_gi.boundingRect().height() - 10
        )
        if self.br_vis_id == matc.globa.BreathingVisalization.line.value:
            text_pointf.setY(DLG_HEIGHT / 2 - self.br_text_gi.boundingRect().height() / 2)
            self.central_line_gi.show()
        elif self.br_vis_id == matc.globa.BreathingVisalization.columns.value:
            self.central_line_gi.show()
        else:
            self.central_line_gi.hide()
        self.br_text_gi.setPos(text_pointf)

        self.is_first_time_shown = False

    @staticmethod
    def get_preview_bitmaps():
        ret_dict = {}
        br_gv = BreathingGraphicsView()
        for i in matc.globa.BreathingVisalization:
            i_val = i.value
            br_gv.initiate_breathing_gv(i_val)
            br_pixmap = br_gv.grab()
            br_new_size = QtCore.QSize(br_pixmap.width() // 2, br_pixmap.height() // 2)
            br_resized_pixmap = br_pixmap.scaled(br_new_size)
            ret_dict[i_val] = br_resized_pixmap
        return ret_dict

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        event.accept()
        if self._can_be_closed_bool:
            self.close_dlg()

    def leaveEvent(self, i_qevent) -> None:
        if self._can_be_closed_bool:
            self.close_dialog_qtimeline.start()

    def enterEvent(self, i_qevent) -> None:
        self.setWindowOpacity(1)
        self.close_dialog_qtimeline.stop()

    def mouseMoveEvent(self, i_mouse_event: QtGui.QMouseEvent) -> None:
        vis_te = (matc.globa.BreathingVisalization.columns.value, matc.globa.BreathingVisalization.line.value)
        if self.br_vis_id in vis_te:
            if i_mouse_event.y() < DLG_HEIGHT // 2:
                self._start_breathing_in()
            else:
                self._start_breathing_out()
        super().mouseMoveEvent(i_mouse_event)

    def _get_ib_ob_html(self, i_ib_focus: bool = False, i_ob_focus: bool = False) -> str:
        margin=0
        if self.br_vis_id == matc.globa.BreathingVisalization.line.value:
            margin=8
        ib_html = matc.globa.get_html(i_text=self.breathing_phrase.in_breath, i_focus=i_ib_focus, i_margin=margin)
        ob_html = matc.globa.get_html(i_text=self.breathing_phrase.out_breath, i_focus=i_ob_focus, i_margin=margin)
        return ib_html + ob_html

    def _start_breathing_in(self) -> None:
        if self.breathing_state == BreathingState.breathing_in:
            return
        self.breathing_state = BreathingState.breathing_in

        self.on_dot_frame_change(TIME_LINE_IB_DOT_FRAME_RANGE_INT)
        br_dots_gi = DotQgo(len(self.br_dots_gi_list))
        self.br_dots_gi_list.append(br_dots_gi)
        self._graphics_scene.addItem(br_dots_gi)
        # br_dots_gi.show()
        for br_dot in self.br_dots_gi_list:
            br_dot.update_pos(len(self.br_dots_gi_list))

        if len(self.br_dots_gi_list) == 1:
            self.first_breathing_gi_signal.emit()

        self.help_text_gi.hide()
        self.br_text_gi.setHtml(self._get_ib_ob_html(i_ib_focus=True))
        self.ob_qtimeline.stop()
        self.ib_qtimeline.start()
        self.dot_qtimeline.stop()
        self.dot_qtimeline.start()

        self.active_bv_go.start_breathing_in()

    def _start_breathing_out(self) -> None:
        if self.breathing_state != BreathingState.breathing_in:
            return
        self.breathing_state = BreathingState.breathing_out

        self.active_bv_go._peak_width_ft = self.active_bv_go.rectf.width()

        self.br_text_gi.setHtml(self._get_ib_ob_html(i_ob_focus=True))
        self.ib_qtimeline.stop()
        self.ob_qtimeline.start()

        self.active_bv_go.start_breathing_out()

    def keyPressEvent(self, i_qkeyevent) -> None:
        if self._keyboard_active_bool:
            if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
                logging.debug("shift key pressed")
                self._start_breathing_in()
            elif i_qkeyevent.key() == QtCore.Qt.Key_Return:
                logging.debug("return key pressed")
                self.close_dlg()

    def keyReleaseEvent(self, i_qkeyevent) -> None:
        if self._keyboard_active_bool:
            if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
                logging.debug("shift key released")
                self._start_breathing_out()

    def _breathing_gi_position_changed(self, i_pos_type: int) -> None:
        if i_pos_type == CursorPosition.inner.value:
            self._start_breathing_in()
        elif i_pos_type == CursorPosition.outside.value:
            self._start_breathing_out()

    def on_frame_change_breathing_in(self, i_frame_nr: int) -> None:
        self.active_bv_go.change_size_br_in(i_frame_nr)

    def on_frame_change_breathing_out(self, i_frame_nr: int) -> None:
        self.active_bv_go.change_size_br_out(i_frame_nr)

    def on_dot_frame_change(self, i_frame_nr: int) -> None:
        if len(self.br_dots_gi_list) <= 0:
            return
        last_dot_git: DotQgo = self.br_dots_gi_list[-1]
        last_dot_git.color.setAlpha(i_frame_nr)
        last_dot_git.update()


class GraphicsTextItem(QtWidgets.QGraphicsTextItem):
    position_signal = QtCore.Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.setDefaultTextColor(QtGui.QColor(matc.globa.DARKER_GREEN_COLOR))
        self.setTextWidth(DLG_WIDTH - 20)

    def set_text(self, i_text: str):
        html_string = matc.globa.get_html(i_text)
        self.setHtml(html_string)


class DotQgo(QtWidgets.QGraphicsObject):
    def __init__(self, i_number: int):
        super().__init__()
        self.number = i_number  # -starts at 0
        self.rectf = QtCore.QRectF(0, 0, 2*DOT_RADIUS_FT, 2*DOT_RADIUS_FT)
        self.setAcceptHoverEvents(False)
        self.color = QtGui.QColor(matc.globa.LIGHT_GREEN_COLOR)
        self.color.setAlpha(0)

    def boundingRect(self):
        return self.rectf

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        t_brush = QtGui.QBrush(self.color)
        i_qpainter.setBrush(t_brush)
        pen = QtGui.QPen()
        pen.setWidth(0)
        i_qpainter.setPen(pen)
        i_qpainter.drawEllipse(self.rectf)

    def update_pos(self, i_total_nr: int) -> None:
        x_delta = (self.number + 0.5 - i_total_nr / 2) * (self.boundingRect().width() + DOT_SPACING)
        x: float = DLG_WIDTH / 2 - self.boundingRect().width() / 2 + x_delta
        y: float = self.boundingRect().height()
        self.setPos(QtCore.QPointF(x, y))


class BreathingQgo(QtWidgets.QGraphicsObject):
    """
    > The QGraphicsObject class provides a base class for all graphics items that require signals,
    slots and properties.
    https://doc.qt.io/qt-5/qgraphicsobject.html

    """
    position_signal = QtCore.Signal(int)

    def change_size_br_in(self, i_frame_nr: int):
        pass

    def change_size_br_out(self, i_frame_nr: int):
        pass

    def start_breathing_in(self):
        pass

    def start_breathing_out(self):
        pass

    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF()
        self.setAcceptHoverEvents(True)
        self._peak_width_ft = 90

    def get_help_text(self) -> str:
        raise NotImplementedError

    def boundingRect(self):
        return self.rectf

    def update_pos_and_origin_point(self) -> None:
        x: float = DLG_WIDTH / 2 - self.boundingRect().width() / 2
        y: float = DLG_HEIGHT / 2 - self.boundingRect().height() / 2
        self.setPos(QtCore.QPointF(x, y))
        self.setTransformOriginPoint(self.boundingRect().center())

    def hoverLeaveEvent(self, i_qgraphicsscenehoverevent) -> None:
        # Please note that this function is entered in case the user hovers over something
        #  on top of this graphics item
        self.position_signal.emit(CursorPosition.outside.value)

    def hoverMoveEvent(self, i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        pass


class BreathingColumnRootQgo(BreathingQgo):
    def __init__(self):
        super().__init__()
        # self.counter = 0
        self.co_refs = []
        # -to avoid intermittent segmentation fault errors we have to store references in Python

    def update_pos_and_origin_point(self) -> None:
        if len(self.childItems()) < 1:
            x: float = DLG_WIDTH / 2
        else:
            last_child_go = self.childItems()[-1]
            width = last_child_go.x()+last_child_go.boundingRect().width()
            x: float = DLG_WIDTH / 2 - width / 2
        self.setX(x)

    def get_help_text(self) -> str:
        return "Hover over the upper half breathing in, and over the lower half breathing out"

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        pass

    def start_breathing_in(self):
        new_child_go = BreathingColumnQgo(len(self.co_refs), i_is_ib=True)
        self.co_refs.append(new_child_go)
        new_child_go.setParentItem(self)

        new_child_go.update_pos_and_origin_point()
        self.update_pos_and_origin_point()

    def start_breathing_out(self):
        new_child_go = BreathingColumnQgo(len(self.co_refs), i_is_ib=False)
        self.co_refs.append(new_child_go)
        new_child_go.setParentItem(self)

    def change_size_br_in(self, i_frame_nr: int):
        if len(self.childItems()) < 1:
            return
        last_child_go = self.childItems()[-1]
        new_height_ft = 0.1 * i_frame_nr
        old_height_ft = last_child_go.rectf.height()
        if new_height_ft < old_height_ft:
            new_height_ft = old_height_ft
        last_child_go.rectf.setHeight(new_height_ft)
        last_child_go.update_pos_and_origin_point()

    def change_size_br_out(self, i_frame_nr: int):
        new_height_ft = 0.1 * i_frame_nr
        last_child_go = self.childItems()[-1]
        old_height_ft = last_child_go.rectf.height()
        if new_height_ft < old_height_ft:
            new_height_ft = old_height_ft
        last_child_go.rectf.setHeight(new_height_ft)
        last_child_go.update_pos_and_origin_point()

    def __del__(self):
        logging.debug("BreathingColumnRootQgo destructor - dereferencing and deleting child items")
        for child_item in self.childItems():
            child_item.setParentItem(None)
            del child_item


class BreathingColumnQgo(BreathingQgo):
    COL_WIDTH = 50

    def __init__(self, i_number: int, i_is_ib: bool = True):
        super().__init__()
        self.rectf = QtCore.QRectF(0, 0, self.COL_WIDTH, 0)
        self.number = i_number
        self.is_ib: bool = i_is_ib

    def get_help_text(self) -> str:
        return ""

    def update_pos_and_origin_point(self) -> None:
        x: float = (self.number // 2) * (5 + self.rectf.width())
        if self.is_ib:
            y: float = DLG_HEIGHT / 2 - self.rectf.height()
        else:
            y: float = DLG_HEIGHT / 2
        self.setPos(QtCore.QPointF(x, y))
        self.setTransformOriginPoint(DLG_WIDTH / 2, DLG_HEIGHT / 2)

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        if self.is_ib:
            color_ = QtGui.QColor(matc.globa.LIGHT_GREEN_COLOR)
        else:
            color_ = QtGui.QColor(matc.globa.DARK_GREEN_COLOR)
        t_brush = QtGui.QBrush(color_)
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawRect(self.rectf)


class BreathingCircleQgo(BreathingQgo):
    """
    breathing in: ignoring the state of the circle, instead using the same starting state
    breathing out: using the state of the circle
    """
    CIRCLE_RADIUS_FT = 45.0

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(
            0, 0,
            2 * self.CIRCLE_RADIUS_FT, 2 * self.CIRCLE_RADIUS_FT
        )

    def get_help_text(self) -> str:
        return "Hover over the green area breathing in, and outside the green area breathing out"

    def change_size_br_in(self, i_frame_nr: int):
        new_width_ft = 2 * self.CIRCLE_RADIUS_FT + 0.1 * i_frame_nr
        self.rectf.setWidth(new_width_ft)
        self.rectf.setHeight(new_width_ft)
        self.update_pos_and_origin_point()

    def change_size_br_out(self, i_frame_nr: int):
        new_width_ft = self._peak_width_ft - 0.06 * i_frame_nr
        if new_width_ft < 2 * self.CIRCLE_RADIUS_FT:
            new_width_ft = 2 * self.CIRCLE_RADIUS_FT
        self.rectf.setWidth(new_width_ft)
        self.rectf.setHeight(new_width_ft)
        self.update_pos_and_origin_point()

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        # i_qpainter.fillRect(self.rectf, t_brush)
        t_brush = QtGui.QBrush(QtGui.QColor(matc.globa.LIGHT_GREEN_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawEllipse(self.rectf)

    # Overridden
    def hoverMoveEvent(self, i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        # self.hover_signal.emit()

        cposx = self.boundingRect().center().x()
        cposy = self.boundingRect().center().y()
        # logging.debug(f"{cposy=}")
        pposx = i_qgraphicsscenehoverevent.pos().x()
        pposy = i_qgraphicsscenehoverevent.pos().y()
        # logging.debug(f"{pposy=}")

        distance_from_center: float = math.dist([0, 0], [pposx-cposx, pposy-cposy])
        # logging.debug(f"{distance_from_center=}")

        if distance_from_center < self.CIRCLE_RADIUS_FT:
            self.position_signal.emit(CursorPosition.inner.value)
        elif distance_from_center > self.rectf.width() // 2:
            self.position_signal.emit(CursorPosition.outside.value)


class BreathingBarQgo(BreathingQgo):
    WIDTH = 140.0
    HEIGHT = 50.0
    CORNER_RADIUS = 5

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def get_help_text(self) -> str:
        return "Hover over the green area breathing in, and outside the green area breathing out"

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        # i_qpainter.fillRect(self.rectf, t_brush)
        t_brush = QtGui.QBrush(QtGui.QColor(matc.globa.LIGHT_GREEN_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawRoundedRect(self.rectf, self.CORNER_RADIUS, self.CORNER_RADIUS)

    def change_size_br_in(self, i_frame_nr: int):
        new_width_ft = self.WIDTH + 0.2 * i_frame_nr
        self.rectf.setWidth(new_width_ft)
        self.update_pos_and_origin_point()

    def change_size_br_out(self, i_frame_nr: int):
        new_width_ft = self._peak_width_ft - 0.12 * i_frame_nr
        if new_width_ft < self.WIDTH:
            new_width_ft = self.WIDTH
        self.rectf.setWidth(new_width_ft)
        self.update_pos_and_origin_point()

    # Overridden
    def hoverMoveEvent(self, i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self.position_signal.emit(CursorPosition.inner.value)


class BreathingLineQgo(BreathingQgo):
    WIDTH = 120.0
    HEIGHT = 3

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def get_help_text(self) -> str:
        return "Hover over the upper half breathing in, and over the lower half breathing out"

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        t_brush = QtGui.QBrush(QtGui.QColor(matc.globa.WHITE_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawRoundedRect(self.rectf, 5, 5)

    def change_size_br_in(self, i_frame_nr: int):
        new_width_ft = self.WIDTH + 0.2 * i_frame_nr
        self.rectf.setWidth(new_width_ft)
        self.update_pos_and_origin_point()

    def change_size_br_out(self, i_frame_nr: int):
        new_width_ft = self._peak_width_ft - 0.12 * i_frame_nr
        if new_width_ft < self.WIDTH:
            new_width_ft = self.WIDTH
        self.rectf.setWidth(new_width_ft)
        self.update_pos_and_origin_point()


class CentralLineQgi(QtWidgets.QGraphicsItem):
    """
    Please note: We have to implement boundingRect() and paint(), when subclassing QGraphicsItem (or QGraphicsObject)
    otherwise we will get a SIGSEGV error

    > To write your own graphics item, you first create a subclass of QGraphicsItem, and then start by implementing its
    > two pure virtual public functions: boundingRect(), which returns an estimate of the area painted by the item, and
    > paint(), which implements the actual painting.

    https://doc.qt.io/qt-6/qgraphicsitem.html#details
    """
    def __init__(self):
        super().__init__()
        line_height = 2
        y = (DLG_HEIGHT - line_height) // 2
        self.rectf = QtCore.QRectF(0, y, DLG_WIDTH, line_height)

    def boundingRect(self):
        return self.rectf

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        t_brush = QtGui.QBrush(QtGui.QColor(matc.globa.DARK_GREEN_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawRect(self.rectf)


if __name__ == "__main__":
    import sys
    matc_qapplication = QtWidgets.QApplication(sys.argv)
    bgv = BreathingGraphicsView()
    bgv.setWindowFlags(WINDOW_FLAGS)
    bgv.show_breathing_dlg()
    matc_qapplication.exec()
