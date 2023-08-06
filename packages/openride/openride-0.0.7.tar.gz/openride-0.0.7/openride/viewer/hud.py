import time
import vtk



class Hud:

    def __init__(self, viewer, position=(0,0)):

        self.viewer = viewer
        self.position = position
        self.time = time.time()
        self._elements = {}

        self.text = vtk.vtkTextActor()
        self.text.SetPosition(self.position[0], self.position[1])
        self.text.GetTextProperty().SetFontSize(16)
        self.viewer.renderer.AddActor(self.text)

        self.fps_count:bool = False
        self.cursor_position:bool = False


    def update(self):
        if self.fps_count: self.add('fps', int(1/(time.time() - self.time)))
        if self.cursor_position: self.add('cursor', self.viewer.interactor.get_cursor_in_world())
        text = ''
        for element in self._elements:
            text += f'{element}: {str(self._elements[element])}\n'
        self.text.SetInput(text)
        self.time = time.time()


    def toggle_fps_count(self):
        self.fps_count = not self.fps_count


    def toggle_cursor_position(self):
        self.cursor_position = not self.cursor_position


    def add(self, name, value):
        self._elements[name] = value