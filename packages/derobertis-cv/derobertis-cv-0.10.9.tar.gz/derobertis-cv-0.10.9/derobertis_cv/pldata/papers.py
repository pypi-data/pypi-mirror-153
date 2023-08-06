from dataclasses import dataclass
from typing import Optional, Sequence, Any, List

import pyexlatex.resume as lr
import pyexlatex as pl
from pyexlatex.typing import PyexlatexItems

from derobertis_cv.models.category import CategoryModel
from derobertis_cv.models.resources import ResourceModel
from derobertis_cv.pldata.authors import CO_AUTHORS
from derobertis_cv.pldata.research_categories import CATEGORIES
from derobertis_cv.pldata.constants.authors import (
    ANDY,
    NIMAL,
    SUGATA,
    CORBIN,
    JIMMY
)
from derobertis_cv.pltemplates.coauthor import CoAuthor


@dataclass
class ResearchProjectModel:
    title: str
    co_authors: Optional[Sequence[CoAuthor]] = None
    href: Optional[str] = None
    description: Optional[str] = None
    latex_description: Optional[Any] = None
    categories: Optional[Sequence[CategoryModel]] = None
    notes_content: Optional[PyexlatexItems] = None
    wip: bool = False
    resources: Optional[Sequence[ResourceModel]] = None
    
    def to_pyexlatex_publication(self, include_description: bool = True) -> lr.Publication:
        if not include_description:
            description = None
        else:
            description = self.latex_description or self.description

            if self.resources is not None:
                resource_links = [resource.to_pyexlatex_contents() for resource in self.resources]
                description = [
                    description,
                    pl.UnorderedList(resource_links)
                ]

        return lr.Publication(
            self.title,
            co_authors=self.co_authors,
            href=self.href,
            description=description,
        )

    @staticmethod
    def list_to_pyexlatex_publication_list(models: List['ResearchProjectModel'], include_descriptions: bool = True):
        return [model.to_pyexlatex_publication(include_description=include_descriptions) for model in models]


def get_working_papers():
    crypto_latex_description = """
    Cryptoassets represent a novel asset class in which tokens are generated and transacted
    using cryptography through blockchains. To date, few studies have attempted to derive a
    fundamental valuation for a cryptocurrency. I developed a model based on the Quantity
    Theory of Money (QTM) that informs us about fundamental value of a currency, and applied it 
    to understand cryptocurrency valuation. For most cryptocurrencies, an expectation
    of future use as a currency drives the valuation. I analyzed attention, sentiment, and R&D
    measures as proxies that form this expectation, and found that they are all significantly
    related to cryptocurrency returns. A portfolio that was long high attention cryptocurrencies
    with weekly rebalancing would have earned a 0.58% daily alpha from mid-2017 to the end
    of 2019. The portfolio which is long high attention cryptocurrencies and short low attention 
    cryptocurrencies has an even higher daily alpha of 0.72%, though it is not currently a
    tradeable strategy due to short-sale constraints. A portfolio formed from cryptocurrencies
    with high investor sentiment would have yielded a 0.33% daily alpha. R&D does not show
    as strong effects, but is still significantly related, and all the proxies for future usage remain
    significant with a variety of analyses and controls including other crypto market factors such
    as $MKT_c$, $SMB_c$, and $UMD_c$, and dual portfolio sorts on maturity, size, and momentum.
    """
    crypto_description = (
        crypto_latex_description
            .replace('$MKT_c$', 'MKT')
            .replace('$SMB_c$', 'SMB')
            .replace('$UMD_c$', 'UMD')
    )


    return [
        ResearchProjectModel(
            'Valuation without Cash Flows: What are Cryptoasset Fundamentals?',
            description=crypto_description,
            latex_description=crypto_latex_description,
            categories=[
                CATEGORIES['Alternative Assets'],
                CATEGORIES['Crypto-assets'],
                CATEGORIES['Asset Pricing'],
                CATEGORIES['Portfolio Analysis'],
                CATEGORIES['Investor Attention'],
                CATEGORIES['Investor Sentiment'],
            ],
            notes_content=[
                f"""
                My job market paper is an empirical asset pricing paper with a theory component that studies 
                how we can value cryptocurrencies. Using a Quantity Theory of Money-based model in a 
                portfolio framework, I find that expected future transaction volume is the most important
                factor in the current price, and that it can be proxied by current investor attention and sentiment.
                This is important because these assets have the potential to revolutionize payments, but their usage 
                is low in part due to volatility arising from the difficulty of valuation. The prior literature has 
                not come up with an empirical valuation approach tied to a theoretical model other than simply using 
                historical transaction volume. I also further the behavioral finance literature by analyzing the 
                interaction between investor attention and investor sentiment, and exploring novel proxies for those
                as well as R&D.
                """,
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Develop model based on QTM',
                            'Value of cryptocurrency is based on both size of economy and percentage of economic '
                            'transactions which are conducted in the cryptocurrency',
                            'Supply of cryptocurrency is driven primarily by the cost of electricity',
                            'For relative valuation, the size of the economy, price of electricity, '
                            'and velocity of money is '
                            'constant so transaction volume is the driver',
                            'Expected transaction volume is what matters, not current',
                            'Attention, sentiment, R&D - drivers of expectation',
                            'Returns are driven by the growth in expected transaction volume'
                        ])
                    ],
                    title='Model'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            '300M hourly observations of 33k trading pairs involving 3.4k cryptocurrencies on 230 exchanges '
                            'collected from CryptoCompare API',
                            'Social information - Twitter, Facebook, Reddit, CryptoCompare, and Github - also collected from '
                            'CryptoCompare API and supplemented via Github API and the Github Archive project',
                            'News articles also from CryptoCompare API, calculated count and polarity',
                            'Calculated attention (twitter followers, CC followers, CC posts), '
                            'sentiment (twitter favorites/trans, code repo stars/trans, news polarity), '
                            'and R&D (commits, LOC added, LOC changed) factors using SEM',
                            'Calculated MKT, SMB, UMD following FF',
                            'Returns calculation was complicated - aggregate across exchanges with data errors, '
                            'convert all to same base currency, often through multiple conversions'
                        ])
                    ],
                    title='Data'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Atention, sentiment, and R&D are all related to cryptocurrency returns '
                            'in a non-linear fashion',
                            'Attention and sentiment are positively related after controlling for other '
                            'factors such as size, maturity, and momentum',
                            'Results are robust to excluding Bitcoin and to returns in BTC',
                        ])
                    ],
                    title='Results'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            '230 exchanges, top exchange has only 499 pairs - very fragmented',
                            'The vast majority of trades in these markets is between cryptocurrencies, '
                            'usually BTC or ETH on one side',
                            'BTC is 60-80% of the market cap depending on the time period',
                        ])
                    ],
                    title='Stylistic Facts'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Released three open source packages in conjuction with this project',
                            pl.UnorderedList([
                                'cryptocompare-py: Easily collect information from CryptoCompare APIs in Python',
                                'project-report: Collect time-series Github information',
                                'py-gh-archive: Easily collect time-series data from the Github Archive project'
                            ]),
                        ])
                    ],
                    title='Other Mentions'
                ),
            ],
            resources=[
                ResourceModel(
                    'Overview Video',
                    'https://youtu.be/8mMqLpFPK7M',
                    author='Nick DeRobertis',
                    description='3-minute video overview of the paper'
                )
            ]
        ),
        ResearchProjectModel(
            'Government Equity Capital Market Intervention and Stock Returns',
            [CO_AUTHORS[ANDY], CO_AUTHORS[NIMAL]],
            description="""
            As part of their market intervention strategy, the Bank of Japan (BOJ) has been purchasing 
            shares of ETFs tracking Japan’s major stock indices, reaching as much as ¥16.3 trillion
            in holdings by December of 2017. We show that firms that end up with high BOJ ownership
            have 1.78% higher daily returns and alpha of 0.29% in the window of (-1, 1) around BOJ purchase 
            days compared to firms with no ownership. We further show that there are significant
            price distortion effects as the BOJ purchases assets proportionally to their index weighting
            and not their market value. We analyze the Nikkei 225 as a price-weighted target index,
            and provide evidence that firms with high price-weightings but low market capitalization
            out-perform by 9.12% annually compared to the average firm. We show evidence that this
            out-performance is due to higher Bank of Japan ownership.
            """,
            categories=[
                CATEGORIES['Asset Pricing'],
                CATEGORIES['Portfolio Analysis'],
                CATEGORIES['Market Intervention'],
                CATEGORIES['Monetary Policy'],
                CATEGORIES['International Finance'],
            ],
            notes_content=[
                f"""
                I also have a joint working paper with my advisors Andy Naranjo and Nimal Nimalendran,
                an empirical asset pricing working paper on the effects of government equity capital 
                market intervention, with a focus on the Bank of Japan's purchasing of equity ETFs. 
                Using a portfolio analysis and event study framework, we exploit the fact that since the bank
                has targeted the Nikkei 225, a price-weighted index, there is substantial 
                cross-sectional variation in the ownership percentage, to show that higher Bank of Japan ownership
                is associated with higher stock returns. This study is important for monetary policy-makers to 
                understand the effects of intervening in equity markets, and to avoid the pitfalls of targeting 
                price-weighted indices. At the time we developed the research, there were no published papers 
                on the topic, and since then none have analyzed as comprehensively the stock performance
                in response to these strategies.
                """,
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Difference of opinion framework grounded in Ed Miller (1977 JF) - investors with '
                            'higher opinion about a stock set the price due to limited supply. Viewing BOJ '
                            'purchase as an investor with high price opinion so will raise stock price',
                            'ETF price increase leads to APs creating more shares which leads to '
                            'buying underlying firms',
                            'Potential negative governance effects due to large passive shareholder, follow up study',
                            'Cost of debt should decrease as this has been shown for other government-backed firms, '
                            'follow up study'
                        ])
                    ],
                    title='Hypothesis'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Stock prices, industries from TR Datastream',
                            'Corporate financials from Capital IQ',
                            'BOJ purchases from BOJ',
                            'FF from Ken French',
                            'ETF holdings from Morningstar - required a complicated process to match holdings '
                            'to identifiers (name matching with machine learning)',
                            'FF portfolio formation on PVD'
                        ])
                    ],
                    title='Data'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Both BOJ ownership and PVD positively related to returns and alphas',
                            '9.12% VW LS PVD',
                            'Results hold controlling for FF 5 fac',
                            'Alphas were greatest at the time BOJ was expanding purchase program in 2015/2016',
                            'Event study: 1% increase in BOJ ownership is associated with 0.29% daily alpha in '
                            'window if -1 to 1 and significant effects persist for 20 trading days',
                            'Empirically confirmed that BOJ purchases when price is dropping and is paying attention '
                            'to only the targeted firms',
                        ])
                    ],
                    title='Results'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'The BOJ owns 72% of the equity index ETF market',
                            'More than 20 years of deflation and stagnant economy after 1989 asset bubble peak, even '
                            'as the bank kept interest rates close to zero',
                            '25% stake in Fast Retailing (high price, lower mkt cap)'
                        ])
                    ],
                    title='Stylistic Facts'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Implemented machine learning for name matching, achieving a prediction accuracy of '
                            '98.3%'
                        ])
                    ],
                    title='Other Mentions'
                ),
            ]
        ),
        ResearchProjectModel(
            'Are Investors Paying (for) Attention?',
            description="""
            I examine the informativeness of investor attention on pricing of
            assets by using a new proxy based on Google search data. In contrast to prior
            studies using Google data, my new proxy contains cross-sectional firm attention information
            in addition to time-series information. I focus on firms that consistently 
            receive high or low attention, rather than attention-grabbing events.
            I find that firms with low attention outperform firms with high attention by
            8.16% annually, and after isolating the unique information in search volume
            and removing the impact of attention-grabbing events, the outperformance is
            still statistically and economically significant at 6.36% annually.
            """,
            categories=[
                CATEGORIES['Asset Pricing'],
                CATEGORIES['Portfolio Analysis'],
                CATEGORIES['Investor Attention'],
                CATEGORIES['Behavioral Finance'],
            ]
        ),
        ResearchProjectModel(
            'OSPIN: Informed Trading in Options and Stock Markets',
            [CO_AUTHORS[JIMMY], CO_AUTHORS[NIMAL], CO_AUTHORS[SUGATA]],
            description="""
            To gain a better understanding of the role of information in the price discovery
            of stock and option markets,  
            we propose and estimate a joint structural model of trading in both markets, yielding
            correlated directional informed trading in both markets, informed
            volatility trading in the option market, and correlated (buy/sell) liquidity trades in both
            markets. The model parameters and the probabilities of informed and liquidity trading in
            both markets are estimated using signed high frequency stock and options trading data for
            different option contracts. We find that moneyness and maturity play an important role in
            informed trading and on the microstructure price discovery of the stock and options markets.
            Further, we find the high frequency informed trading measures in the options market spike just 
            before earnings announcements and remain high for a few days after the announcement.
            """,
            categories=[
                CATEGORIES['Options'],
                CATEGORIES['Volatility'],
                CATEGORIES['Informed Trading'],
                CATEGORIES['Liquidity'],
            ],
            notes_content=[
                f"""
                I also have a joint working paper with Nimal Nimalendran, Sugata Ray, and Yong Jin,
                a microstructure paper on the role of information in the price discovery of stock
                and option markets. Using transaction-level data on both stocks and options, we extend the 
                Easley et al (1996) probability of informed trading model which focused only on 
                stocks to include both stock and option information. We find that the information in 
                the option markets leads that of stock markets, and that analyzing option markets allows
                extraction of volatility information in a addition to the usual direction and liquidity 
                trading information. This study is important for researchers analyzing the information
                structure and price discovery in markets, and it advances the literature by providing 
                a model which extracts more and more timely information on informed trading.  
                """,
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'The world can be in one of 18 states at a time in the model based on H/L/No directional info, '
                            'H/L/No volatility info, and High/Normal liquidity trading',
                            'Uninformed, informed volatility, informed directional, and liquidity traders arrive '
                            'according to independent Poisson processes',
                            'We form the likelihood function based on these independent Poisson processes and 18 '
                            'states of the world',
                            'Checked the model in three ways: Monte Carlo simulation of the trades, in which we '
                            'were able to recover the theory parameters, model-implied moments shown to be '
                            'similar to sample moments, and PIN measures from the model are signficiantly related to '
                            'bid-ask spreads, price impact, and cross-market price impact measures'
                        ])
                    ],
                    title='Model'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Options transaction-level data from Option Price Reporting Authority (OPRA) Option Database',
                            'Stock transation-level data from TAQ',
                            'Greeks, implied volatility, realized volatility - OptionMetrics',
                            'Daily stock data - CRSP',
                            'Lee and Ready (1991) algorithm for signing trades',
                            'Aggregated into 30 minute periods',
                            'Split by option moneyness and maturity for subsample analyses',

                        ])
                    ],
                    title='Data'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'OPIN measures are related to bid-ask spreads, price impact, and cross-market '
                            'price impact measures and have more explanatory power than stock-based measures',
                            'Probability of informed trading in options markets is more than double than '
                            'that of stock markets for directional info',
                            '7% direction up, 6% direction down, 15% volatility up, 6% volatility down (selling '
                            'straddle/strangle/options requires more margin)',
                            '66% uninformed trading, 21% liquidity trading',
                            'Most trades are ATM but also lowest probability of informed trading'
                        ])
                    ],
                    title='Results'
                ),
                pl.SubSection(
                    [
                        pl.UnorderedList([
                            'Implemented model using a computer symbolic algebra system and both ML and GMM approaches'
                        ])
                    ],
                    title='Other Mentions'
                ),
            ]
        )
    ]


def get_works_in_progress():
    return [
        ResearchProjectModel(
            'Explaining the Cross-Section of Cryptocurrency Returns',
            description="""
            There are thousands of cryptocurrencies, but no model to explain their price movements.
            One cryptocurrency stands out in terms of its public awareness and market capitalization: Bitcoin.
            Anecdotal evidence suggests that cryptocurrency returns are related to Bitcoin returns. This study
            seeks to determine a pricing model which relates individual cryptocurrency returns to Bitcoin returns.
            """,
            categories=[
                CATEGORIES['Alternative Assets'],
                CATEGORIES['Crypto-assets'],
                CATEGORIES['Asset Pricing'],
                CATEGORIES['Portfolio Analysis'],
            ],
            wip=True
        ),
        ResearchProjectModel(
            'Does Government Equity Market Intervention Affect Liquidity and Volatility?',
            [CO_AUTHORS[ANDY], CO_AUTHORS[NIMAL]],
            description="""
            Bank of Japan (BOJ) ETF purchases have resulted in the BOJ owning more than 60% of total outstanding 
            ETFs by December of 2017. Considering such a large volume of purchases, we focus on liquidity effects in 
            both the ETF market and the market for the
            underlying shares. Further, as the BOJ is only purchasing 
            and not selling, we examine how downside volatility decreases.
            """,
            categories=[
                CATEGORIES['Market Intervention'],
                CATEGORIES['Monetary Policy'],
                CATEGORIES['International Finance'],
                CATEGORIES['Volatility'],
            ],
            wip=True
        ),
        ResearchProjectModel(
            'The Effect of Equity Market Intervention on Corporate Financing',
            [CO_AUTHORS[ANDY], CO_AUTHORS[NIMAL]],
            description="""
            We show in prior work that
            stock prices of the underlying firms increase in response to Bank of Japan (BOJ) purchases of ETFs of major
            stock indices. Considering a higher share value, firms should
            be more likely to choose equity than debt when raising capital. This effect may be mediated by the low
            cost of debt during this time period.
            """,
            categories=[
                CATEGORIES['Market Intervention'],
                CATEGORIES['Monetary Policy'],
                CATEGORIES['International Finance'],
                CATEGORIES['Corporate Financing'],
                CATEGORIES['Equity'],
                CATEGORIES['Debt'],
            ],
            wip=True
        ),
        ResearchProjectModel(
            'How do CEOs Respond to Public and Investor Scrutiny?',
            [CO_AUTHORS[CORBIN]],
            description="""
            In the United States, there has been a trend towards increased public scrutiny of CEO pay, in both the 
            press and in regulation. As far as regulation, first companies had to release a summary table of 
            compensation, then "Say on Pay" legislation was introduced so that shareholders vote to approve the CEO
            compensation. We examine the quantity and quality of CEOs that move from the public sector to the 
            private sector, using regulatory changes as exogenous shocks. 
            """,
            categories=[
                CATEGORIES['Executive Compensation'],
                CATEGORIES['Investor Scrutiny'],
                CATEGORIES['Regulation'],
            ],
            wip=True
        ),
        ResearchProjectModel(
            'Do Insiders Learn From Short Sellers?',
            [CO_AUTHORS[CORBIN]],
            description="""
            Differing groups of investors, such as insiders, short-sellers, and analysts, have different information 
            sets on which to trade. While the use and transmission of information by insiders has been extensively 
            studied, there is a lack of research on how insiders learn from external investors such as short-sellers.
            We examine the response of insider trading to surprises in short interest.
            """,
            categories=[
                CATEGORIES['Insider Trading'],
                CATEGORIES['Short Sales'],
                CATEGORIES['Information Transmission'],
            ],
            wip=True
        ),
    ]
