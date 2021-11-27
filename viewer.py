import requests
import click
from requests.models import CaseInsensitiveDict
from pyfiglet import figlet_format
import json
from termcolor import colored
import six

# TO DO
#   Tidy up code
#       Page section especially
#   Make UI look nicer
#       FINALZIE FORMAT
#   Error messages
#       API unavailable / invalid response
#           Invalid response: ticket DNE ?
#           API unavailable: probably some way to check in pycurl/requests
#   Testing
#       Helper methods
#       Main methods
#       Make sure UI is good for all base cases
#           Base cases:
#   OAuth
#       ???
#   API: make sure everything is good / most efficient
#   Job status stuff?
#   Look into GET requests

# CONSTANTS

s = 'https://zccagau.zendesk.com/api/v2/'
numberPerPage = 25
maxLineLength = 100
token = 'invalid'

# Helper methods

# Creates a group of commands
@click.group()
def cli():
    pass

# Checks the login
def isValid():
    print('tmp')

# Takes in a URL, uses cURL, and returns a json
def cx(givenUrl):
    headers = {"Authorization" : "Bearer " + token}
    response = requests.get(s + givenUrl, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()

# Customized printing
def log(msg, color, font = 'slant', figlet = False):
    if not figlet:
        six.print_(colored(msg, color))
    else:
        six.print_(colored(figlet_format(
            msg, font=font), color))

# Processes the JSON and ensures that the ticket exists
def processJson(obj, type):
    if type not in obj:
        print("ERR: The ticket does not exist. Returning to view single ticket interface...")
        viewTicket()
    return obj[type]

# Formats the tickets for printing
# Can either do advanced with more detail, or
# not advanced, in sentence format. Advanced is
# only available for printing a single ticket
def formatTickets(x, advanced=False):
    id = str(x["id"])
    subj = str(x["subject"])
    sent = str(x["submitter_id"])
    opened = str(x["created_at"])

    if advanced:
        print('\n*****TICKET INFORMATION*****')
        desc = x["description"]
        print('ID: ' + id)
        print('Subject: ' + subj)
        print('Sent by: ' + sent)
        print('Opened on: ' + opened)
        print('Description:\n' + desc)
    else:
        res = "Ticket " + id + " with subject '" + subj + "' was sent on on " + sent + " and opened on " + opened + "."
        if(len(res) > maxLineLength):
            print(res[0:maxLineLength] + "...")
            # flesh out. add choice to expand
            # Break up into chunks? do 100 chars first line, next 100 next line, make sure to indent + count the tabs
        else:
            print(res)

# Main methods

# Views a ticket
# Asks for an input for a ticket ID
# If 0, return to main
# Else, prompt for the detail to be shown
# If 0, call formatTickets for regular format.
# If 1, call formatTickets for advanced format.
@cli.command(name='1')
def viewTicket():
    choice = str(input("Please enter the ticket ID, or press 0 to return to the menu: ")) #click.prompt('Enter a ticket number: ', type=click.Choice(str))
    if int(choice) > 0:
        mode = int(input("0 for regular, 1 for advanced"))
        advanced = True
        if mode == 0:
            advanced = False
        formatTickets(processJson(cx('tickets/' + choice), "ticket"), advanced)
    choice = input('*****Press any key to return to the main menu*****')
    print("\n")
    main()

# Views all tickets
# Processes the JSON, and allows for 
# one to page through tickets
@cli.command(name='2')
def viewAllTickets():
    # Receives all tickets from cURL as a dictionary
    tickets = processJson(cx('incremental/tickets.json?start_time=0'), "tickets")
    # Max number of tickets
    numTickets = len(tickets)
    # Used to start the loop
    choice = 1
    # Current page
    page = 0
    maxPage = int(numTickets / numberPerPage)
    while choice == 1 or choice == 2 or choice == 3:
        pageStart = numberPerPage * page
        pageEnd = numberPerPage + pageStart
        if pageEnd > numTickets:
            pageEnd = numTickets
        
        for x in range(pageStart, pageEnd):
            formatTickets(tickets[x], False)
        print("\nPage " + str(page + 1) + " of " + str(maxPage + 1))
        choice = int(input("\n1 for prev, 2 for next, 3 to select a page, any other input to exit: "))
        print("\n")

        if choice == 1:
            if page >= 1:
                page -= 1
        elif choice == 2:
            if pageEnd != numTickets:
                page += 1
        elif choice == 3:
            page = int(input("New page: "))
            if page > maxPage:
                page = maxPage
    main()

@cli.command()
def main():
    log('Ticket Viewer', color='blue', figlet = True)
    option = click.prompt('To view a specific ticket, press 1.\nTo view all tickets, press 2.\nTo exit, type exit.\nOption', type=click.Choice(list(cli.commands.keys()) + ['exit']))
    while option != 'exit':
        cli.commands[option]()

@click.command()
def login():
    global token
    token = input('Enter an OAuth Token: ')
    isValid()
    main()

if __name__ == '__main__':
    main()
