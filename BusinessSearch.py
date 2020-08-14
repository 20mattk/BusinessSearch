import requests
import config
from tkinter import Tk, Canvas, PhotoImage, Label, Frame, Entry, Button, Scrollbar, Listbox

def get_businesses():
    """
    Retrieves lists of businesses based on user-entered filters.

    User will first enter a location, business type, and a star rating then search.
    Program will connect to Yelp API with an api key and will pick out the businesses
    that meet the user-entered criteria. The final list of buisnesses and their star
    ratings will be sorted and outputted in descending order by raring for the user 
    to see. Exceptions will be throw if fields are left blank or entered information
    is invalid.

    Parameters: None

    Returns: None
    """

    # Clear lisbox text for new entry
    results_listbox.delete(0, "end") 

    # Asks user for data, will throw an exception if a field is left blank
    try:
        zip_code = location_entry.get() # location
        type_of_place = business_entry.get() # type of buisness
        rest_rate = float(ratings_entry.get()) # rating
    except ValueError:
        results_listbox.insert("end", "All fields required.")

    # Instering user-entered variables and the api key into required fields
    header = {
        "Authorization": "Bearer " + config.api_key
    }
    params = {
        "term": type_of_place.title(),
        "location": zip_code
    }

    # Gaining access to Yelp API and grabbing the buisness information
    # Will throw an exception if user-entered fields cannot be found
    try: 
        response = requests.get(config.url, headers=header, params=params)
        businesses = response.json()["businesses"]
    except:
        results_listbox.insert("end", "Invalid credentials entered.")

    # Fetching and filtering all buisnesses based on user-entered filters
    final = {business["name"]: business["rating"] for business in businesses if business["rating"] >= rest_rate}
    final = sorted(final.items(), key=lambda k: k[1], reverse=True)

    # Adding the results to the listbox for visual feedback in GUI
    for key, value in final:
        results_listbox.insert("end", str(key) + ": " + str(value))

    # Clear the list for program end or another search
    final.clear()


# GUI Setup
root = Tk()
root.title("Business Search")

canvas = Canvas(root, height=600, width=600)
canvas.pack()

# Background Image Setup
background_image = PhotoImage(file="my-vexels-design.png")
bakcground_label = Label(root, image=background_image)
bakcground_label.place(relwidth=1, relheight=1)

# Setup fields for location functionality
location_frame = Frame(root, bg="#6c4cfc", bd=5)
location_frame.place(relx=0.5, rely=0.05, relwidth=0.8, relheight=0.15, anchor="n")

location_label = Label(location_frame, text="Location Indicator", bg="#6c4cfc", fg="white", font=("Century", 20))
location_label.place(relx=0.15, relwidth=0.7, relheight=0.4)

location_entry = Entry(location_frame, font=40, justify="center")
location_entry.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.55)

# Setup fields for type of business functionality
business_frame = Frame(root, bg="#6c4cfc", bd=5)
business_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.15, anchor="n")

business_label = Label(business_frame, text="Type of Business", bg="#6c4cfc", fg="white", font=("Century", 20))
business_label.place(relx=0.15, relwidth=0.7, relheight=0.4)

business_entry = Entry(business_frame, font=40, justify="center")
business_entry.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.55)

# Setup fields for user-entered ratings functionality
ratings_frame = Frame(root, bg="#6c4cfc", bd=5)
ratings_frame.place(relx=0.5, rely=0.35, relwidth=0.8, relheight=0.15, anchor="n")

ratings_label = Label(ratings_frame, text="Stars Out of 5.0", bg="#6c4cfc", fg="white", font=("Century", 20))
ratings_label.place(relx=0.15, relwidth=0.7, relheight=0.4)

ratings_entry = Entry(ratings_frame, font=40, justify="center")
ratings_entry.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.55)

# Setup fields for the search function
find_frame = Frame(root, bg="#6c4cfc", bd=5)
find_frame.place(relx=0.5, rely=0.55, relwidth=0.3, relheight=0.1, anchor="n")

find_button = Button(find_frame, text="GO!", bg="white", command=get_businesses, font=("Century", 20))
find_button.place(relwidth=1, relheight=1)

# Setup fields for the results based on filters
results_frame = Frame(root, bg="#6c4cfc", bd=5)
results_frame.place(relx=0.5, rely=0.7, relwidth=0.8, relheight=0.2, anchor="n")

scrlbr = Scrollbar(results_frame, orient="vertical")

results_listbox = Listbox(results_frame, yscrollcommand=scrlbr.set, font=("Century", 10))
results_listbox.place(relwidth=0.95, relheight=1)

scrlbr.config(command=results_listbox.yview)
scrlbr.place(relwidth = 0.05, relheight=1, relx=0.95, rely=0)

root.mainloop()
