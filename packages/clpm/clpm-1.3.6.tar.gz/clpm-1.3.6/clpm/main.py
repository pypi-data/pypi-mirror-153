# PROJECT: CLPM -- Command Line Password Manager
# AUTHOR: alexjaniak
# FILE: Main project file. Parses arguments from command line.


# IMPORTS
from clpm.sql_utils import *
from clpm.utils import *


@click.group()
@click.version_option(version=1.0)
def cli(): # click command group.
    pass


# TODO: FIX MENU
@cli.command()
@click.option(
    "--password", prompt=True, hide_input=True,
    confirmation_prompt=False
)
def add(password):
    """Adds account to database."""
    con = sql_connect() # Connect to db.
    if sql_compare_master(con, password): # Compare input to master password.
        # Menu for adding accounts.
        click.echo("Enter account details (\033[37;1m!\033[0m = required).") # Bright white unicode.
        click.echo("Press \033[37;1mq\033[0m to quit.") # Bright white unicode.

        account = prompt_rfield("\033[37;1m!\033[0mAccount", "account") # Bright white unicode.
        if qprompt(account): return None # Quit.
        user = prompt_field('Username')
        if qprompt(user): return None
        email = prompt_field('Email')
        if qprompt(email): return None
        tag = prompt_field('Tag')
        if qprompt(tag): return None
        acc_password = prompt_rfield("\033[37;1m!\033[0mPassword", "password")
        if qprompt(password): return None

        # Insert account using user input from menu.
        ct, iv, salt = encrypt_password(password, acc_password) # Encrypt account password.
        sql_insert_account(con, (account, user, ct, email, tag, iv, salt)) # Insert account into db. 
    else:
         click.echo("Password does not match database password.")
    con.close()


@cli.command()
@click.argument('id', default=None, type=int)
@click.option(
    "--password", prompt=True, hide_input=True,
    confirmation_prompt=False
)
def delete(id, password):
    """Deletes account from database."""
    con = sql_connect() # Connect to db. 
    if sql_compare_master(con, password): # Compare input to master password.
        sql_delete_account(con, str(id)) # Delete account from db.
    else:
         click.echo("Password does not match database password.")
    con.close()



@cli.command()
@click.option('-a','--accounts', 'type_', flag_value='accounts',
                help="Query by account.", default=True)
@click.option('-t','--tags', 'type_', flag_value='tags',
                help="Query by tags.")
@click.option('-i','--ids', 'type_', flag_value='id',
                help="Query by id.")
@click.option('-l','--all', 'type_', flag_value='all',
                help="Query all.")
@click.argument('val', default=None, required=False)
@click.option(
    "--password", prompt=True, hide_input=True,
    confirmation_prompt=False
)
def query(type_, val, password):
    """Query database."""
    con = sql_connect() # Connect to db.
    if sql_compare_master(con, password): # Compare input to master password.
        if val == None or type_ == 'all': # Get all accounts if not specified.
            cur = sql_fetch_all_acounts(con)
        else:
            if type_ == 'accounts':
                cur = sql_query_accounts(con, val)
            elif type_ == 'tags':
                cur = sql_query_tags(con, val)
            elif type_ == 'id':
                cur = sql_query_id(con, val)
        print_table(cur, password) # Outputs table with quieried accounts.
    else:
         click.echo("Password does not match database password.")
    con.close()


# TODO: Add description to password prompt. 
@cli.command()
@click.option(
    "--password", prompt=True, hide_input=True,
    confirmation_prompt=True
)
def init(password):
    """Initializes clpm."""
    con = sql_connect() # Connect to db.
    # Create sql tables in passwords db
    sql_create_accounts_table(con) 
    sql_init_master_table(con, password) # Sets master password.
    click.echo("Database initialized")
    con.close()



# TODO: Remove password authentication.
# TODO: Delete database file rather than erasing tables.
@cli.command()
@click.confirmation_option(prompt="Are you sure you want to reset clpm? All data will be lost.")
@click.option(
    "--password", prompt=True, hide_input=True,
    confirmation_prompt=True
)
def reset(password):
    """Resets clpm."""
    con = sql_connect() # Connect to db.
    if sql_compare_master(con, password): # Compare input to master password.
        # Erase db tables.
        sql_drop_accounts_table(con)
        sql_drop_master_table(con)
        click.echo("Database reset")
    else:
        click.echo("Password does not match database password.")
    con.close()




