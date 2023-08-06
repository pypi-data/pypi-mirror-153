from derobertis_cv.models.category import CategoryModel
from derobertis_cv.pltemplates.logo import svg_text

INTRO_FIN_MODEL_CATEGORY = CategoryModel('Introduction to Financial Modeling')
CORPORATE_VALUATION_CATEGORY = CategoryModel('Corporate Valuation')

FIN_MODEL_COURSE_MAIN_CATEGORIES = [
    INTRO_FIN_MODEL_CATEGORY,
    CORPORATE_VALUATION_CATEGORY
]

DEBT_ANALYSIS_CATEGORY = CategoryModel('Debt Analysis')
DEBT_PORTFOLIO_CATEGORY = CategoryModel('Debt Portfolio Management')

DEBT_COURSE_MAIN_CATEGORIES = [
    DEBT_ANALYSIS_CATEGORY,
    DEBT_PORTFOLIO_CATEGORY,
]

EXCEL_CATEGORY = CategoryModel('Excel')

EXCEL_LAB_MAIN_CATEGORIES = [
    EXCEL_CATEGORY,
]

FIN_MODEL_COURSE_CATEGORIES = [
    *FIN_MODEL_COURSE_MAIN_CATEGORIES,

    CategoryModel('Overview', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Basic technical skills and setup – Excel and Python', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Time value of money models', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Basic statistical tools', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Monte Carlo methods', parents=(INTRO_FIN_MODEL_CATEGORY,)),

    CategoryModel('Capital budgeting', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Estimating beta', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Estimating market value of debt', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Weighted average cost of capital (WACC)', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Free cash flow (FCF)', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Pro forma financial statements', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Discounted cash flow (DCF) valuation', parents=(CORPORATE_VALUATION_CATEGORY,)),
]

FM_EXCEL_CATEGORY = CategoryModel('Excel')

FIN_MODEL_COURSE_PREREQ_CATEGORIES = [
    CategoryModel('Algebra'),
    FM_EXCEL_CATEGORY,
    CategoryModel('Data entry, editing', parents=(FM_EXCEL_CATEGORY,)),
    CategoryModel('Number and cell formatting', parents=(FM_EXCEL_CATEGORY,)),
    CategoryModel('How to work with formulas, and knowledge of common math formulas', parents=(FM_EXCEL_CATEGORY,)),
    CategoryModel('Cell references - fixed and relative, when to use each and why', parents=(FM_EXCEL_CATEGORY,)),
    CategoryModel('Managing worksheets and workbooks', parents=(FM_EXCEL_CATEGORY,)),
    CategoryModel('Graphs, charts', parents=(FM_EXCEL_CATEGORY,)),
]

DEBT_COURSE_CATEGORIES = [
    *DEBT_COURSE_MAIN_CATEGORIES,

    CategoryModel('Time value of money', parents=(DEBT_ANALYSIS_CATEGORY,)),
    CategoryModel('Bond pricing', parents=(DEBT_ANALYSIS_CATEGORY,)),
    CategoryModel('Yield to Maturity', parents=(DEBT_ANALYSIS_CATEGORY,)),
    CategoryModel('Interest Rates', parents=(DEBT_ANALYSIS_CATEGORY,)),
    CategoryModel('Types of debt', parents=(DEBT_ANALYSIS_CATEGORY,)),
    CategoryModel('Risk factors for debt', parents=(DEBT_ANALYSIS_CATEGORY,)),
    CategoryModel('Term structure of interest rates', parents=(DEBT_ANALYSIS_CATEGORY,)),

    CategoryModel('Duration', parents=(DEBT_PORTFOLIO_CATEGORY,)),
    CategoryModel('Immunization', parents=(DEBT_PORTFOLIO_CATEGORY,)),
    CategoryModel('Convexity', parents=(DEBT_PORTFOLIO_CATEGORY,)),
    CategoryModel('Credit risk analysis', parents=(DEBT_PORTFOLIO_CATEGORY,)),
    CategoryModel('Bond options', parents=(DEBT_PORTFOLIO_CATEGORY,)),
    CategoryModel('Interest rate swaps', parents=(DEBT_PORTFOLIO_CATEGORY,)),
    CategoryModel('Credit default swaps', parents=(DEBT_PORTFOLIO_CATEGORY,)),
]

EXCEL_LAB_CATEGORIES = [
    *EXCEL_LAB_MAIN_CATEGORIES,
    CategoryModel('Cell references', parents=(EXCEL_CATEGORY,)),
    CategoryModel('Formulas', parents=(EXCEL_CATEGORY,)),
    CategoryModel('Pivot tables', parents=(EXCEL_CATEGORY,)),
    CategoryModel('Iteration', parents=(EXCEL_CATEGORY,)),
    CategoryModel('Macros', parents=(EXCEL_CATEGORY,)),
    CategoryModel('Regressions', parents=(EXCEL_CATEGORY,)),
]

_COURSE_CATEGORIES = [
    *FIN_MODEL_COURSE_CATEGORIES,
    *DEBT_COURSE_CATEGORIES,
    CategoryModel('Algebra'),
    CategoryModel('Excel'),
]

COURSE_CATEGORIES = {cat.title: cat for cat in _COURSE_CATEGORIES}
