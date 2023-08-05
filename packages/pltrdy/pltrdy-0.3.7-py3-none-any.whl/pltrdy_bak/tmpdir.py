import tempfile


class TemporaryDirectory(tempfile.TemporaryDirectory):
    """A TemporaryDirectory similar to tempfile but which can be detached if
       `keep` is True i.e. the directory isn't cleaned up on object garbage
        collection
    """
    def __init__(self, *args, keep=False, **kwargs):
        super(TemporaryDirectory, self).__init__(*args, **kwargs)

        self.keep = keep
        if self.keep:
            self._finalizer.detach()

    def __exit__(self, exc, value, tb):
        if not self.keep or exc is None:
            self.cleanup()
        else:
            _warnings.warn(f"Not cleaning up {self.name} due to exception. "
                           f"Set `keep=False` to force cleanup",
                           ResourceWarning)

