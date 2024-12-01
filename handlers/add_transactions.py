
from typing import List
from fastapi import HTTPException
from models.transaction import Transaction
from storage.in_memory_store import store_transactions

async def add_transactions(csv_data: bytes) -> List[Transaction]:
    
    try:
        s = csv_data.decode('UTF-8')
    except Exception as err:
        raise HTTPException(status_code=400, detail=f'Cannot decode your CSV input. Details: {str(err)}')
    
    lines = s.splitlines()
    
    transactions = []
    for line in lines:
        if line.isspace():
            continue
        if line[0] == "#":
            continue
        
        transaction = parse_transaction(line)
        transactions.append(transaction)
    
    await store_transactions(transactions)
       
    return transactions

def parse_transaction(line: str) -> Transaction:
    fields = [line.strip() for line in line.split(",")]
    n_fields = len(fields)
    if n_fields != 4:
        raise HTTPException(status_code=400, detail=f'Should be 4 fields, not {n_fields} ({line})')
    try:
        transaction = Transaction(date=fields[0], category=fields[1], amount=fields[2], memo=fields[3])
    except Exception as err:
        raise HTTPException(status_code=400, detail=f'Cannot parse one of the CSV lines. Details: {str(err)}')
    return transaction

   