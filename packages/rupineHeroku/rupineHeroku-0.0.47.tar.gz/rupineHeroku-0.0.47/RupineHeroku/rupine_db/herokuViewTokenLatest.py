from psycopg2 import sql
from ..DataStructures.ObjViewEvmTokenHistory import ObjEvmTokenHistory
from ..rupine_db import herokuDbAccess

def ParseObjEvmTokenLatest(data):
    retObj = ObjEvmTokenHistory()
    retObj.token_address = data[0]
    retObj.chain_id = data[1] 
    retObj.abi = data[2]
    retObj.symbol = data[3]
    retObj.name = data[4]
    retObj.decimals = data[5]
    retObj.token_class = data[6]
    retObj.totalsupply = data[7]
    retObj.keywords = data[8]
    retObj.telegram_link = data[9] 
    retObj.creator_address = data[10] 
    retObj.creation_timestamp = data[11] 
    retObj.creation_block_number = data[12] 
    retObj.creation_tx_hash = data[13] 
    retObj.max_tx_amount_percent = data[14]
    retObj.max_wallet_size_percent = data[15]
    retObj.is_verified = data[16]
    retObj.is_honeypot = data[17]
    retObj.buy_tax = data[18]
    retObj.sell_tax = data[19]
    retObj.latest_timestamp = data[20]
    return retObj

def getEvmTokenLatest(connection, schema, chain_id, token_address):
    
    # query database    
    query = sql.SQL("SELECT token_address, chain_id, abi, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax, latest_timestamp \
        FROM {}.v_evm_latest_token WHERE chain_id = %s AND token_address = %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,token_address], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjEvmTokenLatest(tok)
        rows.append(addRow)

    # return objects
    return rows

def getEvmTokenLatestList(connection, schema, chain_id, gteCreatedAt):
    
    # query database    
    query = sql.SQL("SELECT token_address, chain_id, abi, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax, latest_timestamp \
        FROM {}.v_evm_latest_token WHERE chain_id = %s AND creation_timestamp >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjEvmTokenLatest(tok)
        rows.append(addRow)

    # return objects
    return rows

def getEvmTokenLatestWithoutName(connection, schema, chain_id, gteCreatedAt):
    
    # query database    
    query = sql.SQL("SELECT token_address, chain_id, abi, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax, latest_timestamp \
        FROM {}.v_evm_latest_token WHERE chain_id = %s AND (name is NULL OR name = 'n/a') AND creation_timestamp >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjEvmTokenLatest(tok)
        rows.append(addRow)

    # return objects
    return rows