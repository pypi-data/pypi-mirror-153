from ikologikapi.domain.AbstractIkologikInstallationsObject import AbstractIkologikInstallationsObject


class Product(AbstractIkologikInstallationsObject):

    def __init__(self, customer: str, installation: str):
        super().__init__(customer, installation)

        self.groups = None
        self.code = None
        self.description = None
        self.pids = None
        self.quantity = None
        self.price = None
        self.rate = None
