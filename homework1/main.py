import datetime
import threading
import time

from src.Publication import Publication
from src.Subscription import Subscription
from src.config import number_of_threads, number_of_pubs, number_of_subs
from src.pub_generator import generate_pub
from src.sub_generator import generate_subs
from src.utils import cleanup_output_files, acquire_file_lock, release_file_lock


def thread_main(thread_name: str, number_of_pubs: int, number_of_subs: int):
    """
    Functia "main" pentru un thread: genereaza numarul de publicatii si subscriptii specificate si le scrie intr-un
    fisier output.

    :param thread_name: Numele thread-ului care ruleaza functia.
    :param number_of_pubs: Numarul de publicatii pe care thread-ul le va genera.
    :param number_of_subs: Numarul de subscriptii pe care thread-ul le va genera.
    """

    print(f"{thread_name} started!")

    pubs: [Publication] = [generate_pub() for i in range(0, number_of_pubs)]
    subs: [Subscription] = generate_subs(number_of_subs)

    acquire_file_lock("publicatii.txt")
    with open("publicatii.txt", "a", newline='') as f:
        for pub in pubs:
            f.write(pub.to_row())
            f.write('\n')
    release_file_lock("publicatii.txt")

    acquire_file_lock("subscriptii.txt")
    with open("subscriptii.txt", "a") as f:
        for sub in subs:
            f.write(sub.to_row())
            f.write('\n')
    release_file_lock("subscriptii.txt")


# Curat workspace-ul: golesc fisierele output
cleanup_output_files()

# Calculez numarul de publicatii care vor fi generate de catre fiecare thread
number_of_pubs_each_thread_to_generate = round(number_of_pubs / number_of_threads)
number_of_pubs_thread_parameters = [number_of_pubs_each_thread_to_generate] * number_of_threads

if sum(number_of_pubs_thread_parameters) != number_of_pubs:
    # Daca number_of_pubs / number_of_threads da un numar cu perioada, ajustez parametrul ultimului thread
    number_of_pubs_thread_parameters[-1] = number_of_pubs - sum(number_of_pubs_thread_parameters[:-1])

# Calculez numarul de subscriptii care vor fi generate de catre fiecare thread
number_of_subs_each_thread_to_generate = round(number_of_subs / number_of_threads)
number_of_subs_thread_parameters = [number_of_subs_each_thread_to_generate] * number_of_threads

if sum(number_of_subs_thread_parameters) != number_of_subs:
    # Daca number_of_subs / number_of_threads da un numar cu perioada, ajustez parametrul ultimului thread
    number_of_subs_thread_parameters[-1] = number_of_subs - sum(number_of_subs_thread_parameters[:-1])

# Pornesc thread-urile
start_time = datetime.datetime.now()

threads = []
for i in range(0, number_of_threads):
    name = f"Thread {i+1}"

    t = threading.Thread(
        name=name, target=thread_main,
        args=(name, number_of_pubs_thread_parameters[i], number_of_subs_thread_parameters[i])
    )
    t.start()

    threads.append(t)

while any(t.is_alive() for t in threads):
    time.sleep(0.2)

stop_time = datetime.datetime.now()

print(f"Duration: {stop_time.timestamp() - start_time.timestamp()}")
