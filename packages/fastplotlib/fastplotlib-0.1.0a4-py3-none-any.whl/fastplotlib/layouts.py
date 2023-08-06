from itertools import product
from functools import partial
import numpy as np
import pygfx
from .defaults import camera_types, controller_types
from .subplot import Subplot
from typing import *
from wgpu.gui.auto import WgpuCanvas


def _produce_rect(j, i, ncols, nrows, w, h):
    return [
        ((w / ncols) + ((i - 1) * (w / ncols))),
        ((h / nrows) + ((j - 1) * (h / nrows))),
        (w / ncols),
        (h / nrows)
    ]


class GridPlot:
    def __init__(
            self,
            shape: Tuple[int, int],
            cameras: Union[np.ndarray, str] = '2d',
            controllers: np.ndarray = None,
            canvas: WgpuCanvas = None,
            renderer: pygfx.Renderer = None,
    ):
        """
        Parameters
        ----------
        shape:
            nrows, ncols

        cameras: Union[np.ndarray, str]
            One of ``"2d"`` or ``"3d"`` indicating 2D or 3D plots

            OR

            Array of ``2d`` and/or ``3d`` that specifies camera type for each subplot:
            ``2d``: ``pygfx.OrthographicCamera``
            ``3d``: ``pygfx.PerspectiveCamera``

        controllers: np.ndarray
            numpy array of same shape as ``grid_shape`` that defines the controllers
            Example:
            unique controllers for a 2x2 gridplot: np.array([[0, 1], [2, 3]])
            same controllers for first 2 plots: np.array([[0, 0, 1], [2, 3, 4]])

        canvas: WgpuCanvas
            Canvas for drawing

        renderer: pygfx.Renderer
            pygfx renderer instance
        """

        if type(cameras) is str:
            if cameras not in ["2d", "3d"]:
                raise ValueError("If passing a str, `views` must be one of `2d` or `3d`")
            # create the array representing the views for each subplot in the grid
            cameras = np.array([cameras] * shape[0] * shape[1]).reshape(shape)

        if controllers is None:
            controllers = np.arange(shape[0] * shape[1]).reshape(shape)

        if controllers.shape != shape:
            raise ValueError

        if cameras.shape != shape:
            raise ValueError

        if not np.all(np.sort(np.unique(controllers)) == np.arange(np.unique(controllers).size)):
            raise ValueError("controllers must be consecutive integers")

        if canvas is None:
            canvas = WgpuCanvas()

        if renderer is None:
            renderer = pygfx.renderers.WgpuRenderer(canvas)

        self.canvas = canvas
        self.renderer = renderer

        self.shape = shape
        nrows, ncols = self.shape

        self.subplots: np.ndarray[Subplot] = np.ndarray(shape=(nrows, ncols), dtype=object)
        # self.viewports: np.ndarray[Subplot] = np.ndarray(shape=(nrows, ncols), dtype=object)

        self._controllers: List[pygfx.PanZoomController] = [
            pygfx.PanZoomController() for i in range(np.unique(controllers).size)
        ]

        self._controllers = np.empty(shape=cameras.shape, dtype=object)

        for controller in np.unique(controllers):
            cam = np.unique(cameras[controllers == controller])
            if cam.size > 1:
                raise ValueError(f"Controller id: {controller} has been assigned to multiple different camera types")

            self._controllers[controllers == controller] = controller_types[cam[0]]()

        for i, j in self._get_iterator():
            position = (i, j)
            camera = cameras[i, j]
            controller = self._controllers[i, j]

            self.subplots[i, j] = Subplot(
                position=position,
                parent_dims=(nrows, ncols),
                camera=camera,
                controller=controller,
                canvas=canvas,
                renderer=renderer
            )

        self._animate_funcs: List[callable] = list()
        self._current_iter = None

    def animate(self):
        for subplot in self:
            subplot.animate(self.canvas.get_logical_size())

        for f in self._animate_funcs:
            f()

        self.renderer.flush()
        self.canvas.request_draw()

    def add_animations(self, funcs: List[callable]):
        self._animate_funcs += funcs

    def show(self):
        self.canvas.request_draw(self.animate)
        return self.canvas

    def _get_iterator(self):
        return product(range(self.shape[0]), range(self.shape[1]))

    def __iter__(self):
        self._current_iter = self._get_iterator()
        return self

    def __next__(self) -> Subplot:
        pos = self._current_iter.__next__()
        return self.subplots[pos]
