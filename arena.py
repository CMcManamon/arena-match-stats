import pandas as pd
data = pd.read_csv('arena20220314.csv', index_col=False)
# List of desired columns
headers = ['teamPlayerName1', 'teamPlayerName2', 'diffRating', 'enemyPlayerClass1', 'enemyPlayerClass2']

# For 2v2 remove rows where player 3 exists
filteredData = data[data['teamPlayerClass3'].isnull()]
# Remove rows where any data is missing
for header in headers:
    filteredData = filteredData[data[header].notnull()]

# Filter for desired headers
filteredData = filteredData.filter(headers)

# Fill dict with key = team comp and value = win/loss/%
teamComps = { }
for ind in filteredData.index:
    comp = (filteredData['enemyPlayerClass1'][ind], filteredData['enemyPlayerClass2'][ind])
    if comp in teamComps:
        thisData = teamComps[comp]
        thisData[0] = thisData[0] + 1 if filteredData['diffRating'][ind] > 0 else thisData[0]
        thisData[1] = thisData[1] + 1 if filteredData['diffRating'][ind] <= 0 else thisData[1]
        thisData[2] = round(100 * thisData[0] / (thisData[0] + thisData[1]))
    elif (comp[1], comp[0]) in teamComps:
        thisData = teamComps[(comp[1], comp[0])]
        thisData[0] = thisData[0] + 1 if filteredData['diffRating'][ind] > 0 else thisData[0]
        thisData[1] = thisData[1] + 1 if filteredData['diffRating'][ind] <= 0 else thisData[1]
        thisData[2] = round(100 * thisData[0] / (thisData[0] + thisData[1]))
    else:
        win = 1 if filteredData['diffRating'][ind] > 0 else 0
        loss = 0 if win == 1 else 1
        percent = round(100 * win / (win + loss))
        teamComps[comp] = [win, loss, percent]

print("{:<10} {:<10} {:<6} {:<6} {:<6}".format('Class1', 'Class2', 'Win', 'Loss', '%'))
for key, value in sorted(   teamComps.items(),
                            key=lambda item: item[1][2],
                            reverse=True):
    tComp = list(key)
#    print(tComp[0], tComp[1], '\t', value[0], '\t\t', value[1], '\t\t', value[2])
    print("{:<10} {:<10} {:<6} {:<6} {:<6}".format(tComp[0], tComp[1], value[0], value[1], value[2]))
