from deep_translator import GoogleTranslator
import json
from pathlib import Path
from tqdm import tqdm

from icecream import ic
from utility import timing_performance, time


class Translator(GoogleTranslator):
    
    def __init__(self, source: str = "en", target: str = "fr", proxies: dict | None = None, **kwargs):
        self.target = target
        self.target_name = f"{target}_{target}"
        super().__init__(source, target, proxies, **kwargs)


    @staticmethod
    def open_json(path: str | Path) -> dict:
        with open(path, "r") as f:
            return json.load(f)
        
    @staticmethod
    def write_json(content: dict, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(content, f, indent=4)


    def process_file(self, file: Path, base_path: Path, target_lang: str) -> Path:
        translation = self.batch_translate_module(file)

        relative = file.relative_to(base_path / "old")
        target = relative.with_name(f"{target_lang}.json")
        new_path = base_path / "new" / target

        self.write_json(translation, new_path)
        
        return new_path
    
    def translate_module(self, file_path: Path) -> dict[str, str]:
        content: dict[str, str] = self.open_json(file_path)

        translated_content = {}

        # print(f"Starting {self.target} translation of {file_path.parent.parent.name}...")
        a = time.time()
        # for key, value in tqdm(content.items()):
        for key, value in content.items():

            translated_value = self.translate(value)
            translated_content[key] = translated_value

        print(f"{file_path.parent.parent.name} translated in {time.time() - a:.1f}s")
        return translated_content
    
    def batch_translate_module(self, file_path: Path, chunk_size: int | None = None) -> dict[str, str]:
        content: dict[str, str] = self.open_json(file_path)
        values = list(content.values())
        translations = []

        if chunk_size is None:
            chunk_size = len(values)

        # print(f"Starting {self.target} translation of {file_path.parent.parent.name}...")
        a = time.time()
        # for i in tqdm(range(0, len(values), chunk_size)):
        for i in range(0, len(values), chunk_size):
            chunk = values[i:i+chunk_size]
            translations.extend(self.translate_batch(chunk))

        print(f"{file_path.parent.parent.name} translated in {time.time() - a:.1f}s")
        b = time.time()
        translated_content = dict(zip(content.keys(), translations))
        print(f"Reconstruction du json en {time.time() - b:.1f}s")
        print(f"Total {time.time() - a:.1f}s")
        
        return translated_content


@timing_performance
def main(root: Path, target_lang: str, source_lang: str= 'en_us') -> None:
    from concurrent.futures import ThreadPoolExecutor
    
    BASE_PATH = root / "translations"
    MODULES_PATH = BASE_PATH / "old" / "kubejs" / "assets"
    slg, _ = source_lang.split('_')
    tlg, _ = target_lang.split('_')
    
    # translator = Translator(source=slg, target=tlg)

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(
            lambda f: Translator(source=slg, target=tlg).process_file(f, BASE_PATH, target_lang),
            MODULES_PATH.glob(f"*/lang/{source_lang}.json")
        )
                       
                       

if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parent
    
    main(ROOT, 'fr_fr', 'en_us')