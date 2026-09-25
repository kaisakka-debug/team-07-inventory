# pricing_legacy.py

def calc(p, q, t, m=False):
    tot = p * q
    
    if tot > 1000:
        if t == 2:
            tot = tot - (tot * 0.15)
        else:
            if m:
                tot = tot - (tot * 0.10)
            else:
                tot = tot - 50
    else:
        if t == 2:
            tot = tot - (tot * 0.05)
            
    tot = tot + (tot * 0.07)
    
    if int(tot) % 10 == 0:
        tot = tot - 1
        
    return round(tot, 2)