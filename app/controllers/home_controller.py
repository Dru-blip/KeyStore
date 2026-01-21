from fletx.core import FletXController,RxList
from app.models import Vault

class HomeController(FletXController):
    def __init__(self):
        self.vaults=RxList([Vault(name="Personal"),
                            Vault(name="Work"),])
        super().__init__()
