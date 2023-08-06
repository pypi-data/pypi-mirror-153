from solar_crypto.constants import TRANSACTION_TRANSFER
from solar_crypto.identity import address
from solar_crypto.transactions.builder.base import BaseTransactionBuilder


class Transfer(BaseTransactionBuilder):

    transaction_type = TRANSACTION_TRANSFER

    def __init__(self, recipientId, amount, vendorField=None, fee=None):
        """Create a transfer transaction

        Args:
            recipientId (str): address to which you want to send coins
            amount (int): amount of coins you want to transfer
            vendorField (str): value for the vendor field aka smartbridge
            fee (int, optional): fee used for the transaction (default is already set)
        """
        super().__init__()

        if not address.validate_address(recipientId):
            raise ValueError("Invalid recipient address")

        self.transaction.recipientId = recipientId

        if type(amount) == int and amount > 0:
            self.transaction.amount = amount
        else:
            raise ValueError("Amount is not valid")

        self.transaction.vendorField = vendorField.encode() if vendorField else None

        if fee:
            self.transaction.fee = fee
