from mth import WorkspaceImporter, WorkspaceExporter
from translator import Translator
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.contrib.concurrent import thread_map
from tqdm import tqdm


from icecream import ic
from utility import timing_performance


def import_workspace(root: Path) -> None:
    FILE_NAME = "StarT-Dev-Team_Star-Technology-workspace"
    SOURCE_PATH = root / "workspaces" / "imported"
    TARGET_PATH = root / "translations" / "old"
    
    WorkspaceImporter(SOURCE_PATH, TARGET_PATH).import_from_workspace(FILE_NAME)

def export_workspace(root: Path) -> None:
    FILE_NAME = "StarT-Dev-Team_Star-Technology-workspace"
    SOURCE_PATH = root / "workspaces" / "imported"
    TARGET_PATH = root / "workspaces" / "exported"
    MODULES_PATH = root / "translations" / "new" / "kubejs" / "assets"
    
    WorkspaceExporter(SOURCE_PATH, TARGET_PATH).export_to_workspace(MODULES_PATH, FILE_NAME)
    
    

    
  
  
@timing_performance        
def thread_translate_all(root: Path, target_lang: str, source_lang: str= 'en_us') -> None:
    BASE_PATH = root / "translations"
    MODULES_PATH = BASE_PATH / "old" / "kubejs" / "assets"
    slg, _ = source_lang.split('_')
    tlg, _ = target_lang.split('_')

    with ThreadPoolExecutor(max_workers=9) as executor:
        executor.map(
            lambda f: Translator(source=slg, target=tlg).process_file(f, BASE_PATH, target_lang),
            MODULES_PATH.glob(f"*/lang/{source_lang}.json")
        )
        


def main():
    ROOT = Path(__file__).resolve().parent

    import_workspace(ROOT)
    
    thread_translate_all(ROOT, 'fr_fr')

    export_workspace(ROOT)



if __name__ == "__main__":
    main()