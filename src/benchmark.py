import csv
import random
import sys
import time

# Импортируем
from sorts import (
    bubble_sort,
    bucket_sort,
    built_in_sort,
    counting_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    selection_sort,
)

#Защита от глубокой рекурсии
sys.setrecursionlimit(2000000)


#Генераторы данных
def generate_random(n):
    return [random.randint(-10000, 10000) for _ in range(n)]


def generate_sorted(n):
    return list(range(n))


def generate_reversed(n):
    return list(range(n, 0, -1))


def generate_almost_sorted(n):
    mass = list(range(n))
    swaps_count = int(n * 0.05)
    for _ in range(swaps_count):
        idx1 = random.randint(0, n - 1)
        idx2 = random.randint(0, n - 1)
        mass[idx1], mass[idx2] = mass[idx2], mass[idx1]
    return mass


#Логика замеров замеров времени и памяти
def measure_sort(sort_func, data):
    data_copy = data.copy()

    start_time = time.perf_counter()
    res = sort_func(data_copy)
    end_time = time.perf_counter()

    target_data = res if res is not None else data_copy

    # Безопасный замер памяти для CPython / PyPy
    try:
        memory_bytes = sys.getsizeof(target_data)
    except TypeError:
        # Для PyPy рассчитываем базовый объем массива (8 байт на элемент)
        memory_bytes = len(target_data) * 8

    time_ms = (end_time - start_time) * 1000
    memory_kb = memory_bytes / 1024

    return round(time_ms, 4), round(memory_kb, 2)


#Запуск
def run_benchmark():
    sizes = [10, 500, 1000, 50000, 1000000]

    data_generators = {
        "Random": generate_random,
        "Sorted": generate_sorted,
        "Reversed": generate_reversed,
        "Almost Sorted": generate_almost_sorted,
    }

    algorithms = {
        "Bubble": bubble_sort,
        "Selection": selection_sort,
        "Insertion": insertion_sort,
        "Quick": quick_sort,
        "Merge": merge_sort,
        "Heap": heap_sort,
        "Counting": counting_sort,
        "Radix": radix_sort,
        "Bucket": bucket_sort,
        "Built-in": built_in_sort,
    }

    slow_algorithms = ["Bubble", "Selection", "Insertion"]
    results = []

    for n in sizes:
        print(f"--- Запуск замеров для N = {n} ---")
        for data_type, generator in data_generators.items():
            test_data = generator(n)

            for algo_name, sort_func in algorithms.items():
                if n >= 50000 and algo_name in slow_algorithms:
                    print(f"Пропуск {algo_name} для N={n} (таймаут O(N^2))")
                    continue

                try:
                    time_ms, memory_kb = measure_sort(sort_func, test_data)
                    results.append(
                        {
                            "N": n,
                            "Data_Type": data_type,
                            "Algorithm": algo_name,
                            "Time_ms": time_ms,
                            "Memory_KB": memory_kb,
                        }
                    )
                    print(
                        f"N={n} | {data_type} | {algo_name}: {time_ms} мс, {memory_kb} КБ"
                    )
                except Exception as e:
                    print(f"Ошибка при тестировании {algo_name} на N={n}: {e}")

    # Сохраняем в CSV
    output_filename = "results.csv"
    fieldnames = ["N", "Data_Type", "Algorithm", "Time_ms", "Memory_KB"]

    with open(output_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nУспешно")


if __name__ == "__main__":
    run_benchmark()