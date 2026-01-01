"""Finance Sync Service - Main Business Logic"""

import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.database import AccountingDB

logger = logging.getLogger(__name__)

class MonoClient:
    """Monobank Personal API Client"""
    
    def __init__(self, token: str, base_url: str = "https://api.monobank.ua"):
        import requests
        self.token = token
        self.base_url = base_url
        self.headers = {"X-Token": token}
        self.requests = requests
    
    def get_client_info(self) -> Dict[str, Any]:
        """Get client information"""
        response = self.requests.get(
            f"{self.base_url}/personal/client-info",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def get_statements(self, account_id: str, from_time: int, to_time: int) -> List[Dict]:
        """Get transaction statements"""
        response = self.requests.get(
            f"{self.base_url}/personal/statement/{account_id}/{from_time}/{to_time}",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()


class SyncService:
    """Service for syncing Monobank data"""
    
    def __init__(self, mono_token: str, db_path: str = "./data/accounting.db"):
        self.client = MonoClient(mono_token)
        self.db = AccountingDB(db_path)
    
    def sync_all(self, days: int = 7) -> Dict[str, Any]:
        """Sync all data"""
        try:
            client_info = self.client.get_client_info()
            result = {
                'client_name': client_info.get('name'),
                'accounts_synced': 0,
                'transactions_synced': 0,
                'errors': []
            }
            
            to_ts = int(time.time())
            from_ts = int((datetime.utcnow() - timedelta(days=days)).timestamp())
            
            for account in client_info.get('accounts', []):
                try:
                    account_id = account['id']
                    statements = self.client.get_statements(account_id, from_ts, to_ts)
                    
                    for trans in statements:
                        trans['account_id'] = account_id
                        self.db.upsert_transaction(trans)
                    
                    self.db.update_balance(
                        account_id,
                        account.get('balance'),
                        account.get('currencyCode')
                    )
                    
                    result['accounts_synced'] += 1
                    result['transactions_synced'] += len(statements)
                    logger.info(f"Synced {len(statements)} transactions for {account_id}")
                    
                except Exception as e:
                    logger.error(f"Error syncing {account_id}: {str(e)}")
                    result['errors'].append(str(e))
            
            return result
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            raise
    
    def get_statements(self, account_id: str = None, limit: int = 100) -> List[Dict]:
        """Get stored transactions"""
        return self.db.get_transactions(account_id, limit)
