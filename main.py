"""
2015-09-18: v0.1, initial release.

This code downloads PDF versions of the front page of the New York Times.
New York Times started offering this publicly July 6, 2012 onwards.
It only downloads year by year, which should be changed (why not have it download between certain days?)
But it works fine as is.

Possible things to do later:
1) Download from X to Y instead; have better ways to define dates and catch improper inputs.
2) Have the files write to a more reasonable location, user-defined.
3) Have less reliance on loops and use datetime or some other date-related library.
4) Have a better way to show progress, and not bombard the user with that many prints.

"""

import urllib2

def main():
    # Based off of http://www.nytimes.com/images/{year}/{month}/{day}/nytfrontpage/scan.pdf
    # Where {month} and {day} are padded to two digits.
    baseurl = "http://www.nytimes.com/images/"
    file = "/nytfrontpage/scan.pdf"
    # No error checking on the year.
    year = int(raw_input("Download which year? (Only from July 6, 2012 onwards): "))
    # This is just for 2012, downloading only from July 6th onwards.
    if year == 2012:
        for month in range(7, 13):
            if month == 7 or month == 8 or month == 10 or month == 12:
                if month == 7:
                    for day in range(6, 32):
                        # I'm sorry. It's an American-based publication, though.
                        print "Downloading %d/%d/%d" % (month, day, year)
                        download_url(baseurl + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + file, year, month, day)
                else: 
                    for day in range(1, 32):
                        print "Downloading %d/%d/%d" % (month, day, year)
                        download_url(baseurl + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + file, year, month, day)
            else:
                for day in range(1, 31):
                    print "Downloading %d/%d/%d" % (month, day, year)
                    download_url(baseurl + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + file, year, month, day)    
    # The bulk of the code just deals with potential leap years (or not actually leap year leap years?), but it's unlikely we'll get that high.
    else: 
        for month in range(1, 13):
            # 31 days.
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                for day in range(1, 32):
                    print "Downloading %d/%d/%d" % (month, day, year)
                    download_url(baseurl + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + file, year, month, day)
            # 30 days.
            elif month == 4 or month == 6 or month == 9 or month == 11:
                for day in range(1, 31):
                    print "Downloading %d/%d/%d" % (month, day, year)
                    download_url(baseurl + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + file, year, month, day)
            # February.
            else:
                # Actual leap year.
                if (year % 4 == 0) and (year % 400 == 0 or year % 100 != 0):
                    for day in range(1, 30):
                        print "Downloading %d/%d/%d" % (month, day, year)
                        download_url(baseurl + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + file, year, month, day)
                # Fake leap year.
                else:
                    for day in range(1, 29):
                        print "Downloading %d/%d/%d" % (month, day, year)
                        download_url(baseurl + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + file, year, month, day)

def download_url(url, year, month, day):
    try: 
        response = urllib2.urlopen(url)
        # Forced to use "-" versus "/" due to pesky file systems.
        file = open(str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + ".pdf", 'wb')
        file.write(response.read())
        file.close()
        print "Saved file."
    except urllib2.HTTPError, err:
        # Does not gracefully deal with any other issues, like potential rate limiting. Ouch.
        # Also, unsure how to check for multiple counts of 404s in a row, like possibly extending
        # past a set of dates that the front page was posted. It's a function, so how do I keep
        # track within the function?
        if err.code == 404:
            print "PDF not found."
        else:
            raise

if __name__ == "__main__":
    main()