import pycurl
import certifi
from io import BytesIO
import click
from pyfiglet import figlet_format
import json

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


s = 'https://zccagau.zendesk.com/api/v2/'

@click.group()
def cli():
    pass

# Helper methods

def cx(givenUrl):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, s + givenUrl)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(pycurl.USERPWD, '%s:%s' %('ksilvergold18@gmail.com', 'Tmp123'))
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()

    body = buffer.getvalue()
    
    return body.decode('iso-8859-1')

def log(msg, color):
    print("tmp")

def getTicketAmount():
    return cx('tickets/count.json')

def processJson(obj, type):
    x = json.loads(obj)
    if type not in x:
        print("Key DNE")
        viewTicket()
    return x[type]

def formatTickets(x, formatType):
    id = str(x["id"])
    subj = x["subject"]
    sent = '1'
    opened = '1'
    res = "Ticket " + id + " with subject '" + subj + "' was sent on on " + sent + " and opened on " + opened + "."
    if(len(res) > 100):
        print(res[0:100] + "...")
        # flesh out. add choice to expand
        # Break up into chunks? do 100 chars first line, next 100 next line, make sure to indent + count the tabs
    else:
        print(res)
    if formatType:
        desc = x["description"]
        print("Desc: " + desc) # format so x amount of characters

# Main methods

@cli.command(name='1')
def viewTicket():
    choice = str(input("Choice: ")) #click.prompt('Enter a ticket number: ', type=click.Choice(str))
    if int(choice) > 0:
        formatTickets(processJson(cx('tickets/' + choice), "ticket"), False)
    main()

@cli.command(name='2')
def viewAllTickets():
    tickets = processJson(cx('incremental/tickets.json?start_time=0'), "tickets")
    numTickets = len(tickets)
    choice = 1
    page = 0
    while choice == 1 or choice == 2 or choice == 3:
        pageStart = 25 * page
        pageEnd = 25 + pageStart
        if pageEnd > numTickets:
            pageEnd = numTickets
        
        for x in range(pageStart, pageEnd):
            formatTickets(tickets[x], False)
        choice = int(input("1 for prev, 2 for next: "))

        if choice == 1:
            if page >= 1:
                page -= 1
        elif choice == 2:
            if pageEnd != numTickets:
                page += 1
        elif choice == 3:
            page = int(input("New page: "))
            if page > numTickets / 25:
                page = int(numTickets / 25)
            
        
    main()

@cli.command()
def main():
    choice = click.prompt('Select a command to run', type=click.Choice(list(cli.commands.keys()) + ['exit']))
    while choice != 'exit':
        cli.commands[choice]()
    

    # Authorization step w/ option to quit
    # Display options
    # Choose options
    # Quit or choose another option?
    # Options:
    #   1. View a specific ticket
    #       1 -> enter a ticket number
    #       0 -> return to main menu
    #   2. View all tickets
    #       List out, if > 25
    #       1 -> prev page
    #       2 -> next page
    #       3 -> enter custom page
    #           *** list num pages, REJECT errors over ending the program
    #       4 -> return to main menu
    
    # print out some important data before. Could have this in the curl method?
    # What would you want to see?
    # Total number
    # Time it took to receive?
    # Create an enable/disable button for this
    # Rate limit?
    

if __name__ == '__main__':
    main()
