import asyncio
from mth import WorkspaceImporter, WorkspaceExporter
from translator import Translator
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm.contrib.concurrent import thread_map


from icecream import ic
from utility import timing_performance


def import_workspace(root: Path) -> None:
    FILE_NAME = "StarT-Dev-Team_Star-Technology-workspace"
    SOURCE_PATH = root / "workspaces" / "imported"
    TARGET_PATH = root / "translations" / "old"
    
    WorkspaceImporter(SOURCE_PATH, TARGET_PATH).import_from_workspace(FILE_NAME)

def export_worksapce() -> None:
    pass
    
    

    
@timing_performance
def translate_all(root: Path, target_lang: str, source_lang: str= 'en_us') -> None:
    BASE_PATH = root / "translations"
    MODULES_PATH = BASE_PATH / "old" / "kubejs" / "assets"
    slg, _ = source_lang.split('_')
    tlg, _ = target_lang.split('_')
    
    translator = Translator(source=slg, target=tlg)
    for file in MODULES_PATH.glob(f"*/lang/{source_lang}.json"):
        translator.process_file(file, BASE_PATH, target_lang)
  
  
@timing_performance        
def thread_translate_all(root: Path, target_lang: str, source_lang: str= 'en_us') -> None:
    BASE_PATH = root / "translations"
    MODULES_PATH = BASE_PATH / "old" / "kubejs" / "assets"
    slg, _ = source_lang.split('_')
    tlg, _ = target_lang.split('_')

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(
            lambda f: Translator(source=slg, target=tlg).process_file(f, BASE_PATH, target_lang),
            MODULES_PATH.glob(f"*/lang/{source_lang}.json")
        )


# Async version of translate using asyncio for concurrent execution
# This function demonstrates how to run translation tasks concurrently using asyncio.gather
async def async_translate(root: Path, target_lang: str, source_lang: str= 'en_us') -> None:
    BASE_PATH = root / "translations"
    MODULES_PATH = BASE_PATH / "old" / "kubejs" / "assets"
    slg, _ = source_lang.split('_')
    tlg, _ = target_lang.split('_')

    # Define an async wrapper for the translation process
    async def translate_file(file_path: Path):
        # Run the blocking process_file call in a thread to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, Translator(source=slg, target=tlg).process_file, file_path, BASE_PATH, target_lang)

    tasks = [translate_file(f) for f in MODULES_PATH.glob(f"*/lang/{source_lang}.json")]
    await asyncio.gather(*tasks)


# Define translate_all to call async_translate and run the event loop
@timing_performance
def async_translate_all(root: Path, target_lang: str, source_lang: str= 'en_us') -> None:
    # Run the async_translate coroutine using asyncio.run
    asyncio.run(async_translate(root, target_lang, source_lang))




def main():
    ROOT = Path(__file__).resolve().parent

    # import_workspace(ROOT)

    # export_workspace()
    
    BASE_PATH = ROOT / "translations"
    MODULES_PATH = BASE_PATH / "old" / "kubejs" / "assets"
    
    # translate_all(ROOT, 'fr_fr')
    # thread_translate_all(ROOT, 'fr_fr')
    async_translate_all(ROOT, 'fr_fr')



if __name__ == "__main__":
    main()