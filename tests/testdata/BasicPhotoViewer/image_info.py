from pathlib import Path

class ImageInfo:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def _as_viewmodel(self, view, view_cls):
        r = view_cls()
        r.Name = self.name
        r.Path = str(self.path)
        return r


class ImagesRepository:
    def __init__(self):
        self.images = []

    def get_images(self, folder):
        self.images[:] = [ImageInfo(p.name, p) for p in Path(folder).glob("*.jpg")]

    def _as_viewmodel(self, view, view_cls):
        r = view_cls()
        # TODO: Observable
        r.Images = [view.as_viewmodel(i) for i in self.images]
        return r
