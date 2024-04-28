from cnt import *
import datetime

# create the 'bookings' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY,
        movie_name TEXT NOT NULL,
        showtime TEXT NOT NULL,
        adult_tickets INTEGER NOT NULL,
        child_tickets INTEGER NOT NULL,
        senior_tickets INTEGER NOT NULL,
        total_cost INTEGER NOT NULL,
        customer_name TEXT NOT NULL,
        email TEXT NOT NULL,
        booking_time TEXT NOT NULL
    )
''')
con.commit()

def save_booking(selected_movie, selected_showtime,  num_adult_tickets, num_child_tickets, num_senior_tickets, total_cost, full_name, email):
    
    # Insert booking data into the 'bookings' table
    cursor.execute('''
        INSERT INTO bookings (movie_name, showtime, adult_tickets, child_tickets, senior_tickets, total_cost, customer_name, email, booking_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        selected_movie,
        selected_showtime,
        num_adult_tickets,
        num_child_tickets,
        num_senior_tickets,
        total_cost,
        full_name,
        email,
        datetime.datetime.now().strftime("%Y-%m-%d")
        
    ))
    
    con.commit()

# Close the database connection when done
def close_db():
    con.close()
