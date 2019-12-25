import tabula
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
print(rows);