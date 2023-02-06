from framework import Canvas, Context, Scene
from color import White


class MainMenu(Scene):
    def on_render(self, canvas: Canvas) -> None:
        canvas.print(x=0, y=0, string="HALLO", fg=White)

    def listen(self, context: Context):
        super().listen(context)


