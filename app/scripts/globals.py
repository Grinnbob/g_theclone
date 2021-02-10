customer_to_spreadsheet = {
    'adoptics' : 'https://docs.google.com/spreadsheets/d/1sRQpyLCzZHDCHgNhO0U69rZcwGOHenLCzawkdLQiYdo',
    'defihunters' : 'https://docs.google.com/spreadsheets/d/1DGVdL0VZr0XhF8xk8HW6UVJWEEDPCsCTad7dKEqgl6w',
    'adglobi' : 'https://docs.google.com/spreadsheets/d/1c2ih8iG-CnIyvzaE5ZfxWBTBffZf_TyQ4mMBU8D7IQA',
    'digiworksco' : 'https://docs.google.com/spreadsheets/d/1qgb_MPGEpiu-WEnUjegePEHF741cMx0h0MeI7BQL0JQ',
    'theclone' : 'https://docs.google.com/spreadsheets/d/1-3_nsoAChjQ999GLTZIs7o7RCaFpzC2GMgOTPlLIJjQ'
}

customers_blacklist = {
    'digiworksco' : {
        'emails' : ['ks.shilov@gmail.com', 'ks.shilov@howtotoken.com'],
        'domains' : ['defihunters', 'adglobi', 'howtotoken', 'theclone']
    },
    'adglobi': {
        'emails': ['ks.shilov@gmail.com', 'ks.shilov@howtotoken.com'],
        'domains': ['defihunters', 'digiworks', 'howtotoken', 'theclone']
    },
    'adoptics': {
        'emails': ['ks.shilov@gmail.com', 'ks.shilov@howtotoken.com'],
        'domains': ['defihunters', 'digiworks', 'adglobi', 'howtotoken', 'theclone']
    },
    'theclone' : {
        'emails': ['ks.shilov@gmail.com'],
        'domains': ['defihunters', 'digiworks', 'adglobi']
    }
}

customer_to_emails = {
    'all' : [],

    'adoptics' : [
        'kb@adoptics.cc',
        'lj@adoptics.cc',
        'shs@adoptics.co',
        'ss@adoptics.co'
    ],

    'adglobi' : [
        'oj@adglobi.co'
    ],

    'digiworksco' : [
        'ad@digiworksco.cc',
        'ap@digiworksco.co',
        'em@digiworksco.cc',
        'sw@digiworksco.co'
    ],

    'defihunters' : [
        'hj@defihunters.co',
        'iw@defihunters.cc',
        'mp@defihunters.co',
        'mw@defihunters.cc',
    ],

    'theclone' : [
        'k.shilov@theclone.cc',
        'k.shilov@theclone.tech',
        'ks.shilov@theclone.cc',
        'ks.shilov@theclone.tech',
        'k.shilov@howtotoken.co',
        'k.shilov@howtotoken.com',
        'ks.shilov@howtotoken.co',
        'ks.shilov@howtotoken.com'
    ]
}

sequence_groups = {
    'seq_5mCnYDnqQhoPZWZUa0uMuu' : 'adglobi',
    'seq_3ebXZ9kgeJDpT4qbzpprm2' : 'adglobi',

    'seq_6EaLFuKa9iBTvHzcGIbFEj' : 'adoptics',
    'seq_3WWdmkXiPCjLjkuGVuPPwI' : 'adoptics',
    'seq_3OKwKFS5u9TVSPKFBJ8TSl' : 'adoptics',
    'seq_3m1l7Px5mOQJ4WrgORuNiG' : 'adoptics',

    'seq_2yDEbImUooEpJJL9HiSJq6' : 'kirill',
    'seq_2S0GUUk0y61V68NdUYmicf' : 'kirill',
    'seq_0zVm1yTvcxLp0scZyCoE1X' : 'kirill',
    'seq_36Wfp4QHFEIYK4krhkdBZ4' : 'kirill',
    'seq_6dW6jalBUML36aBMHeVcjY' : 'kirill',
    'seq_3eTalNVHUHPJ1E7dqL3Ylh' : 'kirill',
    'seq_1M6qbTJ5ypznTAC1600iyS' : 'kirill',
    'seq_1UKaBGqF9OXr9rIDt3EK9m' : 'kirill',


    'seq_5dlIbiDOCFYAC5KS8FVxFF' : 'defihunters',
    'seq_03IjS1QIHl7vdH7owWX23R' : 'defihunters',
    'seq_56IVgwJx7bo7mo8hLnsgSL' : 'defihunters',
    'seq_5NnCQoOu5Zxs0pk3iRI7TF' : 'defihunters',

    'seq_44EXOAPL1Fthb6ralcWdXj' : 'digiworks',
    'seq_1oREEiSTsVSHQZxAyXwZp2' : 'digiworks',
    'seq_13o3eiPTnGWyfbaIPLYcWW' : 'digiworks',
    'seq_1UMq1jGr4esf271J07Jkhz' : 'digiworks',

    'seq_5F6MHd7fEWvDMNlMN07dDU' : 'howtotoken',
    'seq_1WT9HpFJ33EweitNJHVdLf' : 'test'
}

lead_status = {
    "internal_forward" : 'stat_5Tm5Wci4dMzz8I2RIlNgxO9OEVnKhidYe7MasKYtZ3j',
    "no_show" : 'stat_6MRNmzHIbFfKpV2tyjRIIYVjhJ7grP8oN8n4hcWRtUe',
    "invalid_email" : 'stat_86RE9pzTCp8qLF9MdngBbMlOt47eaQndlmmbg56ajA6',
    "setting_up_time" : 'stat_9gTKK52E2Cn2LUAKSVWBsWU1tQzgvM8gc46aH2Xuddc',
    "scheduled" : 'stat_CRgKH2HWCkk6dg2HcBYP4tbWhhe4kcnbMIaUrrcDffb',
    "new" : 'stat_FzZ89uVnY0NS3zZh36yQHzRRjVatRcxCYdsixGKxBqz',
    "contact_later" : 'stat_Pk8uSpLMiCTgcEu7SK5WHihbYGHESftEUs98IzY5BAN',
    "ignored" : 'stat_TTc949tYZ8y7FDnEVq7tXi1M7NGracxTO6kGLRpb9ct',
    "ooo" : 'stat_VFusrB0TQOdGNJRJlyGEoOkSPDK0bQ3GxZjCBngK1Dw',
    "meeting_booked" : 'stat_W8No5BfU0W7EXqzxBxxir18wyL33jJyBGHJOd4BnKSk',
    "subscription_request_sent" : 'stat_XfwUcObm1NPXeftvRqziENuGIidIF6vZxRha8P3fGF6',
    "subscriber" : 'stat_dUXgnp3zj9g709mZTtOS6GmhP8x7v7GBvBsFKEnJf8y',
    "interested" : 'stat_gKUbj33nqG9HyW1pAegWzudckVw7FJgBV1jYZPy1JPw',
    "not_a_fit" : 'stat_kJeqZyU2mhyWwC148n9n0frWFMnTlEMkML1OqfPAmXB',
    "not_interested" : 'stat_mzOUwxnaJW4M30QSy0fRR39B1FIA7b06SmOhngh9lgy',
    "dialog" : 'stat_wduuoKOD7lzcrbX7yhDE8H5xWJ8b5FbhRNGIR8KxttU',
}


sequence_to_sender = {
    'Marina - request for article' : 'marusya@howtotoken.com',

    'theclone-agency - Kirill Shilov - k.shilov@theclone.cc' : 'k.shilov@theclone.cc',
    'theclone-agency - Kirill Shilov - k.shilov@theclone.tech' : 'k.shilov@theclone.tech',
    'theclone-agency - Kirill Shilov - ks.shilov@theclone.cc' : 'ks.shilov@theclone.cc',
    'theclone-agency - Kirill Shilov - ks.shilov@theclone.tech' : 'ks.shilov@theclone.tech',
    'theclone-cbs - Kirill Shilov - k.shilov@howtotoken.co' : 'k.shilov@howtotoken.co',
    'theclone-cbs - Kirill Shilov - k.shilov@howtotoken.com' : 'k.shilov@howtotoken.com',
    'theclone-gmbl - Kirill Shilov ks.shilov@howtotoken.co' : 'ks.shilov@howtotoken.co',
    'theclone-gmbl - Kirill Shilov ks.shilov@howtotoken.com' : 'ks.shilov@howtotoken.com',

    'adglobi - Evelyn Barnes - variant JACK' : 'eb@adglobi.co',
    'adglobi - Olivia Jones - variant KIRILL' : 'oj@adglobi.co',

    'defihunters - Harper Jenkins - variant JACK' : 'hj@defihunters.co',
    'defihunters - Isabella Wood - variant JACK' : 'iw@defihunters.cc',
    'defihunters - Maria Williams - variant JACK' : 'mw@defihunters.cc',
    'defihunters - Mia Perry - variant JACK' : 'mp@defihunters.co',

    'digiworks - Amelia Patel - JACK' : 'ap@digiworksco.co',
    'digiworks - Ava Davis - JACK' : 'ad@digiworksco.cc',
    'digiworks - Emma Miller - JACK' :  'em@digiworksco.cc',
    'digiworks - Sophia Wilson - JACK' : 'sw@digiworksco.co',

    'adoptics - Karen Brown - kb@adoptics.cc' : 'kb@adoptics.cc',
    'adoptics - Lisa Jones - lj@adoptics.cc' : 'lj@adoptics.cc',
    'adoptics - Shannon Sofield - shs@adoptics.co' : 'shs@adoptics.co',
    'adoptics - Shannon Sofield - ss@adoptics.co' : 'ss@adoptics.co',
}

smartviews_launch_list = {

    # Test
    'save_y7UCYZ2ooAopzelSXJQeacjF6EDjb1IKXiIMCEUt8mG': {
        'title' : 'test smartview',
        'status': 'paused',
        'tasks': [
            {
                'sequence': 'adglobi - Evelyn Barnes - variant JACK',
                'sender': 'eb@adglobi.co'
            },
        ]
    },

    # adoptics
    'save_5QOHIr6zm0NBEaLG1kCxLZGKp0mc4JgC1SJj4TRv1wL': {
        'title': 'adoptics smartview',
        'status': 'active',
        'tasks': [
            {
                'sequence': 'adoptics - Karen Brown - kb@adoptics.cc',
                'sender': 'kb@adoptics.cc'
            },
            {
                'sequence': 'adoptics - Lisa Jones - lj@adoptics.cc',
                'sender': 'lj@adoptics.cc'
            },
            {
                'sequence': 'adoptics - Shannon Sofield - shs@adoptics.co',
                'sender': 'shs@adoptics.co'
            },
            {
                'sequence': 'adoptics - Shannon Sofield - ss@adoptics.co',
                'sender': 'ss@adoptics.co'
            },
        ]
    },

    #adglobi
    'save_OmgSxL24kBzObTyfshm9DdjNM060wcsmIwFG8upHJi5' : {
        'title': 'adglobi smartview',
        'status' : 'active',
        'tasks' : [
            {
                'sequence': 'adglobi - Olivia Jones - variant KIRILL',
                'sender': 'oj@adglobi.co'
            },
        ]
    },

    # defihunters-publications
    'save_PKZEwEp2k9GnlZbTIg045T39go6tkHuy5A2A72P38u0': {
        'title': 'SQF - defihunters-publications 24',
        'status': 'active',
        'tasks': [
            {
                'sequence': 'defihunters - Harper Jenkins - variant JACK',
                'sender': 'hj@defihunters.co'
            },
            {
                'sequence': 'defihunters - Isabella Wood - variant JACK',
                'sender': 'iw@defihunters.cc'
            },
            {
                'sequence': 'defihunters - Maria Williams - variant JACK',
                'sender': 'mw@defihunters.cc'
            },
            {
                'sequence': 'defihunters - Mia Perry - variant JACK',
                'sender': 'mp@defihunters.co'
            },
        ]
    },

    # digiworks
    'save_PnHC3o4uaEbUg9xMjuFMdN3a49AfJuK1Q71IA6yOAdl': {
        'title': 'digiworks smartview',

        'status': 'active',
        'tasks': [
            {
                'sequence': 'digiworks - Amelia Patel - JACK',
                'sender': 'ap@digiworksco.co'
            },
            {
                'sequence': 'digiworks - Ava Davis - JACK',
                'sender': 'ad@digiworksco.cc'
            },
            {
                'sequence': 'digiworks - Emma Miller - JACK',
                'sender': 'em@digiworksco.cc'
            },
            {
                'sequence': 'digiworks - Sophia Wilson - JACK',
                'sender': 'sw@digiworksco.co'
            },
        ]
    },

    # theclone-cbs
    'save_eAjNxQ5DhHqvCD160qeGUo77R5je4dZJFnAtH7EbUOK': {
        'title': 'SQF - theclone-cbs 24',

        'status': 'active',
        'tasks': [
            {
                'sequence' : 'theclone-cbs - Kirill Shilov - k.shilov@howtotoken.co',
                'sender' : 'k.shilov@howtotoken.co',
            },
            {
                'sequence' : 'theclone-cbs - Kirill Shilov - k.shilov@howtotoken.com',
                'sender' : 'k.shilov@howtotoken.com',
            },
        ]
    },

    # theclone-gmbl
    'save_9wV8tpnehuDzLKnXa5K8kVDXjf4yEbKsEYajChO5D3w': {
        'title': 'SQF - theclone-gmbl 24',

        'status': 'active',
        'tasks': [
            {
                'sequence' : 'theclone-gmbl - Kirill Shilov ks.shilov@howtotoken.co',
                'sender' : 'ks.shilov@howtotoken.co',
            },
            {
                'sequence' : 'theclone-gmbl - Kirill Shilov ks.shilov@howtotoken.com',
                'sender' : 'ks.shilov@howtotoken.com',
            },
        ]
    },

    # theclone-agency
    'save_WOyTHsQZclDZwoyi2LLPSjcRMIdBsE1ISBSNIHDWWDd': {
        'title': 'SQF - theclone-agency 24',

        'status': 'active',
        'tasks': [
            {
                'sequence' : 'theclone-agency - Kirill Shilov - k.shilov@theclone.cc',
                'sender' : 'k.shilov@theclone.cc',
            },
            {
               'sequence' :'theclone-agency - Kirill Shilov - k.shilov@theclone.tech',
                'sender' : 'k.shilov@theclone.tech',
            },
            {
                'sequence' : 'theclone-agency - Kirill Shilov - ks.shilov@theclone.cc',
                'sender' : 'ks.shilov@theclone.cc',
            },
            {
                'sequence' : 'theclone-agency - Kirill Shilov - ks.shilov@theclone.tech',
                'sender' : 'ks.shilov@theclone.tech',
            },
        ]
    },

    # Marina
    'save_wDY4KOM64GbtW6VN3dsXRetINU2vO2uCyjS6ON8lYoW': {
        'title': 'Marina howtotoken smartview',

        'status': 'paused',
        'tasks': [
            {
                'sequence': 'Marina - request for article',
                'sender': 'marusya@howtotoken.com'
            },
        ]
    },

    # defihunters
    'save_gJorYAeDfuyf9aubmnfY1ZtKO5LKp7gsFiGvu1itnpg': {
        'title': 'defihunters smartview',
        'status': 'paused',
        'tasks': [
            {
                'sequence': 'defihunters - Harper Jenkins - variant JACK',
                'sender': 'hj@defihunters.co'
            },
            {
                'sequence': 'defihunters - Isabella Wood - variant JACK',
                'sender': 'iw@defihunters.cc'
            },
            {
                'sequence': 'defihunters - Maria Williams - variant JACK',
                'sender': 'mw@defihunters.cc'
            },
            {
                'sequence': 'defihunters - Mia Perry - variant JACK',
                'sender': 'mp@defihunters.co'
            },
        ]
    },

}


