def addToTab(tab, el):
        tab.append(el)
        return tab

def delFromTab(tab, el):
        tab.remove(el)
        return tab

def getVegetables(tab, veg):
        for v in veg:
                try:
                        if tab.count(v) >=1:
                                liste.append(v)
                except:
                        liste = []
                        if tab.count(v) >=1:
                                liste.append(v)
        return liste
