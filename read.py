import config as config
import tabula
import pandas as pd
# reading table using tabula
filepath = './Bank Statement - OCBC.pdf'
rows = tabula.read_pdf(filepath,
                       pages='all',
                       silent=True,
                       pandas_options={
                           'header': None,
                           'error_bad_lines': False,
                           'warn_bad_lines': False
                       })
# converting to list
rows = rows.values.tolist()
#print(len(rows));

# --- GET HEADER ROW -----

# LIST TO CONTAIN ALL HEADERS

headers = []

# loop over all rows
last_cols_matched = ["Balance", "Baki", float("nan"), 'Hold Amount', 'Late Local Cheque']
#for row in rows:
    #print(row)
    #row_length = len(row)     
    #if(str(row[row_length - 1]) in last_cols_matched):
        #print(row[row_length - 1])
        #print(type(row[row_length - 1]))
        #headers.append(rows)
    #else:
        #break
#print(headers)
#exit()
# --- REMOVE HEADERS ----

# list to contain valid transactions

valid_transactions = []

# iterate over all rows
for row in rows:
    #if row not in headers:
    row_length = len(row) 
    if(row[row_length - 1] not in last_cols_matched and pd.isnull(row[row_length - 1]) == False):
        valid_transactions.append(row)
#print(valid_transactions)
#exit();

# initializing variables
transactions = []                                                    # list to store single row entries
d_i = config.BANK_DETAILS['OCBC']['transaction_date']                # from BANK_DETAILS
p_i = config.BANK_DETAILS['OCBC']['transaction_description']         # from BANK_DETAILS

# iterate over all transactions
for v_t in valid_transactions:
    # date exists in the row
    if v_t[d_i] is not None:
        transactions.append(v_t)
    
    # date empty, multiline particular
    else:
        # add v_t's particular to last entry in transactions
        transactions[-1][p_i] += v_t[p_i]
#print(transactions)
#exit()

# initializing variables
w_i = config.BANK_DETAILS['OCBC']['withdrawal']  # from BANK_DETAILS
d_i = config.BANK_DETAILS['OCBC']['deposit']     # from BANK_DETAILS
b_i = config.BANK_DETAILS['OCBC']['balance']     # from BANK_DETAILS
is_negative = False                              # flag for default checking
final_result = []                                # transactions with label assigned

# iterate over all transactions
for transaction in transactions:
    # debit leading to a negative balance
    if type(transaction[w_i]) != 'str' and type(transaction[b_i]) != 'str': 
        if float(transaction[w_i]) > 0 and float(transaction[b_i]) < 0:
            if is_negative:
                # default condition not satisfied so move to debit
                final_result[-1]['type'] = 'Debit'
            
            is_negative = True
            transaction['type'] = 'Default'
            final_result.append(transaction)

            # to avoid last statement of is_negative = False
            continue
        
        # followed by credit of same amount
        elif is_negative:
            # default condition met
            if (float(transaction[d_i]) == final_result[-1]['withdrawal']):
                transaction['type'] = 'Default'
        
            # default condition not met move to debit
            else:
                final_result[-1]['type'] = 'Debit'
            
                # condition not satisfied
                # now start over from current position
                if float(transaction[w_i]) > 0 and float(transaction[b_i]) < 0:
                    is_negative = True
                    transaction['type'] = 'Default'
                    final_result.append(tran)
                
                    continue
                
                # debit
                elif float(transaction[w_i]) > 0:
                    transaction['type'] = 'Debit'
                
                # credit
                elif float(transaction[d_i]) > 0:
                    transaction['type'] = 'Credit'
        
        # debit
        elif float(transaction[w_i]) > 0:
            transaction['type'] = 'Debit'
        
        # credit
        elif float(transaction[d_i]) > 0:
            transaction['type'] = 'Credit'
        
        is_negative = False
        final_result.append(transaction)
    
print(final_result)

# method to categorize a particular
def categorize(particular):
    # tokenizing
    word_list = tokenize(particular)
    
    # multiple similar statements
    if keyword in word_list:
        return category

# iterate over all transactions
for transaction in final_result:
    # assign category
    transaction['category'] = categorize(transaction['particular'])


