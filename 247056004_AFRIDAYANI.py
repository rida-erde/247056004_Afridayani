import random

# Durasi Kegiatan Dalam Jam
durasi = {'A': 2, 'B': 3, 'C': 2, 'D': 4}
max_duration = 8  

# Fungsi Untuk Menghitung Fitness
def fitness(schedule):
    # Cek Apakah A Sebelum B
    if schedule.index('A') > schedule.index('B'):
        return 0

    # Cek Apakah C dan D Tidak Bersebelahan
    for i in range(len(schedule) - 1):
        if (schedule[i] == 'C' and schedule[i + 1] == 'D') or (schedule[i] == 'D' and schedule[i + 1] == 'C'):
            return 0

    # Hitung Total Durasi Dengan Aturan Penggabungan
    total_duration = 0
    # Buat Sebuah List Bernama Gabung adalah index angka genap < panjang index schedule
    gabung = [i for i in range(len(schedule)) if i % 2 == 0]

    # Menggabungkan total_duration dari index 1&2, 3&4
    for i in gabung:
        total_duration += max(durasi[schedule[i]], durasi[schedule[i+1]])

    # Cek Apakah Total Durasi Melebihi Batas
    if total_duration > max_duration:
        return 0

    return total_duration  # Semakin kecil total durasi, semakin baik

# Fungsi untuk Membuat Jadwal Acak
def random_schedule():
    return random.sample(list(durasi.keys()), len(durasi))

# Algoritma Genetika
population_size = 20
generations = 50
population = [random_schedule() for _ in range(population_size)]

for generation in range(generations):
    # Hitung Fitness Setiap Jadwal
    population = sorted(population, key=fitness, reverse=True)

    # Seleksi Jadwal Terbaik
    population = population[:10]

    # Buat Generasi Baru Dengan Crossover dan Mutasi
    new_population = []
    for _ in range(population_size):
        parent1, parent2 = random.sample(population, 2)
        cut = random.randint(1, len(durasi) - 1)
        child = parent1[:cut] + [x for x in parent2 if x not in parent1[:cut]]

        # Mutasi
        if random.random() < 0.1:
            i, j = random.sample(range(len(child)), 2)
            child[i], child[j] = child[j], child[i]

        new_population.append(child)

    population = new_population

# Jadwal Yang Memenuhi Semua Syarat:
population = sorted(population, key=fitness, reverse=True)

# Populations = Populasi Tapi Yang Unique Saja
populations = []
for schedule in population:
    if schedule not in populations:
        populations.append(schedule)

# Print Jadwal yang Memenuhi Semua Syarat
for schedule in populations:
    if fitness(schedule) >= 0:
      print("jadwal: ",schedule, end=" ")
      print("fitness: ",fitness(schedule))

# Solusi Terbaik
best_schedule = max(population, key=fitness)
print("Jadwal terbaik:", best_schedule)
print("Fitness:", fitness(best_schedule))
