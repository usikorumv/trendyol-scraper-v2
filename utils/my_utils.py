class FolderAndFileUtils:
    @staticmethod
    def create_file(path: str, data: str):
        path_list = path.split("/")[:-1]

        paths = ""
        for path_ in path_list:
            paths += f"{path_}/"
            FolderAndFileUtils.create_folder(paths)

        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    @staticmethod
    def create_folder(name):
        from os import path
        from os import mkdir

        if path.exists(name):
            return
        mkdir(name)


class DictionaryUtils:
    @staticmethod
    def get_recursively(search_dict: dict(), to_find):
        fields_found = []

        for key, value in search_dict.items():
            if key == to_find:
                fields_found.append(value)

            elif isinstance(value, dict):
                results = DictionaryUtils.get_recursively(value, to_find)
                for result in results:
                    fields_found.append(result)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        more_results = DictionaryUtils.get_recursively(item, to_find)
                        for another_result in more_results:
                            fields_found.append(another_result)

        return fields_found

    @staticmethod
    def get_dict_by_key_value(lst: list, key, value):
        for item in lst:  # TODO: Speed up search
            if item[key] == value:
                my_item = item
                break
        else:
            # raise Exception(f"dict with '{key}: {value}' wasnt founded")
            return None

    # Not stable
    # @staticmethod
    # def get_dict_by_key_value(lst: list, key, value):
    #     next(
    #       item for item in lst if item[key] == value
    #     )

    @staticmethod
    def get_unique_list(lst: list):
        return [dict(t) for t in {tuple(d.items()) for d in lst}]

    @staticmethod
    def generate_tree(data: list, parent, parent_key):
        levels = {}

        for n in data:
            levels.setdefault(n.get(parent, None), []).append(n)

        def build_tree(parent_id=None):
            nodes = [dict(n) for n in levels.get(parent_id, [])]
            for n in nodes:
                children = build_tree(n[parent_key])
                if children:
                    n["children"] = children
            return nodes

        return build_tree()

    # Not stable
    #  @staticmethod
    # def generate_tree(data, parent, parent_key):
    # new_data = data.copy()

    # for i in range(len(new_data) - 1, -1, -1):
    #     data[i]["children"] = [
    #         child for child in new_data if child[parent] == new_data[i][parent_key]
    #     ]

    #     for child in new_data[i]["children"]:
    #         new_data.remove(child)

    # return new_data
