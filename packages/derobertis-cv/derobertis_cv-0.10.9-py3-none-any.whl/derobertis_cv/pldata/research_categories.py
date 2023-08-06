from derobertis_cv.models.category import CategoryModel
from derobertis_cv.pltemplates.logo import svg_text

_CATEGORIES = [
    CategoryModel('Market Intervention', logo_fa_icon_class_str='fas fa-hand-holding-usd'),
    CategoryModel('Behavioral Finance', logo_fa_icon_class_str='fas fa-brain'),
    CategoryModel('Alternative Assets', logo_fa_icon_class_str='fab fa-ethereum'),
    CategoryModel('Crypto-assets', logo_fa_icon_class_str='fab fa-bitcoin'),
    CategoryModel('Asset Pricing', logo_fa_icon_class_str='fas fa-search-dollar'),
    CategoryModel('Portfolio Analysis', logo_svg_text=svg_text('portfolio-analysis-logo.svg')),
    CategoryModel('Investor Attention', logo_fa_icon_class_str='fas fa-exclamation'),
    CategoryModel('Investor Sentiment', logo_fa_icon_class_str='far fa-smile'),
    CategoryModel('Monetary Policy', logo_fa_icon_class_str='fas fa-money-bill-alt'),
    CategoryModel('International Finance', logo_fa_icon_class_str='fas fa-globe-americas'),
    CategoryModel('Options', logo_svg_text=svg_text('call-option-logo.svg')),
    CategoryModel('Volatility', logo_svg_text=svg_text('sigma-lower.svg')),
    CategoryModel('Informed Trading', logo_fa_icon_class_str='far fa-lightbulb'),
    CategoryModel('Liquidity', logo_fa_icon_class_str='fas fa-tint'),
    CategoryModel('Corporate Financing', logo_fa_icon_class_str='fas fa-money-check-alt'),
    CategoryModel('Equity', logo_fa_icon_class_str='fas fa-handshake'),
    CategoryModel('Debt', logo_fa_icon_class_str='fas fa-university'),
    CategoryModel('Executive Compensation', logo_fa_icon_class_str='fas fa-money-bill-alt'),
    CategoryModel('Investor Scrutiny', logo_fa_icon_class_str='fas fa-bullhorn'),
    CategoryModel('Insider Trading', logo_svg_text=svg_text('insider.svg')),
    CategoryModel('Short Sales', logo_svg_text=svg_text('chart-line-down.svg')),
    CategoryModel('Information Transmission', logo_fa_icon_class_str='fas fa-exchange-alt'),
    CategoryModel('Regulation', logo_fa_icon_class_str='fas fa-gavel'),
]

# TODO [#18]: bring in skills

CATEGORIES = {cat.title: cat for cat in _CATEGORIES}
