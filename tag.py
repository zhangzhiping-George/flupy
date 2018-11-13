def tag(name, *contents, cls=None, **attrs):
    if cls: 
        attrs['class'] = cls
    if attrs:
        attr_str=''.join([' %s="%s"' %(attr, value) for attr, value in attrs.items()])
    else:
        attr_str=''
    #<p class="sidebar">hello</p>
    if contents:
        return '\n'.join(['<%s%s>%s</%s>' %(name, attr_str, c, name) for c in contents])   
    else:
        return '<%s%s/>' %(name, attr_str)

print(tag('p', 'hello', 'world', cls='sidebar', id=33))
print(tag(contents='hello',name='img'))
my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
            'src': 'sunset.jpg', 'cls': 'framed'}
print(tag(**my_tag))
