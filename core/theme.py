class Theme(object):
    # ---------------
    # |   title     |
    # ---------------
    # |   data1     |
    # |   data2     |
    # ---------------
    border_color = '#4a555e'
    title_color = '#4a555e'
    data_color = 'white'
    title_font_size = '15px'
    title_font_color = 'white'
    data_font_size = '13px'
    data_font_color = 'black'

    def __repr__(self):
        return '{"border_color":"'+self.border_color+'"' \
                         ',"title_color":"'+self.title_color+'"' \
                         ',"data_color":"'+self.data_color+'"' \
                       ',"title_font_size":"'+self.title_font_size+'"' \
                       ',"title_font_color":"'+self.title_font_color+'"' \
                     ',"data_font_size":"'+self.data_font_size+'"' \
                       ',"data_font_color":"'+self.data_font_color+'"}'



class Defualt(Theme):
    pass

class GreenWhite(Theme):
    border_color = '#4b804b'
    title_color = '#4b804b'
    data_color = 'white'

class BlackWhite(Theme):
    border_color = 'black'
    title_color = 'black'
    data_color = 'white'

class LightBlackWhite(Theme):
    border_color = '#666666'
    title_color = '#666666'
    data_color = 'white'

class DeepGrayWhite(Theme):
    border_color = '#4a555e'
    title_color = '#4a555e'
    data_color = 'white'

class BlueWhite(Theme):
    border_color = '#0e0be8'
    title_color = '#0e0be8'
    data_color = 'white'

class PurpleWhite(Theme):
    border_color = '#ad0fe0'
    title_color = '#ad0fe0'
    data_color = 'white'


class DeepGreenWhite(Theme):
    border_color = '#327355'
    title_color = '#327355'
    data_color = 'white'

class RedWhite(Theme):
    border_color = '#bf1a31'
    title_color = '#bf1a31'
    data_color = 'white'