class BaseServiceMixin:
    service_class = None

    @property
    def service(self):
        if self.service_class is None:
            raise NotImplementedError("View must define his own service")
        if not hasattr(self, "_service_instance"):
            self._service_instance = self.service_class()
        return self._service_instance