import requests
import click
from requests.models import CaseInsensitiveDict
from pyfiglet import figlet_format
import json
from termcolor import colored
import six

# CONSTANTS
s = 'https://zccagau.zendesk.com/api/v2/'   # Base url for all requests
numberPerPage = 10                          # Number of requests per page when all tickets requested
maxLineLength = 100                         # Max line length of a ticket requested in basic mode
token = 'invalid'                           # The OAuth token inputted by the user
testing = False                             # Allows one to call individual methods

# Helper methods

# Creates a group of commands
@click.group()
def cli():
    pass

def log(msg, color, font = 'slant', figlet = False):
    '''
    Customized printing
    '''
    if not figlet:
        six.print_(colored(msg, color))
    else:
        six.print_(colored(figlet_format(
            msg, font=font), color))

def isValid():
    '''
    Checks login calling a URL that the OAuth token should have access to.
    Returns False and prints the error if the data was not able to be accessed.
    Otherwise, returns True.
    Handles a bad API key or an unavailable API.
    '''
    return cx('tickets/count', logging_in=True)

def cx(givenUrl, logging_in=False):
    '''
    Receives a URL extension and requests the information from the API.
    Prints an error and returns to the main menu if the request is invalid.
    Else, returns a JSON of the received data.
    '''
    headers = {'Authorization' : 'Bearer ' + token}
    try:
        response = requests.get(s + givenUrl, headers=headers)
        response.raise_for_status()
    except Exception as e:
        template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
        message = template.format(type(e).__name__, e.args)
        log(message, 'red')
        if testing:
            return False
        else:
            if logging_in:
                login()
            else:
                main()
    if testing:
        return True
    #if response.status_code != 204:
    return response.json()

def fixLength(str):
    '''
    Fixes the length of a string to 100 characters.
    Adds a newline at every 100 characters.
    '''
    lines = []
    for i in range(0, len(str), maxLineLength):
        lines.append(str[i:i+maxLineLength])
    return '\n'.join(lines)

def formatTickets(x, advanced=False):
    '''
    Formats the tickets for printing
    Can either do advanced with more detail, or
    not advanced, in sentence format. Advanced is
    only available for printing a single ticket
    '''
    id = str(x['id'])
    subj = str(x['subject'])
    sent = str(x['submitter_id'])
    opened = str(x['created_at'])
    if advanced:
        print('\n*****TICKET INFORMATION*****\n')
        desc = x['description']
        template = 'ID: {0}\nSubject: {1}\nSent by: {2}\nOpened on: {3}\nDescription:\n{4}'
        res = template.format(id, fixLength(subj), sent, opened, fixLength(desc))
    else:
        template = 'Ticket {0} with subject {1} was sent on {2} and opened on {3}.\n'
        res = fixLength(template.format(id, subj, sent, opened))
    print(res)

# Main methods

@cli.command(name='1')
def viewTicket():
    '''
    Views a ticket
    Asks for an input for a ticket ID
    If 0, return to main
    Else, request the ticket data from the API
    '''
    # Gets the choice for a ticket ID
    choice = click.prompt('Please enter the ticket ID, or press 0 to return to the menu', type=int)
    if choice > 0:
        formatTickets(cx('tickets/' + str(choice))['ticket'], True)
        choice = input('\n*****Press any key to return to the main menu*****\n')
    if not testing:
        main()

@cli.command(name='2')
def viewAllTickets():
    '''
    Views all tickets
    Allows paging through tickets
    '''
    # Receives all tickets from cURL as a dictionary
    tickets = cx('incremental/tickets.json?start_time=0')['tickets']
    # Total' number of tickets
    numTickets = len(tickets)
    # Used to start the loop
    choice = 1
    # Current page
    page = 0
    maxPage = int(numTickets / numberPerPage)
    while choice == 1 or choice == 2 or choice == 3:
        # 0-based indexing for pages
        pageStart = numberPerPage * page
        pageEnd = numberPerPage + pageStart
        # ensures that the page end does not go past the maximum number of tickets
        if pageEnd > numTickets:
            pageEnd = numTickets
        
        # Print all tickets in that range
        for x in range(pageStart, pageEnd):
            formatTickets(tickets[x], False)
        
        print('\nPage ' + str(page + 1) + ' of ' + str(maxPage + 1))
        # Refresh choice
        choice = click.prompt('\nTo view the previous page, press 1.\nTo view the next page, press 2.\nTo select a page, press 3.\nTo exit, enter any other number\nOption', type=int)
        print('\n')

        if choice == 1:
            if page >= 1:
                page -= 1
        elif choice == 2:
            if page != maxPage:
                page += 1
        elif choice == 3:
            page = click.prompt('New page', type=int) - 1
            if page > maxPage:
                page = maxPage
            elif page < 0:
                page = 0
    if not testing:
        main()

@cli.command()
def main():
    log('Ticket Viewer', color='blue', figlet = True)
    option = click.prompt('To view a specific ticket, press 1.\nTo view all tickets, press 2.\nTo exit, type exit.\nOption', type=click.Choice(list(cli.commands.keys()) + ['exit']))
    while option != 'exit':
        cli.commands[option]()

def login():
    global token
    token = click.prompt('Enter an OAuth Token')
    if isValid() and not testing:
        print('*****WELCOME*****')
        main()

if __name__ == '__main__':
    login()