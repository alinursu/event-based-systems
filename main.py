from src.Publication import Publication
from src.Subscription import Subscription
from src.config import number_of_pubs
from src.pub_generator import generate_pub
from src.sub_generator import generate_subs

pubs: [Publication] = [generate_pub() for i in range(0, number_of_pubs)]
subs: [Subscription] = generate_subs()

with open("publicatii.txt", "w", newline='') as f:
    for pub in pubs:
        f.write(pub.to_row())
        f.write('\n')

with open("subscriptii.txt", "w") as f:
    for sub in subs:
        f.write(sub.to_row())
        f.write('\n')
