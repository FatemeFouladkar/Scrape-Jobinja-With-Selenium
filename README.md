# Scrape-Jobinja-With-Selenium

A short python script to scrape data from [Jobinja.ir](https://jobinja.ir/) with the help of [Selenium](https://www.selenium.dev/).
This script searches for the given title and city and saves all the results to a `.json` and `.csv` file.

## Run the script
---
1. Clone the project and install the dependencies:

    ```
    pip install -r requirements.txt
    ```
2. Add email and password to jobinja.py:
    ```
    login('email', 'password')
    # example:
        login('test@test.com', '1234')
    ```
3. Add filters to jobinja.py:
    ```
    find_by_filter('title', 'city_fa')
    # example:
        find_by_filter('python', 'تهران')
    ```
4. Run the script:
    ```
    python jobinja.py
    ```
### Sample Output:
---

![sample output](output/2022-12-25/django-%D8%AA%D9%87%D8%B1%D8%A7%D9%86.png)
