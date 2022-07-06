from ckan.plugins import toolkit

def format_validator(key, data, errors, context):
    if not data[key]:
        return
    # Make sure similar fomrmats look same Eg .csv, csv, CSV
    data[key] = data[key].upper().replace('.', '')
