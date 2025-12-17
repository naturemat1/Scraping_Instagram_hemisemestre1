import os
from modules.scraper import Scraper
from modules.utils import ask_input, ask_multiple_option
import pandas as pd

def scrape(target):
    chromedriver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
    cookies_path = os.path.join(os.getcwd(), "cookies.json")

    driver = Scraper.create_driver(chromedriver_path)

    print("Intentando cargar cookies desde cookies.json...")
    session_ok = Scraper.load_simple_cookies_and_auth(driver, cookies_path)

    scraper = Scraper(target)
    scraper.driver = driver

    if not session_ok:
        print("Cookies no válidas, autenticando manualmente...")
        username = ask_input('Username: ')
        password = ask_input('Password: ', is_password=True)
        scraper.authenticate(username, password)

    # Get profile info for target
    print(f"\nObteniendo información del perfil de @{target}...")
    profile_info = scraper.get_profile_info(target)
    print("\n=== INFORMACIÓN DEL PERFIL ===")
    print(f"Seguidores: {profile_info['followers']}")
    print(f"Seguidos: {profile_info['following']}")
    print(f"Biografía: {profile_info['bio']}")
    print(f"Descripción: {profile_info['description']}")

    # Get followers list
    print(f"\nObteniendo lista de seguidores de @{target}...")
    followers = scraper.get_users("followers", verbose=True)
    print(f"Se obtuvieron {len(followers)} seguidores.")

    # Optionally get following list
    get_following = ask_input('¿Desea obtener la lista de seguidos? (s/n): ').lower() == 's'
    following = []
    if get_following:
        print(f"\nObteniendo lista de seguidos de @{target}...")
        following = scraper.get_users("following", verbose=True)
        print(f"Se obtuvieron {len(following)} seguidos.")

    scraper.close()

    # Save results
    results = {
        'target': target,
        'profile_info': profile_info,
        'followers': followers,
        'following': following
    }

    # Save profile info to JSON
    import json
    with open(f'{target}_profile.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"\nInformación del perfil guardada en {target}_profile.json")

    # Save to Excel
    if followers:
        df_followers = pd.DataFrame({'Usuario': followers})
        df_followers.to_excel(f'{target}_followers.xlsx', index=False)
        print(f"Lista de seguidores guardada en {target}_followers.xlsx")

    if following:
        df_following = pd.DataFrame({'Usuario': following})
        df_following.to_excel(f'{target}_following.xlsx', index=False)
        print(f"Lista de seguidos guardada en {target}_following.xlsx")

    return results

if __name__ == "__main__":
    target = ask_input('Enter the target username (e.g., nayeli.nxx): ')
    scrape(target)