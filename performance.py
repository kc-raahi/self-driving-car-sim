import time

performance_map = {}
temp_map = {}


def start(id):
    temp_map[id] = time.time()

def stop(id):
    v = time.time() - temp_map[id]
    if id in performance_map:
        performance_map[id] += v
    else:
        performance_map[id] = v


def sort_dict_by_value(d):
    x = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
    return x


def dump():
    print("dump")
    for item in sort_dict_by_value(performance_map).items():
        print(item[0], "=", item[1])


if __name__ == "__main__":
    x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    x = sort_dict_by_value(x)
    print(x)