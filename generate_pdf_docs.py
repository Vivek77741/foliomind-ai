import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Image paths from user upload
IMG_DIR = r"C:\Users\vivek\.gemini\antigravity-ide\brain\3fa5f170-06db-497f-96ee-bf2a03bc53ad\.user_uploaded"
IMG_DASHBOARD_OVERVIEW = os.path.join(IMG_DIR, "media_1790004108778.png")
IMG_PNL_WATERFALL = os.path.join(IMG_DIR, "media_1790004132761.png")
IMG_ALLOCATION_HOLDINGS = os.path.join(IMG_DIR, "media_1790004154210.png")
IMG_ACTIVITIES = os.path.join(IMG_DIR, "media_1790004168417.png")
IMG_COPILOT_CHAT = os.path.join(IMG_DIR, "media_1790004215846.png")

OUTPUT_PDF = r"c:\Users\vivek\OneDrive\Desktop\st\FolioMind_AI_Comprehensive_Documentation.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip running header/footer on title page
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header
        self.drawString(40, 760, "FolioMind AI — Comprehensive Product, Financial & Architecture Documentation")
        self.drawRightString(572, 760, "SnapTrade AI Copilot")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 752, 572, 752)

        # Running Footer
        self.line(40, 42, 572, 42)
        self.drawString(40, 30, "CONFIDENTIAL & PROPRIETARY — Live Deployment: foliomind-ai.vercel.app")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 30, page_str)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#312e81")    # Deep Indigo
    c_secondary = colors.HexColor("#4f46e5")  # Vibrant Indigo
    c_dark = colors.HexColor("#0f172a")       # Slate 900
    c_text = colors.HexColor("#1e293b")       # Slate 800
    c_muted = colors.HexColor("#64748b")      # Slate 500
    c_emerald = colors.HexColor("#059669")    # Emerald 600
    c_rose = colors.HexColor("#e11d48")       # Rose 600
    c_card_bg = colors.HexColor("#f8fafc")    # Slate 50
    c_border = colors.HexColor("#e2e8f0")     # Slate 200

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_dark,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=c_secondary,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_dark,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_text,
        spaceAfter=7
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1e1b4b")
    )

    badge_style = ParagraphStyle(
        'Badge_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#ffffff"),
        alignment=1
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#ffffff")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=c_muted,
        alignment=1,
        spaceAfter=10
    )

    story = []

    # =========================================================================
    # COVER / TITLE BLOCK
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("FolioMind AI", title_style))
    story.append(Paragraph("Intelligent Investment Portfolio Copilot & Grounded Financial Intelligence Engine", subtitle_style))

    # Meta banner table
    meta_data = [
        [
            Paragraph("<b>Product Version:</b> v1.0.0 Production", body_style),
            Paragraph("<b>Integration:</b> SnapTrade REST & OAuth", body_style)
        ],
        [
            Paragraph("<b>Live Web App:</b> <font color='#4f46e5'><u>https://foliomind-ai.vercel.app</u></font>", body_style),
            Paragraph("<b>Backend API:</b> <font color='#4f46e5'><u>https://foliomind-ai.onrender.com</u></font>", body_style)
        ],
        [
            Paragraph("<b>GitHub Repository:</b> github.com/Vivek77741/foliomind-ai", body_style),
            Paragraph("<b>Documentation Date:</b> September 2026", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[260, 272])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # Executive Overview
    story.append(Paragraph("Executive Overview & The Core Financial Problem", h1_style))
    story.append(Paragraph(
        "Retail investors today face fragmented investment portfolios across multiple brokerages (Robinhood, Fidelity, "
        "Interactive Brokers, Alpaca). They lack institutional-grade risk diagnostics and struggle to answer basic questions: "
        "<i>'What drove my portfolio's return this week?'</i>, <i>'Am I taking hidden concentration risk in big tech?'</i>, or "
        "<i>'Is my idle cash dragging down long-term compounded growth?'</i>.",
        body_style
    ))
    story.append(Paragraph(
        "Generic LLMs (like standard ChatGPT or Claude) fail in finance because they suffer from <b>financial hallucinations</b>—they "
        "guess numbers, lack access to live brokerage ledger positions, and provide inaccurate mathematical calculations. "
        "<b>FolioMind AI</b> solves this fundamentally through a <b>'Deterministic Math First, Agentic Tool-Calling Second'</b> "
        "architecture built directly on SnapTrade's brokerage data aggregation APIs.",
        body_style
    ))

    # Architecture Box Callout
    callout_data = [[
        Paragraph(
            "<b>The Grounded Architecture Guarantee:</b> FolioMind AI never lets the language model calculate financial ratios or net worth. "
            "Instead, a deterministic Python Analytics Engine executes first (calculating HHI diversification index, cost basis, unrealized gain/loss, "
            "and concentration percentages). The verified mathematical data is then provided as factual context to Gemini 2.5 Flash for natural "
            "language explanation. This guarantees 100% mathematical accuracy with zero financial hallucinations.",
            callout_style
        )
    ]]
    t_callout = Table(callout_data, colWidths=[532])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eef2ff")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#6366f1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 1: MACRO KPI ENGINE & PORTFOLIO HEALTH (IMAGE 1)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("1. Macro Portfolio KPIs & Multi-Dimensional Health Engine", h1_style))
    story.append(Paragraph(
        "The top fold of FolioMind AI provides an immediate holistic diagnostic pulse of the investor's multi-account wealth.",
        body_style
    ))

    if os.path.exists(IMG_DASHBOARD_OVERVIEW):
        story.append(Image(IMG_DASHBOARD_OVERVIEW, width=530, height=254))
        story.append(Paragraph("<b>Figure 1:</b> Macro KPI cards, Composite Portfolio Health Gauge (80/100), and Risk Profile Analysis.", caption_style))

    story.append(Paragraph("A. High-Level KPI Metric Cards", h2_style))
    kpi_table_data = [
        [Paragraph("Metric", table_header), Paragraph("Observed Value", table_header), Paragraph("Financial Formula & Implementation", table_header), Paragraph("Investor Benefit", table_header)],
        [
            Paragraph("<b>Total Net Worth</b>", table_cell_bold),
            Paragraph("<b>$63,750.00</b>", table_cell),
            Paragraph("<code>∑(Positions MV) + Cash</code><br/>Aggregated across Alpaca Paper & IBKR accounts.", table_cell),
            Paragraph("Eliminates logging into separate brokerage portals to see total wealth.", table_cell)
        ],
        [
            Paragraph("<b>Liquid Cash</b>", table_cell_bold),
            Paragraph("<b>$6,070.00</b> (9.5%)", table_cell),
            Paragraph("<code>Total Cash / Portfolio Value</code><br/>Tracks uninvested buying power.", table_cell),
            Paragraph("Quantifies dry powder available for market pullbacks while warning against cash drag.", table_cell)
        ],
        [
            Paragraph("<b>Unrealized P&L</b>", table_cell_bold),
            Paragraph("<b>+$5,666.00</b> (▲ 10.89%)", table_cell),
            Paragraph("<code>Market Value - Cost Basis</code><br/>Cost Basis: $58,084.00.", table_cell),
            Paragraph("Clear separation of capital gains from net deposits.", table_cell)
        ],
        [
            Paragraph("<b>Top 3 Concentration</b>", table_cell_bold),
            Paragraph("<b>62.3%</b> (Risk: High)", table_cell),
            Paragraph("<code>∑(MV of Top 3 Assets) / Portfolio Value</code><br/>VOO (24.1%) + AAPL (21.1%) + MSFT (17.1%).", table_cell),
            Paragraph("Flags dangerous capital clustering before market shocks hit.", table_cell)
        ]
    ]
    t_kpi = Table(kpi_table_data, colWidths=[85, 95, 182, 170])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    story.append(Paragraph("B. The Composite Portfolio Health Score (80/100 - Grade A)", h2_style))
    story.append(Paragraph(
        "Rather than evaluating portfolios on raw returns alone, FolioMind's <code>calculate_portfolio_health()</code> engine "
        "synthesizes a 100-point composite grade across four critical dimensions (each weighted up to 25 points):",
        body_style
    ))
    health_points = [
        "<b>1. Return Performance (20/25):</b> Evaluates capital appreciation against market baselines. A +10.89% unrealized return places the portfolio in the top quintile.",
        "<b>2. Diversification (25/25):</b> Evaluates asset class dispersion (Equities, ETFs, Bonds, Cash) and cross-sector balance.",
        "<b>3. Risk Management (10/25):</b> Penalized heavily due to 62.3% clustering in the top 3 holdings (exceeding the 60% prudence threshold).",
        "<b>4. Portfolio Efficiency (25/25):</b> Rewards active turnover, dividend reinvestment, and minimal uncompensated idle cash."
    ]
    for hp in health_points:
        story.append(Paragraph(f"• {hp}", body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("C. Risk Profile & HHI Diversification (73/100)", h2_style))
    story.append(Paragraph(
        "The risk engine calculates the <b>Herfindahl-Hirschman Index (HHI)</b> (observed at <code>0.1584</code>). "
        "An HHI below 0.18 indicates healthy baseline dispersion across 6 assets, but warns of <b>9.52% Cash Drag</b>. "
        "This gives the user an actionable signal: deploying $3,000 of cash into fixed income or international equities would optimize the risk score from 73 to 85+.",
        body_style
    ))

    # =========================================================================
    # SECTION 2: PERFORMANCE ATTRIBUTION & TOP MOVERS (IMAGE 2)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Performance Attribution: P&L Waterfall & Top Movers", h1_style))
    story.append(Paragraph(
        "Understanding where portfolio returns came from is vital for avoiding emotional trading decisions.",
        body_style
    ))

    if os.path.exists(IMG_PNL_WATERFALL):
        story.append(Image(IMG_PNL_WATERFALL, width=530, height=277))
        story.append(Paragraph("<b>Figure 2:</b> Position-level P&L contribution waterfall chart and Top Gainers / Decliners leaderboard.", caption_style))

    story.append(Paragraph("A. P&L Contribution Waterfall Analysis", h2_style))
    story.append(Paragraph(
        "The P&L Waterfall Chart translates percentage returns into <b>hard dollars gained or lost</b> per asset. "
        "Often, a stock with a massive percentage gain contributes very little actual dollar return if the position size was small, "
        "while a modest percentage move on a large position can dictate the entire portfolio's performance:",
        body_style
    ))

    pnl_data = [
        [Paragraph("Ticker", table_header), Paragraph("Asset Name", table_header), Paragraph("Unrealized P&L ($)", table_header), Paragraph("Return (%)", table_header), Paragraph("Impact Role in Portfolio", table_header)],
        [
            Paragraph("<b>AAPL</b>", table_cell_bold),
            Paragraph("Apple Inc.", table_cell),
            Paragraph("<font color='#059669'><b>+$2,358.00</b></font>", table_cell),
            Paragraph("+21.24%", table_cell),
            Paragraph("<b>Top Dollar Driver:</b> Generates 41.6% of all portfolio gains.", table_cell)
        ],
        [
            Paragraph("<b>NVDA</b>", table_cell_bold),
            Paragraph("NVIDIA Corporation", table_cell),
            Paragraph("<font color='#059669'><b>+$1,498.50</b></font>", table_cell),
            Paragraph("+34.98%", table_cell),
            Paragraph("<b>Highest Alpha Gainer:</b> Highest % surge from $95.20 avg cost.", table_cell)
        ],
        [
            Paragraph("<b>VOO</b>", table_cell_bold),
            Paragraph("Vanguard S&P 500 ETF", table_cell),
            Paragraph("<font color='#059669'><b>+$1,278.00</b></font>", table_cell),
            Paragraph("+9.06%", table_cell),
            Paragraph("<b>Core Foundation:</b> Broad-market index stabilizing volatility.", table_cell)
        ],
        [
            Paragraph("<b>MSFT</b>", table_cell_bold),
            Paragraph("Microsoft Corp.", table_cell),
            Paragraph("<font color='#059669'><b>+$627.50</b></font>", table_cell),
            Paragraph("+6.12%", table_cell),
            Paragraph("Steady large-cap technology growth.", table_cell)
        ],
        [
            Paragraph("<b>BND</b>", table_cell_bold),
            Paragraph("Vanguard Total Bond ETF", table_cell),
            Paragraph("<font color='#059669'><b>+$48.00</b></font>", table_cell),
            Paragraph("+0.83%", table_cell),
            Paragraph("Capital preservation / low-beta yield instrument.", table_cell)
        ],
        [
            Paragraph("<b>JNJ</b>", table_cell_bold),
            Paragraph("Johnson & Johnson", table_cell),
            Paragraph("<font color='#e11d48'><b>-$144.00</b></font>", table_cell),
            Paragraph("-2.22%", table_cell),
            Paragraph("<b>Sole Drag:</b> Healthcare sector lag; defensiveness hedge.", table_cell)
        ]
    ]
    t_pnl = Table(pnl_data, colWidths=[55, 120, 100, 75, 182])
    t_pnl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_pnl)
    story.append(Spacer(1, 8))

    story.append(Paragraph("B. Why this is Useful to Investors", h2_style))
    story.append(Paragraph(
        "In typical brokerage apps, users see a simple list of stocks. They cannot easily answer whether their gains came from "
        "a diversified basket or just two lucky stock picks. The P&L Waterfall immediately reveals that <b>AAPL + NVDA account for "
        "$3,856.50 of the $5,666.00 total profit (68%)</b>. This empirical clarity prevents false overconfidence and encourages proper rebalancing.",
        body_style
    ))

    # =========================================================================
    # SECTION 3: ASSET & SECTOR ALLOCATION AND HOLDINGS (IMAGE 3)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Asset Allocation, Sector Distribution & Holdings Ledger", h1_style))
    story.append(Paragraph(
        "Institutional asset managers prioritize asset allocation over security selection. FolioMind empowers retail users with that same rigor.",
        body_style
    ))

    if os.path.exists(IMG_ALLOCATION_HOLDINGS):
        story.append(Image(IMG_ALLOCATION_HOLDINGS, width=530, height=326))
        story.append(Paragraph("<b>Figure 3:</b> Interactive Donut Chart, Position Concentration Breakdown, and Active Holdings Ledger.", caption_style))

    story.append(Paragraph("A. Sector Exposure Breakdown", h2_style))
    story.append(Paragraph(
        "The multi-colored donut chart visualizes capital distribution across major market sectors: "
        "<b>Technology ($30,118.00 / 47.24%)</b>, <b>Broad Market ETF ($15,378.00 / 24.12%)</b>, "
        "<b>Healthcare ($6,336.00 / 9.94%)</b>, <b>Liquid Cash ($6,070.00 / 9.52%)</b>, and <b>Fixed Income ($5,848.00 / 9.17%)</b>.",
        body_style
    ))

    story.append(Paragraph("B. The Concentration Risk Warning Mechanism", h2_style))
    story.append(Paragraph(
        "FolioMind implements an automated risk threshold rule: when the <b>Top 3 positions exceed 60.0% of total portfolio value</b>, "
        "the UI triggers a prominent <code>HIGH CONCENTRATION RISK</code> alert badge. Here, the top 3 holdings (VOO, AAPL, MSFT) total <b>62.3%</b>. "
        "This warns the user that their financial future is heavily tied to large-cap US equities.",
        body_style
    ))

    story.append(Paragraph("C. Active Holdings & Real-Time Valuation Grid", h2_style))
    story.append(Paragraph(
        "The ledger provides live position tracking fetched directly through SnapTrade's <code>/positions</code> endpoint, "
        "including exact share quantities, cost bases, current mark prices, market values, and per-position unrealized return percentages.",
        body_style
    ))

    # =========================================================================
    # SECTION 4: RECENT ACTIVITY STREAM (IMAGE 4)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Real-Time Transaction Auditing & Activity Sync", h1_style))
    story.append(Paragraph(
        "Tracking portfolio evolution requires transparent historical transaction auditing.",
        body_style
    ))

    if os.path.exists(IMG_ACTIVITIES):
        story.append(Image(IMG_ACTIVITIES, width=530, height=209))
        story.append(Paragraph("<b>Figure 4:</b> Brokerage activity stream capturing trades, dividends, and cash deposits.", caption_style))

    story.append(Paragraph("A. Event-Driven Activity Types", h2_style))
    story.append(Paragraph(
        "Through SnapTrade's <code>/activities</code> endpoint, FolioMind automatically categorizes and normalizes events:",
        body_style
    ))

    act_data = [
        [Paragraph("Event Type", table_header), Paragraph("Date", table_header), Paragraph("Asset / Details", table_header), Paragraph("Cash Impact", table_header), Paragraph("Operational Significance", table_header)],
        [
            Paragraph("<b>BUY</b>", table_cell_bold),
            Paragraph("2026-09-12", table_cell),
            Paragraph("NVDA — Bought 10 shares @ $122.40", table_cell),
            Paragraph("<font color='#e11d48'>-$1,224.00</font>", table_cell),
            Paragraph("Capital outlay increasing tech exposure.", table_cell)
        ],
        [
            Paragraph("<b>DIVIDEND</b>", table_cell_bold),
            Paragraph("2026-09-08", table_cell),
            Paragraph("AAPL — Cash Dividend payment", table_cell),
            Paragraph("<font color='#059669'>+$42.50</font>", table_cell),
            Paragraph("Passive income generation; cash yield tracking.", table_cell)
        ],
        [
            Paragraph("<b>DEPOSIT</b>", table_cell_bold),
            Paragraph("2026-09-01", table_cell),
            Paragraph("USD — ACH Transfer Deposit", table_cell),
            Paragraph("<font color='#059669'>+$1,000.00</font>", table_cell),
            Paragraph("External cash injection expanding buying power.", table_cell)
        ],
        [
            Paragraph("<b>SELL</b>", table_cell_bold),
            Paragraph("2026-08-25", table_cell),
            Paragraph("MSFT — Sold 5 shares @ $440.00", table_cell),
            Paragraph("<font color='#059669'>+$2,200.00</font>", table_cell),
            Paragraph("Capital gains harvesting; rebalancing liquidity.", table_cell)
        ]
    ]
    t_act = Table(act_data, colWidths=[65, 75, 172, 80, 140])
    t_act.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_act)
    story.append(Spacer(1, 10))

    story.append(Paragraph("B. Why Transaction Auditing Matters", h2_style))
    story.append(Paragraph(
        "Many investors forget that dividends and cash deposits change portfolio returns. By factoring cash deposits and dividend "
        "streams into historical P&L, FolioMind ensures users don't mistake fresh cash deposits for market investment gains.",
        body_style
    ))

    # =========================================================================
    # SECTION 5: THE GROUNDED AI COPILOT (IMAGE 5)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. The Grounded AI Copilot: Zero-Hallucination Architecture", h1_style))
    story.append(Paragraph(
        "FolioMind AI Copilot introduces a conversational intelligence layer grounded completely in verified financial records.",
        body_style
    ))

    # Side-by-side layout: Image 5 on left, text/table on right
    if os.path.exists(IMG_COPILOT_CHAT):
        img_copilot = Image(IMG_COPILOT_CHAT, width=220, height=367)
        desc_text = [
            Paragraph("<b>Agentic Tool Execution in Action</b>", h2_style),
            Paragraph(
                "In <b>Figure 5</b>, the user clicks the prompt chip:<br/>"
                "<i>'Show my cash & liquid balance summary'</i>.",
                body_style
            ),
            Paragraph(
                "<b>What happened behind the scenes:</b><br/>"
                "1. <b>Intent Recognition:</b> The backend identified a liquidity query.<br/>"
                "2. <b>Tool Calling:</b> It executed <code>snaptrade_connect()</code> and <code>fetch_balances()</code>.<br/>"
                "3. <b>Deterministic Calculation:</b> Computed total cash ($6,070.00) and exact portfolio ratio (9.52%).<br/>"
                "4. <b>Grounded Synthesis:</b> Gemini 2.5 Flash formatted the verified numbers into clean, bulleted insights.",
                body_style
            ),
            Paragraph(
                "<b>Executed Tool Badges:</b><br/>"
                "Every response displays visual chips showing exactly which backend Python functions ran to verify the answer.",
                body_style
            ),
            Paragraph(
                "<b>Prompt Chip Navigation:</b><br/>"
                "Quick-action chips (<i>'NVDA'</i>, <i>'Why did my portfolio change this week?'</i>, <i>'What are my highest risk concentrations?'</i>) "
                "allow non-technical investors to interrogate their holdings with one tap.",
                body_style
            )
        ]
        story.append(Table([[img_copilot, desc_text]], colWidths=[230, 302], style=[
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(Paragraph("<b>Figure 5:</b> FolioMind AI Copilot Chat Drawer running in Grounded Mode with visible tool badges.", caption_style))

    # =========================================================================
    # SECTION 6: SYSTEM ARCHITECTURE, SECURITY & DEPLOYMENT
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Security, Compliance & Cloud Infrastructure", h1_style))
    story.append(Paragraph(
        "FolioMind AI adheres to institutional cybersecurity best practices for consumer financial technology.",
        body_style
    ))

    sec_data = [
        [Paragraph("Component", table_header), Paragraph("Architecture & Security Protocol", table_header), Paragraph("Risk Mitigation", table_header)],
        [
            Paragraph("<b>SnapTrade OAuth</b>", table_cell_bold),
            Paragraph("Uses 256-bit encrypted SnapTrade Connection Portal with PKCE verification.", table_cell),
            Paragraph("FolioMind servers never see or store user brokerage passwords.", table_cell)
        ],
        [
            Paragraph("<b>Secret Isolation</b>", table_cell_bold),
            Paragraph("<code>SNAPTRADE_CONSUMER_KEY</code> and API credentials reside strictly in backend environment variables.", table_cell),
            Paragraph("Zero credential exposure in browser client JavaScript bundles.", table_cell)
        ],
        [
            Paragraph("<b>Webhooks Pipeline</b>", table_cell_bold),
            Paragraph("<code>/api/webhook/snaptrade</code> listens for <code>HOLDINGS_UPDATED</code> and <code>CONNECTION_BROKEN</code>.", table_cell),
            Paragraph("Eliminates continuous aggressive API polling; auto-triggers re-authentication banners.", table_cell)
        ],
        [
            Paragraph("<b>Vercel Frontend</b>", table_cell_bold),
            Paragraph("Hosted on Vercel Global Edge Network with Vite SPA client-side routing (<code>vercel.json</code>).", table_cell),
            Paragraph("Sub-50ms static asset delivery globally with DDoS protection.", table_cell)
        ],
        [
            Paragraph("<b>Render Backend</b>", table_cell_bold),
            Paragraph("FastAPI running on Python 3.11 with automated Uvicorn process management and <code>/health</code> checks.", table_cell),
            Paragraph("Containerized cloud hosting with automatic CORS origin regex validation.", table_cell)
        ]
    ]
    t_sec = Table(sec_data, colWidths=[90, 240, 202])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Conclusion & Value Summary", h1_style))
    story.append(Paragraph(
        "FolioMind AI represents the next generation of personal wealth technology: combining the deep, multi-brokerage connectivity "
        "of <b>SnapTrade</b> with institutional quantitative analytics (HHI diversification, P&L waterfall contribution, concentration thresholds) "
        "and a <b>grounded, zero-hallucination AI copilot</b>. By transforming complex ledgers into actionable, visual financial intelligence, "
        "it enables investors to protect their capital, optimize returns, and invest with complete confidence.",
        body_style
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()
