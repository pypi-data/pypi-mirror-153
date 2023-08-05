class ProxyOs:
    FREE_BSD = 'FreeBSD'
    LINUX = 'Linux'
    # MAC_OS_X = 'Mac OS X' # Does not work reliably
    WINDOWS = 'Windows'


TOP_RESIDENTIAL_US_ISPS = [
    'AT&T U-verse',
    'Comcast Cable',
    'Cox Communications',
    'Hughes Network Systems',
    'Mediacom Cable',
    'Spectrum',
    'Verizon Fios'
]

DEFAULT_PROXYRACK_COUNTRY_WEIGHTS = [
    ('US', .70),
    ('CA', .12),
    ('UK', .12),
    ('AU', .06),
]

DEFAULT_PROXYRACK_ISP_WEIGHTS = [
    ('AT&T U-verse', 1),
    ('Comcast Cable', 1),
    ('Cox Communications', 1),
    ('Hughes Network Systems', 1),
    ('Mediacom Cable', 1),
    ('Spectrum', 1),
    ('Verizon Fios', 1),
]