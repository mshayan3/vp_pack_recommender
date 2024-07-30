**VP Pack Recommender**

VP Pack Recommender is a Python application that helps users find the most cost-effective Valorant Points (VP) packages. Given the current exchange rate from Ukrainian Hryvnia (UAH) to Pakistani Rupee (PKR), it calculates the total cost and cost per VP for various packages and provides recommendations for the best and second-best options based on the user's VP needs.

**Features**

Exchange Rate Input: Accepts the current UAH to PKR conversion rate from the user.
Price Calculation: Calculates the total cost and cost per VP for different VP packages.
Best Options: Recommends the best and second-best VP package combinations for the desired VP amount.
User-Friendly Interface: Provides a clear and color-coded display of information and recommendations.
Prerequisites
Python 3.x
colorama library
You can install the required library using pip:

pip install colorama


**Usage**

Clone the repository:

git clone https://github.com/yourusername/vp-pack-recommender.git
cd vp-pack-recommender

Run the application:

python vp_pack_recommender.py
Follow the on-screen prompts:
Enter the current UAH to PKR conversion rate.
View the calculated prices for various VP packages.
Enter the amount of VP you need.
Receive the best and second-best VP package recommendations.

**Code Structure**

packages: Dictionary containing VP packages and their corresponding prices in UAH.
print_fancy_header(text): Prints a fancy header with a given text.
print_info(text): Prints informational text in green.
print_warning(text): Prints warning text in yellow.
print_error(text): Prints error text in red.
calculate_ukrainian_region_prices(uah_to_pkr_rate): Calculates the total cost and cost per VP for each package.
find_best_and_second_best_options(vp_needed, prices): Finds the best and second-best VP package combinations for the desired VP amount.
clear_screen(): Clears the terminal screen.
main(): Main function to run the application.

**Example**

![image](https://github.com/user-attachments/assets/9dd0ae41-4908-4400-afa3-6a9dd11b53e1)


