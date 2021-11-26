import pycurl
import certifi
from io import BytesIO
import click
from pyfiglet import figlet_format
import json

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

def formatTickets(obj, formatType):
    # {"error":"RecordNotFound","description":"Not found"} check for this
    x = json.loads(obj)
    if len(x) == 2:
        print('Ticket DNE')
        viewTicket()
    
    x = x["ticket"]
    id = str(x["id"])
    subj = x["subject"]
    sent = '1'
    opened = '1'
    # print out some important data before
    # What would you want to see?
    # Total number
    # Time it took to receive?
    # Create an enable/disable button for this
    # Rate limit?
    print("Ticket " + id + " with subject " + subj + ", was sent on on " + sent + " and opened on " + opened + ".")

    if formatType:
        desc = x["description"]
        print("Desc: " + desc) # format so x amount of characters. add button to expand/close?

# Main methods

@cli.command(name='1')
def viewTicket():
    choice = str(input("Choice: ")) #click.prompt('Enter a ticket number: ', type=click.Choice(str))
    formatTickets(cx('tickets/' + choice), False)
    main()

@cli.command(name='2')
def viewAllTickets():
    formatTickets(obj = cx('incremental/tickets.json?start_time=0'))
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
    
    

if __name__ == '__main__':
    main()