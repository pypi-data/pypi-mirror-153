
class ObjViewEvmTokenLiqPool:
    token_address = None
    name = None
    symbol = None
    chain_id = None 
    liquidity_pool_address = ''
    exchange_name = ''
    created_at = 0
    modified_at = 0
    token_side = ''
    reserve_a = 0
    reserve_b = 0
    is_sellable = ''
    holder_count = 0
    volume_daily = 0


    def __init__(self):
        pass

    def __eq__(self, other): 
        if not isinstance(other, ObjViewEvmTokenLiqPool):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.token_address == other.token_address and
                self.name == other.name and
                self.symbol == other.symbol and
                self.chain_id == other.chain_id and
                self.liquidity_pool_address == other.liquidity_pool_address and
                self.exchange_name == other.exchange_name and
                self.created_at == other.created_at and
                self.modified_at == other.modified_at and
                self.token_side == other.token_side and
                self.reserve_a == other.reserve_a and
                self.reserve_b == other.reserve_b and
                self.is_sellable == other.is_sellable and
                self.holder_count == other.holder_count and
                self.volume_daily == other.volume_daily)

    def clone(self):
        retTok = ObjViewEvmTokenLiqPool()
        retTok.token_address = self.token_address
        retTok.name = self.name
        retTok.symbol = self.symbol
        retTok.chain_id = self.chain_id
        retTok.liquidity_pool_address = self.liquidity_pool_address
        retTok.exchange_name = self.exchange_name
        retTok.created_at = self.created_at
        retTok.modified_at = self.modified_at
        retTok.token_side = self.token_side
        retTok.reserve_a = self.reserve_a
        retTok.reserve_b = self.reserve_b
        retTok.is_sellable = self.is_sellable
        retTok.holder_count = self.holder_count
        retTok.volume_daily = self.volume_daily
        return retTok