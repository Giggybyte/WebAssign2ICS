# WebAssign2ICS Helper File
# by Dustin "giggybyte" Smith

# This file is solely for parsing the dates given by the second element of each
# assignment.

def parse_date(dStr):
    """
    Splits dStr, and handLes each element individually
    Params ==> dStr -> string -> date string from second element
    """
    # There's a trailing space in each date string, so we solve that
    # problem here.
    dS = dStr[1:]
    dL = dS.split(" ")
    # Convert month to a number. (e.g. May => 5)
    # Add it to an array that will be joined later.
    # This is pretty messy since Python doesn't have case/switch.
    dF = []
    dF.append(dL[2])     # Add the year first
    if   dL[0] == "Jan":
        dF.append("01")
    elif dL[0] == "Feb":
        dF.append("02")
    elif dL[0] == "Mar":
        dF.append("03")
    elif dL[0] == "Apr":
        dF.append("04")
    elif dL[0] == "May":
        dF.append("05")
    elif dL[0] == "Jun":
        dF.append("06")
    elif dL[0] == "Jul":
        dF.append("07")
    elif dL[0] == "Aug":
        dF.append("08")
    elif dL[0] == "Sep":
        dF.append("09")
    elif dL[0] == "Oct":
        dF.append("10")
    elif dL[0] == "Nov":
        dF.append("11")
    elif dL[0] == "Dec":
        dF.append("12")
    else:
        print("Month not found?")
        sys.exit(1)
    # Add trailing zeros to days 1-9.
    if   dL[1] == "1":
        dF.append("01")
    elif dL[1] == "2":
        dF.append("02")
    elif dL[1] == "3":
        dF.append("03")
    elif dL[1] == "4":
        dF.append("04")
    elif dL[1] == "5":
        dF.append("05")
    elif dL[1] == "6":
        dF.append("06")
    elif dL[1] == "7":
        dF.append("07")
    elif dL[1] == "8":
        dF.append("08")
    elif dL[1] == "9":
        dF.append("09")
    else:
        dF.append(dL[1])
    # Conversion to 24hr time.
    ampm  = dL[4]
    aTime = dL[3].split(":")
    if dL[4] == "PM":
        # In 24hr time, midnight is 00.
        if str(int(aTime[0])+12) == "24":
            dF.append("00")
        else:
            dF.append(str(int(aTime[0])+12))
        dF.append(aTime[1])
    else:
        dF.append(aTime[0])
        dF.append(aTime[1])
    # Insert some characters required by the .ics format.
    dF.insert(3,"T")
    dF.insert(6,"00")
    # Swap year and 
    dF = "".join(dF)
    return dF
