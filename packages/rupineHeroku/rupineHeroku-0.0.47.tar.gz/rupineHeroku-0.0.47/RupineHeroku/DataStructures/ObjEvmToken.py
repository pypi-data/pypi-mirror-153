
class ObjEvmToken:
    token_address = None
    abi = None
    chain_id = None 
    symbol = None
    name = None
    decimals = None
    token_class = None
    totalsupply = None
    keywords = None
    telegram_link = None
    creator_address = None
    creation_timestamp = None 
    creation_block_number = None 
    creation_tx_hash = None
    created_at = 0
    modified_at = 0


    def __init__(self):
        pass

    def __eq__(self, other): 
        if not isinstance(other, ObjEvmToken):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.token_address == other.token_address and 
                self.abi == other.abi and
                self.chain_id == other.chain_id and
                self.symbol == other.symbol and
                self.name == other.name and
                self.decimals == other.decimals and
                self.token_class == other.token_class and
                self.totalsupply == other.totalsupply and
                self.keywords == other.keywords and
                self.telegram_link == other.telegram_link and
                self.creator_address == other.creator_address and
                self.creation_timestamp == other.creation_timestamp and
                self.creation_block_number == other.creation_block_number and
                self.creation_tx_hash == other.creation_tx_hash and
                self.created_at == other.created_at and
                self.modified_at == other.modified_at)

    def clone(self):
        retTok = ObjEvmToken()
        retTok.token_address = self.token_address
        retTok.abi = self.abi
        retTok.chain_id = self.chain_id
        retTok.symbol = self.symbol
        retTok.name = self.name
        retTok.decimals = self.decimals
        retTok.token_class = self.token_class
        retTok.totalsupply = self.totalsupply
        retTok.keywords = self.keywords
        retTok.telegram_link = self.telegram_link
        retTok.creator_address = self.creator_address
        retTok.creation_timestamp = self.creation_timestamp
        retTok.creation_block_number = self.creation_block_number
        retTok.creation_tx_hash = self.creation_tx_hash
        retTok.created_at = self.created_at
        retTok.modified_at = self.modified_at
        return retTok