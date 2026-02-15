"""
Moduł agentów AI - różne typy agentów do dekompozycji, wykonania i weryfikacji zadań
"""
import os
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .task_manager import Task, TaskStatus, TaskType, TaskManager
from .persistence import PersistenceManager
from colorama import Fore, Style, init

init(autoreset=True)


class BaseAgent:
    """Bazowa klasa dla wszystkich agentów"""
    
    def __init__(self, name: str, role: str, api_key: Optional[str] = None, 
                 provider: Optional[str] = None, model: Optional[str] = None):
        self.name = name
        self.role = role
        self.provider = provider or os.getenv("AI_PROVIDER", "openai")
        self.model = model or os.getenv("MODEL", "gpt-4o-mini")
        
        # Konfiguracja klienta w zależności od providera
        if self.provider == "openai":
            self.client = OpenAI(api_key=api_key or os.getenv("API_KEY"))
        elif self.provider == "openrouter":
            self.client = OpenAI(
                api_key=api_key or os.getenv("API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            )
        elif self.provider == "ollama":
            self.client = OpenAI(
                api_key="ollama",  # Ollama nie wymaga klucza
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            )
        else:
            raise ValueError(f"Nieobsługiwany dostawca API: {self.provider}")
        
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Wywołuje model językowy"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"{Fore.RED}Błąd wywołania LLM: {e}")
            return ""
    
    def log(self, message: str, color=Fore.WHITE):
        """Loguje wiadomość z kolorami"""
        print(f"{color}[{self.name}] {message}{Style.RESET_ALL}")


class ComplexityAnalyzerAgent(BaseAgent):
    """Agent analizujący złożoność - ocenia czy zadanie wymaga podziału"""
    
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None,
                 model: Optional[str] = None):
        super().__init__("ComplexityAnalyzer", "Complexity Assessment", api_key, provider, model)
    
    def should_decompose(self, task: Task) -> Dict[str, Any]:
        """Ocenia czy zadanie wymaga podziału na podzadania"""
        self.log(f"Analizuję: {task.description[:50]}...", Fore.MAGENTA)
        
        system_prompt = """Jesteś ekspertem w analizie złożoności zadań. OCENIASZ POTENCJALNY OUTPUT!
Oceniasz zadania pod kątem:
1. POTENCJALNEJ ILOŚCI OUTPUTU - ile tekstu/danych wygeneruje to zadanie?
2. Czy zadanie jest wystarczająco PROSTE do bezpośredniego wykonania
3. Liczba kroków wymaganych do wykonania

KRYTERIA POTENCJALNEGO OUTPUTU (to jest KLUCZOWE!):
KRÓTKI (< 500 słów): Prosta odpowiedź, kilka zdań, lista
ŚREDNI (500-1500 słów): Krótkie wyjaśnienie, kilka akapitów
DŁUGI (1500-5000 słów): Raport, wiele sekcji, szczegółowe omówienie
BARDZO_DŁUGI (> 5000 słów): Bardzo szczegółowy raport, analiza wieloaspektowa

Kryteria PROSTEGO zadania (nie wymaga podziału):
- Potencjalny output: KRÓTKI lub ŚREDNI
- Można wykonać w jednym kroku
- Nie wymaga wielu różnych analiz/obliczeń
- Jest konkretne i jednoznaczne

Kryteria ZŁOŻONEGO zadania (wymaga podziału):
- Potencjalny output: DŁUGI lub BARDZO_DŁUGI
- Wymaga wielu kroków lub analiz
- Obejmuje różne aspekty/dziedziny
- Zbyt szerokie lub wielowątkowe

Odpowiedz w formacie:
POTENCJALNY_OUTPUT: [KRÓTKI/ŚREDNI/DŁUGI/BARDZO_DŁUGI]
PODZIAŁ: [TAK/NIE]
LICZBA_PODZADAŃ: [2-5 jeśli TAK, 0 jeśli NIE]
ZŁOŻONOŚĆ: [NISKA/ŚREDNIA/WYSOKA/BARDZO_WYSOKA]
UZASADNIENIE: [wyjaśnienie potencjalnego outputu i decyzji]"""

        user_prompt = f"""Zadanie do oceny:
{task.description}

Aktualny poziom zagnieżdżenia: {task.level}

SKUPIAJ SIĘ NA POTENCJALNYM OUTPUTIE - ile tekstu/danych wygeneruje to zadanie?
Czy to zadanie wymaga podziału na podzadania?"""

        response = self._call_llm(system_prompt, user_prompt)
        
        # Parsuj odpowiedź
        analysis = self._parse_complexity_response(response)
        
        if analysis["should_split"]:
            self.log(f"✓ Zadanie WYMAGA podziału na {analysis['num_subtasks']} podzadań", Fore.YELLOW)
            self.log(f"  Output: {analysis['output_size']} | Złożoność: {analysis['complexity']}", Fore.CYAN)
        else:
            self.log(f"✓ Zadanie jest WYSTARCZAJĄCO PROSTE - wykonaj bezpośrednio", Fore.GREEN)
            self.log(f"  Output: {analysis['output_size']} | Złożoność: {analysis['complexity']}", Fore.CYAN)
        
        return analysis
    
    def _parse_complexity_response(self, response: str) -> Dict[str, Any]:
        """Parsuje odpowiedź o złożoności"""
        import re
        
        analysis = {
            "should_split": False,
            "num_subtasks": 0,
            "complexity": "ŚREDNIA",
            "output_size": "ŚREDNI",
            "reasoning": ""
        }
        
        lines = response.upper().split('\n')
        for line in lines:
            if 'POTENCJALNY_OUTPUT' in line or 'POTENCJALNY OUTPUT' in line:
                if 'BARDZO_D\u0141UGI' in line or 'BARDZO D\u0141UGI' in line or 'BARDZO_DLUGI' in line or 'BARDZO DLUGI' in line:
                    analysis["output_size"] = "BARDZO_D\u0141UGI"
                elif 'D\u0141UGI' in line or 'DLUGI' in line:
                    analysis["output_size"] = "D\u0141UGI"
                elif '\u015aREDNI' in line or 'SREDNI' in line:
                    analysis["output_size"] = "\u015aREDNI"
                elif 'KR\u00d3TKI' in line or 'KROTKI' in line:
                    analysis["output_size"] = "KR\u00d3TKI"
            elif 'PODZIA\u0141:' in line or 'PODZIAL' in line:
                analysis["should_split"] = 'TAK' in line
            elif 'LICZBA_PODZADA\u0143' in line or 'LICZBA PODZADAN' in line or 'LICZBA_PODZADAN' in line:
                numbers = re.findall(r'\d+', line)
                if numbers:
                    analysis["num_subtasks"] = min(int(numbers[0]), 5)
            elif 'Z\u0141O\u017bONO\u015a\u0106:' in line or 'ZLOZONOSC' in line:
                if 'BARDZO_WYSOKA' in line or 'BARDZO WYSOKA' in line or 'BARDZO_WYSOKA' in line:
                    analysis["complexity"] = "BARDZO_WYSOKA"
                elif 'WYSOKA' in line:
                    analysis["complexity"] = "WYSOKA"
                elif '\u015aREDNIA' in line or 'SREDNIA' in line:
                    analysis["complexity"] = "\u015aREDNIA"
                elif 'NISKA' in line:
                    analysis["complexity"] = "NISKA"
            elif 'UZASADNIENIE:' in line:
                analysis["reasoning"] = line.split(':', 1)[1].strip()
        
        # Je\u015bli num_subtasks to 0 ale should_split to True, ustaw domy\u015blnie 3
        if analysis["should_split"] and analysis["num_subtasks"] == 0:
            analysis["num_subtasks"] = 3
        
        return analysis


class CoordinatorAgent(BaseAgent):
    """Agent koordynujący - analizuje cel i dzieli na podzadania"""
    
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None, 
                 model: Optional[str] = None):
        super().__init__("Coordinator", "Task Decomposition", api_key, provider, model)
        
    def decompose_task(self, task: Task, max_subtasks: int, task_manager=None) -> List[str]:
        """Dekomponuje zadanie na podzadania"""
        self.log(f"Analizuję zadanie: {task.description}", Fore.CYAN)
        
        # Jeśli max_subtasks = 1, zadanie jest atomowe
        if max_subtasks == 1:
            self.log("Zadanie ocenione jako atomowe - nie wymaga dekompozycji", Fore.YELLOW)
            return []
        
        system_prompt = f"""Jesteś ekspertem w dekompozycji zadań. Twoim zadaniem jest rozłożenie złożonego 
zadania na dokładnie {max_subtasks} mniejszych, wykonalnych podzadań.

Zasady:
1. Każde podzadanie powinno być konkretne i wykonalne
2. Podzadania powinny być logicznie uporządkowane
3. Razem podzadania powinny w pełni realizować główne zadanie
4. Zwróć DOKŁADNIE {max_subtasks} podzadań, każde w osobnej linii, numerowane
5. Nie zwracaj więcej ani mniej niż {max_subtasks} podzadań"""

        parent_context = ""
        if task.parent_id and task_manager:
            parent_task = task_manager.get_task(task.parent_id)
            if parent_task:
                parent_context = f"\nKontekst z zadania nadrzędnego: {parent_task.description}"

        user_prompt = f"""Główne zadanie (poziom {task.level}):
{task.description}
{parent_context}

Rozłóż to zadanie na DOKŁADNIE {max_subtasks} podzadań."""

        response = self._call_llm(system_prompt, user_prompt)
        
        # Parsuj odpowiedź
        subtasks = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Usuń numerację i białe znaki
                clean_line = line.lstrip('0123456789.-•) ').strip()
                if clean_line:
                    subtasks.append(clean_line)
        
        # Upewnij się, że mamy odpowiednią liczbę
        if len(subtasks) > max_subtasks:
            subtasks = subtasks[:max_subtasks]
        
        self.log(f"Utworzono {len(subtasks)} podzadań", Fore.GREEN)
        return subtasks


class ExecutorAgent(BaseAgent):
    """Agent wykonawczy - realizuje atomowe zadania"""
    
    def __init__(self, agent_id: int, api_key: Optional[str] = None, 
                 provider: Optional[str] = None, model: Optional[str] = None):
        super().__init__(f"Executor-{agent_id}", "Task Execution", api_key, provider, model)
        self.agent_id = agent_id
        
    def execute_task(self, task: Task, context: Dict[str, Any] = None) -> str:
        """Wykonuje zadanie i zwraca wynik"""
        self.log(f"Wykonuję zadanie: {task.description[:50]}...", Fore.BLUE)
        
        context_info = ""
        if context:
            context_info = f"\nKontekst z poprzednich zadań:\n{self._format_context(context)}"
        
        system_prompt = """Jesteś specjalistycznym agentem wykonawczym. Twoim zadaniem jest wykonanie 
konkretnego zadania i przedstawienie szczegółowego wyniku.

Zasady:
1. Wykonaj zadanie dokładnie według opisu
2. Zwróć konkretny, mierzalny wynik
3. Jeśli potrzebujesz danych z kontekstu, wykorzystaj je
4. Wynik powinien być zwięzły ale kompletny
5. Jeśli zadanie nie może być wykonane, wyjaśnij dlaczego"""

        user_prompt = f"""Zadanie do wykonania:
{task.description}
{context_info}

Wykonaj zadanie i przedstaw wynik."""

        result = self._call_llm(system_prompt, user_prompt)
        self.log("Zadanie ukończone", Fore.GREEN)
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatuje kontekst dla LLM"""
        formatted = []
        for key, value in context.items():
            formatted.append(f"- {key}: {value}")
        return "\n".join(formatted)


class VerificationAgent(BaseAgent):
    """Agent weryfikujący - sprawdza jakość wykonania zadań"""
    
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None,
                 model: Optional[str] = None):
        super().__init__("Verifier", "Quality Assurance", api_key, provider, model)
        
    def verify_task(self, task: Task) -> Dict[str, Any]:
        """Weryfikuje wykonanie zadania"""
        self.log(f"Weryfikuję zadanie: {task.description[:50]}...", Fore.MAGENTA)
        
        if not task.result:
            return {
                "passed": False,
                "score": 0.0,
                "feedback": "Brak wyniku do weryfikacji",
                "issues": ["Zadanie nie zostało wykonane"]
            }
        
        system_prompt = """Jesteś ekspertem w kontroli jakości i weryfikacji zadań.
Twoim zadaniem jest ocena czy zadanie zostało wykonane poprawnie i kompletnie.

Zwróć odpowiedź w formacie:
OCENA: [PASS/FAIL]
PUNKTACJA: [0.0-10.0]
FEEDBACK: [Szczegółowa ocena]
PROBLEMY: [Lista problemów lub "Brak"]"""

        user_prompt = f"""Zadanie:
{task.description}

Wynik wykonania:
{task.result}

Oceń jakość wykonania zadania."""

        response = self._call_llm(system_prompt, user_prompt)
        
        # Parsuj odpowiedź
        verification = self._parse_verification(response)
        
        if verification["passed"]:
            self.log(f"✓ Weryfikacja zakończona sukcesem (wynik: {verification['score']}/10)", Fore.GREEN)
        else:
            self.log(f"✗ Weryfikacja nie powiodła się (wynik: {verification['score']}/10)", Fore.RED)
        
        return verification
    
    def _parse_verification(self, response: str) -> Dict[str, Any]:
        """Parsuje odpowiedź weryfikacyjną"""
        lines = response.strip().split('\n')
        verification = {
            "passed": False,
            "score": 0.0,
            "feedback": "",
            "issues": []
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith("OCENA:"):
                verification["passed"] = "PASS" in line.upper()
            elif line.startswith("PUNKTACJA:"):
                try:
                    score_str = line.split(':')[1].strip()
                    verification["score"] = float(score_str.split('/')[0])
                except:
                    verification["score"] = 5.0
            elif line.startswith("FEEDBACK:"):
                verification["feedback"] = line.split(':', 1)[1].strip()
            elif line.startswith("PROBLEMY:"):
                issues_str = line.split(':', 1)[1].strip()
                if issues_str.lower() != "brak":
                    verification["issues"] = [issues_str]
        
        return verification


class DuplicationDetectorAgent(BaseAgent):
    """Agent wykrywający i eliminujący pokrywające się zadania"""
    
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None,
                 model: Optional[str] = None):
        super().__init__("DuplicationDetector", "Duplication Analysis", api_key, provider, model)
    
    def detect_and_eliminate_duplicates(self, subtask_descriptions: List[str], 
                                       parent_task: Task) -> List[str]:
        """Wykrywa i eliminuje pokrywające się zadania"""
        if len(subtask_descriptions) <= 1:
            return subtask_descriptions
        
        self.log(f"Analizuję {len(subtask_descriptions)} podzadań pod kątem duplikatów", Fore.MAGENTA)
        
        system_prompt = """Jesteś ekspertem w analizie zadań i wykrywaniu duplikatów.
Twoim zadaniem jest przeanalizować listę podzadań i:
1. Zidentyfikować zadania, które się pokrywają lub są duplikatami
2. Wybrać najlepsze, najbardziej kompletne wersje zadań
3. Zwrócić TYLKO unikalne, niepokrywające się zadania

Zasady eliminacji:
- Jeśli 2 zadania robią to samo, zostaw JEDNO (bardziej kompletne)
- Jeśli zadanie A zawiera się w zadaniu B, zostaw TYLKO B
- Jeśli zadania są komplementarne (różne aspekty), ZOSTAW OBA
- Zwróć TYLKO listę unikalnych zadań, każde w nowej linii, bez numeracji
- Jeśli wszystkie zadania są unikalne, zwróć wszystkie"""

        tasks_list = "\n".join([f"{i+1}. {desc}" for i, desc in enumerate(subtask_descriptions)])
        
        user_prompt = f"""Zadanie nadrzędne:
{parent_task.description}

Lista podzadań do analizy:
{tasks_list}

Przeanalizuj te podzadania i zwróć TYLKO unikalne, niepokrywające się zadania (bez numeracji)."""

        response = self._call_llm(system_prompt, user_prompt)
        
        # Parsuj odpowiedź
        unique_tasks = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Usuń ewentualną numerację
                clean_line = line.lstrip('0123456789.-•) ').strip()
                if clean_line and len(clean_line) > 10:  # Minimum 10 znaków dla sensownego zadania
                    unique_tasks.append(clean_line)
        
        eliminated_count = len(subtask_descriptions) - len(unique_tasks)
        
        if eliminated_count > 0:
            self.log(f"Wyeliminowano {eliminated_count} pokrywających się zadań", Fore.YELLOW)
            self.log(f"Pozostało {len(unique_tasks)} unikalnych zadań", Fore.GREEN)
        else:
            self.log(f"Wszystkie {len(unique_tasks)} zadania są unikalne", Fore.GREEN)
        
        return unique_tasks if unique_tasks else subtask_descriptions


class MasterOrchestrator:
    """Główny orkiestrator zarządzający wszystkimi agentami"""
    
    def __init__(self, task_manager: TaskManager, api_key: Optional[str] = None,
                 provider: Optional[str] = None, model: Optional[str] = None,
                 max_recursion_depth: int = 10, persistence_dir: str = "results"):
        self.task_manager = task_manager
        self.max_recursion_depth = max_recursion_depth  # Safety limit przeciw nieskończonej rekursji
        self.provider = provider or os.getenv("AI_PROVIDER", "openai")
        self.model = model or os.getenv("MODEL", "gpt-4o-mini")
        self.persistence = PersistenceManager(persistence_dir)
        self.complexity_analyzer = ComplexityAnalyzerAgent(api_key, provider, model)
        self.coordinator = CoordinatorAgent(api_key, provider, model)
        self.duplication_detector = DuplicationDetectorAgent(api_key, provider, model)
        self.verifier = VerificationAgent(api_key, provider, model)
        self.executors = [ExecutorAgent(i, api_key, provider, model) for i in range(1, 6)]
        self.executor_index = 0
        self.context_store: Dict[str, Any] = {}
        self.decomposition_stats = {
            "total_tasks": 0,
            "decomposed": 0,
            "executed_directly": 0,
            "max_level_reached": 0
        }
        self.execution_start_time = time.time()
        
    def log(self, message: str, color=Fore.WHITE):
        """Loguje wiadomość"""
        print(f"{color}[Orchestrator] {message}{Style.RESET_ALL}")
    
    def get_next_executor(self) -> ExecutorAgent:
        """Pobiera następnego dostępnego executora (round-robin)"""
        executor = self.executors[self.executor_index]
        self.executor_index = (self.executor_index + 1) % len(self.executors)
        return executor
    
    def process_task_recursive(self, task: Task) -> bool:
        """Rekursywnie przetwarza zadanie z inteligentną oceną potrzeby podziału"""
        self.log(f"\n{'='*80}\nPoziom {task.level}: Przetwarzanie zadania {task.id}", Fore.YELLOW)
        print(f"Opis: {task.description}\n{'='*80}")
        
        self.decomposition_stats["total_tasks"] += 1
        self.decomposition_stats["max_level_reached"] = max(
            self.decomposition_stats["max_level_reached"], 
            task.level
        )
        
        # Safety limit - ochrona przed nieskończoną rekursją
        if task.level >= self.max_recursion_depth:
            self.log(f"⚠ UWAGA: Osiągnięto limit bezpieczeństwa ({self.max_recursion_depth}) - wymuszam wykonanie", Fore.RED)
            self.decomposition_stats["executed_directly"] += 1
            return self._execute_atomic_task(task)
        
        # Krok 1: Complexity Analyzer ocenia czy zadanie wymaga podziału
        complexity_analysis = self.complexity_analyzer.should_decompose(task)
        
        # Jeśli zadanie jest wystarczająco proste, wykonaj bezpośrednio
        if not complexity_analysis["should_split"]:
            self.decomposition_stats["executed_directly"] += 1
            return self._execute_atomic_task(task)
        
        # Krok 2: Dekompozycja zadania
        num_subtasks = complexity_analysis["num_subtasks"]
        subtask_descriptions = self.coordinator.decompose_task(task, num_subtasks, self.task_manager)
        
        if not subtask_descriptions:
            # Coordinator nie stworzył podzadań - wykonaj bezpośrednio
            self.decomposition_stats["executed_directly"] += 1
            return self._execute_atomic_task(task)
        
        # Krok 3: Detekcja i eliminacja duplikatów
        subtask_descriptions = self.duplication_detector.detect_and_eliminate_duplicates(
            subtask_descriptions, task
        )
        
        if not subtask_descriptions:
            # Po eliminacji duplikatów nie zostało nic - wykonaj zadanie bezpośrednio
            self.decomposition_stats["executed_directly"] += 1
            return self._execute_atomic_task(task)
        
        # Utwórz podzadania
        self.decomposition_stats["decomposed"] += 1
        self.task_manager.update_task_status(task.id, TaskStatus.DECOMPOSED)
        
        for idx, subtask_desc in enumerate(subtask_descriptions, 1):
            subtask = self.task_manager.create_task(
                description=subtask_desc,
                task_type=TaskType.SUBTASK,
                level=task.level + 1,
                parent_id=task.id
            )
            self.log(f"Utworzono podzadanie {idx}/{len(subtask_descriptions)}: {subtask.id}", Fore.CYAN)
        
        # Rekursywnie przetwórz wszystkie podzadania
        all_success = True
        for subtask in task.subtasks:
            success = self.process_task_recursive(subtask)
            if success:
                # Zapisz wynik do kontekstu
                self.context_store[subtask.id] = subtask.result
            all_success = all_success and success
        
        if all_success:
            # Agreguj wyniki podzadań
            task.result = self._aggregate_subtask_results(task)
            self.task_manager.update_task_status(task.id, TaskStatus.COMPLETED)
            
            # Weryfikacja
            verification = self.verifier.verify_task(task)
            self.task_manager.update_verification(task.id, verification)
            
            if verification["passed"]:
                self.task_manager.update_task_status(task.id, TaskStatus.VERIFIED)
                return True
        
        self.task_manager.update_task_status(task.id, TaskStatus.FAILED)
        return False
    
    def print_statistics(self):
        """Wyświetla statystyki dekompozycji"""
        stats = self.decomposition_stats
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}STATYSTYKI DEKOMPOZYCJI")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Wszystkich zadań: {stats['total_tasks']}")
        print(f"Podzielonych na podzadania: {stats['decomposed']}")
        print(f"Wykonanych bezpośrednio: {stats['executed_directly']}")
        print(f"Maksymalny poziom zagnieżdżenia: {stats['max_level_reached']}")
        print(f"Średnia złożoność: {stats['decomposed'] / max(stats['total_tasks'], 1):.2%} zadań wymagało podziału{Style.RESET_ALL}\n")
    
    def save_results(self, task: Task):
        """Zapisuje wszystkie rezultaty do plików"""
        execution_time = time.time() - self.execution_start_time
        
        self.log(f"\n{Fore.CYAN}{'='*80}", Fore.WHITE)
        self.log(f"Zapisuję rezultaty do plików...", Fore.CYAN)
        self.log(f"{'='*80}\n", Fore.WHITE)
        
        # Zapisz czysty output
        if task.result:
            output_path = self.persistence.save_task_output(task.id, task.result)
            self.log(f"✓ Czysty wynik: {output_path}", Fore.GREEN)
        
        # Zapisz szczegółowy raport
        report_path = self.persistence.save_detailed_report(
            task, self.task_manager, self.decomposition_stats, execution_time
        )
        self.log(f"✓ Raport szczegółowy: {report_path}", Fore.GREEN)
        
        # Zapisz tekstowy raport (czytelny dla człowieka)
        text_report_path = self.persistence.export_as_text_report(
            task, self.decomposition_stats, execution_time
        )
        self.log(f"✓ Raport tekstowy: {text_report_path}", Fore.GREEN)
        
        # Zapisz hierarchię zadań
        hierarchy_path = self.persistence.save_task_hierarchy(task, self.task_manager)
        self.log(f"✓ Hierarchia zadań: {hierarchy_path}", Fore.GREEN)
        
        # Zapisz statystyki
        stats_path = self.persistence.save_decomposition_stats(
            self.decomposition_stats, task.id
        )
        self.log(f"✓ Statystyki: {stats_path}", Fore.GREEN)
        
        # Zapisz podsumowanie wykonania
        summary_path = self.persistence.save_execution_summary(
            task.id, task.description, self.decomposition_stats, execution_time
        )
        self.log(f"✓ Podsumowanie: {summary_path}", Fore.GREEN)
        
        # Wyświetl podsumowanie persistencji
        self.persistence.print_summary()
    
    def log(self, message: str, color=Fore.WHITE):
        """Loguje wiadomość z kolorami"""
        print(f"{color}{message}{Style.RESET_ALL}")
    
    def _execute_atomic_task(self, task: Task) -> bool:
        """Wykonuje zadanie atomowe"""
        self.task_manager.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        
        # Zbierz kontekst z zadań na tym samym poziomie
        context = self._gather_context(task)
        
        # Przydziel executora
        executor = self.get_next_executor()
        
        # Wykonaj zadanie
        result = executor.execute_task(task, context)
        self.task_manager.update_task_result(task.id, result)
        self.task_manager.update_task_status(task.id, TaskStatus.COMPLETED)
        
        # Weryfikacja
        verification = self.verifier.verify_task(task)
        self.task_manager.update_verification(task.id, verification)
        
        if verification["passed"]:
            self.task_manager.update_task_status(task.id, TaskStatus.VERIFIED)
            return True
        else:
            self.task_manager.update_task_status(task.id, TaskStatus.FAILED)
            return False
    
    def _aggregate_subtask_results(self, task: Task) -> str:
        """Agreguje wyniki podzadań"""
        results = []
        for subtask in task.subtasks:
            if subtask.result:
                results.append(f"[{subtask.id}] {subtask.result}")
        
        aggregated = f"Zadanie '{task.description}' zostało ukończone poprzez wykonanie {len(task.subtasks)} podzadań:\n\n"
        aggregated += "\n\n".join(results)
        
        return aggregated
    
    def _gather_context(self, task: Task) -> Dict[str, Any]:
        """Zbiera kontekst z poprzednich zadań"""
        context = {}
        
        # Dodaj kontekst z zadania rodzica
        if task.parent_id:
            parent = self.task_manager.get_task(task.parent_id)
            if parent:
                context["parent_task"] = parent.description
                
                # Dodaj wyniki innych podzadań tego samego rodzica
                for sibling in parent.subtasks:
                    if sibling.id != task.id and sibling.result:
                        context[f"sibling_{sibling.id}"] = sibling.result[:200]
        
        return context
