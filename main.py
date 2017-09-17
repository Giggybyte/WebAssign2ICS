# WebAssign2ICS
# by Dustin "giggybyte" Smith

# Given a correct login, will export your current assignments into
# an .ics (calendar) file.

# Handles web requests
import requests as r
# Handles password input
import getpass
# Handles regex
import re
# For naming the .ics file
import datetime
# For parsing the date string
import dateparse as dp

def main():
    """
    Get user/pass from the user and pass it to wa_auth.
    TODO: Let user define a login file so they don't have to type this in
          every single time.
    """
    username = input('WebAssign username: ')
    password = getpass.getpass('WebAssign password (invisible!): ')
    wa_auth(username, password)

def wa_auth(un, pw):
    """
    Authenticate, and download the next page, given the proper UserPass cookie.
    Params ==> un -> string -> user-provided username
               pw -> string -> user-provided password
    """
    # URL to send the POST request to.
    authURL = "https://www.webassign.net/web/auth/login/sso"
    # Build the POST request.
    # TODO: There are certain headers this could probably do without, like
    #       user-agent, cache-control, and referer.
    body = "{\"uid\": \"" + un + "\", \"password\":\"" + pw + "\"}"
    headers = {
        'host': "www.webassign.net",
        'accept': "application/json, text/plain, */*",
        'accept-language': "en-US,en;q=0.5",
        'accept-encoding': "gzip, deflate, br",
        'referer': "https://www.webassign.net/wa-auth/login",
        'content-type': "application/json"
        }
    # Send the request and store the result in reply.
    reply = r.request("POST", authURL, data=body, headers=headers)
    # Check if the UserPath cookie exists.
    if "UserPass" in reply.cookies:
        print("Logged in successfully.")
        wa_page_parse(reply.cookies["UserPass"])
    else:
        print("Login failed. Check your internet connection and ensure " + 
              "that you typed your user/pass correctly.")
 
def wa_page_parse(cookie):
    """
    Download the next page, which includes the assignments and due dates, and
    parse the HTML to get a list of assignments and their due dates.
    Params ==> cookie -> string -> the "UserPass" cookie from logging in
    """
    # URL to grab assignments from.
    # The lack of https isn't a typo -- they have an https login and then a
    # plain old http webpage after logging in.
    assignURL = "http://www.webassign.net/v4cgi/student.pl"
    # Adding the login cookie we obtained earlier to the GET request.
    cookieJar = r.cookies.RequestsCookieJar()
    cookieJar.set("UserPass", cookie, domain="www.webassign.net", path="/")
    reply = r.get(assignURL, cookies=cookieJar)
    # Split the reply for each line.
    htmlBody = reply.text.split("\n")
    # Iterate over each line to find a certain keyword.
    indexList = []
    i = 0
    for line in htmlBody:
        # We can actually use WebAssign's terrible flash requirement to
        # our advantage here. This "Flash required" icon appears near
        # every assignment we have.to do.
        if "WebAssign_Requirement_Flash_icon" in line:
            indexList.append(i)
        i += 1
    if indexList == []:
        print("No assignments found. Enjoy your free time!")
    # Now that we have a list of line numbers that have the keyword, we
    # can do some simple math to get the line numbers before and after
    # the keyword that have the assignment name and due date, respectively.
    matrix = []
    for n in indexList:
        matrix.append([n-4, n+8])
    # Now we get the actual string associated with each line number, and use
    # regex to remove the html
    assignments = []
    for [a, b] in matrix:
        part1 = re.sub("<[^<]+?>", "", htmlBody[a])
        part2 = re.sub("<[^<]+?>", "", htmlBody[b])
        part3 = re.sub("\s+", " ", part2)
        assignments.append([part1, part3])
    list_to_ics(assignments)

def list_to_ics(aList):
    print("Found " + str(len(aList)) + " assignments.")
    t = datetime.datetime.now()
    Y = str(t.year)
    M = str(t.month).zfill(2)
    D = str(t.day).zfill(2)
    h = str(t.hour).zfill(2)
    m = str(t.minute).zfill(2)
    s = str(t.second).zfill(2)
    filename = "WebAssign-"+Y+"."+M+"."+D+"-"+h+"."+m+"."+s+".ics"
    output = open(filename, 'x')
    output.write("BEGIN:VCALENDAR\n")
    output.write("VERSION:2.0\n")
    output.write("CALSCALE:GREGORIAN\n")
    output.write("PRODID:WebAssign2ICS\n")
    # TODO: For each assignment, add to ICS
    for assignment in aList:
        print(" - " + assignment[0] + " due at" + assignment[1])
        dateconv = dp.parse_date(assignment[1])
        output.write("BEGIN:VEVENT\n")
        output.write("DTSTART:"+dateconv+"\n")
        output.write("DTEND:"+dateconv+"\n")
        output.write("SUMMARY:WebAssign -- "+assignment[0]+"\n")
        output.write("END:VEVENT\n")
    output.write("END:VCALENDAR\n")
    print("Output file ==> " + filename)
 
main()
