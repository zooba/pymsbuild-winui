from pathlib import Path

class ImageInfo:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def _init_viewmodel(self, view, viewmodel):
        viewmodel.Name = self.name
        viewmodel.Path = str(self.path)


class ImagesRepository:
    def __init__(self):
        self.images = []

    def get_images(self, folder):
        self.images[:] = [ImageInfo(p.name, p) for p in Path(folder).glob("*.jpg")]

    def _init_viewmodel(self, view, viewmodel):
        from _winui_Collections import ObservableVector
        vec = ObservableVector()
        for i in self.images:
            vec.append(view.wrap(i))
        viewmodel.Images = vec
