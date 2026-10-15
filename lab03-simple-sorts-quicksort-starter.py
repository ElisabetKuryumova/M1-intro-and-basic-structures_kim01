#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab03-simple-sorts-quicksort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import time
import matplotlib
matplotlib.use("Agg")  # сохранение в файл без графического окна
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list) -> tuple[list, int, int]:
    """Сортировка пузырьком. Ожидаемая сложность: TODO (обосновать в отчёте).

    Подсказка: досрочный выход, если за проход не было ни одного обмена, —
    именно он даёт лучший случай на упорядоченном входе.
    """
    # TODO: реализовать; считать сравнения и обмены
    arr = a.copy()                # копия, чтобы не менять оригинал
    comparisons = 0
    swaps = 0
    n = len(arr)
    
    for i in range(n):
        swapped = False           # флаг: был ли обмен за проход
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:           # если обменов не было — выходим
            break
    
    return arr, comparisons, swaps


def insertion_sort(a: list) -> tuple[list, int, int]:
    """Сортировка вставками. Ожидаемая сложность: TODO (лучший/худший случаи)."""
    # TODO: реализовать; считать сравнения и перемещения (сдвиги)
    arr = a.copy()
    comparisons = 0
    shifts = 0
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    
    return arr, comparisons, shifts


def selection_sort(a: list) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: TODO (почему не зависит от входа?)."""
    # TODO: реализовать; считать сравнения и обмены
    arr = a.copy()
    comparisons = 0
    swaps = 0
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    
    return arr, comparisons, swaps


# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.

    Ожидаемая сложность: в среднем TODO, в худшем случае TODO (обосновать
    в отчёте, объяснить роль рандомизации). rng передаётся снаружи, чтобы
    запуск был воспроизводим по seed варианта.
    """
    if rng is None:
        rng = random.Random()
    # TODO: реализовать (рекурсивно или циклом со стеком);
    # TODO: опорный элемент — a[rng.randrange(lo, hi)], не первый и не последний.
    arr = a.copy()
    
    def _quick_sort(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        # Выбираем случайный опорный элемент
        pivot_idx = rng.randrange(lo, hi)
        pivot = arr[pivot_idx]
        # Разбиение (partition)
        i, j = lo, hi - 1
        while i <= j:
            while arr[i] < pivot:
                i += 1
            while arr[j] > pivot:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        # Рекурсивно сортируем левую и правую части
        _quick_sort(lo, j + 1)
        _quick_sort(i, hi)
    
    _quick_sort(0, len(arr))
    return arr


# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны.

    План: взять массив пар (ключ, метка) с повторяющимися ключами, например
    [(2, "a"), (1, "b"), (2, "c"), (1, "d")], отсортировать каждой сортировкой
    по ключу (сравнение только по p[0]!) и напечатать порядок меток при равных
    ключах. Вывод о стабильности каждой сортировки включить в отчёт.
    """
    # TODO: подготовить пары, прогнать все четыре сортировки, напечатать итог
    data = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
    print("\nДемонстрация стабильности:")
    print(f"Исходный: {data}")
    
    # Пузырёк
    res, _, _ = bubble_sort(data)
    print(f"bubble_sort:    {res}")
    
    # Вставки
    res, _, _ = insertion_sort(data)
    print(f"insertion_sort: {res}")
    
    # Выбором
    res, _, _ = selection_sort(data)
    print(f"selection_sort: {res}")
    
    # QuickSort
    res = quick_sort(data)
    print(f"quick_sort:     {res}")
    
    print("\nВывод: bubble_sort и insertion_sort — стабильные,")
    print("selection_sort и quick_sort — нестабильные.")

# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------
def counters_demo() -> None:
    """Показать счётчики сравнений и обменов на маленьком массиве."""
    data = [5, 2, 4, 1]
    print("\nДемонстрация счётчиков на массиве:", data)
    
    res, cmp_, swp = bubble_sort(data)
    print(f"bubble_sort:    результат={res}, сравнений={cmp_}, обменов={swp}")
    
    res, cmp_, shf = insertion_sort(data)
    print(f"insertion_sort: результат={res}, сравнений={cmp_}, сдвигов={shf}")
    
    res, cmp_, swp = selection_sort(data)
    print(f"selection_sort: результат={res}, сравнений={cmp_}, обменов={swp}")

def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def self_check() -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for name, fn in ALGORITHMS.items():
        for a in boundary:
            res = fn(list(a))
            assert is_sorted(res), f"{name}: нарушен порядок на {a}"
            assert sorted(res) == sorted(a), f"{name}: не перестановка входа {a}"

    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        expected = sorted(a)
        for name, fn in ALGORITHMS.items():
            assert fn(list(a)) == expected, f"{name}: расходится с sorted() на {a}"

    # Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе.
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    assert comparisons == 10, "selection_sort: неверный счётчик сравнений"
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    """Замеры всех алгоритмов на трёх классах входов; результат — таблица в stdout."""
    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]
    results = {}  # {algorithm: {class: [(n, t), ...]}}
    for name, fn, sizes in plans:
        print(f"\n{name}:")
        results[name] = {"упорядоченный": [], "случайный": [], "обратный": []}
        for n in sizes:
            for cls, data in make_inputs(n, seed).items():
                t = bench(fn, data)
                print(f"  n={n:>7}  вход={cls:<13} t={t:.6f} c")
                results[name][cls].append((n, t))
    return results

def plot_results(results: dict, out_dir: str = ".") -> None:
    """Строит log-log графики для каждого алгоритма."""
    for name, classes in results.items():
        plt.figure(figsize=(8, 6))
        for cls, points in classes.items():
            ns = [p[0] for p in points]
            ts = [p[1] for p in points]
            plt.loglog(ns, ts, marker="o", label=cls)
        plt.xlabel("размер входа n")
        plt.ylabel("время, с")
        plt.title(f"{name}: log-log")
        plt.grid(True, which="both", linewidth=0.3)
        plt.legend()
        plt.tight_layout()
        filename = f"{name}_loglog.png"
        plt.savefig(filename, dpi=150)
        plt.close()
        print(f"График сохранён: {filename}")

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    counters_demo()
    results = run_benchmarks(seed)
    plot_results(results)


if __name__ == "__main__":
    main()
