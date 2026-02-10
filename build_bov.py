#!/usr/bin/env python3
"""
Build script for 9015 Owensmouth Ave BOV Web Presentation.
Generates a single self-contained index.html with embedded images, CSS, JS, and Leaflet maps.
"""

import base64
import os
import sys
import io
import math

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# CONFIGURATION
# ============================================================

BRAND_DIR = "C:\\Users\\gscher\\LAAA-AI-Prompts\\branding"
PHOTOS_DIR = "C:\\Users\\gscher\\temp-bov-read\\pictures"
OUTPUT_FILE = "C:\\Users\\gscher\\9015-owensmouth-bov\\index.html"

# Photo assignments
HERO_PHOTO = os.path.join(PHOTOS_DIR, "image (5).jpg")
GRID_PHOTOS = [
    os.path.join(PHOTOS_DIR, "image (4).jpg"),
    os.path.join(PHOTOS_DIR, "image (5).jpg"),
    os.path.join(PHOTOS_DIR, "image (6).jpg"),
    os.path.join(PHOTOS_DIR, "image (3).jpg"),
]

LOGO_WHITE = os.path.join(BRAND_DIR, "logos", "LAAA_Team_White.png")
HEADSHOT_GLEN = os.path.join(BRAND_DIR, "headshots", "Glen_Scher.png")
HEADSHOT_FILIP = os.path.join(BRAND_DIR, "headshots", "Filip_Niculete.png")
HEADSHOT_BLAKE = os.path.join(BRAND_DIR, "headshots", "Blake_Lewitt.png")


# ============================================================
# PROPERTY DATA
# ============================================================

PROPERTY = {
    "address": "9015 N. Owensmouth Avenue",
    "city_state_zip": "Canoga Park, CA 91304",
    "full_address": "9015 N. Owensmouth Avenue, Canoga Park, CA 91304",
    "apn": "2779-020-042",
    "year_built": 1972,
    "units": 20,
    "building_sf": 24330,
    "lot_sf": 48134,
    "lot_acres": 1.11,
    "stories": 2,
    "construction": "Wood Frame / Stucco",
    "zoning": "R3-1",
    "toc_tier": "Tier 3",
    "rent_control": "City of LA RSO",
    "parking": "Surface / Carport (est. 30 spaces)",
    "council_district": "To be verified",
    "community_plan": "Canoga Park-Winnetka-Woodland Hills-West Hills",
    "suggested_price": 4850000,
    "owner": "H & Y Investments LP",
    "ownership_since": "February 1986",
    "assessed_value": 1963391,
    "annual_tax": 27508,
    "existing_loan": 1800000,
}

# Coordinates
SUBJECT_COORDS = (34.233910, -118.601738)

# ============================================================
# RENT ROLL
# ============================================================

RENT_ROLL = [
    {"unit": "#101", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1830, "market_rent": 2950},
    {"unit": "#102", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 3000, "market_rent": 3200},
    {"unit": "#103", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 2040, "market_rent": 3200},
    {"unit": "#104", "type": "4 Bed / 2 Bath (Mgr)", "sf": 1350, "current_rent": 3200, "market_rent": 3200},
    {"unit": "#105", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 1859, "market_rent": 3200},
    {"unit": "#106", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 2160, "market_rent": 3200},
    {"unit": "#107", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 2040, "market_rent": 3200},
    {"unit": "#108", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 2040, "market_rent": 3200},
    {"unit": "#109", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 2900, "market_rent": 3200},
    {"unit": "#110", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 2110, "market_rent": 3200},
    {"unit": "#111", "type": "4 Bed / 2 Bath", "sf": 1350, "current_rent": 2180, "market_rent": 3200},
    {"unit": "#112", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1830, "market_rent": 2950},
    {"unit": "#113", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1830, "market_rent": 2950},
    {"unit": "#114", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1830, "market_rent": 2950},
    {"unit": "#115", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1830, "market_rent": 2950},
    {"unit": "#116", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1900, "market_rent": 2950},
    {"unit": "#117", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1762, "market_rent": 2950},
    {"unit": "#118", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1830, "market_rent": 2950},
    {"unit": "#119", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 2850, "market_rent": 2950},
    {"unit": "#120", "type": "3 Bed / 1.5 Bath", "sf": 1100, "current_rent": 1762, "market_rent": 2950},
]

# ============================================================
# OPERATING STATEMENT
# ============================================================

VACANCY_RATE = 0.03
OTHER_INCOME_ANNUAL = 7200

EXPENSES = {
    "Real Estate Taxes": 60625,
    "Insurance": 29330,
    "Utilities": 58800,
    "Trash Removal": 9600,
    "Repairs & Maintenance": 20000,
    "Contract Services": 6000,
    "General & Administrative": 3000,
    "On-Site Manager Rent Credit": 28800,
    "Operating Reserves": 2400,
}
MGMT_FEE_PCT = 0.04

# ============================================================
# FINANCING
# ============================================================

LTV = 0.60
INTEREST_RATE = 0.0575
AMORT_YEARS = 30
LOAN_TERM_YEARS = 3

# ============================================================
# SALE COMPS
# ============================================================

SALE_COMPS = [
    {
        "num": 1,
        "address": "20951 Roscoe Blvd",
        "city": "Canoga Park",
        "units": 34,
        "sf": 34370,
        "sale_date": "12/2025",
        "price": 7000000,
        "gross": 801564,
        "noi": 440860,
        "dom": "N/A",
        "notes": "Larger complex, similar vintage",
        "coords": (34.219995, -118.589690),
    },
    {
        "num": 2,
        "address": "8539 De Soto Ave",
        "city": "Canoga Park",
        "units": 28,
        "sf": 18094,
        "sale_date": "10/2025",
        "price": 4800000,
        "gross": 510924,
        "noi": 276000,
        "dom": "N/A",
        "notes": "1978 build, smaller units",
        "coords": (34.225394, -118.588617),
    },
    {
        "num": 3,
        "address": "21700 Roscoe Blvd",
        "city": "Canoga Park",
        "units": 28,
        "sf": 28821,
        "sale_date": "10/2025",
        "price": 4975000,
        "gross": 550901,
        "noi": 286468,
        "dom": "N/A",
        "notes": "1962 build, value-add play",
        "coords": (34.219642, -118.601763),
    },
]

# ============================================================
# RENT COMPS
# ============================================================

RENT_COMPS_3BR = [
    {"num": 1, "address": "6641 Etiwanda Ave", "type": "3/2", "sf": 1400, "rent": 2850, "date": "02/2025", "coords": (34.190852, -118.531766)},
    {"num": 2, "address": "10331 Lindley Ave #221", "type": "3/2", "sf": 1074, "rent": 2900, "date": "12/2025", "coords": (34.228866, -118.527359)},
    {"num": 3, "address": "10225 Lurline Ave #C", "type": "3/3", "sf": 1363, "rent": 2950, "date": "03/2025", "coords": (34.256428, -118.584290)},
    {"num": 4, "address": "8321 Burnet Ave #3", "type": "3/2", "sf": 1227, "rent": 3000, "date": "08/2025", "coords": (34.221862, -118.463454)},
    {"num": 5, "address": "8965 McLennan Ave", "type": "3/2", "sf": 1000, "rent": 3000, "date": "12/2025", "coords": (34.233652, -118.501025)},
    {"num": 6, "address": "17061 Roscoe Blvd #16", "type": "3/2", "sf": 1493, "rent": 3000, "date": "05/2025", "coords": (34.221289, -118.504775)},
    {"num": 7, "address": "20158 Cohasset St #9", "type": "3/2", "sf": 1340, "rent": 3000, "date": "02/2025", "coords": (34.207010, -118.573249)},
    {"num": 8, "address": "6621 Wilbur Ave #9", "type": "3/2", "sf": 1109, "rent": 3100, "date": "02/2026", "coords": (34.191031, -118.545197)},
]

RENT_COMPS_4BR = [
    {"num": 1, "address": "18512 Mayall St #E", "type": "4/3", "sf": 1370, "rent": 3700, "date": "12/2025", "coords": (34.253186, -118.536485)},
    {"num": 2, "address": "22730 Bassett St", "type": "4/3", "sf": 1598, "rent": 3700, "date": "05/2025", "coords": (34.195247, -118.636568)},
    {"num": 3, "address": "19505 Rinaldi St #61", "type": "4/3", "sf": 1637, "rent": 3740, "date": "03/2025", "coords": (34.274727, -118.557361)},
    {"num": 4, "address": "6620 N. Glade Ave", "type": "4/2", "sf": 1320, "rent": 3754, "date": "03/2025", "coords": (34.200891, -118.608137)},
    {"num": 5, "address": "8055 Canby Ave #1", "type": "4/3", "sf": 1717, "rent": 3850, "date": "10/2025", "coords": (34.216613, -118.534565)},
]

# ============================================================
# BUILDING SYSTEMS
# ============================================================

BUILDING_SYSTEMS = [
    ("Roof", "Flat, hot mop system (replaced)", "2008"),
    ("Plumbing", "Original 1972 (19 of 20 units); Unit 108 re-piped", "1972 / 2008"),
    ("HVAC", "Individual wall heaters (replaced in 13+ units); No central A/C", "2008-2012"),
    ("Electrical", "Original 1972 (19 of 20 units); Unit 108 fully rewired", "1972 / 2008"),
    ("Kitchen", "Original -- renovation opportunity at turnover", "1972"),
    ("Flooring", "Original -- renovation opportunity at turnover", "1972"),
    ("Windows & Doors", "Original; fire damage repairs to Units 107-109", "1972 / 2008"),
    ("Laundry", "To be verified", "--"),
    ("Parking", "Surface / carport (est. 30 spaces)", "1972"),
    ("Soft-Story Retrofit", "2 items on file; completion status to be verified with LADBS", "--"),
]

# ============================================================
# REGULATORY
# ============================================================

REGULATORY = [
    ("Rent Stabilization (RSO)", "Subject to City of Los Angeles RSO"),
    ("Zoning", "R3-1 (City of Los Angeles)"),
    ("Code Violations", "To be verified with LADBS"),
    ("Certificate of Occupancy", "To be verified with LADBS"),
    ("TOC Tier", "Tier 3 (50% density bonus)"),
    ("TOIA (Mixed Income)", "Tier 2"),
    ("Transit Priority Area", "Yes"),
    ("Housing Element Site", "Yes (HE Replacement Required)"),
    ("Opportunity Zone", "Yes"),
    ("Seismic Zone", "No Alquist-Priolo fault zone; no liquefaction risk"),
    ("Flood Zone", "FEMA Zone A (100-year, contained in channel)"),
    ("Tsunami Zone", "No"),
    ("Fire Hazard Zone", "No Very High Fire Hazard Severity Zone"),
    ("Landslide Zone", "No landslide susceptibility"),
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def encode_image(path):
    """Read an image file and return base64 data URI."""
    ext = os.path.splitext(path)[1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif"}
    mime_type = mime.get(ext.lstrip('.'), "image/jpeg")
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('ascii')
    return f"data:{mime_type};base64,{data}"


def fmt_price(val):
    """Format as $X,XXX,XXX."""
    return f"${val:,.0f}"


def fmt_pct(val):
    """Format as X.XX%."""
    return f"{val*100:.2f}%"


def fmt_num(val, decimals=0):
    """Format number with commas."""
    if decimals == 0:
        return f"{val:,.0f}"
    return f"{val:,.{decimals}f}"


def calc_monthly_payment(principal, annual_rate, years):
    """Calculate monthly mortgage payment."""
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)


def calc_loan_constant(annual_rate, years):
    """Calculate annual loan constant."""
    monthly = calc_monthly_payment(1, annual_rate, years)
    return monthly * 12


# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

# Rent roll aggregation
total_sf = sum(u["sf"] for u in RENT_ROLL)
total_current_monthly = sum(u["current_rent"] for u in RENT_ROLL)
total_market_monthly = sum(u["market_rent"] for u in RENT_ROLL)
current_gsr_annual = total_current_monthly * 12
market_gsr_annual = total_market_monthly * 12

# Income
current_vacancy = current_gsr_annual * VACANCY_RATE
current_eri = current_gsr_annual - current_vacancy
current_egi = current_eri + OTHER_INCOME_ANNUAL

market_vacancy = market_gsr_annual * VACANCY_RATE
market_eri = market_gsr_annual - market_vacancy
market_egi = market_eri + OTHER_INCOME_ANNUAL

# Expenses
fixed_expenses = sum(EXPENSES.values())
current_mgmt_fee = current_egi * MGMT_FEE_PCT
market_mgmt_fee = market_egi * MGMT_FEE_PCT
current_total_expenses = fixed_expenses + current_mgmt_fee
market_total_expenses = fixed_expenses + market_mgmt_fee

# NOI
current_noi = current_egi - current_total_expenses
market_noi = market_egi - market_total_expenses

# Financing
price = PROPERTY["suggested_price"]
loan_amount = price * LTV
down_payment = price * (1 - LTV)
loan_constant = calc_loan_constant(INTEREST_RATE, AMORT_YEARS)
annual_debt_service = loan_amount * loan_constant
monthly_payment = annual_debt_service / 12

# Returns at suggested price
current_cap = current_noi / price
market_cap = market_noi / price
current_grm = price / current_gsr_annual
market_grm = price / market_gsr_annual
price_per_unit = price / PROPERTY["units"]
price_per_sf = price / PROPERTY["building_sf"]
current_coc = (current_noi - annual_debt_service) / down_payment
market_coc = (market_noi - annual_debt_service) / down_payment
current_dcr = current_noi / annual_debt_service
market_dcr = market_noi / annual_debt_service

# Rent upside
rent_upside_pct = (total_market_monthly - total_current_monthly) / total_current_monthly
avg_current_rent_per_sf = total_current_monthly / total_sf
avg_market_rent_per_sf = total_market_monthly / total_sf

# Pricing matrix at $50K increments
MATRIX_LOW = 4600000
MATRIX_HIGH = 5100000
MATRIX_STEP = 50000

pricing_matrix = []
for p in range(MATRIX_LOW, MATRIX_HIGH + 1, MATRIX_STEP):
    loan = p * LTV
    dp = p * (1 - LTV)
    ds = loan * loan_constant
    row = {
        "price": p,
        "cap_current": current_noi / p,
        "cap_market": market_noi / p,
        "per_unit": p / PROPERTY["units"],
        "per_sf": p / PROPERTY["building_sf"],
        "grm": p / market_gsr_annual,
        "coc": (market_noi - ds) / dp,
        "dcr": market_noi / ds,
        "highlight": p == price,
    }
    pricing_matrix.append(row)


# ============================================================
# IMAGE ENCODING
# ============================================================

print("Encoding images...")
hero_b64 = encode_image(HERO_PHOTO)
grid_b64 = [encode_image(p) for p in GRID_PHOTOS]
logo_b64 = encode_image(LOGO_WHITE)
glen_b64 = encode_image(HEADSHOT_GLEN)
filip_b64 = encode_image(HEADSHOT_FILIP)
blake_b64 = encode_image(HEADSHOT_BLAKE)
print("Images encoded.")


# ============================================================
# HTML GENERATION
# ============================================================

def build_css():
    return """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; color: #333; background: #fff; line-height: 1.6; }
.page { max-width: 1100px; margin: 0 auto; }

/* Cover */
.cover { background: #1B3A5C; color: #fff; padding: 48px 40px; text-align: center; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.cover-logo { width: 320px; margin-bottom: 30px; }
.cover-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; color: #C5A258; margin-bottom: 20px; }
.cover-title { font-size: 42px; font-weight: 700; margin-bottom: 6px; }
.cover-address { font-size: 22px; font-weight: 300; color: rgba(255,255,255,0.8); margin-bottom: 24px; }
.cover-divider { width: 80px; height: 2px; background: #C5A258; margin: 0 auto 24px; }
.cover-price-label { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: #C5A258; margin-bottom: 8px; }
.cover-price { font-size: 48px; font-weight: 700; margin-bottom: 28px; }
.cover-stats { display: flex; gap: 36px; justify-content: center; margin-bottom: 28px; flex-wrap: wrap; }
.cover-stat { text-align: center; }
.cover-stat-value { font-size: 24px; font-weight: 700; display: block; }
.cover-stat-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: #C5A258; display: block; }
.client-greeting { font-size: 14px; font-weight: 300; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.7); margin-bottom: 28px; }
.cover-photo { width: 100%; max-height: 300px; object-fit: cover; border: 3px solid #C5A258; border-radius: 4px; margin-top: 10px; }

/* Sections */
.section { padding: 48px 40px; }
.section-alt { background: #f8f9fa; }
.section-title { font-size: 28px; font-weight: 700; color: #1B3A5C; margin-bottom: 6px; }
.section-subtitle { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: #C5A258; margin-bottom: 16px; }
.gold-divider { width: 60px; height: 3px; background: linear-gradient(to right, #C5A258, #d4b96a); margin-bottom: 28px; }

/* Photo Grid */
.photo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 28px; }
.photo-grid img { width: 100%; height: 220px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd; }

/* Narrative */
.narrative { margin-bottom: 28px; }
.narrative p { font-size: 14px; line-height: 1.7; margin-bottom: 14px; color: #444; }

/* Info Table (2-col key-value) */
.info-table { width: 100%; border-collapse: collapse; margin-bottom: 28px; }
.info-table td { padding: 10px 14px; font-size: 13px; border-bottom: 1px solid #e0e0e0; }
.info-table td:first-child { font-weight: 600; color: #1B3A5C; width: 40%; }

/* Data Tables */
table { width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px; }
th { background: #1B3A5C; color: #fff; padding: 10px 8px; text-align: left; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
td { padding: 9px 8px; border-bottom: 1px solid #e0e0e0; }
tr:nth-child(even) { background: #f5f5f5; }
tr.summary { background: #e8edf2; font-weight: 600; }
tr.highlight { background: #FFF8E7; border-left: 3px solid #C5A258; border-right: 3px solid #C5A258; }
tr.highlight td { font-weight: 600; }
.table-note { font-size: 11px; color: #888; font-style: italic; margin-top: -16px; margin-bottom: 24px; }
.table-scroll { margin-bottom: 24px; }

/* Metrics Grid */
.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 32px; }
.metric-card { background: #1B3A5C; color: #fff; padding: 20px 16px; border-radius: 6px; text-align: center; }
.metric-value { font-size: 28px; font-weight: 700; display: block; }
.metric-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #C5A258; margin-top: 6px; display: block; }
.metric-sub { font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 4px; display: block; }

/* Two Column */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin-bottom: 28px; }
.two-col h3 { font-size: 16px; font-weight: 600; color: #1B3A5C; margin-bottom: 12px; }

/* Sub headings */
.sub-heading { font-size: 18px; font-weight: 600; color: #1B3A5C; margin: 28px 0 12px; }

/* Condition Note */
.condition-note { background: #FFF8E7; border-left: 4px solid #C5A258; padding: 16px 20px; margin: 20px 0; border-radius: 0 4px 4px 0; font-size: 13px; line-height: 1.6; }
.condition-note strong { color: #1B3A5C; }

/* Buyer Profile Callout */
.buyer-profile { background: #f0f4f8; border-left: 4px solid #1B3A5C; padding: 20px 24px; margin: 24px 0; border-radius: 0 4px 4px 0; }
.buyer-profile-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #1B3A5C; margin-bottom: 12px; }
.buyer-profile ul { list-style: none; padding: 0; margin: 0; }
.buyer-profile li { padding: 8px 0; border-bottom: 1px solid #dce3eb; font-size: 14px; line-height: 1.6; color: #333; }
.buyer-profile li:last-child { border-bottom: none; }
.buyer-profile li strong { color: #1B3A5C; }
.buyer-profile .bp-closing { font-size: 13px; color: #555; margin-top: 12px; font-style: italic; }

/* Leaflet Maps */
.leaflet-map { height: 400px; border-radius: 4px; border: 1px solid #ddd; margin-bottom: 30px; z-index: 1; }
.map-fallback { display: none; font-size: 12px; color: #666; font-style: italic; margin-bottom: 30px; }

/* Footer */
.footer { background: #1B3A5C; color: #fff; padding: 48px 40px; text-align: center; }
.footer-logo { width: 280px; margin-bottom: 28px; }
.footer-team { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 28px; }
.footer-person { text-align: center; flex: 1; min-width: 240px; }
.footer-headshot { width: 60px; height: 60px; border-radius: 50%; border: 2px solid #C5A258; object-fit: cover; margin-bottom: 10px; }
.footer-name { font-size: 15px; font-weight: 600; display: block; }
.footer-title { font-size: 11px; color: #C5A258; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 6px; }
.footer-contact { font-size: 12px; color: rgba(255,255,255,0.7); line-height: 1.5; }
.footer-contact a { color: rgba(255,255,255,0.7); text-decoration: none; }
.footer-office { font-size: 12px; color: rgba(255,255,255,0.5); margin-bottom: 20px; }
.footer-disclaimer { font-size: 10px; color: rgba(255,255,255,0.4); line-height: 1.5; max-width: 800px; margin: 0 auto; }

/* Print */
@media print {
  body { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  .page { max-width: 100%; }
  .cover { min-height: auto !important; padding: 24px 36px; page-break-after: always; }
  .section { padding: 24px 36px; page-break-before: always; }
  table { page-break-inside: auto; font-size: 11px; }
  tr { page-break-inside: avoid; }
  thead { display: table-header-group; }
  .leaflet-map { display: none !important; }
  .map-fallback { display: block !important; }
  .metrics-grid { page-break-inside: avoid; }
  .condition-note { page-break-inside: avoid; }
  .buyer-profile { page-break-inside: avoid; }
  .sub-heading { page-break-after: avoid; }
  .section-title { page-break-after: avoid; }
  p { font-size: 12px; line-height: 1.5; }
  .footer { page-break-before: always; }
}

/* Mobile */
@media (max-width: 768px) {
  .cover { padding: 24px 20px; }
  .cover-logo { width: 200px; margin-bottom: 20px; }
  .cover-title { font-size: 28px; }
  .cover-address { font-size: 16px; margin-bottom: 16px; }
  .cover-price { font-size: 34px; margin-bottom: 16px; }
  .cover-stats { gap: 16px; flex-wrap: wrap; justify-content: center; margin-bottom: 20px; }
  .cover-stat-value { font-size: 20px; }
  .client-greeting { font-size: 13px; letter-spacing: 1.5px; }
  .cover-photo { max-height: 200px; }
  .section { padding: 30px 16px; }
  .section-title { font-size: 22px; }
  .photo-grid { grid-template-columns: 1fr; }
  .two-col { grid-template-columns: 1fr; gap: 16px; }
  .table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; margin-bottom: 24px; }
  .table-scroll table { min-width: 560px; margin-bottom: 0; }
  table { font-size: 12px; }
  th { font-size: 11px; padding: 8px 6px; }
  td { padding: 7px 6px; }
  .metrics-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .metric-card { padding: 14px 10px; }
  .metric-value { font-size: 22px; }
  .leaflet-map { height: 300px; }
  .footer { padding: 30px 16px; }
  .footer-logo { width: 200px; }
  .footer-team { flex-direction: column; gap: 20px; }
}
@media (max-width: 420px) {
  .cover-title { font-size: 24px; }
  .cover-price { font-size: 28px; }
  .metrics-grid { grid-template-columns: 1fr; }
  .section { padding: 24px 12px; }
  .footer { padding: 24px 12px; }
}
"""


def build_cover():
    return f"""
<div class="cover">
  <img src="{logo_b64}" alt="LAAA Team" class="cover-logo">
  <div class="cover-label">Broker Opinion of Value</div>
  <h1 class="cover-title">{PROPERTY['address']}</h1>
  <p class="cover-address">{PROPERTY['city_state_zip']}</p>
  <div class="cover-divider"></div>
  <div class="cover-price-label">Suggested List Price</div>
  <div class="cover-price">{fmt_price(PROPERTY['suggested_price'])}</div>
  <div class="cover-stats">
    <div class="cover-stat"><span class="cover-stat-value">{PROPERTY['units']}</span><span class="cover-stat-label">Units</span></div>
    <div class="cover-stat"><span class="cover-stat-value">{fmt_num(PROPERTY['building_sf'])}</span><span class="cover-stat-label">Square Feet</span></div>
    <div class="cover-stat"><span class="cover-stat-value">{PROPERTY['year_built']}</span><span class="cover-stat-label">Year Built</span></div>
    <div class="cover-stat"><span class="cover-stat-value">{PROPERTY['lot_acres']}</span><span class="cover-stat-label">Acres</span></div>
  </div>
  <p class="client-greeting" id="client-greeting">Prepared Exclusively for {PROPERTY['owner']}</p>
  <img src="{hero_b64}" alt="{PROPERTY['address']}" class="cover-photo">
</div>
"""


def build_property_overview():
    grid_imgs = "".join(f'<img src="{b}" alt="Property Photo">' for b in grid_b64)
    
    return f"""
<div class="section">
  <h2 class="section-title">Property Overview</h2>
  <div class="section-subtitle">{PROPERTY['full_address']}</div>
  <div class="gold-divider"></div>
  
  <div class="photo-grid">{grid_imgs}</div>
  
  <div class="narrative">
    <p>The LAAA Team is proud to present {PROPERTY['address']}, a {PROPERTY['units']}-unit townhouse-style multifamily community on an oversized {PROPERTY['lot_acres']}-acre parcel in the western San Fernando Valley's Canoga Park neighborhood. Constructed in {PROPERTY['year_built']}, the property comprises approximately {fmt_num(PROPERTY['building_sf'])} square feet across {PROPERTY['units']} two-story units averaging approximately 1,217 square feet each. The unit mix includes 10 three-bedroom/1.5-bath units at 1,100 SF and 10 four-bedroom/2-bath units at 1,350 SF, totaling 70 bedrooms and 40 bathrooms. This family-sized product type commands premium rents in a market heavily saturated with studio and one-bedroom inventory and historically experiences lower tenant turnover.</p>
    
    <p>The property is subject to the City of Los Angeles Rent Stabilization Ordinance (RSO). With nearly 40 years of continuous ownership under the current seller, in-place rents averaging {fmt_price(total_current_monthly / PROPERTY['units'])}/month are significantly below market levels, where comparable unrenovated three-bedroom units achieve $2,850-$3,100/month and four-bedroom units achieve $3,700-$3,850/month. Costa-Hawkins vacancy decontrol allows rents to reset to market upon unit turnover, creating a phased value-add opportunity that preserves cash flow during execution. Interior renovations at turnover, estimated at $20,000-$30,000 per unit, can drive an additional 25-35% rent premium. Current annual income totals {fmt_price(current_gsr_annual)} with a pro forma gross of {fmt_price(market_gsr_annual)}, representing {fmt_pct(rent_upside_pct)} upside.</p>
    
    <p><strong>Location.</strong> The subject property is situated in the western San Fernando Valley's Canoga Park neighborhood, a predominantly residential community experiencing significant investment momentum driven by its proximity to the Warner Center employment hub. The immediate area benefits from designation as a Transit Priority Area with access to the Metro G Line Bus Rapid Transit system, currently undergoing a $668M improvement project scheduled for completion in 2027 that will enhance connectivity to the Metro Red Line at North Hollywood. Canoga Park's western 91304 corridor provides convenient freeway access to the US-101 and SR-118. Ongoing area development, including 149 middle-income apartments under construction on Topanga Canyon Boulevard and a recently approved 211-unit mixed-use project on Vanowen Street, signals continued neighborhood evolution. With over 70% renter-occupied housing stock and a median home value of $847,600, the Canoga Park submarket demonstrates durable rental demand and sustained property appreciation.</p>
  </div>
  
  <div class="buyer-profile">
    <div class="buyer-profile-label">Target Buyer Profile</div>
    <ul>
      <li><strong>Value-Add Investors</strong> &mdash; Deep below-market rents ({fmt_pct(rent_upside_pct)} upside) with Costa-Hawkins vacancy decontrol provide a clear path to NOI growth through phased rent resets at turnover. Interior renovations at $20K-$30K per unit drive an additional 25-35% rent premium.</li>
      <li><strong>Development-Oriented Buyers</strong> &mdash; The oversized 1.11-acre parcel is dramatically underbuilt at 18 units/acre. R3-1 zoning supports ~60 units by right, while TOC Tier 3 allows ~90 units with an affordable set-aside&mdash;a 4.5x increase over current density. Stacked incentives (Opportunity Zone, TPA, Housing Element Site) enhance feasibility.</li>
      <li><strong>1031 Exchange Investors</strong> &mdash; Immediate cash flow from 20 occupied units with {fmt_pct(1 - VACANCY_RATE)} occupancy provides stable day-one income while executing a long-term value-add strategy. The family-sized product type experiences lower turnover than studio/1BR inventory.</li>
      <li><strong>Small Portfolio Investors</strong> &mdash; The {fmt_price(price)} price point ({fmt_price(price_per_unit)}/unit) offers an accessible entry into the West Valley multifamily market at a basis well below comparable locations, with multiple paths to value creation.</li>
    </ul>
    <p class="bp-closing">Broad appeal across buyer segments supports competitive pricing and a short expected marketing period.</p>
  </div>
  
  <table class="info-table">
    <tr><td>Address</td><td>{PROPERTY['full_address']}</td></tr>
    <tr><td>APN</td><td>{PROPERTY['apn']}</td></tr>
    <tr><td>Year Built</td><td>{PROPERTY['year_built']}</td></tr>
    <tr><td>Total Units</td><td>{PROPERTY['units']}</td></tr>
    <tr><td>Building Size</td><td>&plusmn;{fmt_num(PROPERTY['building_sf'])} SF</td></tr>
    <tr><td>Lot Size</td><td>&plusmn;{fmt_num(PROPERTY['lot_sf'])} SF / {PROPERTY['lot_acres']} Acres</td></tr>
    <tr><td>Construction</td><td>{PROPERTY['construction']}</td></tr>
    <tr><td>Stories</td><td>{PROPERTY['stories']}</td></tr>
    <tr><td>Zoning</td><td>{PROPERTY['zoning']}</td></tr>
    <tr><td>TOC Tier</td><td>{PROPERTY['toc_tier']}</td></tr>
    <tr><td>Rent Control</td><td>{PROPERTY['rent_control']}</td></tr>
    <tr><td>Parking</td><td>{PROPERTY['parking']}</td></tr>
    <tr><td>Community Plan</td><td>{PROPERTY['community_plan']}</td></tr>
  </table>
</div>
"""


def build_building_systems():
    rows = ""
    for system, condition, year in BUILDING_SYSTEMS:
        rows += f"<tr><td>{system}</td><td>{condition}</td><td>{year}</td></tr>\n"
    return f"""
<div class="section section-alt">
  <h2 class="section-title">Building Systems & Capital Improvements</h2>
  <div class="section-subtitle">{PROPERTY['full_address']}</div>
  <div class="gold-divider"></div>
  <div class="table-scroll">
  <table>
    <thead><tr><th>System</th><th>Condition / Status</th><th>Year</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
  <p class="table-note">Capital improvement data sourced from LADBS permit records and property inspection. Buyers should verify all systems during due diligence.</p>
</div>
"""


def build_regulatory():
    rows = ""
    for item, status in REGULATORY:
        rows += f"<tr><td>{item}</td><td>{status}</td></tr>\n"
    return f"""
<div class="section">
  <h2 class="section-title">Regulatory & Compliance Summary</h2>
  <div class="section-subtitle">{PROPERTY['full_address']}</div>
  <div class="gold-divider"></div>
  <div class="table-scroll">
  <table>
    <thead><tr><th>Item</th><th>Status</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
  <p class="table-note">Sources: ZIMAS, LADBS, FEMA, City of Los Angeles Planning Department. Data as of February 2026.</p>
  <div class="condition-note">
    <strong>RSO & Vacancy Decontrol.</strong> The property is subject to the City of Los Angeles Rent Stabilization Ordinance. Under Costa-Hawkins, landlords may reset rents to market upon voluntary vacancy. With nearly 40 years of continuous ownership, in-place rents are substantially below market, creating significant upside upon turnover. Buyers should also verify the soft-story retrofit status with LADBS, as the property's pre-1978 wood-frame construction and likely tuck-under parking configuration may trigger mandatory retrofit requirements.
  </div>
  <div class="condition-note">
    <strong>Flood Zone.</strong> The property carries a FEMA Zone A (100-year flood, contained in channel) designation, which may affect insurance costs. Buyers should obtain a flood insurance quote during due diligence.
  </div>
</div>
"""


def build_transaction_history():
    return f"""
<div class="section section-alt">
  <h2 class="section-title">Transaction History</h2>
  <div class="section-subtitle">{PROPERTY['full_address']}</div>
  <div class="gold-divider"></div>
  <div class="table-scroll">
  <table>
    <thead><tr><th>Date</th><th>Event</th><th>Amount</th><th>$/Unit</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>Feb 1986</td><td>Acquisition</td><td>N/A</td><td>N/A</td><td>Current owner (H & Y Investments LP) acquired property</td></tr>
      <tr><td>Dec 2021</td><td>Refinance</td><td>$1,800,000</td><td>$90,000</td><td>Symetra Life Insurance Co.</td></tr>
      <tr><td>2025</td><td>Assessed Value</td><td>{fmt_price(PROPERTY['assessed_value'])}</td><td>{fmt_price(PROPERTY['assessed_value'] / PROPERTY['units'])}</td><td>Total assessed value; annual tax: {fmt_price(PROPERTY['annual_tax'])}</td></tr>
      <tr class="highlight"><td>2026</td><td>Suggested List Price</td><td>{fmt_price(price)}</td><td>{fmt_price(price_per_unit)}</td><td>LAAA Team Broker Opinion of Value</td></tr>
    </tbody>
  </table>
  </div>
  <div class="narrative">
    <p>The property has been held by the current ownership entity since February 1986&mdash;approximately 40 years of continuous ownership. The low assessed value of {fmt_price(PROPERTY['assessed_value'])} reflects the Proposition 13 base and confirms long-term hold. The suggested list price of {fmt_price(price)} ({fmt_price(price_per_unit)}/unit) represents a significant premium to the tax basis, justified by the property's deep below-market rents, oversized lot with exceptional density upside, and multiple layers of development incentives.</p>
  </div>
</div>
"""


def build_sale_comps():
    rows = ""
    prices = []
    per_units = []
    caps = []
    grms = []
    for c in SALE_COMPS:
        pu = c["price"] / c["units"]
        psf = c["price"] / c["sf"]
        cap = c["noi"] / c["price"]
        grm = c["price"] / c["gross"]
        prices.append(c["price"])
        per_units.append(pu)
        caps.append(cap)
        grms.append(grm)
        rows += f'<tr><td>{c["num"]}</td><td>{c["address"]}, {c["city"]}</td><td>{c["units"]}</td><td>{c["sale_date"]}</td><td>{fmt_price(c["price"])}</td><td>{fmt_price(pu)}</td><td>{fmt_pct(cap)}</td><td>{grm:.2f}x</td><td>{c["dom"]}</td><td>{c["notes"]}</td></tr>\n'
    
    avg_price = sum(prices)/len(prices)
    avg_pu = sum(per_units)/len(per_units)
    avg_cap = sum(caps)/len(caps)
    avg_grm = sum(grms)/len(grms)
    rows += f'<tr class="summary"><td></td><td>Average</td><td></td><td></td><td>{fmt_price(avg_price)}</td><td>{fmt_price(avg_pu)}</td><td>{fmt_pct(avg_cap)}</td><td>{avg_grm:.2f}x</td><td></td><td></td></tr>'
    
    # Map markers JS
    markers_js = ""
    for c in SALE_COMPS:
        pu = c["price"] / c["units"]
        markers_js += f"""
        L.marker([{c['coords'][0]}, {c['coords'][1]}], {{icon: L.divIcon({{className: '', html: '<div style="background:#1B3A5C;color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,0.3);">{c["num"]}</div>', iconSize: [26, 26], iconAnchor: [13, 13]}}) }}).addTo(saleMap).bindPopup('<strong>{c["address"]}</strong><br>{c["units"]} units | {fmt_price(c["price"])} | {fmt_price(pu)}/unit');
        """
    
    return f"""
<div class="section">
  <h2 class="section-title">Comparable Sales (Closed)</h2>
  <div class="section-subtitle">{PROPERTY['full_address']}</div>
  <div class="gold-divider"></div>
  <div id="saleMap" class="leaflet-map"></div>
  <p class="map-fallback">Interactive map available at the live URL.</p>
  <div class="table-scroll">
  <table>
    <thead><tr><th>#</th><th>Address</th><th>Units</th><th>Sale Date</th><th>Price</th><th>$/Unit</th><th>Cap</th><th>GRM</th><th>DOM</th><th>Notes</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
  <p class="table-note">Comparable sales within Canoga Park submarket, 20+ units, closed Q4 2025. Data from public records and CoStar.</p>
  <div class="narrative">
    <p>The three comparable sales bracket the subject's pricing at {fmt_price(price)} ({fmt_price(price_per_unit)}/unit). The average closed sale transacted at {fmt_price(avg_pu)}/unit, with capitalization rates ranging from {fmt_pct(min(caps))} to {fmt_pct(max(caps))}. The subject's suggested pricing at {fmt_pct(market_cap)} pro forma cap rate reflects its deep below-market rents and exceptional density upside that is not available in the comparable set.</p>
    <p>The 20951 Roscoe sale at {fmt_price(SALE_COMPS[0]['price'])} ({fmt_price(SALE_COMPS[0]['price']/SALE_COMPS[0]['units'])}/unit) for a 34-unit complex represents the upper end of the submarket, while the De Soto and Roscoe sales in October 2025 establish a baseline of approximately {fmt_price(SALE_COMPS[1]['price']/SALE_COMPS[1]['units'])}-{fmt_price(SALE_COMPS[2]['price']/SALE_COMPS[2]['units'])}/unit for 28-unit properties. The subject's larger unit sizes (avg. 1,217 SF vs. typical 600-800 SF) and family-oriented product type support premium pricing on a per-unit basis.</p>
  </div>
  <script>
    var saleMap = L.map('saleMap').setView([{SUBJECT_COORDS[0]}, {SUBJECT_COORDS[1]}], 13);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ attribution: '&copy; OpenStreetMap contributors' }}).addTo(saleMap);
    L.marker([{SUBJECT_COORDS[0]}, {SUBJECT_COORDS[1]}], {{icon: L.divIcon({{className: '', html: '<div style="background:#C5A258;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.4);">&#9733;</div>', iconSize: [32, 32], iconAnchor: [16, 16]}}) }}).addTo(saleMap).bindPopup('<strong>Subject: {PROPERTY["address"]}</strong><br>{PROPERTY["units"]} units | {fmt_price(price)}');
    {markers_js}
    var saleBounds = L.latLngBounds([[{SUBJECT_COORDS[0]},{SUBJECT_COORDS[1]}],{','.join(f'[{c["coords"][0]},{c["coords"][1]}]' for c in SALE_COMPS)}]);
    saleMap.fitBounds(saleBounds.pad(0.15));
  </script>
</div>
"""


def build_rent_comps():
    # 3BR table
    rows_3br = ""
    rents_3br = []
    for c in RENT_COMPS_3BR:
        psf = c["rent"] / c["sf"]
        rents_3br.append(c["rent"])
        rows_3br += f'<tr><td>{c["num"]}</td><td>{c["address"]}</td><td>{c["type"]}</td><td>{fmt_num(c["sf"])}</td><td>{fmt_price(c["rent"])}</td><td>${psf:.2f}</td></tr>\n'
    avg_3br = sum(rents_3br) / len(rents_3br)
    avg_3br_sf = sum(c["rent"]/c["sf"] for c in RENT_COMPS_3BR) / len(RENT_COMPS_3BR)
    rows_3br += f'<tr class="summary"><td></td><td>Average</td><td></td><td></td><td>{fmt_price(avg_3br)}</td><td>${avg_3br_sf:.2f}</td></tr>'
    
    # 4BR table
    rows_4br = ""
    rents_4br = []
    for c in RENT_COMPS_4BR:
        psf = c["rent"] / c["sf"]
        rents_4br.append(c["rent"])
        rows_4br += f'<tr><td>{c["num"]}</td><td>{c["address"]}</td><td>{c["type"]}</td><td>{fmt_num(c["sf"])}</td><td>{fmt_price(c["rent"])}</td><td>${psf:.2f}</td></tr>\n'
    avg_4br = sum(rents_4br) / len(rents_4br)
    avg_4br_sf = sum(c["rent"]/c["sf"] for c in RENT_COMPS_4BR) / len(RENT_COMPS_4BR)
    rows_4br += f'<tr class="summary"><td></td><td>Average</td><td></td><td></td><td>{fmt_price(avg_4br)}</td><td>${avg_4br_sf:.2f}</td></tr>'
    
    # Map markers
    all_rent_comps = RENT_COMPS_3BR + RENT_COMPS_4BR
    markers_js = ""
    for i, c in enumerate(all_rent_comps, 1):
        markers_js += f"""
        L.marker([{c['coords'][0]}, {c['coords'][1]}], {{icon: L.divIcon({{className: '', html: '<div style="background:#1B3A5C;color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,0.3);">{i}</div>', iconSize: [26, 26], iconAnchor: [13, 13]}}) }}).addTo(rentMap).bindPopup('<strong>{c["address"]}</strong><br>{c["type"]} | {fmt_num(c["sf"])} SF | {fmt_price(c["rent"])}/mo');
        """
    
    bounds_list = f"[{SUBJECT_COORDS[0]},{SUBJECT_COORDS[1]}]," + ",".join(f'[{c["coords"][0]},{c["coords"][1]}]' for c in all_rent_comps)
    
    subject_3br_rent = 2950
    subject_4br_rent = 3200
    
    return f"""
<div class="section section-alt">
  <h2 class="section-title">Rent Comparables</h2>
  <div class="section-subtitle">{PROPERTY['full_address']}</div>
  <div class="gold-divider"></div>
  <div id="rentMap" class="leaflet-map"></div>
  <p class="map-fallback">Interactive map available at the live URL.</p>
  
  <h3 class="sub-heading">3-Bedroom Comparables</h3>
  <div class="table-scroll">
  <table>
    <thead><tr><th>#</th><th>Address</th><th>Type</th><th>SF</th><th>Rent</th><th>$/SF</th></tr></thead>
    <tbody>{rows_3br}</tbody>
  </table>
  </div>
  
  <h3 class="sub-heading">4-Bedroom Comparables</h3>
  <div class="table-scroll">
  <table>
    <thead><tr><th>#</th><th>Address</th><th>Type</th><th>SF</th><th>Rent</th><th>$/SF</th></tr></thead>
    <tbody>{rows_4br}</tbody>
  </table>
  </div>
  <p class="table-note">Rent comparables from MLS leased data within the western San Fernando Valley, Q1 2025 - Q1 2026.</p>
  <div class="narrative">
    <p>The rent comp survey confirms strong market support for the subject's pro forma rent assumptions. Three-bedroom units in the submarket achieve an average of {fmt_price(avg_3br)}/month (${avg_3br_sf:.2f}/SF), supporting the subject's market rent assumption of {fmt_price(subject_3br_rent)}/month for its 1,100 SF 3BR/1.5BA units. The subject's current average 3BR rent of $1,925/month represents a {((subject_3br_rent - 1925) / 1925 * 100):.0f}% discount to market.</p>
    <p>Four-bedroom units command a significant premium, averaging {fmt_price(avg_4br)}/month (${ avg_4br_sf:.2f}/SF). The subject's market rent assumption of {fmt_price(subject_4br_rent)}/month for its 1,350 SF 4BR/2BA units is conservatively underwritten relative to the comp average, providing a buffer for the underwriting. Current in-place 4BR rents averaging $2,353/month represent a {((subject_4br_rent - 2353) / 2353 * 100):.0f}% discount to the pro forma assumption. The phased nature of RSO turnover ensures cash flow stability during the value-add execution.</p>
  </div>
  <script>
    var rentMap = L.map('rentMap').setView([{SUBJECT_COORDS[0]}, {SUBJECT_COORDS[1]}], 12);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ attribution: '&copy; OpenStreetMap contributors' }}).addTo(rentMap);
    L.marker([{SUBJECT_COORDS[0]}, {SUBJECT_COORDS[1]}], {{icon: L.divIcon({{className: '', html: '<div style="background:#C5A258;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.4);">&#9733;</div>', iconSize: [32, 32], iconAnchor: [16, 16]}}) }}).addTo(rentMap).bindPopup('<strong>Subject: {PROPERTY["address"]}</strong><br>{PROPERTY["units"]} units');
    {markers_js}
    var rentBounds = L.latLngBounds([{bounds_list}]);
    rentMap.fitBounds(rentBounds.pad(0.1));
  </script>
</div>
"""


def build_financial_analysis():
    # Rent roll table rows
    rr_rows = ""
    for u in RENT_ROLL:
        cr_sf = u["current_rent"] / u["sf"]
        mr_sf = u["market_rent"] / u["sf"]
        rr_rows += f'<tr><td>{u["unit"]}</td><td>{u["type"]}</td><td>{fmt_num(u["sf"])}</td><td>{fmt_price(u["current_rent"])}</td><td>${cr_sf:.2f}</td><td>{fmt_price(u["market_rent"])}</td><td>${mr_sf:.2f}</td></tr>\n'
    avg_cr = total_current_monthly / PROPERTY["units"]
    avg_mr = total_market_monthly / PROPERTY["units"]
    rr_rows += f'<tr class="summary"><td></td><td>Totals / Avg</td><td>{fmt_num(total_sf)}</td><td>{fmt_price(total_current_monthly)}</td><td>${avg_current_rent_per_sf:.2f}</td><td>{fmt_price(total_market_monthly)}</td><td>${avg_market_rent_per_sf:.2f}</td></tr>'
    
    # Operating statement
    current_expense_pct = current_total_expenses / current_egi * 100 if current_egi else 0
    market_expense_pct = market_total_expenses / market_egi * 100 if market_egi else 0
    
    # Pricing matrix rows
    matrix_rows = ""
    for row in pricing_matrix:
        hl = ' class="highlight"' if row["highlight"] else ""
        matrix_rows += f'<tr{hl}><td>{fmt_price(row["price"])}</td><td>{fmt_pct(row["cap_market"])}</td><td>{fmt_price(row["per_unit"])}</td><td>${row["per_sf"]:.2f}</td><td>{row["grm"]:.2f}x</td><td>{fmt_pct(row["coc"])}</td><td>{row["dcr"]:.2f}x</td></tr>\n'
    
    return f"""
<div class="section section-alt">
  <h2 class="section-title">Financial Analysis</h2>
  <div class="section-subtitle">{PROPERTY['full_address']}</div>
  <div class="gold-divider"></div>
  
  <div class="metrics-grid">
    <div class="metric-card">
      <span class="metric-value">{fmt_pct(current_cap)}</span>
      <span class="metric-label">Current Cap Rate</span>
      <span class="metric-sub">{fmt_pct(market_cap)} Market</span>
    </div>
    <div class="metric-card">
      <span class="metric-value">{fmt_price(price_per_unit)}</span>
      <span class="metric-label">Price Per Unit</span>
      <span class="metric-sub">${price_per_sf:.2f}/SF</span>
    </div>
    <div class="metric-card">
      <span class="metric-value">{fmt_pct(rent_upside_pct)}</span>
      <span class="metric-label">Rent Upside</span>
      <span class="metric-sub">${avg_current_rent_per_sf:.2f} &rarr; ${avg_market_rent_per_sf:.2f}/SF</span>
    </div>
  </div>
  
  <h3 class="sub-heading">Unit Mix & Rent Roll</h3>
  <div class="table-scroll">
  <table>
    <thead><tr><th>Unit</th><th>Type</th><th>SF</th><th>Current Rent</th><th>Rent/SF</th><th>Market Rent</th><th>Mkt Rent/SF</th></tr></thead>
    <tbody>{rr_rows}</tbody>
  </table>
  </div>
  
  <div class="two-col">
    <div>
      <h3>Operating Statement</h3>
      <table>
        <thead><tr><th>Income</th><th>Current</th><th>Pro Forma</th></tr></thead>
        <tbody>
          <tr><td>Gross Scheduled Rent</td><td>{fmt_price(current_gsr_annual)}</td><td>{fmt_price(market_gsr_annual)}</td></tr>
          <tr><td>Less: Vacancy ({fmt_pct(VACANCY_RATE)})</td><td>({fmt_price(current_vacancy)})</td><td>({fmt_price(market_vacancy)})</td></tr>
          <tr><td>Effective Rental Income</td><td>{fmt_price(current_eri)}</td><td>{fmt_price(market_eri)}</td></tr>
          <tr><td>Other Income</td><td>{fmt_price(OTHER_INCOME_ANNUAL)}</td><td>{fmt_price(OTHER_INCOME_ANNUAL)}</td></tr>
          <tr class="summary"><td><strong>Effective Gross Income</strong></td><td><strong>{fmt_price(current_egi)}</strong></td><td><strong>{fmt_price(market_egi)}</strong></td></tr>
        </tbody>
      </table>
      <table>
        <thead><tr><th>Expenses</th><th>Current</th><th>Pro Forma</th></tr></thead>
        <tbody>
          <tr><td>Real Estate Taxes</td><td>{fmt_price(EXPENSES['Real Estate Taxes'])}</td><td>{fmt_price(EXPENSES['Real Estate Taxes'])}</td></tr>
          <tr><td>Insurance</td><td>{fmt_price(EXPENSES['Insurance'])}</td><td>{fmt_price(EXPENSES['Insurance'])}</td></tr>
          <tr><td>Utilities</td><td>{fmt_price(EXPENSES['Utilities'])}</td><td>{fmt_price(EXPENSES['Utilities'])}</td></tr>
          <tr><td>Trash Removal</td><td>{fmt_price(EXPENSES['Trash Removal'])}</td><td>{fmt_price(EXPENSES['Trash Removal'])}</td></tr>
          <tr><td>Repairs & Maintenance</td><td>{fmt_price(EXPENSES['Repairs & Maintenance'])}</td><td>{fmt_price(EXPENSES['Repairs & Maintenance'])}</td></tr>
          <tr><td>Contract Services</td><td>{fmt_price(EXPENSES['Contract Services'])}</td><td>{fmt_price(EXPENSES['Contract Services'])}</td></tr>
          <tr><td>General & Administrative</td><td>{fmt_price(EXPENSES['General & Administrative'])}</td><td>{fmt_price(EXPENSES['General & Administrative'])}</td></tr>
          <tr><td>On-Site Manager Credit</td><td>{fmt_price(EXPENSES['On-Site Manager Rent Credit'])}</td><td>{fmt_price(EXPENSES['On-Site Manager Rent Credit'])}</td></tr>
          <tr><td>Operating Reserves</td><td>{fmt_price(EXPENSES['Operating Reserves'])}</td><td>{fmt_price(EXPENSES['Operating Reserves'])}</td></tr>
          <tr><td>Management Fee ({fmt_pct(MGMT_FEE_PCT)})</td><td>{fmt_price(current_mgmt_fee)}</td><td>{fmt_price(market_mgmt_fee)}</td></tr>
          <tr class="summary"><td><strong>Total Expenses</strong></td><td><strong>{fmt_price(current_total_expenses)}</strong></td><td><strong>{fmt_price(market_total_expenses)}</strong></td></tr>
          <tr><td>Expenses % of EGI</td><td>{current_expense_pct:.1f}%</td><td>{market_expense_pct:.1f}%</td></tr>
          <tr class="summary"><td><strong>Net Operating Income</strong></td><td><strong>{fmt_price(current_noi)}</strong></td><td><strong>{fmt_price(market_noi)}</strong></td></tr>
        </tbody>
      </table>
    </div>
    <div>
      <h3>Returns at Asking Price</h3>
      <table>
        <thead><tr><th>Metric</th><th>Current</th><th>Market</th></tr></thead>
        <tbody>
          <tr><td>Cap Rate</td><td>{fmt_pct(current_cap)}</td><td>{fmt_pct(market_cap)}</td></tr>
          <tr><td>GRM</td><td>{current_grm:.2f}x</td><td>{market_grm:.2f}x</td></tr>
          <tr><td>Cash-on-Cash</td><td>{fmt_pct(current_coc)}</td><td>{fmt_pct(market_coc)}</td></tr>
          <tr><td>Debt Coverage Ratio</td><td>{current_dcr:.2f}x</td><td>{market_dcr:.2f}x</td></tr>
        </tbody>
      </table>
      <h3>Financing Terms</h3>
      <table>
        <tbody>
          <tr><td>Purchase Price</td><td>{fmt_price(price)}</td></tr>
          <tr><td>Down Payment ({fmt_pct(1-LTV)})</td><td>{fmt_price(down_payment)}</td></tr>
          <tr><td>Loan Amount ({fmt_pct(LTV)})</td><td>{fmt_price(loan_amount)}</td></tr>
          <tr><td>Interest Rate</td><td>{fmt_pct(INTEREST_RATE)}</td></tr>
          <tr><td>Amortization</td><td>{AMORT_YEARS} Years</td></tr>
          <tr><td>Annual Debt Service</td><td>{fmt_price(annual_debt_service)}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  
  <h3 class="sub-heading">Pricing Matrix</h3>
  <div class="table-scroll">
  <table>
    <thead><tr><th>Price</th><th>Cap Rate (Mkt)</th><th>$/Unit</th><th>$/SF</th><th>GRM</th><th>Cash-on-Cash</th><th>DCR</th></tr></thead>
    <tbody>{matrix_rows}</tbody>
  </table>
  </div>
  <p class="table-note">Highlighted row indicates suggested list price. Returns based on {fmt_pct(LTV)} LTV, {fmt_pct(INTEREST_RATE)} interest rate, {AMORT_YEARS}-year amortization. Cap rate and GRM based on pro forma income.</p>
  
  <div class="narrative">
    <p>At the suggested list price of {fmt_price(price)}, the property delivers a {fmt_pct(market_cap)} pro forma cap rate and {market_grm:.2f}x GRM on market rents of {fmt_price(market_gsr_annual)} annually. The {fmt_pct(rent_upside_pct)} rent upside from current to market levels represents the primary value driver, with additional upside available through interior renovations and RUBS implementation. With {fmt_pct(LTV)} leverage at {fmt_pct(INTEREST_RATE)}, the investment generates a {fmt_pct(market_coc)} cash-on-cash return at pro forma with a comfortable {market_dcr:.2f}x debt coverage ratio.</p>
    <p>The pricing reflects the property's unique combination of immediate cash flow, phased value-add potential, and exceptional long-term density upside through TOC Tier 3 and Opportunity Zone incentives. At {fmt_price(price_per_unit)}/unit, the basis is well below comparable West Valley multifamily locations and the replacement cost for family-sized townhome product.</p>
  </div>
</div>
"""


def build_footer():
    return f"""
<div class="footer">
  <img src="{logo_b64}" alt="LAAA Team" class="footer-logo">
  <div class="footer-team">
    <div class="footer-person">
      <img src="{glen_b64}" alt="Glen Scher" class="footer-headshot">
      <span class="footer-name">Glen Scher</span>
      <span class="footer-title">Senior Managing Director Investments</span>
      <div class="footer-contact">
        <a href="tel:8182122808">(818) 212-2808</a><br>
        <a href="mailto:Glen.Scher@marcusmillichap.com">Glen.Scher@marcusmillichap.com</a><br>
        License: CA 01962976
      </div>
    </div>
    <div class="footer-person">
      <img src="{filip_b64}" alt="Filip Niculete" class="footer-headshot">
      <span class="footer-name">Filip Niculete</span>
      <span class="footer-title">Senior Managing Director Investments</span>
      <div class="footer-contact">
        <a href="tel:8182122748">(818) 212-2748</a><br>
        <a href="mailto:Filip.Niculete@marcusmillichap.com">Filip.Niculete@marcusmillichap.com</a><br>
        License: CA 01905352
      </div>
    </div>
    <div class="footer-person">
      <img src="{blake_b64}" alt="Blake Lewitt" class="footer-headshot">
      <span class="footer-name">Blake Lewitt</span>
      <span class="footer-title">Associate Investments</span>
      <div class="footer-contact">
        <a href="tel:8186656908">(818) 665-6908</a><br>
        <a href="mailto:Blake.Lewitt@marcusmillichap.com">Blake.Lewitt@marcusmillichap.com</a>
      </div>
    </div>
  </div>
  <p class="footer-office">LA Apartment Advisors (LAAA) | 16830 Ventura Blvd, Ste. 100, Encino, CA 91436 | marcusmillichap.com/laaa-team</p>
  <p class="footer-disclaimer">This information has been secured from sources we believe to be reliable, but we make no representations or warranties, expressed or implied, as to the accuracy of the information. Buyer must verify the information and bears all risk for any inaccuracies. Marcus & Millichap Real Estate Investment Services, Inc. | License: CA 01930580.</p>
</div>
"""


def build_html():
    css = build_css()
    cover = build_cover()
    overview = build_property_overview()
    systems = build_building_systems()
    regulatory = build_regulatory()
    history = build_transaction_history()
    sales = build_sale_comps()
    rents = build_rent_comps()
    financials = build_financial_analysis()
    footer = build_footer()
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BOV - {PROPERTY['address']}, {PROPERTY['city_state_zip']}</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>{css}</style>
</head>
<body>
<div class="page">
{cover}
{overview}
{systems}
{regulatory}
{history}
{sales}
{rents}
{financials}
{footer}
</div>
<script>
var params = new URLSearchParams(window.location.search);
var client = params.get('client');
if (client) {{
  var el = document.getElementById('client-greeting');
  if (el) el.textContent = 'Prepared Exclusively for ' + client;
}}
</script>
</body>
</html>"""


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("Building BOV presentation...")
    html = build_html()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"Generated: {OUTPUT_FILE}")
    print(f"File size: {size_kb:.1f} KB")
    print("Done!")
