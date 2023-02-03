Read Me of App Dev Proj
Used to keep track of work progress, updates, and TO-DO List

// To-Do List
1. Edit functions call original text from database  
    - User, Events, Facilities ✔️ (11/1/23)
    - Booking - Partial Complete? (17/1/2023)

2. Add venue and location to Events
    - Location (No integration) ✔️ (14/1/23)
    - Venue (No integration) ✔️ (14/1/23)

3. Add Event Start Date ✔️ (14/1/23)
4. Add Event Status (Active/Closed) ✔️ (14/1/23)
5. Change ID of Facilities ✔️ (13/1/23)
6. Event Venue max vacancies and form error checking for vacancies (Vacancies cannot be larger than venue size) ✔️ (14/1/23)
7. Event Start date cannot be behind end date - will need more testing  ✔️ (2/2/23) //TODO : Check this
8. Edit Facility to change facil type into location.
9. Edit and Deletion affects sign up
10. Data required for datetime for events (Start and End Date)
11. Fix date for events - cant replicate the issue shown ✔️ (2/2/23)
12. Event type, location, venue, status validation message.
13. Search Function - Events ✔️ (1/2/23)
14. Fix user search function ✔️ (2/2/23)
15. Make datetime for events show validation message for incorrect format (IMPT) / Check validation for event start < end (IMPT) ✔️ (4/2/23) man it jus turned 12 in the morn - Alan
16. Restrict users from using admin@activeplay.sg being registered under any field ✔️ (3/2/23)
17. Restrict users from using special symbols (except hyphen, underscore, and period) in username ✔️ (3/2/23)
18. Fix issue where user database css breaks when user entry is too long ✔️ (3/2/23) - CSS does not mess up due to 15 letter limit (Alan)
19. Remove "this field is required" message on user edit
20. 

// Updates
11/1/23 - Updated edit functions
13/1/23 - Updated Facilities, unique key now changed to count instead of prev ID 
15/1/23 - Integrated Event Creation with Available Facilities. 
          ( Event venue -> Available facilities, Event Vacancy -> Facility Slots.)
          ( Error Checking to ensure Vacancy is not greater than Facility Slots)
16/1/23 - Emails cannot be duplicated (emails)
        - Reworked RegisteredEvents/Facilities CSS
        - Added new updated 2023 blessings to 404 & 500 buddha
17/1/23 - Changed edit for Booking, made previous data enter edit form immediately, albeit partially (Location)
        - Integrated Booking with Available Facilities
        - Changed small details of Facility display
18/1/23 - Integrated Users with Booking
27/1/23 - Updated User to include phone no and date joined
        - Can log in using Phone number or email
        - Changed facility location to reflect name instead of postal code
        - Updated dynamic options for facilities in regard to events and booking
        - Added location to booking (Temp until i find a new solution)
30/1/23 - Added validation for faciility rate
1/2/23 - Added Search Function - Alan



// Work Progress
- General CRUD (Create, Remove, Update, Display) 
    - Users ✔️
    - Events ✔️
    - Facilities ✔️
    - Booking ✔️

- Integration
    - User x Signed Up Event ✔️
    - Events Location x Facility - (IMPT) ✔️ (Available / Unavailable - discuss later)
    - Booking x Facilities

- Others
    - Find new prayers to add to 404 Buddha (Needs to be updated to 2023) ✔️




// Ideas
Facility availability in a list, allows selection based on list only. ✔️
