import time

STG = "[ANALYSIS] "

def combobulate_min(pkgs):
    for x in pkgs:
        test_exists(x)

def combobulate_heur(pkgs):
    for x in pkgs:
        test_exists(x)
        if x.exists == True:
            test_score(x)
            test_timestamp(x)
            test_verCount(x)
    stats_exists(pkgs)

def test_exists(x):
    if x.exists == True:
        print(STG +"Package: ", x, "  is present on public provider.")
    elif x.exists == False:
        print(STG + "Package: ", x, "  is NOT present on public provider.")
    elif x.exists == None:
        print(STG + "Package: ", x, "  test skipped.")

def test_score(x):
    threshold = 0.6
    risky = 0.15
    ttxt = ". Mid set to " + str(threshold) + ")"
    if x.score != None:
        if x.score > threshold:
            print(STG + ".... package scored ABOVE MID - "+ str(x.score) + ttxt)
        elif x.score <= threshold and x.score > risky:
            print(STG + ".... [RISK] package scored BELOW MID - "+ str(x.score) + ttxt)
        elif x.score <= risky:
            print(STG + ".... [RISK] package scored LOW - "+ str(x.score) + ttxt)

def test_timestamp(x):
    if x.timestamp != None:
        dayspast = ((time.time()*1000 - x.timestamp)/86400000)
        print(STG + ".... package is " + str(int(dayspast)) + " days old.")
        if (dayspast < 2): #freshness test
            print(".... [RISK] package is SUSPICIOUSLY NEW.")

def stats_exists(pkgs):
    count = 0
    for x in pkgs:
        if x.exists == True: 
            count = count + 1
    toutof = STG + str(count) + " out of " + str(len(pkgs)) + \
        " packages were present on the public provider"
    perc = "(" + str(count/len(pkgs)*100) + f"% of total)"
    print(toutof + " " + perc + ".")

def test_verCount(x):
    if x.verCount != None:
        if x.verCount < 2:
            print(STG + ".... [RISK] package history is SHORT. Total " + \
                str(x.verCount) + " versions committed.")
        else:
            print(STG + ".... Total " + \
                str(x.verCount) + " versions committed.")