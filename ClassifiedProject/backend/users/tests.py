from django.conf import settings
from django.core import signing

value = signing.dumps({"foo":"bar"})
src = signing.loads(value)
print(value)
print(src)
# Create your tests here.

