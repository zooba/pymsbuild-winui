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
        from _winui_Collections import ObservableVector
        vec = ObservableVector()
        for i in self.images:
            vec.append(view.as_viewmodel(i))
        r.Images = vec
        return r
