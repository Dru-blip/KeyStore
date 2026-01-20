from fletx.core import FletXController,RxList
from app.models import Vault

class HomeController(FletXController):
    def __init__(self):
        self.vaults=RxList([Vault(name="Personal"),
                            Vault(name="Work"),
                            Vault(name="Projects"),
                            Vault(name="Archive"),
                            Vault(name="Miscellaneous"),
                            Vault(name="Travel"),
                            Vault(name="Finance"),
                            Vault(name="Health"),
                            Vault(name="Education"),
                            Vault(name="Hobbies"),
                            Vault(name="Family"),
                            Vault(name="Friends"),
                            Vault(name="Events"),])
        super().__init__()
