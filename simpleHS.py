import sys, random
from math import pow, log

# This solution only considers 2 inputs. Think of it
# as analogous to a piece of music having 2 instruments.
# It also always assumes the problem as a minimization problem.

lowerBounds = [-10, -10]
upperBounds = [10, 10]
improvisations = 100
pitchAdjustingRate = 0.5
pitchAdjustingProportion = 0.5
worstFitness = 0
HM_ConsideringRate = 0.75
HM_Size = 100
harmonyMemory = [None] * HM_Size

def init():
    global worstFitness
    # Initialise Harmony Memory with random values
    for i in range(len(harmonyMemory)):
        newHarmony = [
            (random.uniform(lowerBounds[0],upperBounds[0])),
            (random.uniform(lowerBounds[1],upperBounds[1]))]
        print(str(i) + "  |  " + str(newHarmony))
        initFitness = fitness(newHarmony)
        # Keep track of the worst fitness during initialisation
        # We will use this when we update Harmony Memory with better results
        # TODO: Track the index (where the worst fitness is) rather than the value
        if initFitness > worstFitness:
            worstFitness = initFitness
            print("New worst fitness: " + str(worstFitness))
        harmonyMemory[i] = newHarmony

def fitness(harmony):
    return log(1 + pow(1 - harmony[0], 2) + 100 * pow(harmony[1] - pow(harmony[0], 2), 2))

def consider(index):
    where = random.randint(0, HM_Size - 1)
    print("Harmony being considered at " + str(where))
    return harmonyMemory[where][index]

def main():
    global improvisations
    num_imp = 0
    init()
    while(num_imp < improvisations):
        harmony = [0, 0]
        print("Main: New harmony generated")
        for i in range(len(harmony)):
            # Iterate through both notes of this harmony (2)
            if random.random() < HM_ConsideringRate:
                # Consider Harmony Memory: a note is selected from this index randomly
                newNote = consider(i)
                harmony[i] = newNote
                print(str(newNote) + ": Newly considered note at index " + str(i))
                if random.random() < pitchAdjustingRate:
                    # Pitch adjustment at the current index
                    newPitch = pitchAdjustingProportion * (random.choice([-1, 1]))
                    harmony[i] += newPitch
                    print("Note has been pitch adjusted, current note is " + str(harmony[i]))
                    print("^^^ Note adjusted by " + str(newPitch))
            else:
                # Generate new note randomly based on bounds
                randomNote = random.uniform(lowerBounds[0],upperBounds[0])
                harmony[i] = randomNote
                print("New note generated at index " + str(i) + ": " + str(randomNote))

        # Increment num_imp. The loop ends once this reaches the value of "improvisations".
        # TODO: Evaluate the fitness of the harmony after every iteration
        # TODO: Adjust Harmony Memory according to the evaluated fitness
        num_imp += 1

if __name__ == "__main__":
    main()