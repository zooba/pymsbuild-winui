import image_info

from pathlib import Path

SAMPLE_GALLERY = Path(__file__).absolute().parent / "Photos"

class MainWindow:
    def __init__(self, view, viewmodels):
        self.view = view
        self.view.add_viewmodel(image_info.ImageInfo, viewmodels.ImageInfo)
        self.view.add_viewmodel(image_info.ImagesRepository, viewmodels.ImageRepository)

    def SelectFolderClick(self, sender, e):
        repo = image_info.ImagesRepository()
        repo.get_images(SAMPLE_GALLERY)
        
        self.view.ImagesRepository = self.view.as_viewmodel(repo)

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
        op = self.view.AboutDialog.ShowAsync()
        def update_bar(status):
            self.view.ImageCollectionInfoBar.Message = f"Status {status}"
            self.view.ImageCollectionInfoBar.IsOpen = True
        op.Completed(update_bar)

    def OnElementPointerEntered(self, sender, e):
        # TODO: Animation
        pass

    def OnElementPointerExited(self, sender, e):
        # TODO: Animation
        pass
