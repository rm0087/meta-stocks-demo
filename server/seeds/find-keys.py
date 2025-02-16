#!/usr/bin/env python3

# Standard library imports
from random import random, randint, choice as rc
import os
import json


# Remote library imports


# Local imports
from app import app
from models import db, Company, BalanceSheet
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
with app.app_context():

   print("Starting seed...")

   # Start account normailzation #################################################################################################################################################################################
   # Filter these IN
   cash_want = ['Cash', 
                'CashAndCashEquivalentsAtCarryingValue', 
                'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents',
   ]

   assets_want = ['Assets',
                  'AssetsCurrent',
                  'AssetsNoncurrent',
   ]

   liabilities_want = ['Liabilities',
                       'LiabilitiesAndStockholdersEquity', 
                       'LiabilitiesCurrent', 
                       'LiabilitiesNoncurrent',
   ]

   stockholders_equity_want = ['StockholdersEquity',
   
   ]

   ## Filter these OUT
   cash_filter = ['CashAndCashEquivalentsPeriodIncreaseDecrease', 
                  'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations',
                  'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect', 
                  'CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations',
                  'CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations', 
                  'CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations', 
                  'CashSurrenderValueOfLifeInsurance',
                  'CashAndDueFromBanks',
                  'CashFlowHedgeGainLossToBeReclassifiedWithinTwelveMonths',
                  'CashAndCashEquivalentsFairValueDisclosure',
                  'CashPaidForCapitalizedInterest',
                  'CashSurrenderValueFairValueDisclosure'
                  'CashFDICInsuredAmount',
                  'CashFDICInsuredAmount',
                  'CashUninsuredAmount',
                  'CashPeriodIncreaseDecrease',
                  'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseExcludingExchangeRateEffect',
                  'CashAndCashEquivalentsPeriodIncreaseDecreaseExcludingExchangeRateEffect',
                  'CashCashEquivalentsAndFederalFundsSold',
                  'CashFlowHedgeGainLossReclassifiedToCostOfSalesNet',
                  'CashFlowsBetweenTransfereeAndTransferorProceedsFromCollectionsReinvestedInRevolvingPeriodTransfers',
                  'CashFlowsBetweenTransfereeAndTransferorPurchasesOfPreviouslyTransferredFinancialAssets',
                  'CashFlowsBetweenTransfereeAndTransferorReceiptsOnInterestsThatContinueToBeHeldOther',
                  'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsDisposalGroupIncludingDiscontinuedOperations',
                  'CashAcquiredFromAcquisition',
                  'CashAcquiredInExcessOfPaymentsToAcquireBusiness',
                  'CashAndCashEquivalentsAtCarryingValueIncludingDiscontinuedOperations',
                  'CashDividends',
                  'CashDividendsPaidToParentCompany',
                  'CashFlowHedgeDerivativeInstrumentAssetsAtFairValue', 
                  'CashFlowHedgeDerivativeInstrumentLiabilitiesAtFairValue',
                  'CashCollateralForBorrowedSecurities',
                  'CashFlowsBetweenTransfereeAndTransferorProceedsFromNewTransfers',
                  'CashFlowsBetweenTransferorAndTransfereeBeneficialInterest',
                  'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffectContinuingOperations', 
                  'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffectDisposalGroupIncludingDiscontinuedOperations',
                  'CashDivestedFromDeconsolidation',
                  'CashSurrenderValueFairValueDisclosure',
                  'CashFlowHedgeGainLossReclassifiedToInterestExpenseNet',
                  'CashIncludingDiscontinuedOperations',
                  'CashFlowHedgesDerivativeInstrumentsAtFairValueNet',
                  'CashDividendsPaidToParentCompanyByConsolidatedSubsidiaries',
                  'CashReserveDepositRequiredAndMade',
                  'CashEquivalentsAtCarryingValue',


   ]
   assets_filter = ['AssetsHeldForSaleLongLivedFairValueDisclosure',
                    'AssetsOfDisposalGroupIncludingDiscontinuedOperation',
                    'AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent',
                    'AssetsNet',
                    'AssetsNoncurrentOtherThanNoncurrentInvestmentsAndPropertyPlantAndEquipment',
                    'AssetsFairValueDisclosure',
                    'AssetsOfDisposalGroupIncludingDiscontinuedOperationNoncurrent',
                    'AssetsFairValueDisclosureRecurring',
                    'AssetsFairValueDisclosureNonrecurring',
                    'AssetsHeldForSaleNotPartOfDisposalGroupCurrent',
                    'AssetsHeldForSaleNotPartOfDisposalGroup',
                    'AssetsDisposedOfByMethodOtherThanSaleInPeriodOfDispositionGainLossOnDisposition',
                    'AssetsDisposedOfByMethodOtherThanSaleInPeriodOfDispositionGainLossOnDisposition1',
                    'AssetsHeldForSaleCurrent',
                    'AssetsHeldForSaleAtCarryingValue',
                    'AssetsHeldInTrustNoncurrent',
                    'AssetsFairValueAdjustment', 
                    'AssetsNeededForImmediateSettlementAggregateFairValue',
                    'AssetsHeldInTrustCurrent',
                    'AssetsSoldUnderAgreementsToRepurchaseRepurchaseLiability',
                    'AssetsHeldForSaleNotPartOfDisposalGroupOther',
                    'AssetsHeldInTrust', 
                    'AssetsHeldForSaleNotPartOfDisposalGroupOther',


   ]
   liabilities_filter = ['LiabilitiesOfDisposalGroupIncludingDiscontinuedOperation',
                         'LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent',
                         'LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationNoncurrent',
                         'LiabilitiesAssumed',
                         'LiabilitiesAssumed1',
                         'LiabilitiesFairValueDisclosure',
                         'LiabilitiesFairValueDisclosureNonrecurring',
                         'LiabilitiesFairValueDisclosureRecurring',
                         'LiabilitiesOtherThanLongtermDebtNoncurrent',
                         'LiabilitiesSubjectToCompromiseEarlyContractTerminationFees',
                         'LiabilitiesOfAssetsHeldForSale',
                         'LiabilitiesSubjectToCompromisePaymentsUnderBankruptcyCourtOrderForTradeAccountsPayable',
                         'LiabilitiesSubjectToCompromiseEnvironmentalContingencies',
                         'LiabilitiesOfBusinessTransferredUnderContractualArrangementCurrent', 
                         'LiabilitiesOfBusinessTransferredUnderContractualArrangementNoncurrent',


   ]
   stockholders_equity_filter = ['StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
                                 'StockholdersEquityOther',
                                 'StockholdersEquityPeriodIncreaseDecrease',
                                 'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterestAdjustedBalance1',
                                 'StockholdersEquityNoteSubscriptionsReceivable',
                                 'StockholdersEquityBeforeTreasuryStock',
                                 'StockholdersEquityNoteSpinoffTransaction',
                                 'StockholdersEquityNoteStockSplitConversionRatio1',
   ]
   
  
   
   r = randint(1,10165)
   # companies = Company.query.filter(Company.balance_sheets == True ).all()
   balance_sheets = set(sheet.company_cik for sheet in BalanceSheet.query.with_entities(BalanceSheet.company_cik).all())
   companies = Company.query.filter(~Company.cik.in_(balance_sheets)).all()
   # for in :
   #    try:
         
   print(companies)
   print(len(companies))







   

   # for company in companies:
   #    db.session.refresh(company)
   #    file_path = f'json/CIK{company.cik_10}.json'
      
   #    json_file = open(file_path,'r')
      
   #    try:
   #       data = json.load(json_file)
   #       gaap = data.get('facts', {}).get('us-gaap')

   #       if gaap:
               
   #          stockholders_equity_keys = [key for key in data['facts']['us-gaap'].keys() if key.startswith('Stockholders') and key not in stockholders_equity_filter]
   #          if 'StockholdersEquity' not in stockholders_equity_keys:
   #             print(f'{company.id} - {company.ticker} - {company.name}')
   #             print()
   #             print(stockholders_equity_keys)
   #       else:
   #          pass
   #    except:
   #       pass
            
            
            
               
      
      
      
      # json_file.close()

      # End account normalization #################################################################################################################################################################################

   print("Seed successful")
