import sys, random
from math import pow, log

# This solution only considers 2 inputs. Think of it
# as analogous to a piece of music having 2 instruments.
# It also always assumes the problem as a minimization problem.

lowerBounds = [-10, -10]
upperBounds = [10, 10]
improvisations = 1000
pitchAdjustingRate = 0.5
pitchAdjustingProportion = 0.5
worstFitnessIndex = 0
worstFitness = 0
HM_ConsideringRate = 0.75
HM_Size = 100
harmonyMemory = [[0, 0]] * HM_Size

def init():
    global worstFitnessIndex
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
        if initFitness > fitness(harmonyMemory[worstFitnessIndex]):
            worstFitnessIndex = i
            worstFitness = initFitness
            print("New worst fitness at index " + str(worstFitnessIndex) + ": " + str(initFitness))
        harmonyMemory[i] = newHarmony

def fitness(harmony):
    return log(1 + pow(1 - harmony[0], 2) + 100 * pow(harmony[1] - pow(harmony[0], 2), 2))

def consider(index):
    where = random.randint(0, HM_Size - 1)
    print("Harmony being considered at index " + str(where) + " of harmony memory")
    return harmonyMemory[where][index]

def find_best():
    # Used at the end of our harmony search to return the best fitness
    bestFitnessIndex = 0
    bestFitness = 100
    for i in range(len(harmonyMemory)):
        tempFitness = fitness(harmonyMemory[i])
        if tempFitness < bestFitness:
            bestFitness = tempFitness
            bestFitnessIndex = i
    # Returns the best fitness found in HM and its index in HM
    return [bestFitness, bestFitnessIndex]

def update_memory(harmony):
    # If our newly generated harmony has a better fitness than the
    # worst fitness in HM, we replace the corresponding harmony with the new one.
    global worstFitness
    global worstFitnessIndex
    newFitness = fitness(harmony)
    if newFitness < worstFitness:
        harmonyMemory[worstFitnessIndex] = harmony
        print("worstFitness being deleted...  being replaced by " + str(newFitness))
        worstFitness = 0
        for i in range(len(harmonyMemory)):
            # Iterate through HM to find the new worstFitness
            tempFitness = fitness(harmonyMemory[i])
            if tempFitness > worstFitness:
                worstFitness = tempFitness
                worstFitnessIndex = i
                # print("update_memory: " + str(worstFitness) + " is the newest worstFitness at index " + str(worstFitnessIndex))

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
        update_memory(harmony)
        num_imp += 1
        results = find_best()
        print("----------------------------------")
        print("Best Harmony: " + str(harmonyMemory[results[1]]))
        print("Best Fitness: " + str(results[0]))
    

if __name__ == "__main__":
    main()