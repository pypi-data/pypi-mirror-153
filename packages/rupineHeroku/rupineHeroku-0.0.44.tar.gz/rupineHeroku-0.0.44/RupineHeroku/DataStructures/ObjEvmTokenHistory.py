
class ObjEvmTokenHistory:
    timestamp = 0
    token_address = None
    chain_id = None 
    max_tx_amount_percent = None
    max_wallet_size_percent = None
    is_verified = None
    is_honeypot = None
    buy_tax = None
    sell_tax = None
    created_at = 0
    modified_at = 0

    def __init__(self):
        pass

    def __eq__(self, other): 
        if not isinstance(other, ObjEvmTokenHistory):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.timestamp == other.timestamp and 
                self.token_address == other.token_address and 
                self.chain_id == other.chain_id and
                self.max_tx_amount_percent == other.max_tx_amount_percent and
                self.max_wallet_size_percent == other.max_wallet_size_percent and
                self.is_verified == other.is_verified and
                self.is_honeypot == other.is_honeypot and
                self.buy_tax == other.buy_tax and
                self.sell_tax == other.sell_tax and
                self.created_at == other.created_at and
                self.modified_at == other.modified_at)

    def clone(self):
        retTok = ObjEvmTokenHistory()
        retTok.timestamp = self.timestamp
        retTok.token_address = self.token_address
        retTok.chain_id = self.chain_id
        retTok.max_tx_amount_percent = self.max_tx_amount_percent
        retTok.max_wallet_size_percent = self.max_wallet_size_percent
        retTok.is_verified = self.is_verified
        retTok.is_honeypot = self.is_honeypot
        retTok.buy_tax = self.buy_tax
        retTok.sell_tax = self.sell_tax
        retTok.created_at = self.created_at
        retTok.modified_at = self.modified_at
        return retTok