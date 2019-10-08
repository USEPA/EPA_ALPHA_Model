"""Code
   ----

    Describe Code Here: This routine uses the datetime function to print the date and time"""

from datetime import datetime

now = datetime.now()

mm = str(now.month)

dd = str(now.day)

yyyy = str(now.year)

hour = str(now.hour)

mi = str(now.minute)

ss = str(now.second)

print(mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss)



