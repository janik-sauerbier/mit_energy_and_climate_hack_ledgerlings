import os
import streamlit as st
import streamlit.components.v1 as components
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import numpy as np
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

import streamlit as st
import streamlit.components.v1 as components

# Highcharts JavaScript and HTML code
highcharts_html = """
<html>

<head>

    <title>Mapping individual investment footprints</title>

    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>

    <script src="https://code.highcharts.com/highcharts.js"></script>

    <script src="https://code.highcharts.com/highcharts-more.js"></script>

    <script src="https://code.highcharts.com/modules/exporting.js"></script>

    <script type="text/javascript">

        $(function() {

            Highcharts.chart('container', {

                chart: {

                    type: 'packedbubble',

                    height: '100%'

                },

                title: {

                    text: 'Largest investment carbon footprint of individuals'

                },

                tooltip: {

                    useHTML: true,

                    pointFormat: '<b>{point.name}:</b> {point.value}t CO<sub>2</sub>'

                },

                plotOptions: {

                    packedbubble: {

                        minSize: '30%',

                        maxSize: '120%',

                        zMin: 0,

                        zMax: 1000,

                        layoutAlgorithm: {

                            splitSeries: false,

                            gravitationalConstant: 0.02

                        },

                        dataLabels: {

                            enabled: true,

                            format: '{point.name}',

                            filter: {

                                property: 'y',

                                operator: '>',

                                value: 250

                            },

                            style: {

                                color: 'black',

                                textOutline: 'none',

                                fontWeight: 'normal'

                            }

                        }

                    }

                },

                series: [{

                    name: 'Other',

                    data: [{

                        name: 'Alisher Usmanov',

                        value: 8079.6

                    }, {

                        name: 'Dieter Schwarz',

                        value: 3944.1

                    }, {

                        name: "Gianluigi Aponte",

                        value: 1103.0

                    }, {

                        name: "Giovanni Ferrero & family",

                        value: 783.0

                    }, {

                        name: "Jacqueline Badger Mars",

                        value: 565.3

                    }, {

                        name: "John Mars",

                        value: 565.3

                    }, {

                        name: "Philip Anschutz",

                        value: 231.0

                    }, {

                        name: "Donald Newhouse",

                        value: 152.0

                    }, {

                        name: "Grosvenor family",

                        value: 29.6

                    }, {

                        name: "Abigail Johnson",

                        value: 34.5

                    }, {

                        name: "Renata Kellnerova",

                        value: 12.2

                    }, {

                        name: "Idan Ofer",

                        value: 0.6

                    }, {

                        name: "Cyrus Poonawalla",

                        value:0.6

                    }]

                }, {

                    name: 'Asia',

                    data: [{

                        name: "Gautam Adani",

                        value: 29528.4

                    }, {

                        name: "Mukesh Ambani",

                        value: 19352.0

                    }, {

                        name: "Savitri Jindal",

                        value: 20282.5

                    }, {

                        name: "Kumar Birla",

                        value: 10425.2

                    }, {

                        name: "Sarath Ratanavadi",

                        value: 7114.0

                    }, {

                        name: "Robert Kuok",

                        value: 1809.2

                    }, {

                        name: "Charoen Sirivadhanabhakdi",

                        value: 2010.5

                    }, {

                        name: "Sunil Mittal",

                        value: 213.1

                    }, {

                        name: "Dilip Shanghvi",

                        value: 167.81

                    }, {

                        name: "Goh Cheng Liang",

                        value: 151.6

                    }, {

                        name: "Masayoshi Son",

                        value: 128.0

                    }, {

                        name: "Shiv Nadar",

                        value: 92.7

                    }, {

                        name: "Azim Premji",

                        value: 61.0

                    }, {

                        name: "Tadashi Yanai",

                        value: 56.9

                    }, {

                        name: "Budi Hartono",

                        value: 29.7

                    }, {

                        name: "Michael Hartono",

                        value: 28.5

                    }, {

                        name: "Wee Cho Yaw",

                        value: 26.7

                    }, {

                        name: "Budi Hartono",

                        value: 29.7

                    }, {

                        name: "Michael Hartono",

                        value: 28.5

                    }, {

                        name: "Wee Cho Yaw",

                        value: 26.7

                    }, {

                        name: "Uday Kotak",

                        value: 6.2

                    }, {

                        name: "Eyal Ofer",

                        value: 4.1

                    }, {

                        name: "Takemitsu Takizaki",

                        value: 0.7

                    }]

                }, {

                    name: 'Europe',

                    data: [{

                        name: "Lakshmi Mittal",

                        value: 51787.7

                    }, {

                        name: "Carlos Slim",

                        value: 6974.4

                    }, {

                        name: "Len Blavatnik",

                        value: 5257.912

                    }, {

                        name: "Paolo Rocca & family",

                        value: 8949.2

                    }, {

                        name: "Klaus-Michael Kuehne",

                        value: 4157.5

                    }, {

                        name: "Iris Fontbona & family",

                        value: 1635.8

                    }, {

                        name: "Mikhail Fridman",

                        value: 1041.6

                    }, {

                        name: "Amancio Ortega",

                        value: 346.3

                    }, {

                        name: "Stefan Quandt",

                        value: 199.8

                    }, {

                        name: "Susanne Klatten",

                        value: 357.9

                    }, {

                        name: "Bernard Arnault & family",

                        value: 134.5

                    }, {

                        name: "Melker Schorling",

                        value: 129.8

                    }, {

                        name: "Viktor Vekselberg",

                        value: 58.1

                    }]

                }, {

                    name: 'North America',

                    data: [{

                        name: "Bill Gates",

                        value: 4824.8

                    }, {

                        name: "Warren Buffett",

                        value: 3547.3

                    }, {

                        name: "German Larrea",

                        value: 3467.2

                    }, {

                        name: "Harold Hamm",

                        value: 2391.7

                    }, {

                        name: "Alice Walton",

                        value: 2194.2

                    }, {

                        name: "Jim Walton",

                        value: 2189.1

                    }, {

                        name: "Rob Walton",

                        value: 2169.0

                    }, {

                        name: "Graeme Hart",

                        value: 2240.1

                    }, {

                        name: "John Fredriksen",

                        value: 2671.4

                    }, {

                        name: "Miriam Adelson",

                        value: 414.6

                    }, {

                        name: "Mark Zuckerberg",

                        value: 378.3

                    }, {

                        name: "Jerry Jones",

                        value: 293.2

                    }, {

                        name: "Michael Dell",

                        value: 244.5

                    }, {

                        name: "Larry Ellison",

                        value: 134.9

                    }, {

                        name: "Elon Musk",

                        value: 79.2

                    }, {

                        name: "Ricardo Salinas",

                        value: 71.0

                    }]

                }]

            });

        });

    </script>

</head>

<body>

    <div id="container" style="min-width: 320px; max-width: 800px;margin: 0 auto;"> </div>

</body>

</html>
"""

def main():
    st.title('Mapping individual investment footprints')

    # Embed the Highcharts HTML in the Streamlit app
    components.html(highcharts_html, height=1000)

if __name__ == "__main__":
    main()
