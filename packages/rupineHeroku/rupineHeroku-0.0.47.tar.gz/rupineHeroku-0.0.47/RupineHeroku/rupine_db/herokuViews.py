from ..rupine_db import herokuDbAccess
from ..DataStructures.ObjViewEvmTokenLiqPool import ObjViewEvmTokenLiqPool
from psycopg2 import sql

def ParseObjViewEvmTokenLiqPool(data):
    retObj = ObjViewEvmTokenLiqPool()
    retObj.token_address = data[0]
    retObj.name = data[1]
    retObj.symbol = data[2]
    retObj.chain_id = data[3] 
    retObj.liquidity_pool_address = data[4] 
    retObj.exchange_name = data[5] 
    retObj.created_at = data[6] 
    retObj.modified_at = data[7] 
    retObj.token_side = data[8] 
    retObj.reserve_a = data[9] 
    retObj.reserve_b = data[10] 
    retObj.is_sellable = data[11] 
    retObj.holder_count = data[12] 
    retObj.volume_daily = data[13] 
    return retObj

def getEvmLatestTokenLiquidityPools(connection, schema, chain_id):
    
    # query database    
    query = sql.SQL("SELECT token_address, abi, chain_id, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, created_at, modified_at \
        FROM {}.v_evm_latest_token_liquidity_pools WHERE chain_id = %s").format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id], connection)  

    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjViewEvmTokenLiqPool(tok)
        rows.append(addRow)

    # return objects
    return rows

def getEvmLatestTokenLiquidityPoolsWithoutName(connection, schema, chain_id, gteCreatedAt):

    # query database    
    query = sql.SQL("SELECT token_address, abi, chain_id, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, created_at, modified_at \
        FROM {}.v_evm_latest_token_liquidity_pools WHERE chain_id = %s AND name = 'n/a' AND created_at >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjViewEvmTokenLiqPool(tok)
        rows.append(addRow)
    
    # return objects
    return rows

def getEvmLatestTokenLiquidityPoolsNotLaunched(connection, schema, chain_id, gteCreatedAt):
    
    # query database    
    query = sql.SQL("SELECT token_address, abi, chain_id, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, created_at, modified_at \
         FROM {}.v_evm_latest_token_liquidity_pools WHERE chain_id = %s AND liquidity_pool_address is NULL AND created_at >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection) 

    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjViewEvmTokenLiqPool(tok)
        rows.append(addRow)

    # return objects
    return rows