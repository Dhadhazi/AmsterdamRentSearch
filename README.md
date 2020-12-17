# Amsterdam Rental Apartment Search

After setup the program grabs listings from Pararius and fills in a google forms with the data.
Made with Selenium to practice automatic form filling and submitting - althogh API connection to sheets or saving into CSV would be probably better

## Setup:
Pararius link - The end listing page with filters where you want to grab the listings
Number of pages - How many pages deep should it grab the data
Chrom dirver path - Selenium needs it

### Make the google form
Based on the screenshot below, only title, link, price, advertiser are guaranteed fields
![Google sheets form](https://github.com/Dhadhazi/AmsterdamRentSearch/blob/main/screenshot/form.png)

#### Project inspired by 100 days of Python course, but made enteriley by me
