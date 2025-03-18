import os
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

class TravelPlanner:
    def __init__(self, budget):
        self.best_plan = None
        self.max_value = 0
        self.total_budget = budget  # Budget dari input
        
    def plan_trip_to_china(self, destinations, hotels, transportations, activities):
        """
        Plan an optimal trip to China using backtracking algorithm.
        
        Args:
            destinations: List of possible destinations in China
            hotels: Dictionary of hotels with costs
            transportations: Dictionary of transportation options with costs
            activities: Dictionary of activities with costs and values
        """
        selected_items = []
        self.backtrack(destinations, hotels, transportations, activities, selected_items, 0, 0)
        return self.best_plan
    
    def backtrack(self, destinations, hotels, transportations, activities, selected, current_cost, current_value):
        """
        Backtracking function to find optimal combination.
        """
        # Check if we've exceeded budget
        if current_cost > self.total_budget:
            return
        
        # Check if we have a complete valid solution
        has_destination = any(item[0] == "destination" for item in selected)
        has_hotel = any(item[0] == "hotel" for item in selected)
        has_transport = any(item[0] == "transportation" for item in selected)
        
        if has_destination and has_hotel and has_transport:
            # Valid complete solution - check if it's the best so far
            if current_value > self.max_value:
                self.max_value = current_value
                self.best_plan = selected.copy()
        
        # Try adding a destination
        if not has_destination:
            for dest in destinations:
                dest_cost = destinations[dest]["cost"]
                dest_value = destinations[dest]["value"]
                
                selected.append(("destination", dest, dest_cost, dest_value))
                self.backtrack(destinations, hotels, transportations, activities, 
                               selected, current_cost + dest_cost, current_value + dest_value)
                selected.pop()
        
        # Try adding a hotel
        elif not has_hotel:
            for hotel in hotels:
                hotel_cost = hotels[hotel]["cost"]
                hotel_value = hotels[hotel]["value"]
                
                selected.append(("hotel", hotel, hotel_cost, hotel_value))
                self.backtrack(destinations, hotels, transportations, activities, 
                               selected, current_cost + hotel_cost, current_value + hotel_value)
                selected.pop()
        
        # Try adding transportation
        elif not has_transport:
            for transport in transportations:
                transport_cost = transportations[transport]["cost"]
                transport_value = transportations[transport]["value"]
                
                selected.append(("transportation", transport, transport_cost, transport_value))
                self.backtrack(destinations, hotels, transportations, activities, 
                               selected, current_cost + transport_cost, current_value + transport_value)
                selected.pop()
        
        # Try adding activities (optional)
        else:
            # Try each possible activity
            for activity in activities:
                # Skip if we already selected this activity
                if any(item[0] == "activity" and item[1] == activity for item in selected):
                    continue
                    
                activity_cost = activities[activity]["cost"]
                activity_value = activities[activity]["value"]
                
                # Check if adding this would exceed budget
                if current_cost + activity_cost <= self.total_budget:
                    selected.append(("activity", activity, activity_cost, activity_value))
                    self.backtrack(destinations, hotels, transportations, activities, 
                                   selected, current_cost + activity_cost, current_value + activity_value)
                    selected.pop()
            
            # Also consider the possibility of not adding any more activities
            if current_value > self.max_value:
                self.max_value = current_value
                self.best_plan = selected.copy()


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_title(title):
    """Print a styled title."""
    width = 60
    print(Fore.CYAN + "═" * width)
    print(Fore.YELLOW + Style.BRIGHT + title.center(width))
    print(Fore.CYAN + "═" * width)


def print_subtitle(subtitle):
    """Print a styled subtitle."""
    print(Fore.GREEN + Style.BRIGHT + "\n" + subtitle)
    print(Fore.GREEN + "-" * len(subtitle))


def print_china_ascii_art():
    """Display ASCII art related to China."""
    china_ascii = """
    {1}                  .''.
    {1}         *''*    :_\/_:     . 
    {1}        _\/_   .: {2}/\ {1}:  .'.:.'.
    {1}    .''.: {2}/\ {1}:   ':'  /:' *''*
    {1}   :_\/_:    '. {2}/\ {1}  :  :
    {1}   : {2}/\ {1}    /  '  :   '
    {0}    {2}'  {0}旅行计划  {2}到中国{0}
    {1}       *''*        *''*
    """.format(Fore.RED + Style.BRIGHT, Fore.WHITE, Fore.YELLOW)
    
    print(china_ascii)


def loading_animation(text, duration=3):
    """Display a simple loading animation."""
    for _ in range(duration):
        for c in ["|", "/", "-", "\\"]:
            print(f"\r{Fore.CYAN}{text} {c}", end="")
            time.sleep(0.2)
    print("\r" + " " * (len(text) + 2), end="\r")


def input_number(prompt):
    """Helper function untuk memvalidasi input angka dengan styling."""
    print(Fore.YELLOW + prompt, end="")
    while True:
        try:
            value = int(input(" "))
            return value
        except ValueError:
            print(Fore.RED + "✗ Input harus berupa angka. Silakan coba lagi: ", end="")


def display_menu(title, options):
    """Display a menu with numbered options and return user choice."""
    clear_screen()
    print_china_ascii_art()
    print_title(title)
    
    for i, option in enumerate(options, 1):
        print(f"{Fore.YELLOW}{i}. {Fore.WHITE}{option}")
    
    print(f"{Fore.RED}0. {Fore.WHITE}Kembali / Selesai")
    
    choice = input_number(f"\n{Style.BRIGHT}Pilih menu [0-{len(options)}]")
    while choice < 0 or choice > len(options):
        print(Fore.RED + f"✗ Pilihan harus antara 0 dan {len(options)}")
        choice = input_number(f"{Style.BRIGHT}Pilih menu [0-{len(options)}]")
    
    return choice


def input_item(item_type):
    """Input a single item with cost and value."""
    print_subtitle(f"Input {item_type.capitalize()}")
    
    name = input(f"{Fore.YELLOW}Nama {item_type}: ")
    if not name:
        return None, None, None
    
    cost = input_number(f"Biaya {name} (dalam Rupiah)")
    value = input_number(f"Nilai kepuasan {name} (1-100)")
    
    while value < 1 or value > 100:
        print(Fore.RED + "✗ Nilai kepuasan harus antara 1-100")
        value = input_number(f"Nilai kepuasan {name} (1-100)")
    
    return name, cost, value


def view_items(items, item_type, color=Fore.WHITE):
    """View all items of a specific type."""
    if not items:
        print(f"\n{Fore.RED}Tidak ada {item_type} yang tersedia.")
        input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...")
        return
    
    print_subtitle(f"Daftar {item_type.capitalize()}")
    
    for i, (name, data) in enumerate(items.items(), 1):
        print(f"{color}{i}. {Fore.WHITE}{name} - {Fore.GREEN}{data['cost']:,} IDR, {Fore.YELLOW}Nilai: {data['value']}%")
    
    input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...")


def manage_items(items, item_type, color):
    """Menu to manage (add, view, edit, delete) items of a specific type."""
    while True:
        choice = display_menu(f"KELOLA {item_type.upper()}", [
            f"Tambah {item_type} baru",
            f"Lihat semua {item_type}",
            f"Edit {item_type}",
            f"Hapus {item_type}"
        ])
        
        if choice == 0:
            return items
        
        elif choice == 1:  # Add new item
            clear_screen()
            print_china_ascii_art()
            print_title(f"TAMBAH {item_type.upper()}")
            
            name, cost, value = input_item(item_type)
            if name:
                items[name] = {"cost": cost, "value": value}
                print(f"\n{Fore.GREEN}✓ {item_type.capitalize()} '{name}' berhasil ditambahkan!")
                time.sleep(1)
        
        elif choice == 2:  # View all items
            clear_screen()
            print_china_ascii_art()
            print_title(f"DAFTAR {item_type.upper()}")
            view_items(items, item_type, color)
        
        elif choice == 3:  # Edit item
            if not items:
                clear_screen()
                print_china_ascii_art()
                print_title(f"EDIT {item_type.upper()}")
                print(f"\n{Fore.RED}Tidak ada {item_type} yang tersedia untuk diedit.")
                input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...")
                continue
            
            clear_screen()
            print_china_ascii_art()
            print_title(f"EDIT {item_type.upper()}")
            view_items(items, item_type, color)
            
            item_names = list(items.keys())
            item_index = input_number(f"\nPilih nomor {item_type} yang akan diedit [1-{len(item_names)}] (0 untuk batal)") - 1
            
            if item_index == -1 or item_index >= len(item_names):
                continue
                
            name = item_names[item_index]
            print(f"\n{Fore.YELLOW}Edit {item_type} '{name}':")
            
            cost = input_number(f"Biaya baru (sebelumnya: {items[name]['cost']:,} IDR)")
            value = input_number(f"Nilai kepuasan baru (sebelumnya: {items[name]['value']}%)")
            
            while value < 1 or value > 100:
                print(Fore.RED + "✗ Nilai kepuasan harus antara 1-100")
                value = input_number(f"Nilai kepuasan baru (sebelumnya: {items[name]['value']}%)")
            
            items[name] = {"cost": cost, "value": value}
            print(f"\n{Fore.GREEN}✓ {item_type.capitalize()} '{name}' berhasil diperbarui!")
            time.sleep(1)
        
        elif choice == 4:  # Delete item
            if not items:
                clear_screen()
                print_china_ascii_art()
                print_title(f"HAPUS {item_type.upper()}")
                print(f"\n{Fore.RED}Tidak ada {item_type} yang tersedia untuk dihapus.")
                input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...")
                continue
                
            clear_screen()
            print_china_ascii_art()
            print_title(f"HAPUS {item_type.upper()}")
            view_items(items, item_type, color)
            
            item_names = list(items.keys())
            item_index = input_number(f"\nPilih nomor {item_type} yang akan dihapus [1-{len(item_names)}] (0 untuk batal)") - 1
            
            if item_index == -1 or item_index >= len(item_names):
                continue
                
            name = item_names[item_index]
            confirm = input(f"\n{Fore.RED}Apakah Anda yakin ingin menghapus {item_type} '{name}'? (y/n) ").lower()
            
            if confirm == 'y':
                del items[name]
                print(f"\n{Fore.GREEN}✓ {item_type.capitalize()} '{name}' berhasil dihapus!")
                time.sleep(1)


def print_plan_result(optimal_plan, budget, max_value):
    """Display the optimal travel plan with improved formatting."""
    if not optimal_plan:
        print(Fore.RED + "\n❌ Tidak dapat menemukan rencana perjalanan yang sesuai dengan budget.")
        print(Fore.RED + "   Coba tingkatkan budget atau kurangi biaya komponen perjalanan.")
        return False
    
    print("\n" + Fore.CYAN + "═" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "🌟 RENCANA PERJALANAN OPTIMAL KE CHINA 🌟".center(60))
    print(Fore.CYAN + "═" * 60)
    
    print(Fore.WHITE + f"💰 Budget Total: {Fore.GREEN}{budget:,} IDR")
    
    total_cost = 0
    
    # Group items by type
    destinations = []
    hotels = []
    transportations = []
    activities = []
    
    for item_type, item_name, cost, value in optimal_plan:
        total_cost += cost
        if item_type == "destination":
            destinations.append((item_name, cost, value))
        elif item_type == "hotel":
            hotels.append((item_name, cost, value))
        elif item_type == "transportation":
            transportations.append((item_name, cost, value))
        else:
            activities.append((item_name, cost, value))
    
    # Print destinations
    print(f"\n{Fore.YELLOW}🏙️ {Style.BRIGHT}Destinasi:")
    for name, cost, value in destinations:
        print(f"  {Fore.WHITE}• {name} - {Fore.GREEN}{cost:,} IDR {Fore.YELLOW}({value}% nilai)")
    
    # Print hotels
    print(f"\n{Fore.BLUE}🏨 {Style.BRIGHT}Hotel:")
    for name, cost, value in hotels:
        print(f"  {Fore.WHITE}• {name} - {Fore.GREEN}{cost:,} IDR {Fore.YELLOW}({value}% nilai)")
    
    # Print transportation
    print(f"\n{Fore.MAGENTA}✈️ {Style.BRIGHT}Transportasi:")
    for name, cost, value in transportations:
        print(f"  {Fore.WHITE}• {name} - {Fore.GREEN}{cost:,} IDR {Fore.YELLOW}({value}% nilai)")
    
    # Print activities if any
    if activities:
        print(f"\n{Fore.CYAN}🎭 {Style.BRIGHT}Aktivitas:")
        for name, cost, value in activities:
            print(f"  {Fore.WHITE}• {name} - {Fore.GREEN}{cost:,} IDR {Fore.YELLOW}({value}% nilai)")
    
    # Print summary
    print(Fore.CYAN + "\n" + "-" * 60)
    print(f"{Fore.WHITE}💸 Total Biaya: {Fore.GREEN}{total_cost:,} IDR")
    remaining = budget - total_cost
    print(f"{Fore.WHITE}💵 Sisa Budget: {Fore.GREEN if remaining >= 0 else Fore.RED}{remaining:,} IDR")
    print(f"{Fore.WHITE}⭐ Skor Nilai Perjalanan: {Fore.YELLOW}{max_value}")
    return True


def save_result_to_file(optimal_plan, budget, max_value, filename="rencana_perjalanan.txt"):
    """Save the travel plan result to a text file."""
    if not optimal_plan:
        return False
    
    try:
        with open(filename, "w") as f:
            f.write("=" * 60 + "\n")
            f.write("RENCANA PERJALANAN OPTIMAL KE CHINA\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Budget Total: {budget:,} IDR\n\n")
            
            total_cost = 0
            
            # Group items by type
            destinations = []
            hotels = []
            transportations = []
            activities = []
            
            for item_type, item_name, cost, value in optimal_plan:
                total_cost += cost
                if item_type == "destination":
                    destinations.append((item_name, cost, value))
                elif item_type == "hotel":
                    hotels.append((item_name, cost, value))
                elif item_type == "transportation":
                    transportations.append((item_name, cost, value))
                else:
                    activities.append((item_name, cost, value))
            
            # Write destinations
            f.write("DESTINASI:\n")
            for name, cost, value in destinations:
                f.write(f"  • {name} - {cost:,} IDR ({value}% nilai)\n")
            
            # Write hotels
            f.write("\nHOTEL:\n")
            for name, cost, value in hotels:
                f.write(f"  • {name} - {cost:,} IDR ({value}% nilai)\n")
            
            # Write transportation
            f.write("\nTRANSPORTASI:\n")
            for name, cost, value in transportations:
                f.write(f"  • {name} - {cost:,} IDR ({value}% nilai)\n")
            
            # Write activities if any
            if activities:
                f.write("\nAKTIVITAS:\n")
                for name, cost, value in activities:
                    f.write(f"  • {name} - {cost:,} IDR ({value}% nilai)\n")
            
            # Write summary
            f.write("\n" + "-" * 60 + "\n")
            f.write(f"Total Biaya: {total_cost:,} IDR\n")
            remaining = budget - total_cost
            f.write(f"Sisa Budget: {remaining:,} IDR\n")
            f.write(f"Skor Nilai Perjalanan: {max_value}\n")
            f.write("\n" + "=" * 60 + "\n")
            f.write("Dibuat dengan Program Perencanaan Perjalanan Ke China\n")
            f.write("Menggunakan Algoritma Backtracking\n")
            
        return True
    except:
        return False


def run_backtracking_algorithm(budget, destinations, hotels, transportations, activities):
    """Run the backtracking algorithm with animation."""
    loading_animation("🧮 Menjalankan algoritma backtracking untuk optimasi perjalanan...", 3)
    
    # Jalankan algoritma backtracking
    planner = TravelPlanner(budget)
    optimal_plan = planner.plan_trip_to_china(destinations, hotels, transportations, activities)
    
    # Tampilkan hasil
    if print_plan_result(optimal_plan, budget, planner.max_value):
        # Tanya apakah user ingin menyimpan hasil
        save_option = input(f"\n{Fore.YELLOW}Apakah Anda ingin menyimpan rencana perjalanan ini ke file? (y/n) ").lower()
        if save_option == 'y':
            filename = input(f"{Fore.YELLOW}Masukkan nama file (default: rencana_perjalanan.txt): ")
            if not filename:
                filename = "rencana_perjalanan.txt"
                
            if not filename.endswith('.txt'):
                filename += '.txt'
                
            if save_result_to_file(optimal_plan, budget, planner.max_value, filename):
                print(f"\n{Fore.GREEN}✓ Rencana perjalanan berhasil disimpan ke '{filename}'!")
            else:
                print(f"\n{Fore.RED}✗ Gagal menyimpan rencana perjalanan ke file.")
    
    input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali ke menu utama...")


def default_data():
    """Return default data if user doesn't want to input anything."""
    destinations = {
        "Beijing": {"cost": 20000000, "value": 90},
        "Shanghai": {"cost": 25000000, "value": 85},
        "Xi'an": {"cost": 15000000, "value": 80}
    }
    
    hotels = {
        "Luxury Hotel": {"cost": 40000000, "value": 95},
        "Mid-range Hotel": {"cost": 25000000, "value": 80},
        "Budget Hotel": {"cost": 15000000, "value": 60}
    }
    
    transportations = {
        "Direct Flight": {"cost": 30000000, "value": 90},
        "Connecting Flight": {"cost": 20000000, "value": 70},
        "Train": {"cost": 15000000, "value": 60}
    }
    
    activities = {
        "Great Wall Tour": {"cost": 5000000, "value": 95},
        "Forbidden City Visit": {"cost": 3000000, "value": 90},
        "Local Food Tour": {"cost": 2000000, "value": 80}
    }
    
    return destinations, hotels, transportations, activities


def about_program():
    """Display information about the program."""
    clear_screen()
    print_china_ascii_art()
    print_title("TENTANG PROGRAM")
    
    print(f"{Fore.WHITE}Program Perencanaan Perjalanan ke China adalah aplikasi yang menggunakan")
    print(f"{Fore.WHITE}algoritma backtracking untuk menemukan kombinasi optimal dari:")
    print(f"{Fore.YELLOW}  • Destinasi di China")
    print(f"{Fore.BLUE}  • Hotel")
    print(f"{Fore.MAGENTA}  • Transportasi")
    print(f"{Fore.CYAN}  • Aktivitas opsional")
    
    print(f"\n{Fore.WHITE}Algoritma backtracking akan mencari kombinasi terbaik yang:")
    print(f"{Fore.GREEN}  1. Tidak melebihi budget yang ditentukan")
    print(f"{Fore.GREEN}  2. Memaksimalkan nilai kepuasan total")
    print(f"{Fore.GREEN}  3. Memastikan setiap rencana memiliki destinasi, hotel, dan transportasi")
    
    print(f"\n{Fore.WHITE}Program ini juga memungkinkan Anda untuk:")
    print(f"{Fore.YELLOW}  • Mengelola berbagai opsi perjalanan")
    print(f"{Fore.YELLOW}  • Menyimpan rencana perjalanan optimal ke file")
    print(f"{Fore.YELLOW}  • Menggunakan data default atau memasukkan data sendiri")
    
    print(f"\n{Fore.CYAN}Dibuat oleh: Your Name")
    print(f"{Fore.CYAN}Versi: 1.0")
    
    input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali ke menu utama...")


def main():
    try:
        # Initialize variables
        budget = 100000000  # Default budget
        destinations = {}
        hotels = {}
        transportations = {}
        activities = {}
        budget_set = False
        
        while True:
            main_menu_options = [
                "Set Budget Perjalanan",
                "Kelola Destinasi",
                "Kelola Hotel",
                "Kelola Transportasi",
                "Kelola Aktivitas",
                "Jalankan Optimasi Perjalanan",
                "Gunakan Data Default",
                "Tentang Program",
                "Keluar"
            ]
            
            # Update first menu item if budget is already set
            if budget_set:
                main_menu_options[0] = f"Ubah Budget (Saat ini: {budget:,} IDR)"
            
            choice = display_menu("PROGRAM PERENCANAAN PERJALANAN KE CHINA", main_menu_options)
            
            if choice == 1:  # Set Budget
                clear_screen()
                print_china_ascii_art()
                print_title("SET BUDGET PERJALANAN")
                
                budget = input_number("💰 Masukkan budget perjalanan (dalam Rupiah)")
                budget_set = True
                print(f"\n{Fore.GREEN}✓ Budget berhasil diatur: {budget:,} IDR")
                time.sleep(1)
            
            elif choice == 2:  # Manage Destinations
                destinations = manage_items(destinations, "destinasi", Fore.YELLOW)
                
            elif choice == 3:  # Manage Hotels
                hotels = manage_items(hotels, "hotel", Fore.BLUE)
                
            elif choice == 4:  # Manage Transportation
                transportations = manage_items(transportations, "transportasi", Fore.MAGENTA)
                
            elif choice == 5:  # Manage Activities
                activities = manage_items(activities, "aktivitas", Fore.CYAN)
                
            elif choice == 6:  # Run Optimization
                # Check if we have the required data
                if not destinations:
                    print(f"\n{Fore.RED}✗ Anda belum menambahkan destinasi apapun!")
                    input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...")
                    continue
                    
                if not hotels:
                    print(f"\n{Fore.RED}✗ Anda belum menambahkan hotel apapun!")
                    input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...")
                    continue
                    
                if not transportations:
                    print(f"\n{Fore.RED}✗ Anda belum menambahkan transportasi apapun!")
                    input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...")
                    continue
                
                clear_screen()
                print_china_ascii_art()
                print_title("OPTIMASI PERJALANAN")
                
                run_backtracking_algorithm(budget, destinations, hotels, transportations, activities)
                
            elif choice == 7:  # Use Default Data
                clear_screen()
                print_china_ascii_art()
                print_title("GUNAKAN DATA DEFAULT")
                
                confirm = input(f"{Fore.YELLOW}Apakah Anda yakin ingin menggunakan data default? (y/n) ").lower()
                if confirm == 'y':
                    destinations, hotels, transportations, activities = default_data()
                    print(f"\n{Fore.GREEN}✓ Data default berhasil dimuat!")
                    time.sleep(1)
            
            elif choice == 8:  # About Program
                about_program()
                
            elif choice == 9 or choice == 0:  # Exit
                clear_screen()
                print_china_ascii_art()
                print_title("TERIMA KASIH")
                print(Fore.YELLOW + "Terima kasih telah menggunakan Program Perencanaan Perjalanan!".center(60))
                print(Fore.YELLOW + "Semoga perjalanan Anda ke China menyenangkan!".center(60))
                break
    
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(Fore.RED + f"\n\nTerjadi kesalahan: {e}")


if __name__ == "__main__":
    main()