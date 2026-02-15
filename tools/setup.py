#!/usr/bin/env python3
"""
Skrypt setup - interaktywna konfiguracja systemu
"""
import os
import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

def setup_wizard():
    """Interaktywny wizard konfiguracji"""
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}🤖 Multi-Agent Task Decomposition - Setup")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    # Sprawdzenie Python
    if sys.version_info < (3, 8):
        print(f"{Fore.RED}❌ Wymaga Python 3.8+, masz {sys.version}{Style.RESET_ALL}")
        return False
    
    print(f"{Fore.GREEN}✓ Python {sys.version.split()[0]}{Style.RESET_ALL}\n")
    
    # Sprawdzenie venv
    print(f"{Fore.YELLOW}Sprawdzam virtual environment...{Style.RESET_ALL}")
    venv_path = ROOT / "venv"
    if venv_path.exists():
        print(f"{Fore.GREEN}✓ venv znaleziony{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠ venv nie znaleziony - należy go stworzyć{Style.RESET_ALL}")
        print(f"  Uruchom: python3 -m venv venv")
        print(f"  Potem: source venv/bin/activate")
    
    # Konfiguracja config/.env
    print(f"\n{Fore.YELLOW}Konfiguracja API (config/.env){Style.RESET_ALL}")
    
    env_file = ROOT / "config" / ".env"
    if env_file.exists():
        print(f"{Fore.GREEN}✓ config/.env już istnieje{Style.RESET_ALL}")
        modify = input("Chcesz go zmodyfikować? (y/n): ").lower() == 'y'
        if not modify:
            return validate_env()
    
    print("\nWybierz dostawcę API:")
    print("  1) OpenRouter (REKOMENDOWANY - tańszy)")
    print("  2) OpenAI (oficjalny)")
    print("  3) Ollama (lokalnie)")
    
    choice = input("Wybór (1-3): ").strip()
    
    api_provider = {
        "1": "openrouter",
        "2": "openai",
        "3": "ollama"
    }.get(choice, "openrouter")
    
    # Klucz API
    api_key = ""
    if api_provider in ["openai", "openrouter"]:
        if api_provider == "openrouter":
            print(f"\n{Fore.CYAN}OpenRouter:https://openrouter.ai/keys{Style.RESET_ALL}")
            print("Klucz powinien zaczynać się od: sk-or-v1-")
        else:
            print(f"\n{Fore.CYAN}OpenAI: https://platform.openai.com/api-keys{Style.RESET_ALL}")
            print("Klucz powinien zaczynać się od: sk-")
        
        api_key = input("Wklej API key: ").strip()
        
        if not api_key:
            print(f"{Fore.RED}❌ API key nie może być pusty{Style.RESET_ALL}")
            return False
    
    # Model
    print("\nWybierz model:")
    if api_provider == "openrouter":
        print("  1) meta-llama/llama-2-70b-chat (szybki, tani)")
        print("  2) gpt-4o-mini (OpenAI, drogi)")
        print("  3) mistralai/mistral-7b-instruct (lekki)")
    elif api_provider == "openai":
        print("  1) gpt-4o-mini (rekomendowany)")
        print("  2) gpt-4o (mądrzejszy, drogi)")
    else:
        print("  1) llama2 (standardowy)")
        print("  2) mistral (inteligentniejszy)")
    
    model_input = input("Wybór (domyślnie 1): ").strip() or "1"
    
    if api_provider == "openrouter":
        model = {
            "1": "meta-llama/llama-2-70b-chat",
            "2": "gpt-4o-mini",
            "3": "mistralai/mistral-7b-instruct"
        }.get(model_input, "meta-llama/llama-2-70b-chat")
    elif api_provider == "openai":
        model = {
            "1": "gpt-4o-mini",
            "2": "gpt-4o"
        }.get(model_input, "gpt-4o-mini")
    else:
        model = {
            "1": "llama2",
            "2": "mistral"
        }.get(model_input, "llama2")
    
    # Zapis do config/.env
    print(f"\n{Fore.YELLOW}Zapisuję konfigurację do config/.env...{Style.RESET_ALL}")
    
    env_content = f"""# Multi-Agent Task Decomposition System - Konfiguracja
# Autogenerowana przez setup.py

# Dostawca API
AI_PROVIDER={api_provider}

# API Key (nie pushuj do Gita!)
API_KEY={api_key if api_key else ""}

# Model do użycia
MODEL={model}

# URL Ollama (jeśli używasz ollama)
OLLAMA_BASE_URL=http://localhost:11434/v1

# Katalog do persistencji
PERSISTENCE_DIR=results
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"{Fore.GREEN}✓ Konfiguracja zapisana do config/.env{Style.RESET_ALL}")
    
    # Test konfiguracji
    print(f"\n{Fore.YELLOW}Testowanie konfiguracji...{Style.RESET_ALL}")
    
    try:
        from cad_ai.agents import BaseAgent
        agent = BaseAgent()
        print(f"{Fore.GREEN}✓ Konfiguracja API OK{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Błąd: {e}{Style.RESET_ALL}")
        return False
    
    return True


def validate_env():
    """Walidacja istniejącego .env"""
    
    try:
        from pathlib import Path
        if not (ROOT / "config" / ".env").exists():
            print(f"{Fore.RED}❌ Brak pliku config/.env{Style.RESET_ALL}")
            return False
        
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=ROOT / "config" / ".env")
        
        import os
        provider = os.getenv("AI_PROVIDER")
        api_key = os.getenv("API_KEY")
        model = os.getenv("MODEL")
        
        print(f"AI_PROVIDER: {Fore.YELLOW}{provider}{Style.RESET_ALL}")
        print(f"MODEL: {Fore.YELLOW}{model}{Style.RESET_ALL}")
        
        if not provider:
            print(f"{Fore.RED}❌ AI_PROVIDER nie ustawiony{Style.RESET_ALL}")
            return False
        
        if provider in ["openai", "openrouter"] and not api_key:
            print(f"{Fore.RED}❌ API_KEY wymagany dla {provider}{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}✓ Konfiguracja poprawna{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Błąd walidacji: {e}{Style.RESET_ALL}")
        return False


def main():
    """Główna funkcja"""
    
    # Sprawdzenie katalogów
    print(f"{Fore.YELLOW}Sprawdzam strukturę projektu...{Style.RESET_ALL}")
    
    required_files = [
        "src/cad_ai/agents.py",
        "src/cad_ai/task_manager.py",
        "src/cad_ai/persistence.py",
        "requirements.txt"
    ]
    
    for f in required_files:
        if not (ROOT / f).exists():
            print(f"{Fore.RED}❌ Brakuje: {f}{Style.RESET_ALL}")
            return False
        print(f"{Fore.GREEN}✓ {f}{Style.RESET_ALL}")
    
    # Instalacja zależności
    print(f"\n{Fore.YELLOW}Instalowanie zależności...{Style.RESET_ALL}")
    
    try:
        import openai
        print(f"{Fore.GREEN}✓ openai{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.YELLOW}  pip install openai{Style.RESET_ALL}")
        os.system("pip install openai")
    
    try:
        import dotenv
        print(f"{Fore.GREEN}✓ python-dotenv{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.YELLOW}  pip install python-dotenv{Style.RESET_ALL}")
        os.system("pip install python-dotenv")
    
    try:
        import colorama
        print(f"{Fore.GREEN}✓ colorama{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.YELLOW}  pip install colorama{Style.RESET_ALL}")
        os.system("pip install colorama")
    
    # Setup
    if not setup_wizard():
        print(f"\n{Fore.RED}Setup nie powiódł się!{Style.RESET_ALL}")
        return False
    
    # Podsumowanie
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.GREEN}✅ Setup ukończony!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    print("Następne kroki:")
    print(f"  1. Aktywuj venv: {Fore.YELLOW}source venv/bin/activate{Style.RESET_ALL}")
    print(f"  2. Uruchom demo: {Fore.YELLOW}python demos/demo_persistence.py{Style.RESET_ALL}")
    print(f"  3. Program interaktywny: {Fore.YELLOW}python scripts/main.py{Style.RESET_ALL}")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
