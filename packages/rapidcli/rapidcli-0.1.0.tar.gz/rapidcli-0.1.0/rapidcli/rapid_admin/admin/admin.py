from ..rapidcli.extension_registrar import register_extension
from rad rapidcli import utils  as framework_utils
import shutil

@register_extension()
class RapidAdmin():
    def start():
        self.show_input_menu("main")

    def create_cli(project_dir: str = "", project_name: str = ""):
        """Given the project path, create a cli project at the project path."""
        new_cli_project_path = os.path.join(os.sep, project_dir, project_name)
        shutil.copytree(self.get_rendered_extension_templates("rapidcli"), destination_dir)