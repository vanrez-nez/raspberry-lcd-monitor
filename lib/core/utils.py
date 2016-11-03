#stackoverflow.com/questions/1094841
def format_bytes( num, suffix='B' ):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei' ]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" %s (num, 'Zi', suffix)
    
