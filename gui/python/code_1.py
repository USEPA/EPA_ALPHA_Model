# The following section demonstrates how to insert a header into the code file
# that will be recorded when the auto-documentation is built.
# "Code" will be the name of the sub-heading in the documentation using the
# formatting shown.


"""Code
   ----

   The ``code_1.py`` file demonstrates how to auto-document code.

   A full functional description of the file contents will be
   located here.

       ::

        A highlighted literal section may also be added here if needed.

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
