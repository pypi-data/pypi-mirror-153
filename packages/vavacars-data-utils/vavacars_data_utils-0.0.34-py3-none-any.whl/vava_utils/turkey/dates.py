import datetime

months_translation = {'Ocak': 1,
                      'Şubat': 2,
                      'Mart': 3,
                      'Nisan': 4,
                      'Mayıs': 5,
                      'Haziran': 6,
                      'Temmuz': 7,
                      'Ağustos': 8,
                      'Eylül': 9,
                      'Ekim': 10,
                      'Kasım': 11,
                      'Aralık': 12}


def turkish_to_datetime(s):
    """
    Converts a string containing a turkish date into a datetime object.

    Input format of the date as 'dd turkish_month year': 08 Aralık 2021

    Parameters:
        s (str): String with turkish date
    """
    try:
        (day, month, year) = s.split()
        return datetime.datetime(int(year), months_translation[month], int(day))
    except Exception as e:
        return datetime.datetime(1900, 1, 1)
