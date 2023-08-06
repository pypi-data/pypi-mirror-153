import click, requests, json, os
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

API_URL = os.getenv("API_URL")
CGC_SECRET = os.getenv("CGC_SECRET")


@click.group("billing")
def billing_group():
    """
    Group to store all the billing commands.
    """
    pass


@billing_group.command("status")
def billing_status():
    """
    Shows billing status for user namespace
    """
    click.echo("Showing billing status!")


@billing_group.command("pay")
def billing_pay():
    """
    Interface for easy payment
    """
    click.echo("Initializing payment!")


@click.group("fvat")
def fvat_group():
    """
    Group to store all invoice commands
    """
    pass


@fvat_group.command("ls")
def fvat_ls():
    """
    Lists all invoices for user namespace
    """
    click.echo("Listing all invoices!")


@fvat_group.command("id")
@click.argument("id")
def fvat_id(id: str):
    """
    Opens invoice with given ID
    """
    click.echo(f"Opening invoice {id}!")


billing_group.add_command(fvat_group)
