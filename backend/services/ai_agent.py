import logging
import json
from typing import Dict, Any, List, Optional
from services.snaptrade_service import snaptrade_service
from services.analytics_engine import analytics_engine
from config import settings

logger = logging.getLogger("copilot")

class AIAgentService:
    def __init__(self):
        self.gemini_client = None
        self.init_gemini()

    def init_gemini(self):
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("Successfully initialized Gemini GenAI Client")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini SDK: {e}")

    async def process_user_query(
        self,
        query: str,
        user_id: str,
        user_secret: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process natural language queries with grounded tool execution.
        """
        if not self.gemini_client and settings.GEMINI_API_KEY:
            self.init_gemini()

        query_clean = query.strip()
        query_lower = query_clean.lower()

        # Step 1: Fetch raw SnapTrade data
        positions = await snaptrade_service.get_positions(user_id, user_secret)
        balances = await snaptrade_service.get_balances(user_id, user_secret)
        activities = await snaptrade_service.get_activities(user_id, user_secret)

        # Step 2: Calculate deterministic financial metrics
        summary = analytics_engine.calculate_portfolio_summary(positions, balances)
        allocation = analytics_engine.calculate_asset_allocation(positions, summary["total_cash"])
        concentration = analytics_engine.calculate_concentration_risk(positions, summary["total_cash"])
        performers = analytics_engine.calculate_top_performers(positions)

        # Check if query matches a specific stock ticker in user's positions (e.g., "nvda", "aapl", "msft", "voo")
        matched_position = None
        for p in positions:
            sym = p.get("symbol", "").lower()
            desc = p.get("description", "").lower()
            if query_lower == sym or query_lower in desc or f" {sym} " in f" {query_lower} ":
                matched_position = p
                break

        tools_executed = ["fetch_positions()", "fetch_balances()", "fetch_activities()"]
        response_text = ""

        # Step 3: Call Gemini API if available for rich grounded response
        if self.gemini_client:
            try:
                tools_executed.append("gemini-2.5-flash-synthesis()")
                prompt = f"""
You are FolioMind AI, an expert, highly intelligent financial copilot integrated with SnapTrade APIs.
The user asked: "{query_clean}"

Here is the exact live, 100% grounded portfolio data from SnapTrade:
- Total Portfolio Value: ${summary['total_portfolio_value']:,.2f}
- Cash Balance: ${summary['total_cash']:,.2f}
- Overall Unrealized Gain/Loss: +${summary['total_unrealized_pnl']:,.2f} (+{summary['total_pnl_percent']}%)
- Positions: {json.dumps(positions)}
- Asset Allocation by Sector: {json.dumps(allocation['by_sector'])}
- Concentration Risk (Top 3 Holdings): {concentration['top_3_concentration_pct']}% (Risk Level: {concentration['risk_level']})
- Recent Activities: {json.dumps(activities[:5])}

Instructions:
1. Answer the user's query directly and accurately based ONLY on the grounded data above.
2. If the user types a stock symbol or asks about a position (like NVDA or Apple), give a detailed breakdown for that asset (Shares, Avg Price, Current Price, Total Value, P&L, % of Portfolio).
3. Format your response cleanly using clean Markdown formatting. Use bold text for numbers and key insights. Do not use messy double asterisks without text.
"""
                gemini_res = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if gemini_res and gemini_res.text:
                    return {
                        "query": query,
                        "response": gemini_res.text.strip(),
                        "tools_executed": tools_executed,
                        "grounded_data": {"summary": summary, "concentration": concentration}
                    }
            except Exception as e:
                logger.warning(f"Gemini generation error, falling back to deterministic response: {e}")

        # Step 4: Deterministic fallback engine
        if matched_position:
            tools_executed.append(f"get_position_detail('{matched_position['symbol']}')")
            sym = matched_position['symbol']
            desc = matched_position['description']
            val = matched_position['market_value']
            units = matched_position['units']
            price = matched_position['price']
            open_price = matched_position['open_price']
            pnl = matched_position['unrealized_pnl']
            pnl_pct = matched_position['unrealized_pnl_percent']
            sec = matched_position['sector']
            port_pct = round((val / summary['total_portfolio_value']) * 100, 2)
            is_pos = pnl >= 0

            response_text = (
                f"📈 **Position Detail: {sym} ({desc})**\n\n"
                f"• **Current Market Value:** **${val:,.2f}** ({port_pct}% of total portfolio)\n"
                f"• **Shares Held:** **{units}** shares\n"
                f"• **Current Price:** **${price:,.2f}** (Avg Purchase Price: ${open_price:,.2f})\n"
                f"• **Unrealized P&L:** **{'+\$' if is_pos else '-\$'}{abs(pnl):,.2f} ({'+' if is_pos else ''}{pnl_pct}%)**\n"
                f"• **Sector:** **{sec}**\n\n"
                f"**Summary:** {sym} is your {'highest' if port_pct > 20 else 'key'} holding in the {sec} sector, representing **{port_pct}%** of your total invested capital."
            )

        elif any(w in query_lower for w in ["performance", "fall", "lose", "gain", "profit", "change", "top", "performer"]):
            tools_executed.append("calculate_top_performers()")
            gainers_str = ", ".join([f"{g['symbol']} (+{g['unrealized_pnl_percent']}%)" for g in performers['gainers']]) or "None"
            decliners_str = ", ".join([f"{d['symbol']} ({d['unrealized_pnl_percent']}%)" for d in performers['decliners']]) or "None"

            response_text = (
                f"📊 **Portfolio Performance Breakdown**\n\n"
                f"Your portfolio is currently valued at **${summary['total_portfolio_value']:,.2f}** with an overall unrealized gain of **+${summary['total_unrealized_pnl']:,.2f} (+{summary['total_pnl_percent']}%)**.\n\n"
                f"• **Top Performers:** {gainers_str}\n"
                f"• **Laggards / Losses:** {decliners_str}\n\n"
                f"**Key Insight:** Your highest single contributor to total gains is **{performers['gainers'][0]['symbol'] if performers['gainers'] else 'N/A'}**."
            )

        elif any(w in query_lower for w in ["diversif", "allocat", "sector", "risk", "concentrat", "asset"]):
            tools_executed.append("calculate_asset_allocation()")
            top_sector = allocation['by_sector'][0] if allocation['by_sector'] else {"name": "N/A", "percentage": 0}
            top_3_pct = concentration['top_3_concentration_pct']

            response_text = (
                f"🔍 **Portfolio Diversification & Risk Analysis**\n\n"
                f"• **Dominant Sector:** **{top_sector['name']}** ({top_sector['percentage']}% of total portfolio)\n"
                f"• **Concentration Risk Level:** **{concentration['risk_level']}**\n"
                f"• **Top 3 Holdings Weight:** **{top_3_pct}%** of your total assets\n\n"
                f"**Holdings Weight Breakdown:**\n"
                + "\n".join([f"  - **{h['symbol']}**: ${h['market_value']:,.2f} ({h['percentage']}%)" for h in concentration['top_holdings']])
            )

        elif any(w in query_lower for w in ["cash", "buying power", "balance", "money", "deposit"]):
            tools_executed.append("calculate_portfolio_summary()")
            response_text = (
                f"💵 **Cash & Account Balance Summary**\n\n"
                f"• **Total Liquid Cash:** **${summary['total_cash']:,.2f}**\n"
                f"• **Total Portfolio Value:** **${summary['total_portfolio_value']:,.2f}**\n"
                f"• **Cash Ratio:** **{round((summary['total_cash']/summary['total_portfolio_value'])*100, 1)}%**"
            )

        else:
            tools_executed.append("get_portfolio_overview()")
            response_text = (
                f"🤖 **FolioMind Portfolio Overview**\n\n"
                f"Here is a summary of your connected SnapTrade accounts:\n\n"
                f"• **Total Portfolio Value:** **${summary['total_portfolio_value']:,.2f}**\n"
                f"• **Unrealized Gain/Loss:** **+${summary['total_unrealized_pnl']:,.2f} (+{summary['total_pnl_percent']}%)**\n"
                f"• **Active Holdings Count:** {summary['total_positions_count']} positions\n"
                f"• **Available Cash:** **${summary['total_cash']:,.2f}**\n\n"
                f"You can ask me questions like:\n"
                f"👉 *'NVDA'* or *'Show me AAPL position details'*\n"
                f"👉 *'Why did my portfolio change this week?'*\n"
                f"👉 *'How diversified am I across sectors?'*"
            )

        return {
            "query": query,
            "response": response_text,
            "tools_executed": tools_executed,
            "grounded_data": {
                "summary": summary,
                "concentration": concentration
            }
        }

ai_agent = AIAgentService()
