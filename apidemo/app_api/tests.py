from django.test import TestCase

# Create your tests here.
weapons = ["Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"]
results = [w for w in weapons if "k" in w.lower()]
print(results)