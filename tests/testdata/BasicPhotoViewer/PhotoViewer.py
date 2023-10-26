import image_info

from pathlib import Path

SAMPLE_GALLERY = Path(__file__).absolute().parent / "Photos"

class MainWindow:
    def __init__(self, view, viewmodels):
        self.view = view
        self.view.models[image_info.ImageInfo] = viewmodels.ImageInfo
        self.view.models[image_info.ImagesRepository] = viewmodels.ImageRepository
        self.view.ExtendsContentIntoTitleBar = True
        self.view.SetTitleBar(self.view.CustomTitleBar)

    def SelectFolderClick(self, sender, e):
        self.repo = repo = image_info.ImagesRepository()
        repo.get_images(SAMPLE_GALLERY)
        
        # Also be aware you need to resize the window to see these
        # https://github.com/microsoft/microsoft-ui-xaml/issues/5052
        self.view.ImagesRepository = self.view.wrap(repo)

        self.view.ImageCollectionInfoBar.Message = f"{len(repo.images)} images loaded."
        self.view.ImageCollectionInfoBar.IsOpen = True

    def ImageClick(self, sender, e):
        sender = sender.as_("Microsoft.UI.Xaml.Controls.Control")
        imageInfo = self.view.unwrap(sender.DataContext)
        if isinstance(imageInfo, image_info.ImageInfo):
            # TODO: Open new window and set content to the image
            self.view.ImageCollectionInfoBar.Message = f"Selected {imageInfo.name}"
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
