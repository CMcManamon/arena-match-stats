import collections

import pandas as pd
data = pd.read_csv('5v5.csv', index_col=False)
# List of desired columns
enemyClasses = ['enemyPlayerClass1', 'enemyPlayerClass2', 'enemyPlayerClass3', 'enemyPlayerClass4', 'enemyPlayerClass5']

# Remove rows where any data is missing
filteredData = data[data['diffRating'].notnull()]
for eClass in enemyClasses:
    filteredData = filteredData[data[eClass].notnull()]

# Filter for desired headers
filteredData = filteredData.filter(items=enemyClasses + ['diffRating'])

# Fill dict with key = team comp and value = win/loss/%
teamComps = {}
for ind in filteredData.index:
    comp = []
    for eClass in enemyClasses:
        comp.append(filteredData[eClass][ind])

    comp.sort()
    comp = tuple(comp)
    if comp in teamComps:
        thisData = teamComps[comp]
        thisData[0] = thisData[0] + 1 if filteredData['diffRating'][ind] > 0 else thisData[0]
        thisData[1] = thisData[1] + 1 if filteredData['diffRating'][ind] <= 0 else thisData[1]
        thisData[2] = round(100 * thisData[0] / (thisData[0] + thisData[1]))
    else:
        win = 1 if filteredData['diffRating'][ind] > 0 else 0
        loss = 0 if win == 1 else 1
        percent = round(100 * win / (win + loss))
        teamComps[comp] = [win, loss, percent]

totalWin = 0
totalLoss = 0
print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<6} {:<6} {:<6}".format('Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Win', 'Loss', '%'))
for key, value in sorted(   teamComps.items(),
                            key=lambda item: item[1][2],
                            reverse=True):
    tComp = list(key)
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<6} {:<6} {:<6}".format(tComp[0], tComp[1], tComp[2], tComp[3], tComp[4], value[0], value[1], value[2]))
    totalWin += value[0]
    totalLoss += value[1]

print("Games Played: ", (totalWin + totalLoss), "\tWin: ", totalWin, "\tLoss: ", totalLoss, "\t%", round(100 * totalWin / (totalWin + totalLoss)))