"""Code
   ----

   Information related to the code is placed here

       ::

        A literal section can also be added

    """


from datetime import datetime

now = datetime.now()

mm = str(now.month)

dd = str(now.day)

yyyy = str(now.year)

hour = str(now.hour)

mi = str(now.minute)

ss = str(now.second)

print(mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss)



