"""Finance Sync Service - Database Layer"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any

class AccountingDB:
    """SQLite database for accounting transactions"""
    
    def __init__(self, db_path: str = "./data/accounting.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    currency_code TEXT NOT NULL,
                    description TEXT,
                    time INTEGER NOT NULL,
                    raw_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS balances (
                    account_id TEXT PRIMARY KEY,
                    balance INTEGER NOT NULL,
                    currency_code TEXT NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def upsert_transaction(self, transaction: Dict[str, Any]) -> str:
        """Insert or update a transaction"""
        with sqlite3.connect(self.db_path) as conn:
            trans_id = transaction.get('id', str(transaction.get('time')))
            conn.execute("""
                INSERT OR REPLACE INTO transactions 
                (id, account_id, amount, currency_code, description, time, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                trans_id,
                transaction.get('account_id'),
                transaction.get('amount'),
                transaction.get('currencyCode'),
                transaction.get('description'),
                transaction.get('time'),
                json.dumps(transaction)
            ))
            conn.commit()
        return trans_id
    
    def get_transactions(self, account_id: str = None, limit: int = 100) -> List[Dict]:
        """Get recent transactions"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM transactions"
            params = []
            if account_id:
                query += " WHERE account_id = ?"
                params.append(account_id)
            query += " ORDER BY time DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def update_balance(self, account_id: str, balance: int, currency_code: str):
        """Update account balance"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO balances (account_id, balance, currency_code)
                VALUES (?, ?, ?)
            """, (account_id, balance, currency_code))
            conn.commit()
