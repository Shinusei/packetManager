import requests
import sys


def get_list(pack):
    packs = set()
    requests.head("https://pypi.org/pypi/", timeout=1)
    url = "https://pypi.org/pypi/" + pack + "/json"
    json = requests.get(url).json()
    if "message" in json:
        return
    else:
        list_of_deps = json['info']['requires_dist']
        if list_of_deps:
            for i in range(len(list_of_deps)):
                list_of_deps[i] = list_of_deps[i].split(";")[0]

            list_of_deps = set(list_of_deps)
            list_of_deps = list(list_of_deps)
            for i in range(len(list_of_deps)):
                package_name = list_of_deps[i]
                if package_name.find(">") != -1:
                    package_name = package_name[:package_name.find(">"):]
                if package_name.find("<") != -1:
                    package_name = package_name[:package_name.find("<"):]
                if package_name.find("^") != -1:
                    package_name = package_name[:package_name.find("^"):]
                if package_name.find("`") != -1:
                    package_name = package_name[:package_name.find("~"):]
                if package_name.find(" ") != -1:
                    package_name = package_name[:package_name.find(" "):]
                if package_name.find("=") != -1:
                    package_name = package_name[:package_name.find("="):]
                if package_name.find("[") != -1:
                    package_name = package_name[:package_name.find("["):]
                if (package_name != pack and package_name != sys.argv[1]):
                    packs.add(package_name)
            packs = list(packs)
            for i in range(len(packs)):
                packs[i] = (packs[i], 1, pack)
            return packs


def print_list(T, number):
    queue = T
    while queue:
        V = queue.pop(0)
        print('   "' + str(V[2]) + '"->"' + V[0] + '"')
        if V[1] < number:
            temp = get_list(V[0])
            if temp:
                for i in range(len(temp)):
                    temp[i] = (temp[i][0], V[1] + 1, temp[i][2])
                for i in temp:
                    queue.insert(0, i)


if __name__ == "__main__" and len(sys.argv) > 1:
    if (len(sys.argv) > 2):
        pack = sys.argv[1]
        requests.head("https://pypi.org/pypi/", timeout=1)
        url = "https://pypi.org/pypi/" + pack + "/json"
        json = requests.get(url).json()
        if "message" in json:
            print("Package not found")
        else:
            print("digraph G {")
            print_list(get_list(sys.argv[1]), int(sys.argv[2]))
            print("}")
    else:
        print("Write deep number")
else:
    print("Write package name")