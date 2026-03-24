from pathlib import Path
import json
from tqdm import tqdm


from icecream import ic


class WorkspaceExporter:

    def __init__(self, source: Path | str, target: Path | str) -> None:
        self.source = Path(source)
        self.target = Path(target)

    @staticmethod
    def open_json(path: str | Path) -> dict:
        with open(path, "r") as f:
            return json.load(f)
        
    @staticmethod
    def write_json(content: dict, path: str | Path) -> None:
        with open(path, "w") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            
    
    def open_workspace(self, file_name: str) -> dict:
        path = self.source / f"{file_name}.json"
        return json.load(path.open())

    def create_file(self, content: dict) -> Path:
        """Create a the corresponding json langage file and return his directory location

        Args:
            content (dict): File data dict

        Returns:
            Path: Directory path
        """
        file_path: str = content['path']
        dir_path = self.target / Path(file_path).parent

        try:
            self.write_json(content['content'], file_path)
            
        except FileNotFoundError:
            self.write_json(content['content'], file_path)
        
        return dir_path
    
    @staticmethod
    def get_module_index(files: list[dict], namespace: str, language: str) -> int | None:
        for i, file in enumerate(files):
            if (file['namespace'] == namespace) and (file['language'] == language):
                return i


    def export_to_workspace(self, dir_path: Path, file_name: str="StarT-Dev-Team_Star-Technology-workspace") -> None:
        """Export kubejs directory into a single json file workspace formated for Minecraft Translation Helper

        Args:
            file_name (str): Name of the generated .json to export
        """
        workspace = self.open_workspace(file_name)

        for file in tqdm(dir_path.glob("*/lang/*.json")):
            data = json.load(file.open())
            lang, _ = file.name.split('.')
            idx = self.get_module_index(workspace['files'], file.parent.parent.name, lang)
           
            if idx is not None:
                workspace['files'][idx]['content'] = data
        
        path = self.target / f"{file_name}.json"
        self.write_json(workspace, path)





if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parent.parent
    SOURCE_PATH = ROOT / "workspaces" / "imported"
    TARGET_PATH = ROOT / "workspaces" / "exported"
    BASE_PATH = ROOT / "translations"
    MODULES_PATH = BASE_PATH / "new" / "kubejs" / "assets"

    WorkspaceExporter(SOURCE_PATH, TARGET_PATH).export_to_workspace(MODULES_PATH)