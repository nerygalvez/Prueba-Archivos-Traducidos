module.exports = {
    port : process.env.PORT || 5000,
    SECRET : ['-----BEGIN RSA PRIVATE KEY-----',
        'MIICWwIBAAKBgFtrLl2JH5B0BLlQFX0Il4tWTuA9goiDXM95kQz+LUqaLXJEcKnv',
        'pvSJUqdh2QZfTjspzEunD9VccI1EOiFL4+ny+vVNzzw80YVkpWekHa20iviaYP2i',
        '8SdZdIxQw5m5IJBgw8YrOGqIXRuXzTFAHnicEaM+2VtBJbOfGEN/caSBAgMBAAEC',
        'gYAnD3q2GHrWG9xQ2bj0vZESxgPZqC536bjkJUsmxAvSDmJQqpGA6pbpcStRvWsf',
        'X+VrPga+ZFlNjrvAgGBeDbEJqCjIiWb9/Tly0HfJgubPvJOrT+QOfd0nAlAdpn/W',
        '9LnJF/2QBE3IpGqlOeaoQex9Svmt1WWLMpg40at+MM4eKQJBAJ6wEkv4xxMt1Tf/',
        'qexhzZVoZ66vYUQg6ZmHzUptzs32JZt4KW7MCd6bYOOOYQDKgoU1BUJH/P/B2/oU',
        'Rv2R7ksCQQCTersN1iuxpNunzkJwHGSdtINk7NlLdBkc1fuBAofKmCln7d42thd4',
        'AuqfXZpboBrPLZK2rBg044caTqSTKwjjAkEAjwni1DxBJdaQdVOtFXfrWhusKdfI',
        'cyK/rjatI8PrP9f6ejNMFaUx2Ehyg2vZoF7qW6w5O0+si9VwtfEFNJgQFQJAdN2z',
        'rrJBq6LFAUOcODT3slTiLi7VvkoAwG38v+2eZ3eOkDHZfidrj4lYHPNSpzrHI9es',
        'RB85i2elnr4lAg3/GwJABWxeb3UUSto4Q8et7WT9s0QzQQS5VD3aiOSdPc8R9hGA',
        'LtrbjK9p00YtryIbNVcyO00U29PWFisRHuMAr9xR1w==',
        '-----END RSA PRIVATE KEY-----'].join('\n'),
    db : process.env.MONGODB || 'mongodb://jwtdb:27017/jwt-bd'
}