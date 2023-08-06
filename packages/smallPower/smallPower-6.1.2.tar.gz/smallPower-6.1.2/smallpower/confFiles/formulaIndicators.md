---
useMath:true
---
<!-- <div class="math">
\begin{equation}
I = \sum{I_k}$ -->

# constants
F = 96485 C/mol: Faraday Constant

# sum courant stacks
'courrant stacks total': $I = \sum{I_k}$

I_k = 'STK.*IT.*HM05'
# production O2
Po2mols = I*25/(4*F)
because there are 25 cells
Po2Nlmin = Po2mols*22.4*60
# fuite air
QairAval = df[airAval]+Po2Nlmin
fuiteAir = df[airAmont]-(QairAval)
txFuite = fuiteAir/df[airAmont]*100
coefficientDeFuite = fuiteAir/df[pressionDiffuseur]

dfmodeHUB=self.getModeHub(timeRange_Window,**kwargs)
# dfmodeHUB=self.getModeHub(timeRange_Window,rs=rs)

varUnitsCalculated = {
    'production O2(mol/s)':{'unit':'mol/s','var':Po2mols},
    'production O2(Nl/min)':{'unit':'Nl/min','var':Po2Nlmin},
    'flux air aval(aval + production O2)':{'unit':'Nl/min','var':QairAval},
    'fuite air':{'unit':'Nl/min','var':fuiteAir},
    'taux de fuite air':{'unit':'%','var':txFuite},
    'coefficient de fuite':{'unit':'N/min/mbar','var':coefficientDeFuite},
    'mode hub':{'unit':'mode hub','var':dfmodeHUB['value']}
}
