from typing import Any

from dsframework.base.trainer import *


class generatedClass(ZIDSNetwork):
    """! Define your networks here, or load from pretrained model.

    for example:
        @code
        nnetwork = nn.Sequential(
            nn.Linear(28 * 28, 64),
            nn.ReLU(),
            nn.Linear(64, 3),
            nn.Linear(3, 64),
            nn.ReLU(),
            nn.Linear(64, 28 * 28)
        )
        @endcode

    Another example:
        @code
        nnetwork_wine = nn.Sequential(
        nn.Linear(11, 1),
        nn.ReLU(),
        nn.Linear(1, 1))
        @endcode

    Another example:
        @code
        self.bert = BertModel.from_pretrained("bert-base-cased")
        @endcode
    """

    nnetwork = None

    if nnetwork is None:
        raise Exception("Network not defined. please define in network_module.py")

    def __init__(self):
        super().__init__(self.nnetwork)

    def from_pretrained(self) -> Any:
        pass
