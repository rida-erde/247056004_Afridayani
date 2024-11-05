import random

# Durasi kegiatan dalam jam
durations = {'A': 2, 'B': 3, 'C': 2, 'D': 4}
max_duration = 8

# Fungsi untuk menginisialisasi individu (jadwal acak)
def create_individual():
    return [random.randint(0, max_duration - 1) for _ in range(4)]

# Fungsi untuk membuat populasi awal
def create_population(size):
    return [create_individual() for _ in range(size)]

# Fungsi untuk menghitung fitness dari individu (jadwal)
def evaluate(individual):
    start_times = {'A': individual[0], 'B': individual[1], 'C': individual[2], 'D': individual[3]}
    end_times = {act: start + durations[act] for act, start in start_times.items()}

    # Syarat 1: A harus sebelum B
    if not (start_times['A'] + durations['A'] <= start_times['B']):
        return float('inf')  # Penalti besar jika A tidak sebelum B

    # Syarat 2: C dan D tidak boleh terjadi bersamaan
    if not (end_times['C'] <= start_times['D'] or end_times['D'] <= start_times['C']):
        return float('inf')  # Penalti besar jika C dan D tumpang tindih

    # Syarat 3: Total durasi tidak boleh lebih dari 8 jam
    if max(end_times.values()) > max_duration:
        return float('inf')  # Penalti besar jika total durasi melebihi 8 jam

    # Jika semua syarat terpenuhi, fitness adalah total waktu yang digunakan
    return max(end_times.values())

# Fungsi untuk melakukan crossover (persilangan) dua individu
def crossover(ind1, ind2):
    point = random.randint(1, len(ind1) - 1)
    child1 = ind1[:point] + ind2[point:]
    child2 = ind2[:point] + ind1[point:]
    return child1, child2

# Fungsi untuk melakukan mutasi pada individu
def mutate(individual, mutation_rate=0.1):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, max_duration - 1)

# Fungsi untuk memilih individu terbaik dalam populasi (seleksi turnamen)
def tournament_selection(population, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: evaluate(ind))
    return selected[0]

# Fungsi utama Algoritma Genetika
def genetic_algorithm(pop_size=100, generations=50, mutation_rate=0.1):
    population = create_population(pop_size)
    best_individual = None
    best_fitness = float('inf')

    for generation in range(generations):
        new_population = []

        # Membuat generasi baru
        for _ in range(pop_size // 2):
            # Seleksi orang tua
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            # Crossover
            child1, child2 = crossover(parent1, parent2)

            # Mutasi
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)

            # Menambahkan anak ke generasi baru
            new_population.extend([child1, child2])

        # Menggantikan populasi lama dengan generasi baru
        population = new_population

        # Memperbarui individu terbaik
        for individual in population:
            fitness = evaluate(individual)
            if fitness < best_fitness:
                best_fitness = fitness
                best_individual = individual

    return best_individual, best_fitness

# Menjalankan algoritma genetika dan menampilkan solusi terbaik
best_schedule, best_fitness = genetic_algorithm()

# Mencetak hasil terbaik
print("Best schedule:", best_schedule)
print("Fitness:", best_fitness)

# Waktu mulai dan akhir dari setiap kegiatan
start_times = {'A': best_schedule[0], 'B': best_schedule[1], 'C': best_schedule[2], 'D': best_schedule[3]}
end_times = {act: start + durations[act] for act, start in start_times.items()}
print("Start times:", start_times)
print("End times:", end_times)
