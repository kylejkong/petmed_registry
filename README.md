# PetMed Registry
#### Video Demo:  https://youtu.be/lR8_iOBnd-4
#### Description:

The PetMed Registry project is a web-based application that serves as a centralized database for storing and managing pet medical records. The application is designed to make it easy for pet owners to keep track of their pets' medical history, and for veterinarians to access and update this information as needed.

The application allows pet owners to create accounts and add their pets to the database. They can then enter information such as their pets' name, breed, age, and medical history, including past surgeries, vaccinations, and medications. Pet owners can also add notes or upload documents such as lab reports or X-rays.

The PetMed Registry application is built using Flask, a Python web framework, and uses SQLite as its database. It also uses various web technologies such as HTML, CSS, and JavaScript to create a responsive and user-friendly interface.

Overall, the PetMed Registry project aims to make it easier for pet owners and veterinarians to manage and access important medical information about pets. The application provides a convenient and secure way to store and share pet medical records, and can help improve the quality of care for pets by ensuring that veterinarians have access to complete and up-to-date information.

Below are the files created for the app and their purpose:

1. The `static` folder contains `style.css` and a picture of an angry cat, letting the user know that one of the pages is still under construction.
2. `helpers.py` contains two utility functions that are used by `apps.py`. I borrowed and modified these functions to suit my needs in this project.
3. `petmed.db` contains various tables with data of users, user profiles, and pets, etc.
4. Within the `templates` folder, there are several HTML files I created for this project:
    1. `allpets.html`: It is used to show all pets in the database if the current user is an admin.
    2. `allusers.html`: It is used to show all user profiles in the database if the current user is an admin.
    3. `appointment.html`: It is used to make an appointment. It returns the pet name, user ID, date, and time to `apps.py` to check against the database to see if the selectedtime slot is available. If available, the appointment is made, and all passed data is saved to the appointment table. Otherwise, the page shows the user the available time slots on the selected date.
    4. `contact.html`: It allows both registered users and non-registered users to contact the page admin.
    5. `editprofile.html`: It allows registered users to edit their profile (name, phone number, email, address).
    6. `index.html`: It is the index page of the site.
    7. `layout.html`: It is used for defining the structure of the site. It contains the navbar, footer, links, and other elements, etc.
    8. `lostnfound.html`: It allows users to report a lost pet and find their missing pets. Currently, the page is under construction.
    9. `med_records.html`: It displays the details of the registered pets of the currently logged-in user.
    10. `register.html`: It allows new users to register for my website.
    11. `registerpet.html`: It allows registered and logged-in users to register their pet. When a pet is registered, their name, age, gender, breed, photo, medical history, and microchip number are passed to the function to check against the database. If the microchip number already exists, the registration is unsuccessful.
    12. `userprofile.html`: It shows currently logged-in user info and it has an edit button to allow users to edit their own profile. It also has a button to direct user to med_records.html to see their own registered pets.




    Written By Kyle J Kong
