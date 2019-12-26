# initializing variables
w_i = config.BANK_DETAILS['OCBC']['withdrawal']  # from BANK_DETAILS
d_i = config.BANK_DETAILS['OCBC']['deposit']     # from BANK_DETAILS
b_i = config.BANK_DETAILS['OCBC']['balance']     # from BANK_DETAILS
is_negative = False               				 # flag for default checking
final_result = []                 				 # transactions with label assigned

# iterate over all transactions
for transaction in transactions:
    # debit leading to a negative balance
    if transaction[w_i] > 0 and transaction[b_i] < 0:
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
        if transaction[d_i] == final_result[-1]['withdrawal']):
            transaction['type'] = 'Default'
    
        # default condition not met move to debit
        else:
            final_result[-1]['type'] = 'Debit'
        
            # condition not satisfied
            # now start over from current position
            if transaction[w_i] > 0 and transaction[b_i] < 0:
                is_negative = True
                transaction['type'] = 'Default'
                final_result.append(tran)
            
                continue
            
            # debit
            elif transaction[w_i] > 0:
                transaction['type'] = 'Debit'
            
            # credit
            elif transaction[d_i] > 0:
                transaction['type'] = 'Credit'
    
    # debit
    elif transaction[w_i] > 0:
        transaction['type'] = 'Debit'
    
    # credit
    elif transaction[d_i] > 0:
        transaction['type'] = 'Credit'
    
    is_negative = False
    final_result.append(transaction)