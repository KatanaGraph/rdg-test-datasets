# Fannie Mae (FNMA) Test Dataset

This file is a sample from a much larger dataset that is released by FNMA on a quarterly basis. It includes the performance of a select number of fixed mortgages and is a useful dataset in predicting if a loan will default on its obligations. More info can be found here: 

https://capitalmarkets.fanniemae.com/credit-risk-transfer/single-family-credit-risk-transfer/fannie-mae-single-family-loan-performance-data

# Import

The current import file is using the Dask importer because of some of the complexities in processing the data. 

The import script is shown below until this repo supports Dask imports: 

```python


from katana import remote
from katana.remote import import_data
from katana.remote.import_data import Operation
import dask.dataframe as dd

#os.environ["KATANA_SERVER_ADDRESS"] = "host.docker.internal:8080"
#os.environ["KATANA_SERVER_ADDRESS"] = "localhost:8089"

## Dask Data Types

fnma_col_names = ['POOL_ID','LOAN_ID','ACT_PERIOD','CHANNEL','SELLER','SERVICER','MASTER_SERVICER','ORIG_RATE','CURR_RATE','ORIG_UPB','ISSUANCE_UPB','CURRENT_UPB','ORIG_TERM','ORIG_DATE','FIRST_PAY','LOAN_AGE','REM_MONTHS','ADJ_REM_MONTHS','MATR_DT','OLTV','OCLTV','NUM_BO','DTI','CSCORE_B','CSCORE_C','FIRST_FLAG','PURPOSE','PROP','NO_UNITS','OCC_STAT','STATE','MSA','ZIP','MI_PCT','PRODUCT','PPMT_FLG','IO','FIRST_PAY_IO','MNTHS_TO_AMTZ_IO','DLQ_STATUS','PMT_HISTORY','MOD_FLAG','MI_CANCEL_FLAG','Zero_Bal_Code','ZB_DTE','LAST_UPB','RPRCH_DTE','CURR_SCHD_PRNCPL','TOT_SCHD_PRNCPL','UNSCHD_PRNCPL_CURR','LAST_PAID_INSTALLMENT_DATE','FORECLOSURE_DATE','DISPOSITION_DATE','FORECLOSURE_COSTS','PROPERTY_PRESERVATION_AND_REPAIR_COSTS','ASSET_RECOVERY_COSTS','MISCELLANEOUS_HOLDING_EXPENSES_AND_CREDITS','ASSOCIATED_TAXES_FOR_HOLDING_PROPERTY','NET_SALES_PROCEEDS','CREDIT_ENHANCEMENT_PROCEEDS','REPURCHASES_MAKE_WHOLE_PROCEEDS','OTHER_FORECLOSURE_PROCEEDS','NON_INTEREST_BEARING_UPB','PRINCIPAL_FORGIVENESS_AMOUNT','ORIGINAL_LIST_START_DATE','ORIGINAL_LIST_PRICE','CURRENT_LIST_START_DATE','CURRENT_LIST_PRICE','ISSUE_SCOREB','ISSUE_SCOREC','CURR_SCOREB','CURR_SCOREC','MI_TYPE','SERV_IND','CURRENT_PERIOD_MODIFICATION_LOSS_AMOUNT','CUMULATIVE_MODIFICATION_LOSS_AMOUNT','CURRENT_PERIOD_CREDIT_EVENT_NET_GAIN_OR_LOSS','CUMULATIVE_CREDIT_EVENT_NET_GAIN_OR_LOSS','HOMEREADY_PROGRAM_INDICATOR','FORECLOSURE_PRINCIPAL_WRITE_OFF_AMOUNT','RELOCATION_MORTGAGE_INDICATOR','ZERO_BALANCE_CODE_CHANGE_DATE','LOAN_HOLDBACK_INDICATOR','LOAN_HOLDBACK_EFFECTIVE_DATE','DELINQUENT_ACCRUED_INTEREST','PROPERTY_INSPECTION_WAIVER_INDICATOR','HIGH_BALANCE_LOAN_INDICATOR','ARM_5_YR_INDICATOR','ARM_PRODUCT_TYPE','MONTHS_UNTIL_FIRST_PAYMENT_RESET','MONTHS_BETWEEN_SUBSEQUENT_PAYMENT_RESET','INTEREST_RATE_CHANGE_DATE','PAYMENT_CHANGE_DATE','ARM_INDEX','ARM_CAP_STRUCTURE','INITIAL_INTEREST_RATE_CAP','PERIODIC_INTEREST_RATE_CAP','LIFETIME_INTEREST_RATE_CAP','MARGIN','BALLOON_INDICATOR','PLAN_NUMBER','FORBEARANCE_INDICATOR','HIGH_LOAN_TO_VALUE_HLTV_REFINANCE_OPTION_INDICATOR','DEAL_NAME','RE_PROCS_FLAG','ADR_TYPE','ADR_COUNT','ADR_UPB','LOAN_SNAPSHOT']
fnma_dtypes = {

    'POOL_ID': 'string',
    'LOAN_ID': 'string',
    'ACT_PERIOD': 'string',
    'CHANNEL': 'string',
    'SELLER': 'string',
    'SERVICER': 'string',
    'MASTER_SERVICER': 'string',
    'ORIG_RATE': 'float',
    'CURR_RATE': 'float',
    'ORIG_UPB': 'float',
    'ISSUANCE_UPB': 'float',
    'CURRENT_UPB': 'float',
    'ORIG_TERM': 'float',
    'ORIG_DATE': 'string',
    'FIRST_PAY': 'string',
    'LOAN_AGE': 'float',
    'REM_MONTHS': 'float',
    'ADJ_REM_MONTHS': 'float',
    'MATR_DT': 'string',
    'OLTV': 'float',
    'OCLTV': 'float',
    'NUM_BO': 'string',
    'DTI': 'float',
    'CSCORE_B': 'float',
    'CSCORE_C': 'float',
    'FIRST_FLAG': 'string',
    'PURPOSE': 'string',
    'PROP': 'string',
    'NO_UNITS': 'float',
    'OCC_STAT': 'string',
    'STATE': 'string',
    'MSA': 'string',
    'ZIP': 'string',
    'MI_PCT': 'float',
    'PRODUCT': 'string',
    'PPMT_FLG': 'string',
    'IO': 'string',
    'FIRST_PAY_IO': 'string',
    'MNTHS_TO_AMTZ_IO': 'float',
    'DLQ_STATUS': 'string',
    'PMT_HISTORY': 'string',
    'MOD_FLAG': 'string',
    'MI_CANCEL_FLAG': 'string',
    'Zero_Bal_Code': 'string',
    'ZB_DTE': 'string',
    'LAST_UPB': 'float',
    'RPRCH_DTE': 'string',
    'CURR_SCHD_PRNCPL': 'float',
    'TOT_SCHD_PRNCPL': 'float',
    'UNSCHD_PRNCPL_CURR': 'float',
    'LAST_PAID_INSTALLMENT_DATE': 'string',
    'FORECLOSURE_DATE': 'string',
    'DISPOSITION_DATE': 'string',
    'FORECLOSURE_COSTS': 'float',
    'PROPERTY_PRESERVATION_AND_REPAIR_COSTS': 'float',
    'ASSET_RECOVERY_COSTS': 'float',
    'MISCELLANEOUS_HOLDING_EXPENSES_AND_CREDITS': 'float',
    'ASSOCIATED_TAXES_FOR_HOLDING_PROPERTY': 'float',
    'NET_SALES_PROCEEDS': 'float',
    'CREDIT_ENHANCEMENT_PROCEEDS': 'float',
    'REPURCHASES_MAKE_WHOLE_PROCEEDS': 'float',
    'OTHER_FORECLOSURE_PROCEEDS': 'float',
    'NON_INTEREST_BEARING_UPB': 'float',
    'PRINCIPAL_FORGIVENESS_AMOUNT': 'float',
    'ORIGINAL_LIST_START_DATE': 'string',
    'ORIGINAL_LIST_PRICE': 'float',
    'CURRENT_LIST_START_DATE': 'string',
    'CURRENT_LIST_PRICE': 'float',
    'ISSUE_SCOREB': 'float',
    'ISSUE_SCOREC': 'float',
    'CURR_SCOREB': 'float',
    'CURR_SCOREC': 'float',
    'MI_TYPE': 'float',
    'SERV_IND': 'string',
    'CURRENT_PERIOD_MODIFICATION_LOSS_AMOUNT': 'float',
    'CUMULATIVE_MODIFICATION_LOSS_AMOUNT': 'float',
    'CURRENT_PERIOD_CREDIT_EVENT_NET_GAIN_OR_LOSS': 'float',
    'CUMULATIVE_CREDIT_EVENT_NET_GAIN_OR_LOSS': 'float',
    'HOMEREADY_PROGRAM_INDICATOR': 'string',
    'FORECLOSURE_PRINCIPAL_WRITE_OFF_AMOUNT': 'float',
    'RELOCATION_MORTGAGE_INDICATOR': 'string',
    'ZERO_BALANCE_CODE_CHANGE_DATE': 'float',
    'LOAN_HOLDBACK_INDICATOR': 'string',
    'LOAN_HOLDBACK_EFFECTIVE_DATE': 'float',
    'DELINQUENT_ACCRUED_INTEREST': 'float',
    'PROPERTY_INSPECTION_WAIVER_INDICATOR': 'string',
    'HIGH_BALANCE_LOAN_INDICATOR': 'string',
    'ARM_5_YR_INDICATOR': 'float',
    'ARM_PRODUCT_TYPE': 'float',
    'MONTHS_UNTIL_FIRST_PAYMENT_RESET': 'float',
    'MONTHS_BETWEEN_SUBSEQUENT_PAYMENT_RESET': 'float',
    'INTEREST_RATE_CHANGE_DATE': 'float',
    'PAYMENT_CHANGE_DATE': 'float',
    'ARM_INDEX': 'float',
    'ARM_CAP_STRUCTURE': 'float',
    'INITIAL_INTEREST_RATE_CAP': 'float',
    'PERIODIC_INTEREST_RATE_CAP': 'float',
    'LIFETIME_INTEREST_RATE_CAP': 'float',
    'MARGIN': 'float',
    'BALLOON_INDICATOR': 'float',
    'PLAN_NUMBER': 'string',
    'FORBEARANCE_INDICATOR': 'string',
    'HIGH_LOAN_TO_VALUE_HLTV_REFINANCE_OPTION_INDICATOR': 'string',
    'DEAL_NAME': 'string',
    'RE_PROCS_FLAG': 'string',
    'ADR_TYPE': 'string',
    'ADR_COUNT': 'float',
    'ADR_UPB': 'float',
    'LOAN_SNAPSHOT': 'string'
}

sf_node_properties = {
        "Loan_SF":  {
                        "CHANNEL": "string",
                        "ORIG_RATE": "float",
                        "CURR_RATE": "float",
                        "ORIG_UPB": "float",
                        "CURRENT_UPB": "float",
                        "ORIG_TERM": "float",
                        "ORIG_DATE": "string",
                        "FIRST_PAY": "string",
                        "MATR_DT": "string",
                        "OLTV": "float",
                        "OCLTV": "float",
                        "PURPOSE": "string",
                        "MI_PCT": "float",
                        "PRODUCT": "string",
                        "PPMT_FLG": "string",
                        "IO": "string",
                        "FIRST_PAY_IO": "string",
                        "MI_TYPE": "float",
                        "HIGH_BALANCE_LOAN_INDICATOR": "string"
                    },
        "Borrower": {
                        "NUM_BO": "string",
                        "DTI": "float",
                        "CSCORE_B": "float",
                        "CSCORE_C": "float",
                        "FIRST_FLAG": "string"
                    },
        "Property": {
                        "PROP": "string",
                        "NO_UNITS": "float",
                        "OCC_STAT": "string",
                        "STATE": "string",
                        "PROPERTY_INSPECTION_WAIVER_INDICATOR": "string"
                    },
        "Loan_Snapshot": {
                        "ACT_PERIOD": "string",
                        "MNTHS_TO_AMTZ_IO": "float",
                        "DLQ_STATUS": "string",
                        "PMT_HISTORY": "string",
                        "MOD_FLAG": "string",
                        "MI_CANCEL_FLAG": "string",
                        "Zero_Bal_Code": "string",
                        "ZB_DTE": "string",
                        "LAST_UPB": "float",
                        "RPRCH_DTE": "string",
                        "CURR_SCHD_PRNCPL": "float",
                        "TOT_SCHD_PRNCPL": "float",
                        "UNSCHD_PRNCPL_CURR": "float",
                        "LAST_PAID_INSTALLMENT_DATE": "string",
                        "FORECLOSURE_DATE": "string",
                        "DISPOSITION_DATE": "string",
                        "FORECLOSURE_COSTS": "float",
                        "PROPERTY_PRESERVATION_AND_REPAIR_COSTS": "float",
                        "ASSET_RECOVERY_COSTS": "float",
                        "MISCELLANEOUS_HOLDING_EXPENSES_AND_CREDITS": "float",
                        "ASSOCIATED_TAXES_FOR_HOLDING_PROPERTY": "float",
                        "NET_SALES_PROCEEDS": "float",
                        "CREDIT_ENHANCEMENT_PROCEEDS": "float",
                        "REPURCHASES_MAKE_WHOLE_PROCEEDS": "float",
                        "OTHER_FORECLOSURE_PROCEEDS": "float",
                        "NON_INTEREST_BEARING_UPB": "float",
                        "PRINCIPAL_FORGIVENESS_AMOUNT": "float",
                        "SERV_IND": "string",
                        "HOMEREADY_PROGRAM_INDICATOR": "string",
                        "FORECLOSURE_PRINCIPAL_WRITE_OFF_AMOUNT": "float",
                        "RELOCATION_MORTGAGE_INDICATOR": "string",
                        "FORBEARANCE_INDICATOR": "string",
                        "HIGH_LOAN_TO_VALUE_HLTV_REFINANCE_OPTION_INDICATOR": "string",
                        "RE_PROCS_FLAG": "string",
                        "ADR_TYPE": "string",
                        "ADR_COUNT": "float",
                        "ADR_UPB": "float"
                        }
}

snapshot = sf_node_properties["Loan_Snapshot"]

cas_node_properties = {
    "Loan_CAS": sf_node_properties["Loan_SF"],
    "Borrower": sf_node_properties["Borrower"],
    "Property": sf_node_properties["Property"],
    "Loan_Snapshot": snapshot
}

snapshot = cas_node_properties["Loan_Snapshot"]
snapshot.update(
                            {
                                "ARM_5_YR_INDICATOR": "float",
                                "ARM_PRODUCT_TYPE": "float",
                                "MONTHS_UNTIL_FIRST_PAYMENT_RESET": "float",
                                "MONTHS_BETWEEN_SUBSEQUENT_PAYMENT_RESET": "float",
                                "INTEREST_RATE_CHANGE_DATE": "float",
                                "PAYMENT_CHANGE_DATE": "float",
                                "ARM_INDEX": "float",
                                "ARM_CAP_STRUCTURE": "float",
                                "INITIAL_INTEREST_RATE_CAP": "float",
                                "PERIODIC_INTEREST_RATE_CAP": "float",
                                "LIFETIME_INTEREST_RATE_CAP": "float",
                                "MARGIN": "float",
                                "BALLOON_INDICATOR": "float",
                                "PLAN_NUMBER": "string" 
                            })
cirt_node_properties = {
    "Loan_CIRT": sf_node_properties["Loan_SF"],
    "Borrower": sf_node_properties["Borrower"],
    "Property": sf_node_properties["Property"],
    "Loan_Snapshot": snapshot
}

nodes =  {
    "Loan_SF": {
        "id_column": "LOAN_ID", 
        "id_space": "Loan_SF"
    },
    "Loan_CAS": {
        "id_column": "LOAN_ID", 
        "id_space": "Loan_CAS"
    },    
    "Loan_CIRT": {
        "id_column": "LOAN_ID", 
        "id_space": "Loan_CIRT"
    },        
    "Borrower" : {
        "id_column": "BORROWER_ID", 
        "id_space": "Borrower"
    },
    "Property": {
        "id_column": "PROPERTY_ID", 
        "id_space": "Property"
    },
    "Loan_Snapshot": {
        "id_column": "LOAN_SNAPSHOT", 
        "id_space": "Loan_Snapshot"
    },
    "MSA": {
        "id_column": "MSA", 
        "id_space": "MSA"
    },
    "Zip": {
        "id_column": "ZIP", 
        "id_space": "Zip"
    },
    "Seller": {
        "id_column": "SELLER", 
        "id_space": "SellerOrServicer"
    },
    "Servicer": {
        "id_column": "SERVICER", 
        "id_space": "SellerOrServicer"
    },
    "MBS": {
        "id_column": "POOL_ID", 
        "id_space": "MBS"
    },
    "Deal": {
        "id_column": "DEAL_NAME", 
        "id_space": "Deal"
    }                                    
}
edges = {
    "hasLoanSnapshot" : {
        "source_label": "Loan",
        "dest_label": "Loan_Snapshot"
    },
    "isCollateralizedBy" : {
        "source_label": "Loan",
        "dest_label": "Property"
    },
    "hasBorrower" : {
        "source_label": "Loan",
        "dest_label": "Borrower"
    },
    "isLocatedInMSA" : {
        "source_label": "Property",
        "dest_label": "MSA"
    },
    "isLocatedInZip" : {
        "source_label": "Property",
        "dest_label": "Zip"
    },    
    "originatedLoan" : {
        "source_label": "Seller",
        "dest_label": "Loan"
    },
    "servicesLoan" : {
        "source_label": "Servicer",
        "dest_label": "Loan"
    },    
    "hasSecuritizedLoan" : {
        "source_label": "MBS",
        "dest_label": "Loan"
    },    
    "hasLoan" : {
        "source_label": "Deal",
        "dest_label": "Loan"
    }     
}

dataset_config = [
    {
        "dataset": "sf",
        "xsm_path": "csv/finance_fnma/fnma_sf_2000Q1.csv",  
        "loan_label": "Loan_SF",
        "properties": sf_node_properties,
        "nodes": ["Loan", "Borrower", "Property", "MSA", "Zip", "Loan_Snapshot", "Seller", "Servicer"],
        "edges": ["hasLoanSnapshot", "hasBorrower", "isCollateralizedBy", "isLocatedInMSA", "isLocatedInZip", "originatedLoan", "servicesLoan"]
    } 
]

graph = remote.Client(disable_version_check=False).create_graph(
    num_partitions=4
)
print("graph id:", graph.graph_id)

path = "xsm_path"
for i in dataset_config:
    df = dd.read_csv(i[path],
                     blocksize=25e6,
                     sep="|",             
                     header=None,
                     dtype=fnma_dtypes,
                     names=fnma_col_names)
    df[i["dataset"]] = "true"
    df["PROPERTY_ID"] = df["LOAN_ID"]
    df["BORROWER_ID"] = df["LOAN_ID"]
    df["LOAN_SNAPSHOT"] = df["LOAN_ID"].astype('string') + df["ACT_PERIOD"].astype('string')
    i["dask_df"] = df

reverse_edges=True
with import_data.DataFrameImporter(graph) as df_importer:   
    
    ### NODES ###
    for dataset in dataset_config:
        for node_label in dataset["nodes"]:
            # use specific loan label (ie SF, CIRT, CAS)
            if node_label == "Loan": 
                node_label = dataset["loan_label"]
            # set node props if featureless node
            if node_label in ["Zip", "MSA", "Seller", "Servicer", "Deal", "MBS"]:
                node_props = {}
                node_props[dataset["dataset"]] = "string"
            else: 
                node_props = dataset["properties"][node_label]
                        
            # import node label
            df_importer.nodes_dataframe(dataset["dask_df"],
                                    id_column=nodes[node_label]["id_column"],
                                    id_space=nodes[node_label]["id_space"], 
                                    property_columns=node_props,
                                    label=node_label)

    ### EDGES ### 
    for dataset in dataset_config:
        for edge_type in dataset["edges"]:
            source_label = edges[edge_type]["source_label"]
            if source_label == "Loan": 
                source_label = dataset["loan_label"]
            dest_label = edges[edge_type]["dest_label"]
            if dest_label == "Loan": 
                dest_label = dataset["loan_label"]    
            
            df_importer.edges_dataframe(dataset["dask_df"][[nodes[source_label]["id_column"],nodes[dest_label]["id_column"]]].drop_duplicates(),
                                    source_id_space=nodes[source_label]["id_space"],
                                    destination_id_space=nodes[dest_label]["id_space"],
                                    source_column=nodes[source_label]["id_column"],
                                    destination_column=nodes[dest_label]["id_column"],
                                    type=edge_type)
            # reverse edges
            if reverse_edges:
                df_importer.edges_dataframe(dataset["dask_df"][[nodes[source_label]["id_column"],nodes[dest_label]["id_column"]]].drop_duplicates(),
                                        source_id_space=nodes[dest_label]["id_space"],
                                        destination_id_space=nodes[source_label]["id_space"],
                                        source_column=nodes[dest_label]["id_column"],
                                        destination_column=nodes[source_label]["id_column"],
                                        type=f"rev_{edge_type}")            

```