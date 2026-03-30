import json
import os


def keep_original_resource_pack():
    mc_plants = json.loads(open(r"D:\App\Game\Minecraft\Config\Original.json", 'r', encoding='utf-8').read())
    resources_path = mc_plants['base_path']
    block_states_path = resources_path + r'\blockstates'
    models_path = resources_path + r'\models'
    textures_path = resources_path + r'\textures\block'

    def is_scheduled_data(filename) -> bool:
        for category in mc_plants["category"].values():
            for plant in category:
                if plant in filename: return True
                pass
            pass
        return False

    def del_work(folder_path):
        for f in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path):
                if not is_scheduled_data(f): os.remove(file_path)
            elif os.path.isdir(file_path) and not is_scheduled_data(f):
                del_work(file_path)
            pass
        pass

    if os.path.exists(block_states_path):
        del_work(block_states_path)
        pass
    if os.path.exists(models_path):
        del_work(models_path)
        pass
    if os.path.exists(textures_path):
        del_work(textures_path)
        pass
    pass
