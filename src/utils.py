import os.path
import time


def cleanup_output_files():
    """
    Sterge fisierele output din folder-ul curent
    """

    if os.path.exists(os.path.join(os.getcwd(), "publicatii.txt")):
        open(os.path.join(os.getcwd(), "publicatii.txt"), 'w').close()

    if os.path.exists(os.path.join(os.getcwd(), "subscriptii.txt")):
        open(os.path.join(os.getcwd(), "subscriptii.txt"), 'w').close()


def acquire_file_lock(file: str):
    """
    Obtine lock-ul unui fisier de pe disc prin crearea unui alt fisier, cu acelasi nume, avand extensia ".lock". Daca
    fisierul este deja blocat de catre un alt thread (adica daca exista deja fisierul ".lock" pentru resursa comuna),
    atunci va astepta pana cand lock-ul va fi sters.

    :param file: Fisierul pentru care se va obtine lock-ul.
    """

    print(f"Acquiring lock for {file}")

    lock_file_path = os.path.join(os.getcwd(), f"{file}.lock")

    while os.path.exists(lock_file_path):
        time.sleep(0.5)

    open(lock_file_path, 'w').close()

    print(f"Lock acquired for {file}")


def release_file_lock(file: str):
    """
    Elibereaza lock-ul pentru un fisier prin stergerea fisierului cu extensia ".lock".

    :param file: Fisierul pentru care va elibera lock-ul.
    """

    lock_file_path = os.path.join(os.getcwd(), f"{file}.lock")

    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)

        print(f"Lock released for {file}")


def copy_dict(to_copy: dict) -> dict:
    """
    Creeaza un deep copy pentru un dictionar.

    :param to_copy: Dictionarul care va fi copiat.
    :return: Copia dictionarului.
    """

    obj = {}

    for key, value in to_copy.items():
        obj[key] = value

    return obj
