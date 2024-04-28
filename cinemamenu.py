from cnt import *
import cinemadb  
import datetime

current_time = datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M:%S")

# Define ticket prices
ticket_prices = {
    "Adult": 20,
    "Child": 10,
    "Senior Citizen": 15,
}

# Define movie showtimes
# Also states available seats for each showtime
movie_details = {
    "SAW X": {
        "10:00 AM": 50,   
        "2:00 PM": 50,
        "6:00 PM": 50,
    },
    "Oppenheimer": {
        "11:00 AM": 60,
        "3:00 PM": 60,
        "7:00 PM": 60,
    },
    "Barbie": {
        "12:00 PM": 40,
        "4:00 PM": 40,
        "8:00 PM": 40,
    },
    "The Equaliser 3": {
        "1:00 PM": 30,
        "5:00 PM": 30,
        "9:00 PM": 30,
    },
    "The Nun 2": {
        "2:00 PM": 55,
        "6:00 PM": 55,
        "10:00 PM": 55,
    },
}

def list_movies():
    # Define a list of available movies
    movies = list(movie_details.keys())
    
    print("\nAvailable Movies:")
    for idx, movie in enumerate(movies, start=1):
        print(f"{idx}. {movie}")
    
    return movies

def book_tickets(selected_movie):
    print(f"Booking tickets for '{selected_movie}'")
    
    # Show available showtimes and seats for the selected movie
    showtimes = movie_details[selected_movie]
    print("Available Showtimes:")
    for idx, (showtime, available_seats) in enumerate(showtimes.items(), start=1):
        print(f"{idx}. {showtime} - Available Seats: {available_seats}")
    
    # Gather booking details from the user
    showtime_choice = int(input("Enter the number of the showtime you prefer: "))
    if 1 <= showtime_choice <= len(showtimes):
        selected_showtime = list(showtimes.keys())[showtime_choice - 1]
    else:
        print("Invalid showtime choice.")
        return
    
    num_adult_tickets = int(input("How many Adult tickets would you like to book: "))
    num_child_tickets = int(input("How many Child tickets would you like to book: "))
    num_senior_tickets = int(input("How many Senior Citizen tickets would you like to book: "))
    
    # Calculate the total cost
    total_cost = (
        num_adult_tickets * ticket_prices["Adult"]
        + num_child_tickets * ticket_prices["Child"]
        + num_senior_tickets * ticket_prices["Senior Citizen"]
    )

    # Check if there are enough available seats
    if (
        movie_details[selected_movie][selected_showtime]
        >= num_adult_tickets + num_child_tickets + num_senior_tickets
    ):
        # Reduce the available seats for the selected showtime
        movie_details[selected_movie][selected_showtime] -= (
            num_adult_tickets + num_child_tickets + num_senior_tickets
        )
    else:
        print("Not enough available seats. Booking canceled.")
        return
    
    # Gather customer details
    email = input("Enter your email: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    confirm = input("Confirm booking? (yes/no): ").lower()
    full_name = (first_name + " " +last_name)
    
    if confirm == "yes":
        print("Booking confirmed. \nEnjoy the movie! See you soon.")
        
        # Print tickets
        print_ticket(selected_movie, selected_showtime, num_adult_tickets, num_child_tickets, num_senior_tickets, total_cost, full_name, email)
        
        # Save booking details using the save_booking function from the database module
        cinemadb.save_booking(selected_movie, selected_showtime, num_adult_tickets, num_child_tickets, num_senior_tickets, total_cost, full_name, email)
    else:
        print("Booking not confirmed. Returning to the beginning of the booking process.")

def print_ticket(movie, showtime, num_adult_tickets, num_child_tickets, num_senior_tickets, total_cost, full_name, email):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d") , datetime.datetime.now().strftime("%H:%M:%S")
    print("\n--- Ticket Details ---")
    print(f"Movie: {movie}")
    print(f"Showtime: {showtime}")
    print(f"Number of Adult Tickets: {num_adult_tickets}")
    print(f"Number of Child Tickets: {num_child_tickets}")
    print(f"Number of Senior Citizen Tickets: {num_senior_tickets}")
    print(f"Total Cost: £{total_cost}")
    print(f"Booker's Name: {full_name}")
    print(f"Booker's Email: {email}")
    print(f"Purchase time: {current_date},")

# Define the delete_booking function
def delete_booking():
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    try:
        booking_id_to_delete = int(input("Enter the ID of the booking to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid booking ID.")
        return

    if booking_id_to_delete in [booking[0] for booking in bookings]:
        cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id_to_delete,))
        con.commit()
        print(f"Booking with ID {booking_id_to_delete} has been deleted.")
    else:
        print("Invalid booking ID. Please enter a valid booking ID.")

    

def view_bookings():
    # Retrieve and display all booking details from the database
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    
    if not bookings:
        print("No bookings found.")
        return
    

    print("\nBooking Details:")
    for booking in bookings:
        print(f"Booking ID: {booking[0]}")
        print(f"Movie: {booking[1]}")
        print(f"Showtime: {booking[2]}")
        print(f"Customer: {booking[7]}")
        print(f"Email: {booking[8]}")
        print(f"Booking Time: {booking[9]}\n")



# Main program loop
while True:
    print("\nOptions:")
    print("1. Book tickets")
    print("2. View bookings")
    print("3. Delete booking")
    print("4. Quit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        movies = list_movies()
        movie_choice = int(input("Enter the number of the movie you want to watch: "))
        
        if 1 <= movie_choice <= len(movies):
            selected_movie = movies[movie_choice - 1]
            book_tickets(selected_movie)
        else:
            print("Invalid movie choice.")
    elif choice == '2':
        view_bookings()
    elif choice == '3':
        delete_booking()  
    elif choice == '4':
        print("You're welcome back any time!")
        break
    else:
        print("Invalid choice. Please try again.")
