import os
from modules.scraper import Scraper
from modules.utils import ask_input, ask_multiple_option
import pandas as pd

def scrape(target):
    chromedriver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
    cookies_path = os.path.join(os.getcwd(), "cookies.json")

    driver = Scraper.create_driver(chromedriver_path)

    scraper = Scraper(target)
    scraper.driver = driver

    print("Intentando cargar cookies desde cookies.json...")
    session_ok = Scraper.load_simple_cookies_and_auth(driver, cookies_path)

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

    # Get following list (limited to 100)
    print(f"\nObteniendo lista de seguidos de @{target} (máximo 100)...")
    following = scraper.get_users("following", verbose=True, max_users=100)
    print(f"Se obtuvieron {len(following)} seguidos.")

    # Get profile info for each followed user
    if following:
        print(f"\nObteniendo información de perfiles de los {len(following)} seguidos...")
        following_profiles = scraper.get_profiles_info(following)
    else:
        following_profiles = {}

    # Optionally get followers list
    get_followers = ask_input('¿Desea obtener la lista de seguidores? (s/n): ').lower() == 's'
    followers = []
    followers_profiles = {}
    if get_followers:
        print(f"\nObteniendo lista de seguidos de @{target} (máximo 100)...")
        followers = scraper.get_users("followers", verbose=True, max_users=100)
        print(f"Se obtuvieron {len(followers)} seguidores.")
        if followers:
            print(f"\nObteniendo información de perfiles de los {len(followers)} seguidores...")
            followers_profiles = scraper.get_profiles_info(followers)

    scraper.close()

    # Save results
    results = {
        'target': target,
        'profile_info': profile_info,
        'followers': followers,
        'followers_profiles': followers_profiles,
        'following': following,
        'following_profiles': following_profiles
    }

    # Save profile info to JSON
    import json
    with open(f'{target}_profile.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"\nInformación del perfil guardada en {target}_profile.json")

    # Save to Excel
    if following:
        df_following = pd.DataFrame({
            'Usuario': list(following_profiles.keys()),
            'Seguidores': [p['followers'] for p in following_profiles.values()],
            'Seguidos': [p['following'] for p in following_profiles.values()],
            'Biografía': [p['bio'] for p in following_profiles.values()],
            'Descripción': [p['description'] for p in following_profiles.values()]
        })
        df_following.to_excel(f'{target}_following.xlsx', index=False)
        print(f"Lista de seguidos con info guardada en {target}_following.xlsx")

    if followers:
        df_followers = pd.DataFrame({
            'Usuario': list(followers_profiles.keys()),
            'Seguidores': [p['followers'] for p in followers_profiles.values()],
            'Seguidos': [p['following'] for p in followers_profiles.values()],
            'Biografía': [p['bio'] for p in followers_profiles.values()],
            'Descripción': [p['description'] for p in followers_profiles.values()]
        })
        df_followers.to_excel(f'{target}_followers.xlsx', index=False)
        print(f"Lista de seguidores con info guardada en {target}_followers.xlsx")

    return results

if __name__ == "__main__":
    target = ask_input('Enter the target username (e.g., nayeli.nxx): ')
    scrape(target)