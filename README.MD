Employee Name
=INDEX([MasterData.xlsx]NameDataBase!$D$2:$D$338, RANDBETWEEN(2, 300))

Age
=RANDBETWEEN(25, 55)

Male or Female
=IF(RANDBETWEEN(0,1)=0,"Male","Female")

Salary
=RANDBETWEEN(1, 99)*1000


