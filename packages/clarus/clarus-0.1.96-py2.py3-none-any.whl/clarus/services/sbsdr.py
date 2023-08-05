import clarus.services

def mostactive(output=None, **params):
    return clarus.services.api_request('SBSDR', 'MostActive', output=output, **params)

def volume(output=None, **params):
    return clarus.services.api_request('SBSDR', 'Volume', output=output, **params)

