# ------Used Rich Library for colorful output --------

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import track
import json
import os
import time

console = Console()
FILE_NAME = "library.txt"

# ---------------- BANNER ----------------
def display_banner():
    console.print("📚 Welcome to Your Personal Library Manager!\n", style="bold green")

# ---------------- FILE HANDLING ----------------
def load_library():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_library(library):
    with open(FILE_NAME, "w") as f:
        json.dump(library, f)

# ---------------- CORE FEATURES ----------------
def add_book(library):
    console.rule("[bold green]Add a Book")
    title = Prompt.ask("📖 Title")
    author = Prompt.ask("✍️ Author")
    year = int(Prompt.ask("📅 Publication Year"))
    genre = Prompt.ask("🏷️ Genre")
    read = Confirm.ask("✅ Have you read this book?")

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }

    library.append(book)
    console.print("🎉 Book added successfully!", style="bold green")

def remove_book(library):
    console.rule("[bold red]Remove a Book")
    title = Prompt.ask("Enter the title to remove")
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            console.print(f"🗑️ '{title}' removed successfully!", style="bold red")
            return
    console.print("⚠️ Book not found.", style="yellow")

def search_book(library):
    console.rule("[bold cyan]Search a Book")
    method = Prompt.ask("Search by", choices=["title", "author"])
    keyword = Prompt.ask(f"Enter {method}")
    results = [
        book for book in library
        if keyword.lower() in book[method].lower()
    ]
    if results:
        show_books(results)
    else:
        console.print("😔 No matching books found.", style="yellow")

def show_books(library):
    if not library:
        console.print("📭 No books in the library.", style="yellow")
        return

    table = Table(title="📚 Your Library", title_style="bold magenta")
    table.add_column("No.", style="dim")
    table.add_column("Title", style="bold")
    table.add_column("Author")
    table.add_column("Year", justify="right")
    table.add_column("Genre")
    table.add_column("Read", justify="center")

    for i, book in enumerate(library, start=1):
        read_status = "[green]✔[/green]" if book["read"] else "[red]✘[/red]"
        table.add_row(str(i), book["title"], book["author"], str(book["year"]), book["genre"], read_status)

    console.print(table)

def show_statistics(library):
    console.rule("[bold blue]Library Statistics")
    total = len(library)
    read = sum(1 for book in library if book["read"])
    percent = (read / total * 100) if total else 0
    console.print(f"📚 Total books: [bold]{total}[/bold]")
    console.print(f"📖 Books read: [bold green]{read}[/bold green] ({percent:.1f}%)")

def animated_exit(library):
    save_library(library)
    console.print("\n💾 Saving library...", style="cyan")
    for _ in track(range(20), description="Saving..."):
        time.sleep(0.02)
    console.print("👋 Goodbye! Come back soon.", style="bold green")
    exit()

# ---------------- MAIN MENU ----------------
def main():
    library = load_library()
    display_banner()

    while True:
        console.rule("[bold yellow]Main Menu")
        console.print("""
[bold cyan]1.[/bold cyan] Add a book  
[bold cyan]2.[/bold cyan] Remove a book  
[bold cyan]3.[/bold cyan] Search for a book  
[bold cyan]4.[/bold cyan] Display all books  
[bold cyan]5.[/bold cyan] Display statistics  
[bold cyan]6.[/bold cyan] Exit
""")

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            show_books(library)
        elif choice == "5":
            show_statistics(library)
        elif choice == "6":
            animated_exit(library)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    main()
