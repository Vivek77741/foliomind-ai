from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.snaptrade_service import snaptrade_service
from services.analytics_engine import analytics_engine

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])

@router.get("/overview")
async def get_portfolio_overview(
    user_id: str = Query("demo_user"),
    user_secret: str = Query("mock_secret_demo_user")
):
    """Fetch complete aggregated portfolio view with full analytics suite."""
    try:
        accounts = await snaptrade_service.get_accounts(user_id, user_secret)
        positions = await snaptrade_service.get_positions(user_id, user_secret)
        balances = await snaptrade_service.get_balances(user_id, user_secret)
        activities = await snaptrade_service.get_activities(user_id, user_secret)

        summary = analytics_engine.calculate_portfolio_summary(positions, balances)
        allocation = analytics_engine.calculate_asset_allocation(positions, summary["total_cash"])
        concentration = analytics_engine.calculate_concentration_risk(positions, summary["total_cash"])
        performers = analytics_engine.calculate_top_performers(positions)
        pnl_waterfall = analytics_engine.calculate_pnl_waterfall(positions)
        risk_metrics = analytics_engine.calculate_risk_metrics(positions, summary["total_cash"])
        health = analytics_engine.calculate_portfolio_health(summary, risk_metrics, concentration, positions)

        return {
            "summary": summary,
            "allocation": allocation,
            "concentration": concentration,
            "performers": performers,
            "pnl_waterfall": pnl_waterfall,
            "risk_metrics": risk_metrics,
            "health": health,
            "positions": positions,
            "accounts": accounts,
            "activities": activities,
            "connection_status": {
                "is_active": True,
                "needs_reauth": False,
                "brokerage_name": accounts[0]["brokerage_name"] if accounts else "Demo Brokerage",
                "is_demo": snaptrade_service.is_demo or "mock_secret" in user_secret
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
