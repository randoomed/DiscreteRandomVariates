from MVN.MVNTimingStrings import MVNTimingStrings as vTimingString
from tableMethod.tableMethodTimingStrings import tableMethodTimingStrings as tTimingString
from alliasMethod.alliasTimingStrings import alliasTimingStrings as aTimingString
from rejectionMethod.rejectionTimingStrings import rejectionTimingStrings as rTimingString
import timeit
import gc
import sys

#get all parameters, stripping the script name
inputs = sys.argv[1:]

if len(inputs) == 0:
    print "geef parameters mee: seed timeitHerhalingen algorithme aantalEvents minweight maxweight algorithmeParams"
#print timeit(TS.MVNGenerate(),TS.MVNSetup(),number=1000000)
else:
    #print inputs
    #get the random numbers from a seeded random number generator
    seed = inputs[0]
    #repeat experiment with multiple sets of random numbers
    timeitnumber = inputs[1]
    timeitRepeat = 1

    #repeat a number of times for each group of random numbers
    minWeight = inputs[4]
    maxWeight = inputs[5]
    nrEvents = inputs[3]
    algorithm = inputs[2]

    canRun = True;

    #select the correct timing strings
    if algorithm == 'tableGen' or algorithm == 'tableUpdate' or algorithm == 'tableBuild' or algorithm == 'tableExtGen' or algorithm == 'tableExtUpdate' or algorithm == 'tableExtBuild':
        TS = tTimingString()
    elif algorithm == 'aliasGen' or algorithm == 'aliasBuild' or algorithm == 'aliasEnhGen' or algorithm == 'aliasEnhUpdate' or algorithm == 'aliasEnhBuild' or algorithm == 'aliasEnhDegrade':
        TS = aTimingString()
    elif algorithm == 'rejectionGen' or algorithm == 'rejectionUpdate' or algorithm == 'rejectionBuild':
        TS = rTimingString()
    else:
        TS = vTimingString()

    #MVN tollerance parameters
    if algorithm == 'MVNToleranceGen' or algorithm == 'MVNToleranceUpdate':
        tollerance = inputs[6]
        c = inputs[7]

    if algorithm == 'tableGen' or algorithm == 'tableUpdate' or algorithm == 'tableBuild':
        base = inputs[6]

    if algorithm == 'tableExtGen' or algorithm == 'tableExtUpdate' or algorithm == 'tableExtBuild':
        base = inputs[6]
        spaceMultiplier = inputs[7]

    if algorithm == 'aliasEnhGen' or algorithm == 'aliasEnhUpdate' or algorithm == 'aliasEnhBuild':
        rebuildFactor = inputs[6]

    if algorithm == 'aliasEnhDegrade':
        updates = inputs[6]

    #MVN timing
    if algorithm == 'MVNGen':
        T = timeit.Timer(TS.MVNGenerate(),TS.MVNSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))
    elif algorithm == 'MVNUpdate':
        T = timeit.Timer(TS.MVNUpdate(nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight), TS.MVNSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))
    elif algorithm == 'MVNBuild':
        T = timeit.Timer(TS.MVNBuild(),TS.MVNBuildSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))

    #MVN with tolerance
    elif algorithm == 'MVNToleranceGen':
        T = timeit.Timer(TS.MVNGenerate(),TS.MVNTolleranceSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, tolerance = tollerance, c = c))
    elif algorithm == 'MVNToleranceUpdate':
        T = timeit.Timer(TS.MVNUpdate(nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight), TS.MVNTolleranceSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, tolerance = tollerance, c = c))
    elif algorithm == 'MVNToleranceBuild':
        T = timeit.Timer(TS.MVNTolleranceBuild(),TS.MVNTolleranceBuildSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))

    #table method timings
    elif algorithm == 'tableGen':
        T = timeit.Timer(TS.tableGenerate(),TS.tableSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, base = base))
    elif algorithm == 'tableUpdate':
        T = timeit.Timer(TS.tableUpdate(nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight),TS.tableSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, base = base))
    elif algorithm == 'tableBuild':
        T = timeit.Timer(TS.tableBuild(base = base),TS.tableBuildSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))

    #table method extended timings
    elif algorithm == 'tableExtGen':
        T = timeit.Timer(TS.tableGenerate(),TS.tableExtSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, base = base, spaceMultiplier = spaceMultiplier))
    elif algorithm == 'tableExtUpdate':
        T = timeit.Timer(TS.tableUpdate(nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight),TS.tableExtSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, base = base, spaceMultiplier = spaceMultiplier))
    elif algorithm == 'tableExtBuild':
        T = timeit.Timer(TS.tableExtBuild(base = base, spaceMultiplier = spaceMultiplier),TS.tableExtBuildSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))

    #rejection method timings
    elif algorithm == 'rejectionGen':
        T = timeit.Timer(TS.rejectionGenerate(),TS.rejectionSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))
    elif algorithm == 'rejectionUpdate':
        T = timeit.Timer(TS.rejectionUpdate(nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight),TS.rejectionSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))
    elif algorithm == 'rejectionBuild':
        T = timeit.Timer(TS.rejectionBuild(),TS.rejectionBuildSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))

    #allias method
    elif algorithm == 'aliasGen':
        T = timeit.Timer(TS.aliasGenerate(),TS.aliasSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))
    elif algorithm == 'aliasBuild':
        T = timeit.Timer(TS.aliasBuild(),TS.aliasBuildSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))

    #allias method
    elif algorithm == 'aliasEnhGen':
        T = timeit.Timer(TS.aliasGenerate(),TS.aliasEnhSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, rebuildFactor = rebuildFactor))
    elif algorithm == 'aliasEnhUpdate':
        T = timeit.Timer(TS.aliasEnhUpdate(nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight),TS.aliasEnhSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, rebuildFactor = rebuildFactor))
    elif algorithm == 'aliasEnhBuild':
        T = timeit.Timer(TS.aliasEnhBuild(rebuildFactor = rebuildFactor),TS.aliasEnhBuildSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight))
    elif algorithm == 'aliasEnhDegrade':
        T = timeit.Timer(TS.aliasGenerate(),TS.aliasEnhDegradeSetup(seed = seed, nrEvents = nrEvents, minWeight = minWeight, maxWeight = maxWeight, updates = updates))

    else:
        print "beschikbare algorithmes: MVNGen, MVNUpdate, MVNToleranceGen, MVNToleranceUpdate"
        canRun = False;

    if canRun:
        sys.stdout.write("%s\t"%(T.timeit(number=int(timeitnumber))))
        sys.stdout.flush()
