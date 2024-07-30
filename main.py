import os
import time
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

packages = {
    "420 VP": 80,
    "880 VP": 160,
    "1825 VP": 320,
    "3200 VP": 560,
    "4650 VP": 800,
    "9650 VP": 1600
}


def print_fancy_header(text):
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + text.center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)


def print_info(text):
    print(Fore.GREEN + text)


def print_warning(text):
    print(Fore.YELLOW + text)


def print_error(text):
    print(Fore.RED + text)


def calculate_ukrainian_region_prices(uah_to_pkr_rate):
    results = {}
    for vp, uah in packages.items():
        total_cost = uah * uah_to_pkr_rate * 1.058
        cost_per_vp = total_cost / int(vp.split()[0])
        results[vp] = {
            "Total Cost (PKR)": round(total_cost, 2),
            "Cost per VP (PKR/VP)": round(cost_per_vp, 2)
        }
    return results


def find_best_and_second_best_options(vp_needed, prices):
    sorted_packages = sorted([(k, int(k.split()[0])) for k in packages.keys()], key=lambda x: x[1], reverse=True)

    def calculate_cost_and_vp(vp_needed, selected_packs):
        total_cost = 0
        total_vp = 0
        for pack_name, pack_vp in selected_packs:
            total_vp += pack_vp
            total_cost += prices[pack_name]["Total Cost (PKR)"]
        return total_cost, total_vp

    best_option = {'packs': None, 'total_cost': float('inf'), 'total_vp': 0}
    second_best_option = {'packs': None, 'total_cost': float('inf'), 'total_vp': 0}

    # Best option computation
    for i in range(len(sorted_packages)):
        selected_packs = []
        remaining_vp = vp_needed

        for pack_name, pack_vp in sorted_packages[i:]:
            while pack_vp <= remaining_vp:
                selected_packs.append((pack_name, pack_vp))
                remaining_vp -= pack_vp

        # Cover remaining VP with smallest pack
        if remaining_vp > 0:
            smallest_pack = sorted_packages[-1][0]
            smallest_pack_vp = sorted_packages[-1][1]
            num_smallest_packs = (remaining_vp + smallest_pack_vp - 1) // smallest_pack_vp
            selected_packs.extend([(smallest_pack, smallest_pack_vp)] * num_smallest_packs)

        total_cost, total_vp = calculate_cost_and_vp(vp_needed, selected_packs)
        if total_cost < best_option['total_cost']:
            second_best_option = best_option
            best_option = {'packs': selected_packs, 'total_cost': total_cost, 'total_vp': total_vp}
        elif total_cost < second_best_option['total_cost'] and total_cost != best_option['total_cost']:
            second_best_option = {'packs': selected_packs, 'total_cost': total_cost, 'total_vp': total_vp}

    # Find second-best option with a larger pack included
    for pack_name, pack_vp in sorted_packages:
        if pack_name not in dict(best_option['packs']).keys():
            selected_packs = [(pack_name, pack_vp)]
            remaining_vp = vp_needed - pack_vp

            for next_pack_name, next_pack_vp in sorted_packages:
                while next_pack_vp <= remaining_vp:
                    selected_packs.append((next_pack_name, next_pack_vp))
                    remaining_vp -= next_pack_vp

            # Cover remaining VP with smallest pack
            if remaining_vp > 0:
                smallest_pack = sorted_packages[-1][0]
                smallest_pack_vp = sorted_packages[-1][1]
                num_smallest_packs = (remaining_vp + smallest_pack_vp - 1) // smallest_pack_vp
                selected_packs.extend([(smallest_pack, smallest_pack_vp)] * num_smallest_packs)

            total_cost, total_vp = calculate_cost_and_vp(vp_needed, selected_packs)
            if total_cost < second_best_option['total_cost']:
                second_best_option = {'packs': selected_packs, 'total_cost': total_cost, 'total_vp': total_vp}

    return best_option, second_best_option


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear_screen()
    print_fancy_header("Welcome to the VP Pack Recommender!")

    while True:
        try:
            current_uah_to_pkr_rate = float(
                input(Fore.CYAN + "\nEnter the current UAH to PKR conversion rate: " + Fore.RESET))
            break
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")

    prices = calculate_ukrainian_region_prices(current_uah_to_pkr_rate)

    clear_screen()
    print_fancy_header("VP Package Prices")
    for vp, details in prices.items():
        print(
            f"{Fore.YELLOW}{vp}: {Fore.GREEN}Total Cost = {details['Total Cost (PKR)']} PKR, {Fore.BLUE}Cost per VP = {details['Cost per VP (PKR/VP)']} PKR/VP")

    print_info("\nPress Enter to continue...")
    input()

    while True:
        clear_screen()
        print_fancy_header("VP Pack Recommender")
        print_info("Enter the amount of VP you need (or type 0 to exit): ")
        try:
            vp_needed = int(input(Fore.CYAN + "> " + Fore.RESET))
            if vp_needed == 0:
                break
            if vp_needed < 0:
                raise ValueError
        except ValueError:
            print_error("Invalid input. Please enter a positive integer.")
            time.sleep(2)
            continue

        best_option, second_best_option = find_best_and_second_best_options(vp_needed, prices)

        clear_screen()
        print_fancy_header(f"Recommendations for {vp_needed} VP")

        print(Fore.YELLOW + "\nBest Option:")
        if best_option['packs']:
            pack_summary = {}
            for pack_name, _ in best_option['packs']:
                pack_summary[pack_name] = pack_summary.get(pack_name, 0) + 1
            for pack_name, num_packs in pack_summary.items():
                print(f"{Fore.CYAN}{pack_name}: {Fore.GREEN}{num_packs} pack(s)")
            print(f"\n{Fore.MAGENTA}Total VP: {best_option['total_vp']}")
            print(f"{Fore.MAGENTA}Total Cost: {round(best_option['total_cost'], 2)} PKR")
        else:
            print_warning("No packs available.")

        print(Fore.YELLOW + "\nSecond Best Option (with larger pack):")
        if second_best_option['packs']:
            pack_summary = {}
            for pack_name, _ in second_best_option['packs']:
                pack_summary[pack_name] = pack_summary.get(pack_name, 0) + 1
            for pack_name, num_packs in pack_summary.items():
                print(f"{Fore.CYAN}{pack_name}: {Fore.GREEN}{num_packs} pack(s)")
            print(f"\n{Fore.MAGENTA}Total VP: {second_best_option['total_vp']}")
            print(f"{Fore.MAGENTA}Total Cost: {round(second_best_option['total_cost'], 2)} PKR")
        else:
            print_warning("No alternative packs available.")

        print_info("\nPress Enter to continue...")
        input()

    clear_screen()
    print_fancy_header("Thank you for using the VP Pack Recommender!")
    print_info("\nPress Enter to exit...")
    input()


if __name__ == "__main__":
    main()
