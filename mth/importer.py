from pathlib import Path
import json
from tqdm import tqdm



class WorkspaceImporter:
    
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
            json.dump(content, f, indent=4)


    def create_directory(self, path: Path, dir_name: str="") -> Path:
            """
            Create a directory structure based on the test name and date.

            Args:
                base_path (str): The base path where the directory structure will be created.
                dir_name (str): The name of the directory. 
                date (dt): The date of the test.

            Returns:
                Path: The path to the created directory structure.
            """
            dir = Path(path) / dir_name if dir_name else path
            
            try:
                dir.mkdir(parents=True, exist_ok=False)
                print(f"> Directory created: {dir}")
                
            except FileExistsError:
                print(f"[!] Directory already exists: {dir}")

            return dir
        
    def create_file(self, content: dict) -> Path:
        """Create a the corresponding json langage file and return his directory location

        Args:
            content (dict): File data dict

        Returns:
            Path: Directory path
        """
        file_path = Path(content['path'])
        full_path = self.target / file_path 
        dir_path = full_path.parent

        try:
            self.write_json(content['content'], full_path)
            
        except FileNotFoundError:
            self.create_directory(dir_path)
            self.write_json(content['content'], full_path)
        
        return dir_path


    def import_from_workspace(self, file_name: str) -> None:
        """Import Minecraft Translation Helper workspace from the generated json file and rebuild original kubejs directory

        Args:
            file_name (str): Name of the generated .json to import
        """
        file_path = self.source / f"{file_name}.json"
        data = self.open_json(file_path)

        for file in tqdm(data['files']):
            self.create_file(file)
            
        





if __name__ == '__main__':
    ROOT = Path(__file__).parent.parent
    FILE_NAME = "StarT-Dev-Team_Star-Technology-workspace"
    SOURCE_PATH = ROOT / "workspaces" / "imported"
    TARGET_PATH = ROOT / "translations" / "old"
    
    WorkspaceImporter(SOURCE_PATH, TARGET_PATH).import_from_workspace(FILE_NAME)