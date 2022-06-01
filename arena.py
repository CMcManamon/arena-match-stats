import pandas as pd
# File
csvFileName = 'arena20220314.csv'
# Filters
players = ('Fadeleafz', 'Kaooz')
teamSize = len(players)

data = pd.read_csv(csvFileName, index_col=False)
# List of desired columns
headers = ['teamPlayerName1', 'teamPlayerName2', 'diffRating', 'enemyPlayerClass1', 'enemyPlayerClass2']

# For 2v2 remove rows where player 3 exists
if teamSize == 2:
    filteredData = data[data['teamPlayerClass3'].isnull()]
# For 3v3, remove rows where player 4 exists
elif teamSize == 3:
    filteredData = data[data['teamPlayerClass4'].isnull()]
    headers.append(['teamPlayerName3', 'enemyPlayerClass3'])
elif teamSize == 5:
    headers.append(['teamPlayerName3', 'enemyPlayerClass3',
                    'teamPlayerName4', 'enemyPlayerClass4',
                    'teamPlayerName5', 'enemyPlayerClass5'])

# Remove rows where any data is missing
for header in headers:
    filteredData = filteredData[data[header].notnull()]

# Filter for games matching the players
filteredData = filteredData[(filteredData['teamPlayerName1'].isin(players))
                            & (filteredData['teamPlayerName2'].isin(players))]
if teamSize == 3:
    filteredData = filteredData[filteredData['teamPlayerName3'].isin(players)]
if teamSize == 5:
    filteredData = filteredData[filteredData['teamPlayerName4'].isin(players)]
    filteredData = filteredData[filteredData['teamPlayerName5'].isin(players)]

# Filter for desired headers
filteredData = filteredData.filter(headers)


# Fill dict with key = team comp and value = win/loss/%
teamComps = { }
for ind in filteredData.index:
    comp = []
    for i in range(1, teamSize + 1):
        comp.append(filteredData['enemyPlayerClass' + str(i)][ind])
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

for key, value in sorted(teamComps.items(),
                         key=lambda item: item[1][2],
                         reverse=True):
    tComp = list(key)
    print("{:<10} {:<10} {:<6} {:<6} {:<6}".format(tComp[0], tComp[1], value[0], value[1], value[2]))
    totalWin += value[0]
    totalLoss += value[1]

print("Games Played: ", (totalWin + totalLoss), "\tWin: ", totalWin, "\tLoss: ", totalLoss, "\t%", round(100 * totalWin / (totalWin + totalLoss)))