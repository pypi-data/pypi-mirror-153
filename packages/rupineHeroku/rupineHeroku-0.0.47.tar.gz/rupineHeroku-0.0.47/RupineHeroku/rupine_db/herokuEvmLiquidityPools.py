from psycopg2 import sql
from ..DataStructures import ObjEvmToken
from . import herokuDbAccess

def postEvmToken(connection, schema:str, chain_id, liquidity_pool_address, token_address_a, token_address_b, exchange_name):

    query = sql.SQL("INSERT INTO {}.evm_token (chain_id, liquidity_pool_address, token_address_a, token_address_b, exchange_name) \
           VALUES (%s,%s,%s,%s,%s)").format(sql.Identifier(schema))
    params = (
        chain_id,
        liquidity_pool_address,
        token_address_a,
        token_address_b,
        exchange_name)
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getEvmLiquidityPool(connection, schema, chain_id, token_address):
    
    query = sql.SQL("SELECT chain_id, liquidity_pool_address, token_address_a, token_address_b, exchange_name, created_at, modified_at \
                        FROM {}.evm_token_liquidity_pools \
                        WHERE chain_id = %s AND (token_address_a = %s OR token_address_b = %s").format(sql.Identifier(schema))
    
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,token_address,token_address], connection)    
    return result