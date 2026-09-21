import httpx
import logging
from typing import Dict, Any, List, Optional
from config import settings

logger = logging.getLogger("snaptrade")

class SnapTradeService:
    def __init__(self):
        self.client_id = settings.SNAPTRADE_CLIENT_ID
        self.consumer_key = settings.SNAPTRADE_CONSUMER_KEY
        self.base_url = "https://api.snaptrade.com/api/v1"
        self.is_demo = self.client_id in ["DEMO_CLIENT_ID", ""] or self.consumer_key in ["DEMO_CONSUMER_KEY", ""]

    def _headers(self, user_secret: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "clientId": self.client_id,
            "consumerKey": self.consumer_key
        }
        if user_secret:
            headers["userSecret"] = user_secret
        return headers

    async def register_user(self, user_id: str) -> Dict[str, Any]:
        """Register a user with SnapTrade or return mock registration."""
        if self.is_demo:
            logger.info(f"Demo mode: registering user {user_id}")
            return {
                "user_id": user_id,
                "user_secret": f"mock_secret_{user_id}",
                "status": "success",
                "is_demo": True
            }

        url = f"{self.base_url}/snapTrade/registerUser"
        async with httpx.AsyncClient() as client:
            res = await client.post(url, json={"userId": user_id}, headers=self._headers())
            if res.status_code in [200, 201]:
                data = res.json()
                return {
                    "user_id": user_id,
                    "user_secret": data.get("userSecret"),
                    "status": "success",
                    "is_demo": False
                }
            else:
                logger.error(f"Failed to register user: {res.text}")
                # Fallback to demo mode on API error
                return {
                    "user_id": user_id,
                    "user_secret": f"mock_secret_{user_id}",
                    "status": "demo_fallback",
                    "is_demo": True
                }

    async def get_connection_portal_url(self, user_id: str, user_secret: str) -> Dict[str, Any]:
        """Generate a SnapTrade Connection Portal URL."""
        if self.is_demo or "mock_secret" in user_secret:
            return {
                "redirect_url": f"{settings.FRONTEND_URL}/dashboard?connected=true&demo=true",
                "is_demo": True
            }

        url = f"{self.base_url}/snapTrade/login"
        async with httpx.AsyncClient() as client:
            res = await client.post(
                url,
                json={"immediateRedirect": True, "customRedirect": f"{settings.FRONTEND_URL}/dashboard?connected=true"},
                headers=self._headers(user_secret),
                params={"userId": user_id, "userSecret": user_secret}
            )
            if res.status_code == 200:
                data = res.json()
                return {"redirect_url": data.get("redirectURI"), "is_demo": False}
            else:
                logger.error(f"Error getting login URL: {res.text}")
                return {
                    "redirect_url": f"{settings.FRONTEND_URL}/dashboard?connected=true&demo=true",
                    "is_demo": True
                }

    async def get_accounts(self, user_id: str, user_secret: str) -> List[Dict[str, Any]]:
        """Fetch user accounts from SnapTrade or return rich demo accounts."""
        if self.is_demo or "mock_secret" in user_secret:
            return [
                {
                    "id": "acc_alpaca_paper_01",
                    "brokerage_name": "Alpaca Paper Trading",
                    "account_number": "PA3928104",
                    "name": "Primary Growth Account",
                    "type": "Margin",
                    "institution_name": "Alpaca Securities",
                    "status": "ACTIVE"
                },
                {
                    "id": "acc_ibkr_demo_02",
                    "brokerage_name": "Interactive Brokers",
                    "account_number": "U8472910",
                    "name": "Dividend Retirement Fund",
                    "type": "Roth IRA",
                    "institution_name": "Interactive Brokers LLC",
                    "status": "ACTIVE"
                }
            ]

        url = f"{self.base_url}/accounts"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self._headers(user_secret), params={"userId": user_id, "userSecret": user_secret})
            if res.status_code == 200:
                return res.json()
            return []

    async def get_positions(self, user_id: str, user_secret: str, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch positions across accounts."""
        if self.is_demo or "mock_secret" in user_secret:
            return [
                {
                    "account_id": "acc_alpaca_paper_01",
                    "symbol": "NVDA",
                    "description": "NVIDIA Corporation",
                    "units": 45.0,
                    "price": 128.50,
                    "open_price": 95.20,
                    "market_value": 5782.50,
                    "unrealized_pnl": 1498.50,
                    "unrealized_pnl_percent": 34.98,
                    "asset_class": "Equities",
                    "sector": "Technology"
                },
                {
                    "account_id": "acc_alpaca_paper_01",
                    "symbol": "AAPL",
                    "description": "Apple Inc.",
                    "units": 60.0,
                    "price": 224.30,
                    "open_price": 185.00,
                    "market_value": 13458.00,
                    "unrealized_pnl": 2358.00,
                    "unrealized_pnl_percent": 21.24,
                    "asset_class": "Equities",
                    "sector": "Technology"
                },
                {
                    "account_id": "acc_alpaca_paper_01",
                    "symbol": "MSFT",
                    "description": "Microsoft Corporation",
                    "units": 25.0,
                    "price": 435.10,
                    "open_price": 410.00,
                    "market_value": 10877.50,
                    "unrealized_pnl": 627.50,
                    "unrealized_pnl_percent": 6.12,
                    "asset_class": "Equities",
                    "sector": "Technology"
                },
                {
                    "account_id": "acc_alpaca_paper_01",
                    "symbol": "VOO",
                    "description": "Vanguard S&P 500 ETF",
                    "units": 30.0,
                    "price": 512.60,
                    "open_price": 470.00,
                    "market_value": 15378.00,
                    "unrealized_pnl": 1278.00,
                    "unrealized_pnl_percent": 9.06,
                    "asset_class": "ETF",
                    "sector": "Broad Market"
                },
                {
                    "account_id": "acc_ibkr_demo_02",
                    "symbol": "JNJ",
                    "description": "Johnson & Johnson",
                    "units": 40.0,
                    "price": 158.40,
                    "open_price": 162.00,
                    "market_value": 6336.00,
                    "unrealized_pnl": -144.00,
                    "unrealized_pnl_percent": -2.22,
                    "asset_class": "Equities",
                    "sector": "Healthcare"
                },
                {
                    "account_id": "acc_ibkr_demo_02",
                    "symbol": "BND",
                    "description": "Vanguard Total Bond Market ETF",
                    "units": 80.0,
                    "price": 73.10,
                    "open_price": 72.50,
                    "market_value": 5848.00,
                    "unrealized_pnl": 48.00,
                    "unrealized_pnl_percent": 0.83,
                    "asset_class": "Bonds",
                    "sector": "Fixed Income"
                }
            ]

        url = f"{self.base_url}/positions"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self._headers(user_secret), params={"userId": user_id, "userSecret": user_secret})
            if res.status_code == 200:
                return res.json()
            return []

    async def get_balances(self, user_id: str, user_secret: str) -> List[Dict[str, Any]]:
        """Fetch cash and portfolio balances."""
        if self.is_demo or "mock_secret" in user_secret:
            return [
                {
                    "account_id": "acc_alpaca_paper_01",
                    "currency": "USD",
                    "cash": 4250.00,
                    "buying_power": 8500.00,
                    "total_portfolio_value": 49746.00
                },
                {
                    "account_id": "acc_ibkr_demo_02",
                    "currency": "USD",
                    "cash": 1820.00,
                    "buying_power": 1820.00,
                    "total_portfolio_value": 14004.00
                }
            ]

        url = f"{self.base_url}/balances"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self._headers(user_secret), params={"userId": user_id, "userSecret": user_secret})
            if res.status_code == 200:
                return res.json()
            return []

    async def get_activities(self, user_id: str, user_secret: str) -> List[Dict[str, Any]]:
        """Fetch historical brokerage transactions & activity."""
        if self.is_demo or "mock_secret" in user_secret:
            return [
                {
                    "id": "act_01",
                    "account_id": "acc_alpaca_paper_01",
                    "type": "BUY",
                    "symbol": "NVDA",
                    "units": 10.0,
                    "price": 122.40,
                    "amount": -1224.00,
                    "date": "2026-09-12T14:30:00Z",
                    "description": "Bought 10 shares of NVDA @ $122.40"
                },
                {
                    "id": "act_02",
                    "account_id": "acc_alpaca_paper_01",
                    "type": "DIVIDEND",
                    "symbol": "AAPL",
                    "units": 0,
                    "price": 0,
                    "amount": 42.50,
                    "date": "2026-09-08T09:00:00Z",
                    "description": "Cash Dividend payment from AAPL"
                },
                {
                    "id": "act_03",
                    "account_id": "acc_ibkr_demo_02",
                    "type": "DEPOSIT",
                    "symbol": "USD",
                    "units": 0,
                    "price": 0,
                    "amount": 1000.00,
                    "date": "2026-09-01T11:15:00Z",
                    "description": "ACH Transfer Deposit"
                },
                {
                    "id": "act_04",
                    "account_id": "acc_alpaca_paper_01",
                    "type": "SELL",
                    "symbol": "MSFT",
                    "units": 5.0,
                    "price": 440.00,
                    "amount": 2200.00,
                    "date": "2026-08-25T16:00:00Z",
                    "description": "Sold 5 shares of MSFT @ $440.00"
                }
            ]

        url = f"{self.base_url}/activities"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self._headers(user_secret), params={"userId": user_id, "userSecret": user_secret})
            if res.status_code == 200:
                return res.json()
            return []

snaptrade_service = SnapTradeService()
