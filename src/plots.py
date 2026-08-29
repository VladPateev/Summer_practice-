import matplotlib.pyplot as plt
import pandas as pd


df_cpython = pd.read_csv("results_CPython.csv")
df_pypy = pd.read_csv("results_Pypy.csv")

algorithms = df_cpython["Algorithm"].unique()
data_types = df_cpython["Data_Type"].unique()



def plot_interpreter_results(df, name):
    for d_type in data_types:
        plt.figure(figsize=(9, 5))

        for algo in algorithms:
            sub = df[(df["Data_Type"] == d_type) & (df["Algorithm"] == algo)]
            if not sub.empty:
                plt.plot(sub["N"], sub["Time_ms"], marker="o", label=algo)

        plt.xscale("log")
        plt.yscale("log")
        plt.title(f"Время работы ({name}) — {d_type}")
        plt.xlabel("Размер массива (N)")
        plt.ylabel("Время (мс)")
        plt.grid(True)
        plt.legend()

        plt.savefig(f"plot_time_{name}_{d_type}.png")
        plt.show()



plot_interpreter_results(df_cpython, "CPython")
plot_interpreter_results(df_pypy, "PyPy")

#Сравнение CPython vs PyPy на N = 1 000 000 (Random)
max_n = 1000000
cp_max = df_cpython[
    (df_cpython["N"] == max_n) & (df_cpython["Data_Type"] == "Random")
]
pypy_max = df_pypy[(df_pypy["N"] == max_n) & (df_pypy["Data_Type"] == "Random")]

if not cp_max.empty and not pypy_max.empty:
    merged = pd.merge(
        cp_max, pypy_max, on="Algorithm", suffixes=("_CPython", "_PyPy")
    )

    plt.figure(figsize=(10, 5))
    x = range(len(merged["Algorithm"]))
    width = 0.35

    plt.bar(
        [i - width / 2 for i in x],
        merged["Time_ms_CPython"],
        width,
        label="CPython",
    )
    plt.bar(
        [i + width / 2 for i in x], merged["Time_ms_PyPy"], width, label="PyPy"
    )

    plt.xticks(x, merged["Algorithm"])
    plt.title(f"Сравнение CPython vs PyPy на N = {max_n} (Random)")
    plt.xlabel("Алгоритм")
    plt.ylabel("Время (мс)")
    plt.grid(True, axis="y")
    plt.legend()

    plt.savefig("plot_compare_cpython_vs_pypy.png")
    plt.show()

print("Все графики построены")