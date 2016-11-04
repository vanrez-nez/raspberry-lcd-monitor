
#stackoverflow.com/questions/1094841
def format_bytes( num, append_unit=True, decimals=1 ):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB' ]:
        if abs(num) < 1024.0:
            num = round( num, decimals )
            unit = " %s" % unit if append_unit else ''
            return "%s%s" % ( num, unit )
        num /= 1024.0
    return "%.1f %s" % (num, 'ZB')
    
