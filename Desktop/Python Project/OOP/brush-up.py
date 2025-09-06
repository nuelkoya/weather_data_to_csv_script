
class Shelter:
    shelterPetHistory = []
    petsInShelter = []
    @classmethod
    def registerPet(cls, pet):
        if pet in cls.shelterPetHistory:
            print("Pet already registered")
        else:
            cls.petsInShelter.append(pet)
            cls.shelterPetHistory.append(pet)
            print(f"{pet.name} has been registered to the shelter.")

    @classmethod
    def acceptReturnedPet(cls, pet):
        if (pet in cls.petsInShelter):
            print("Pet already returned")
        else:
            pet.isAdopted = False
            pet.adoptedBy = None
            cls.petsInShelter.append(pet)
            print(f"Accepting your pet {pet.name} back")
    
    @classmethod 
    def adoptPet(cls, pet, adoptee):
        pet.isAdopted = True
        pet.adoptedBy = adoptee

        try:
            indexOfPet = cls.petsInShelter.index(pet)
            cls.petsInShelter.pop(indexOfPet)
            print(f"Congratulation {adoptee}, here is your pet {pet.name}")
        except ValueError:
            print(f"Error: {pet.name} is not currently in the shelter list")
        cls.availablePetsInShelter()

    @classmethod
    def availablePetsInShelter(cls):
        for pet in cls.petsInShelter:
             if not pet.isAdopted:
                print(pet.name)

class Pet:
    allPets = []

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
        self.isAdopted = False
        self.adoptedBy = None
        Pet.allPets.append(self)
    
    def speak(self):
        print("I'm a pet")


    @classmethod
    def available_pets(cls):
        print([f"Name: {pet.name} / Age:{pet.age}" for pet in cls.allPets])

    
    def __str__(self):
        return f"This is a {self.species}, named {self.name} and is {self.age} years old."



class Dog(Pet):

    def __init__(self, name, age):
        super().__init__(name, "Dog", age)
    
    def speak(self):
        super().speak()
        print(f"woof! My name is {self.name}")

class Cat(Pet):

    def __init__(self, name, age):
        super().__init__(name, "Cat", age)
    
    def speak(self):
        super().speak()
        print(f"Meow! My name is {self.name}")


class Person:

    def __init__(self, name):
        self.name = name
    
    def adoptPet(self, petName):
        for pet in Shelter.shelterPetHistory:
            if pet.name == petName and pet.isAdopted == False:
                Shelter.adoptPet(pet, self.name)
                break
            elif pet.name == petName and pet.isAdopted == True:
                print("This pet has been adopted")
                break
        else:
            print('This pet is not in our shelter')

    def returnPet(self, petName):
        for pet in Shelter.shelterPetHistory:
            if pet.name == petName and pet.isAdopted:
                Shelter.acceptReturnedPet(pet)
                break
        else:
            print('pet is not from our shelter')



    





import unittest
from io import StringIO
import sys

# Assuming your classes Shelter, Pet, Dog, Cat, Person are defined above or imported

class TestPetShelter(unittest.TestCase):

    def setUp(self):
        # Reset shelter lists before each test to avoid cross-test contamination
        Shelter.shelterPetHistory.clear()
        Shelter.petsInShelter.clear()
        Pet.allPets.clear()
        # Create some pets for testing
        self.dog = Dog("Buddy", 3)
        self.cat = Cat("Whiskers", 2)

    def test_register_pet(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        Shelter.registerPet(self.dog)
        Shelter.registerPet(self.dog)  # Duplicate register

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Buddy has been registered to the shelter.", output)
        self.assertIn("Pet already registered", output)

    def test_adopt_pet(self):
        Shelter.registerPet(self.dog)
        person = Person("Alice")

        captured_output = StringIO()
        sys.stdout = captured_output

        person.adoptPet("Buddy")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Congratulation Alice, here is your pet Buddy", output)

    def test_adopt_pet_already_adopted(self):
        Shelter.registerPet(self.dog)
        person1 = Person("Alice")
        person2 = Person("Bob")

        person1.adoptPet("Buddy")

        captured_output = StringIO()
        sys.stdout = captured_output

        person2.adoptPet("Buddy")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("This pet has been adopted", output)

    def test_return_pet(self):
        Shelter.registerPet(self.dog)
        person = Person("Alice")
        person.adoptPet("Buddy")

        captured_output = StringIO()
        sys.stdout = captured_output

        person.returnPet("Buddy")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Accepting your pet Buddy back", output)

    def test_return_pet_not_adopted(self):
        Shelter.registerPet(self.dog)
        person = Person("Alice")

        captured_output = StringIO()
        sys.stdout = captured_output

        person.returnPet("Buddy")  # Buddy not adopted yet

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("pet is not from our shelter", output)

    def test_adopt_pet_not_in_shelter(self):
        person = Person("Alice")

        captured_output = StringIO()
        sys.stdout = captured_output

        person.adoptPet("Ghost")  # Pet not registered

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("This pet is not in our shelter", output)

if __name__ == "__main__":
    unittest.main()
