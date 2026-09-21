from typing import List, Dict, Any
import math

class AnalyticsEngine:
    @staticmethod
    def calculate_portfolio_summary(positions: List[Dict[str, Any]], balances: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute aggregated net worth, cash, total gain/loss, and position count."""
        total_cash = sum(b.get("cash", 0) for b in balances)
        positions_market_value = sum(p.get("market_value", 0) for p in positions)
        total_portfolio_value = total_cash + positions_market_value
        
        total_unrealized_pnl = sum(p.get("unrealized_pnl", 0) for p in positions)
        cost_basis = positions_market_value - total_unrealized_pnl
        total_pnl_percent = (total_unrealized_pnl / cost_basis * 100) if cost_basis > 0 else 0.0

        return {
            "total_portfolio_value": round(total_portfolio_value, 2),
            "total_cash": round(total_cash, 2),
            "positions_market_value": round(positions_market_value, 2),
            "total_unrealized_pnl": round(total_unrealized_pnl, 2),
            "total_pnl_percent": round(total_pnl_percent, 2),
            "total_positions_count": len(positions),
            "accounts_count": len(balances)
        }

    @staticmethod
    def calculate_asset_allocation(positions: List[Dict[str, Any]], total_cash: float) -> Dict[str, Any]:
        """Compute allocation percentages by sector and asset class."""
        total_value = sum(p.get("market_value", 0) for p in positions) + total_cash
        if total_value <= 0:
            return {"by_sector": [], "by_asset_class": []}

        # By Sector
        sector_totals: Dict[str, float] = {}
        for p in positions:
            sec = p.get("sector", "Other")
            val = p.get("market_value", 0)
            sector_totals[sec] = sector_totals.get(sec, 0) + val
        if total_cash > 0:
            sector_totals["Cash"] = total_cash

        by_sector = [
            {"name": sec, "value": round(val, 2), "percentage": round((val / total_value) * 100, 2)}
            for sec, val in sector_totals.items()
        ]
        by_sector.sort(key=lambda x: x["value"], reverse=True)

        # By Asset Class
        asset_totals: Dict[str, float] = {}
        for p in positions:
            ac = p.get("asset_class", "Equities")
            val = p.get("market_value", 0)
            asset_totals[ac] = asset_totals.get(ac, 0) + val
        if total_cash > 0:
            asset_totals["Cash"] = total_cash

        by_asset_class = [
            {"name": ac, "value": round(val, 2), "percentage": round((val / total_value) * 100, 2)}
            for ac, val in asset_totals.items()
        ]
        by_asset_class.sort(key=lambda x: x["value"], reverse=True)

        return {"by_sector": by_sector, "by_asset_class": by_asset_class}

    @staticmethod
    def calculate_concentration_risk(positions: List[Dict[str, Any]], total_cash: float) -> Dict[str, Any]:
        """Identify position concentration and top holdings risk metrics."""
        total_value = sum(p.get("market_value", 0) for p in positions) + total_cash
        if total_value <= 0:
            return {"top_holdings": [], "top_3_concentration_pct": 0}

        sorted_positions = sorted(positions, key=lambda x: x.get("market_value", 0), reverse=True)
        top_holdings = []
        top_3_val = 0.0

        for i, p in enumerate(sorted_positions):
            val = p.get("market_value", 0)
            pct = (val / total_value) * 100
            top_holdings.append({
                "symbol": p.get("symbol"),
                "name": p.get("description"),
                "market_value": round(val, 2),
                "percentage": round(pct, 2)
            })
            if i < 3:
                top_3_val += val

        top_3_pct = round((top_3_val / total_value) * 100, 2)
        risk_level = "High" if top_3_pct > 60 else ("Moderate" if top_3_pct > 35 else "Low")

        return {
            "top_holdings": top_holdings[:5],
            "top_3_concentration_pct": top_3_pct,
            "risk_level": risk_level
        }

    @staticmethod
    def calculate_top_performers(positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find highest and lowest performing positions in terms of P&L percentage."""
        if not positions:
            return {"gainers": [], "decliners": []}

        sorted_by_pnl = sorted(positions, key=lambda x: x.get("unrealized_pnl_percent", 0), reverse=True)
        return {
            "gainers": [
                {
                    "symbol": p.get("symbol"),
                    "name": p.get("description"),
                    "unrealized_pnl": p.get("unrealized_pnl"),
                    "unrealized_pnl_percent": p.get("unrealized_pnl_percent")
                }
                for p in sorted_by_pnl if p.get("unrealized_pnl_percent", 0) > 0
            ],
            "decliners": [
                {
                    "symbol": p.get("symbol"),
                    "name": p.get("description"),
                    "unrealized_pnl": p.get("unrealized_pnl"),
                    "unrealized_pnl_percent": p.get("unrealized_pnl_percent")
                }
                for p in sorted_by_pnl[::-1] if p.get("unrealized_pnl_percent", 0) <= 0
            ]
        }

    @staticmethod
    def calculate_pnl_waterfall(positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate per-position P&L contribution data for a waterfall/bar chart."""
        if not positions:
            return []
        
        # Sort by absolute P&L impact
        sorted_pos = sorted(positions, key=lambda x: abs(x.get("unrealized_pnl", 0)), reverse=True)
        top_positions = sorted_pos[:10]  # Top 10 by impact
        
        result = []
        for p in top_positions:
            pnl = p.get("unrealized_pnl", 0) or 0
            pnl_pct = p.get("unrealized_pnl_percent", 0) or 0
            result.append({
                "symbol": p.get("symbol", "N/A"),
                "pnl": round(pnl, 2),
                "pnl_percent": round(pnl_pct, 2),
                "is_gain": pnl >= 0
            })
        
        return result

    @staticmethod
    def calculate_risk_metrics(positions: List[Dict[str, Any]], total_cash: float) -> Dict[str, Any]:
        """
        Compute a comprehensive set of risk metrics:
        - Diversification Score (0-100): based on Herfindahl-Hirschman Index
        - Cash Drag %: how much idle cash is weighing on returns
        - Sector Concentration: dominant sector weight
        - Overall Risk Score (0-100, lower is riskier)
        """
        total_equity = sum(p.get("market_value", 0) for p in positions)
        total_value = total_equity + total_cash
        
        if total_value <= 0:
            return {
                "diversification_score": 0,
                "cash_drag_pct": 0,
                "hhi_score": 1.0,
                "dominant_sector": "N/A",
                "dominant_sector_pct": 0,
                "risk_label": "Unknown",
                "risk_color": "gray"
            }
        
        # Herfindahl-Hirschman Index (lower HHI = more diversified)
        weights = [p.get("market_value", 0) / total_value for p in positions if total_value > 0]
        hhi = sum(w ** 2 for w in weights)  # ranges 1/n to 1.0
        
        # Normalize to diversification score: 0 = fully concentrated, 100 = perfectly spread
        n = len(positions)
        min_hhi = (1 / n) if n > 0 else 1.0
        max_hhi = 1.0
        div_score = 100 * (1 - (hhi - min_hhi) / (max_hhi - min_hhi + 1e-9)) if n > 1 else 0
        div_score = max(0, min(100, round(div_score)))
        
        # Cash Drag
        cash_drag_pct = round((total_cash / total_value) * 100, 2) if total_value > 0 else 0
        
        # Dominant Sector
        sector_vals: Dict[str, float] = {}
        for p in positions:
            sec = p.get("sector", "Other")
            sector_vals[sec] = sector_vals.get(sec, 0) + p.get("market_value", 0)
        
        dominant_sector = max(sector_vals, key=sector_vals.get) if sector_vals else "N/A"
        dominant_sector_pct = round((sector_vals.get(dominant_sector, 0) / total_value) * 100, 2)
        
        # Overall composite risk score
        concentration_penalty = min(50, dominant_sector_pct * 0.5)
        cash_drag_penalty = min(20, cash_drag_pct * 0.4)
        base_score = div_score - concentration_penalty - cash_drag_penalty
        risk_score = max(0, min(100, round(base_score)))
        
        if risk_score >= 70:
            risk_label, risk_color = "Well Diversified", "emerald"
        elif risk_score >= 45:
            risk_label, risk_color = "Moderately Diversified", "amber"
        else:
            risk_label, risk_color = "Concentrated Risk", "rose"
        
        return {
            "diversification_score": div_score,
            "risk_score": risk_score,
            "cash_drag_pct": cash_drag_pct,
            "hhi": round(hhi, 4),
            "dominant_sector": dominant_sector,
            "dominant_sector_pct": dominant_sector_pct,
            "risk_label": risk_label,
            "risk_color": risk_color,
            "position_count": n
        }

    @staticmethod
    def calculate_portfolio_health(
        summary: Dict[str, Any],
        risk_metrics: Dict[str, Any],
        concentration: Dict[str, Any],
        positions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compute an overall Portfolio Health Score (0-100) with sub-scores
        across four dimensions: Returns, Diversification, Risk Management, Activity.
        """
        # --- Returns Score (0-25) ---
        pnl_pct = summary.get("total_pnl_percent", 0)
        if pnl_pct >= 15:
            returns_score = 25
        elif pnl_pct >= 5:
            returns_score = 20
        elif pnl_pct >= 0:
            returns_score = 12
        else:
            returns_score = max(0, 12 + pnl_pct)  # deduct per negative %

        # --- Diversification Score (0-25) ---
        div_raw = risk_metrics.get("diversification_score", 0)
        diversification_score = round(div_raw * 0.25)

        # --- Risk Management Score (0-25) ---
        conc_pct = concentration.get("top_3_concentration_pct", 100)
        risk_mgmt_score = 25 if conc_pct < 30 else (18 if conc_pct < 50 else (10 if conc_pct < 70 else 3))
        
        # --- Activity Score (0-25): based on position count & cash ratio ---
        n = len(positions)
        cash_drag = risk_metrics.get("cash_drag_pct", 0)
        activity_score = 25
        if n < 3:
            activity_score -= 10
        if cash_drag > 30:
            activity_score -= 10
        elif cash_drag > 15:
            activity_score -= 5
        activity_score = max(0, activity_score)

        total_score = returns_score + diversification_score + risk_mgmt_score + activity_score

        if total_score >= 80:
            grade, label = "A", "Excellent"
        elif total_score >= 65:
            grade, label = "B", "Good"
        elif total_score >= 50:
            grade, label = "C", "Fair"
        elif total_score >= 35:
            grade, label = "D", "Needs Work"
        else:
            grade, label = "F", "Critical"

        return {
            "total_score": total_score,
            "grade": grade,
            "label": label,
            "breakdown": {
                "returns": {"score": returns_score, "max": 25, "label": "Return Performance"},
                "diversification": {"score": diversification_score, "max": 25, "label": "Diversification"},
                "risk_management": {"score": risk_mgmt_score, "max": 25, "label": "Risk Management"},
                "activity": {"score": activity_score, "max": 25, "label": "Portfolio Efficiency"}
            }
        }

analytics_engine = AnalyticsEngine()
