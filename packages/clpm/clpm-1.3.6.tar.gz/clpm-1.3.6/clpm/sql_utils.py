# PROJECT: CLPM -- Command Line Password Manager
# AUTHOR: alexjaniak
# FILE: SQL helper functions.


# IMPORTS
import sqlite3 as sql
from clpm.utils import * 

def sql_connect():
    """Connects/Creates to database."""
    try:
        # Get db path.
        project_dir = str(Path(__file__).parent.absolute()) 
        db_path = os.path.join(project_dir, "passwords.db")
        
        con = sql.connect(db_path) # Connect to db. 
        return con

    except sql.Error as error:
        click.echo("Error accessing database:")
        raise error

def sql_create_accounts_table(con):
    """Creates accounts table. Holds all of the account information & encrypted passwords."""
    try: 
        cursor = con.cursor() 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account VARCHAR(255) NOT NULL,
            username VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            tag VARCHAR(50) DEFAULT 'NONE',
            iv CHAR(32),
            salt CHAR(32)
        )""")
        con.commit()
    except sql.Error as error:
        click.echo("Error creating accounts table:")
        raise error

def sql_drop_accounts_table(con):
    """Drops accounts table."""
    cursor = con.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS accounts")
        con.commit()
    except sql.Error as error:
        click.echo("Error droping account table:")
        raise error

def sql_insert_account(con, vals):
    """
        Insert a row/account into the accounts table.
        param vals: (account, username, password, email, tag, iv, salt)
        tag, iv, & salt are required for password decryption. 
    """
    cursor = con.cursor()
    try:
        cursor.execute("""
        INSERT INTO accounts (account, username, password, email, tag, iv, salt)
        VALUES (?,?,?,?,?,?,?)
        """, vals)
        con.commit()
    except sql.Error as error:
        click.echo("Error inserting account:")
        raise error

def sql_delete_account(con, id_):
    """
        Deletes an account from the accounts table.
        param id_: row/account id 
    """
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM accounts WHERE id=?", id_) # Delete row.
        con.commit()
    except sql.Error as error:
        click.echo("Error deleting account, make sure id exists:")
        raise error


def sql_query_accounts(con, account):
    """Returns cursor of accounts that match specific account from the accounts table."""
    cursor = con.cursor()
    try:
        cursor.execute("""
        SELECT * FROM accounts
        WHERE account=?
        """, (account,))
        return cursor # Return cursor query
    except sql.Error as error:
        click.echo("Error querying accounts:")
        raise error

def sql_query_tags(con, tag):
    """Returns cursor of accounts that match specific tag from the accounts table."""
    cursor = con.cursor()
    try:
        cursor.execute("""
        SELECT * FROM accounts
        WHERE tag=?
        """, (tag,))
        return cursor # Return cursor query
    except sql.Error as error:
        click.echo("Error querying accounts:")
        raise error

def sql_query_id(con, id_):
    """Returns cursor of accounts that match specific id from the accounts table."""
    cursor = con.cursor()
    try:
        cursor.execute("""
        SELECT * FROM accounts
        WHERE id=?
        """, (id_,))
        return cursor # Return cursor query
    except sql.Error as error:
        click.echo("Error querying accounts:")
        raise error

def sql_fetch_all_acounts(con):
    """Return cursor with all rows from the accounts table."""
    cursor = con.cursor()
    cursor.execute("SELECT * FROM accounts") # Select all rows.
    return cursor # Return cursor query

def sql_init_master_table(con, password):
    """Creates master password table and inserts master password."""
    cursor = con.cursor()
    digest = digest_sha_256(password) # Hash password using 256 bit SHA.
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS master(
            id INTEGER PRIMARY KEY,
            password TEXT(256) NOT NULL
        )
        """)
        cursor.execute("""
        INSERT INTO master(id, password)
        VALUES (1,?)""", (digest,))
        con.commit()
    except sql.Error as error:
        click.echo("Error initializing master table:")
        raise error

def sql_drop_master_table(con):
    """Drops master password table."""
    cursor = con.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS master")
        con.commit()
    except sql.Error as error:
        click.echo("Error erasing master table:")
        raise error

def sql_compare_master(con, password):
    """Compare string to master password."""
    cursor = con.cursor()
    digest = digest_sha_256(password) # Hash string using 256 bit SHA.
    try:
        cursor.execute("""
        SELECT * FROM master
        WHERE id=1 """) 
        master_pass = cursor.fetchone()[1] # Returns row as list of cols.

    except sql.Error as error:
        click.echo("Error comparing master to input:")
        raise error

    if master_pass == digest: return True
    return False

