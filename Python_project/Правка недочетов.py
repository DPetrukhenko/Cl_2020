import pickle


def open_file(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def write_file(file_name, data):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


# грузим файлы
prtf = open_file('prtf.pickle')
prts = open_file('prtf_short.pickle')
adj_full = open_file('ADJ_full.pickle')
adj_short = open_file('ADJ_short.pickle')
adj_cmp = open_file('adj_cmp.pickle')
adj_sup = open_file('adj_sup.pickle')

#  проверка на ляпы (из-за метода replace)
for sent in adj_short:
    answer = adj_short[sent][1]
    if answer.count(answer[:3]) >= 2:
        print(sent, '\n', adj_short[sent])


# правим причастия
prtf['Краевая дислокация представляет собой локализованное искажение атомной плоскости за счет введения в нее дополнительной атомной полуплоскости – экстраплоскости, расположенной перпендикулярно плоскости чертежа.'] = ['локализованноерасположенной', 'Краевая дислокация представляет собой (локализовать) искажение атомной плоскости за счет введения в нее дополнительной атомной полуплоскости – экстраплоскости, (расположить) перпендикулярно плоскости чертежа.']
prtf.pop('Таким образом, и винтовая, и краевая дислокации – это границы между сдвинутой и несдвинутой частями кристалла, причем краевая дислокация перпендикулярна вектору сдвига, а винтовая – параллельна ему.')
prtf.pop('Рыбы всегда спокойны и безразличны к окружающему.')
prtf.pop('Современные психологи считают, что для этого достаточно знать любимый цвет этого человека.')

# краткие причастия
prts['Но знай, внимающий этим камням, никто не забыт и ничто не забыто.'] = ['Но знай, внимающий этим камням, никто не (забыть) и ничто не (забыть).', 'забытзабыто']
# слишком много примеров со словом "показан"
pokazan = 0
key_to_delete = []
for sent in prts:
    if 'показан' in prts[sent][1]:
        pokazan += 1
        if pokazan > 20:
            key_to_delete.append(sent)
for key in key_to_delete:
    prts.pop(key)

# сравнительная степень прилагательных (почему-то deeppavlov считает "выше" и "ниже" леммами)
for key in adj_cmp:
    if '(ниже)' in adj_cmp[key][0]:
        adj_cmp[key] = [adj_cmp[key][0].replace('(ниже)', '(низкий)'), adj_cmp[key][1]]
for key in adj_cmp:
    if '(выше)' in adj_cmp[key][0]:
        adj_cmp[key] = [adj_cmp[key][0].replace('(выше)', '(высокий)'), adj_cmp[key][1]]
# превосходная степень прилагательных
adj_sup['Наилучший из этих элементов – хром.'][1] = 'лучший'
# ошибки в прилагательных
adj_full.pop('Вещества с кристаллическим строением называют кристаллическими веществами.')
adj_full.pop('Теплопроводность характеризует теплофизические свойства материалов, определяя их принадлежность по назначению к теплоизоляционным, конструкционно-теплоизоляционным и конструкционным материалам.')
adj_full.pop('Различают химическую коррозию, обусловленную воздействием на металл сухих газов и неэлектролитов (например, нефтепродуктов) и электрохимическую, возникающую под действием жидких электролитов или влажного воздуха.')
adj_full.pop('Ее делят на равномерную и неравномерную в зависимости от того, одинаковая ли глубина коррозионного разрушения на разных участках.')
adj_full.pop('В здании Кунсткамеры находились также первая научная библиотека и первая обсерватория.')
adj_full.pop('В этом романе писатель показал, что армию Наполеона победила не русская армия, а весь русский народ, выступивший на защиту своей родины.')
adj_short['Материалы этого типа не должны выделять токсичных веществ и должны быть совместимыми с тканями человека (т. е. не должны вызывать реакции отторжения).'] = ['Материалы этого типа не (должный) выделять токсичных веществ и (должный) быть совместимыми с тканями человека (т. е. не (должный) вызывать реакции отторжения).', 'должныдолжныдолжны']
# записываем финальный вариант
write_file('PRTF_final.pickle', prtf)
write_file('PRTS_final.pickle', prts)
write_file('ADJ_full_final.pickle', adj_full)
write_file('ADJ_short_final.pickle', adj_short)
write_file('Adj_cmp_final.pickle', adj_cmp)
write_file('Adj_sup_final.pickle', adj_sup)
