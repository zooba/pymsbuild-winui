import image_info

from pathlib import Path

SAMPLE_GALLERY = Path(__file__).absolute().parent / "Photos"

class MainWindow:
    def __init__(self, view, viewmodels):
        self.view = view
        self._viewmodels = viewmodels
        #self.view.add_viewmodel(image_info.ImageInfo, viewmodels.ImageInfo)
        #self.view.add_viewmodel(image_info.ImageRepository, viewmodels.ImageRepository)

    # TODO: Move this into the view object and use registrations instead
    def as_viewmodel(self, o):
        if isinstance(o, image_info.ImageInfo):
            return o._as_viewmodel(self, self._viewmodels.ImageInfo)
        if isinstance(o, image_info.ImagesRepository):
            return o._as_viewmodel(self, self._viewmodels.ImageRepository)
        raise TypeError(f"Cannot view {type(o)}")

    def SelectFolderClick(self, sender, e):
        repo = image_info.ImagesRepository()
        repo.get_images(SAMPLE_GALLERY)
        
        self.view.ImagesRepository = self.as_viewmodel(repo)

        self.view.ImageCollectionInfoBar.Message = f"{len(repo.images)} images loaded."
        self.view.ImageCollectionInfoBar.IsOpen = True

    def ImageClick(self, sender, e):
        imageInfo = sender.DataContext
        if isinstance(imageInfo, self.ImageInfo):
            # TODO: Open new window and set content to the image
            self.view.ImageCollectionInfoBar.Message = f"Selected {imageInfo.Name}"
            self.view.ImageCollectionInfoBar.IsOpen = True
        else:
            self.view.ImageCollectionInfoBar.IsOpen = False

    def AboutClick(self, sender, e):
        self.view.show_dialog(
            Title = "About Simple Photo Viewer",
            Content = "Thank you //Build 2022",
            CloseButtonText = "Ok",
            XamlRoot = None #sender.XamlRoot if sender else None
        )

    def OnElementPointerEntered(self, sender, e):
        # TODO: Animation
        pass

    def OnElementPointerExited(self, sender, e):
        # TODO: Animation
        pass
