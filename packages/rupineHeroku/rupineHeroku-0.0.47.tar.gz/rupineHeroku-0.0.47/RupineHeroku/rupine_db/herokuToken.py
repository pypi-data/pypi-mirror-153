from psycopg2 import sql
from ..DataStructures.ObjEvmToken import ObjEvmToken
from ..rupine_db import herokuDbAccess

def ParseObjEvmToken(data):
    retObj = ObjEvmToken()
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

def postEvmToken(connection, schema:str, token:ObjEvmToken):

    query = sql.SQL("INSERT INTO {}.evm_token (token_address, abi, chain_id, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash) \
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))
    params = (
        token.token_address,
        token.abi,
        token.chain_id,
        token.symbol,
        token.name,
        token.decimals,
        token.token_class,
        token.totalsupply,
        token.keywords,
        token.telegram_link,
        token.creator_address,
        token.creation_timestamp,
        token.creation_block_number,
        token.creation_tx_hash)
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getEvmToken(connection, schema, chain_id, token_address):
    
    # query database    
    query = sql.SQL("SELECT token_address, abi, chain_id, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, created_at, modified_at \
        FROM {}.evm_token WHERE chain_id = %s AND token_address = %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,token_address], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjEvmToken(tok)
        rows.append(addRow)

    # return objects
    return rows

def getEvmTokenList(connection, schema, chain_id, gteCreatedAt):
    
    # query database    
    query = sql.SQL("SELECT token_address, abi, chain_id, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, created_at, modified_at \
        FROM {}.evm_token WHERE chain_id = %s AND created_at >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjEvmToken(tok)
        rows.append(addRow)

    # return objects
    return rows

def getEvmTokenWithoutName(connection, schema, chain_id, gteCreatedAt):
    
    # query database    
    query = sql.SQL("SELECT token_address, abi, chain_id, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, created_at, modified_at \
        FROM {}.evm_token WHERE chain_id = %s AND name is NULL AND created_at >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjEvmToken(tok)
        rows.append(addRow)

    # return objects
    return rows