from django.utils.text import slugify
import random
import string

def random_string_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    size = random.randint(30,45)
    key = random_string_generator(size=size, chars=(string.digits + string.ascii_letters))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_key_generator(instance)
    return key



def unique_order_id_generator(instance):
    
    order_new_id = random_string_generator(size=10, chars=string.ascii_uppercase + string.digits)
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id



def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug= slugify(instance.title)
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        randstr = random_string_generator()
        new_slug = f'{slug}-{randstr}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
        
