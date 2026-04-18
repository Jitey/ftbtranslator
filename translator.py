from deep_translator import GoogleTranslator
import json
from pathlib import Path
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from icecream import ic



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


    def process_file(self, file: Path, base_path: Path, target_lang: str, chunk_size: int | None = None) -> Path:
        if chunk_size is None:
            translation = self.translate_module(file)
        else:
            translation = self.batch_translate_module(file, chunk_size)

        relative = file.relative_to(base_path / "old")
        target = relative.with_name(f"{target_lang}.json")
        new_path = base_path / "new" / target

        self.write_json(translation, new_path)
        
        return new_path
    
    def translate_module(self, file_path: Path) -> dict[str, str]:
        content: dict[str, str] = self.open_json(file_path)
        translated_content = {}

        already_file = file_path.parent / f"{self.target_name}.json"
        already_translated: dict[str, str] = {}
        if already_file.exists():
            already_translated = self.open_json(already_file)
        
        for key, value in tqdm(content.items(), desc=file_path.parent.parent.name):
            if key in already_translated and already_translated[key]:
                translated_content[key] = already_translated[key]
            else:
                translated_content[key] = self.translate(value)

        return translated_content
    
    def batch_translate_module(self, file_path: Path, chunk_size: int) -> dict[str, str]:
        content: dict[str, str] = self.open_json(file_path)

        already_file = file_path.parent / f"{self.target_name}.json"
        already_translated: dict[str, str] = {}
        if already_file.exists():
            already_translated = self.open_json(already_file)

        keys = list(content.keys())
        values = list(content.values())

        translations = [None] * len(values)
        to_translate_indices = [
            i for i, k in enumerate(keys)
            if not (k in already_translated and already_translated[k])
        ]

        pending_values = [values[i] for i in to_translate_indices]

        translated_pending = []
        for i in tqdm(range(0, len(pending_values), chunk_size), desc=file_path.parent.parent.name):
            chunk = pending_values[i:i+chunk_size]
            translated_pending.extend(self.translate_batch(chunk))

        pending_iter = iter(translated_pending)

        for idx, key in enumerate(keys):
            if key in already_translated and already_translated[key]:
                translations[idx] = already_translated[key]
            else:
                translations[idx] = next(pending_iter)

        translated_content = dict(zip(keys, translations))
        
        return translated_content


                       
                       

if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parent
