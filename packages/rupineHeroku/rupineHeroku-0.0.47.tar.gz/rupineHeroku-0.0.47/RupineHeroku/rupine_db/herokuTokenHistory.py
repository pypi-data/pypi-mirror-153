from psycopg2 import sql
from ..DataStructures.ObjEvmTokenHistory import ObjEvmTokenHistory
from ..rupine_db import herokuDbAccess

def ParseObjEvmTokenHistory(data):
    retObj = ObjEvmTokenHistory()
    retObj.token_address = data[0]
    retObj.abi = data[1]
    retObj.chain_id = data[2] 
    retObj.symbol = data[3]
    retObj.name = data[4]
    retObj.decimals = data[5]
    retObj.token_class = data[6]
    retObj.totalsupply = data[7]
    retObj.keywords = data[8]
    retObj.telegram_link = data[9] 
    retObj.creator_address = data[10] 
    retObj.creation_timestamp = data[11] 
    retObj.creation_timestamp = data[12] 
    retObj.creation_tx_hash = data[13] 
    retObj.created_at = data[14] 
    retObj.modified_at = data[15] 
    return retObj

#TODO: continue here... implement connection to that table

def postEvmTokenHistory(connection, schema:str, token:ObjEvmTokenHistory):

    query = sql.SQL('INSERT INTO {}.evm_token_history ("timestamp", token_address, chain_id, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax) \
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)').format(sql.Identifier(schema))
    params = (
        token.timestamp,
        token.token_address,
        token.chain_id,
        token.max_tx_amount_percent,
        token.max_wallet_size_percent,
        token.is_verified,
        token.is_honeypot,
        token.buy_tax,
        token.sell_tax)
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getEvmTokenHistory(connection, schema, chain_id, token_address):
    
    # query database    
    query = sql.SQL('SELECT "timestamp", token_address, chain_id, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax, created_at, modified_at \
        FROM {}.evm_token_history WHERE chain_id = %s AND token_address = %s').format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,token_address], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjEvmTokenHistory(tok)
        rows.append(addRow)

    # return objects
    return rows