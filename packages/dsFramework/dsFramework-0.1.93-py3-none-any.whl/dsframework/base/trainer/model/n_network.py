from typing import Any


class ZIDSNetwork:
    """! Base class for neural network definition:

    for example:
        @code
            nnetwork = nn.Sequential(
                nn.Linear(28 * 28, 64),
                nn.ReLU(),
                nn.Linear(64, 3),
            )
        @endcode

    Another example:
        @code
        self.bert = BertModel.from_pretrained("bert-base-cased")
        @endcode
    """
    nnetwork = None

    def __init__(self, nnetwork=None):

        self.nnetwork = nnetwork

        if self.nnetwork is None:
            raise Exception("Network not defined. please define in network_module.py")

    def from_pretrained(self) -> Any:
        pass
