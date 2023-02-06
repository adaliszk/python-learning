class Screen:
    _padding: int = 4
    _height: int
    _width: int

    def __init__(self, width: int, height: int):
        self._height = height
        self._width = width

    @property
    def padding(self):
        return self._padding

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def inner_height(self):
        return self._height - self._padding * 2 - 1

    @property
    def inner_width(self):
        return self._width - self._padding * 2 - 1

    @property
    def inner_left(self):
        return self._padding

    @property
    def inner_top(self):
        return self._padding

    @property
    def inner_right(self):
        return self.inner_left + self.inner_width

    @property
    def inner_bottom(self):
        return self.inner_top + self.inner_height
