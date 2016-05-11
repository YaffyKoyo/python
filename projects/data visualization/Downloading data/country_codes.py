from pygal_maps_world.i18n import COUNTRIES

def get_country_code(country_name):

    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    # If the country wasn't found, return None.
    return None

