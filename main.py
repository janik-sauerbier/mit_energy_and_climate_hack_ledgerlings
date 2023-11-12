import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from openai import OpenAI
import matplotlib.pyplot as plt
from io import BytesIO


st.set_page_config(
    page_title="🌎 Climate Ledger",
    layout="wide"
)

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106"

df = pd.read_csv("./datasets/country_data.csv")
df = df.apply(pd.to_numeric, errors='ignore')

st.markdown("<h1 style='text-align: center;'>🌎 Climate Ledger</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    components.html("""
      <div id="globeViz1"></div>

      <script src="//unpkg.com/globe.gl"></script>
      <script>
        const world1 = Globe()
          (document.getElementById('globeViz1'))
          .backgroundColor('#FFFFFF')
          .globeImageUrl('//unpkg.com/three-globe/example/img/earth-day.jpg')
          .pointOfView({ altitude: 4 }, 5000)
          .polygonCapColor(feat => 'rgba(100, 100, 100, 0.6)')
          .polygonSideColor(() => 'rgba(100, 100, 100, 0.3)')
          .polygonLabel(({ properties: d }) => `
              <b>${d.ADMIN} (${d.ISO_A2})</b> <br />
              Cumulative CO2e Emission until 2022: <i>${Math.round(+d.POP_EST)} mt</i>
            `);

        // Auto-rotate
        world1.controls().autoRotate = true;
        world1.controls().autoRotateSpeed = 1.8;

        fetch('https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/emissions_2022.geojson').then(res => res.json()).then(countries => {
          world1.polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'));

          setTimeout(() => world1
            .polygonsTransitionDuration(2000)
            .polygonAltitude(feat => Math.max(0.02, Math.sqrt(+feat.properties.POP_EST) * 1e-4))
          , 2000);
        });
      </script>
    """, height=500)
    st.markdown("<p style='text-align: center;'><b>2022 CO2e Emissions</b></p>", unsafe_allow_html=True)

with col2:
    components.html("""
      <div id="globeViz2"></div>

      <script src="//unpkg.com/globe.gl"></script>
      <script>
        const world2 = Globe()
          (document.getElementById('globeViz2'))
          .backgroundColor('#FFFFFF')
          .globeImageUrl('//unpkg.com/three-globe/example/img/earth-day.jpg')
          .pointOfView({ altitude: 4 }, 5000)
          .polygonCapColor(feat => 'rgba(100, 100, 100, 0.6)')
          .polygonSideColor(() => 'rgba(100, 100, 100, 0.3)')
          .polygonLabel(({ properties: d }) => `
              <b>${d.ADMIN} (${d.ISO_A2})</b> <br />
              Cumulative CO2e Emission until 2022: <i>${Math.round(+d.POP_EST)} mt</i>
            `);

        // Auto-rotate
        world2.controls().autoRotate = true;
        world2.controls().autoRotateSpeed = 1.8;

        fetch('https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/emissions_cumulative.geojson').then(res => res.json()).then(countries => {
          world2.polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'));

          setTimeout(() => world2
            .polygonsTransitionDuration(2000)
            .polygonAltitude(feat => Math.max(0.02, Math.sqrt(+feat.properties.POP_EST) * 1e-4))
          , 2000);
        });
      </script>
    """, height=500)
    st.markdown("<p style='text-align: center;'><b>Cumulative CO2e Emissions</b></p>", unsafe_allow_html=True)


with col3:
    components.html("""
      <div id="globeViz3"></div>

      <script src="//unpkg.com/globe.gl"></script>
      <script>
        const world3 = Globe()
          (document.getElementById('globeViz3'))
          .backgroundColor('#FFFFFF')
          .globeImageUrl('//unpkg.com/three-globe/example/img/earth-day.jpg')
          .pointOfView({ altitude: 4 }, 5000)
          .polygonCapColor(feat => 'rgba(100, 100, 100, 0.6)')
          .polygonSideColor(() => 'rgba(100, 100, 100, 0.3)')
          .polygonLabel(({ properties: d }) => `
              <b>${d.ADMIN} (${d.ISO_A2})</b> <br />
              Climate Debt: <i>${Math.round(+d.POP_EST)} W/m^2</i>
            `);

        // Auto-rotate
        world3.controls().autoRotate = true;
        world3.controls().autoRotateSpeed = 1.8;

        fetch('https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/climate_debt.geojson').then(res => res.json()).then(countries => {
          world3.polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'));

          setTimeout(() => world3
            .polygonsTransitionDuration(2000)
            .polygonAltitude(feat => Math.max(0.02, Math.sqrt(+feat.properties.POP_EST) * 1e-4))
          , 3000);
        });
      </script>
    """, height=500)
    st.markdown("<p style='text-align: center;'><b>Actual Climate Impact</b>*</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>* Greenhouse gases (GHGs) persist in the atmosphere for extended periods, significantly contributing to the warming of the Earth's surface. GHGs emitted centuries ago continue to play a role in our current global heating. Consequently, we face a finite carbon budget to achieve our objective of staying below a 1.5-degree increase. Cumulative Radiative Forcing stands as a widely employed measure to gauge the impact of past emissions—essentially quantifying the climate debt of various entities, be it nations, companies, or individuals. Assessing the accumulated climate debt of each entity redirects our focus from individual consumers to those accountable and capable of actively contributing to a solution</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>👇<i> Scroll down here to continue </i>👇</p>", unsafe_allow_html=True)

col1a, col2a, col3a = st.columns(3)

select = st.empty

with col2a:
    select = st.selectbox("Country Selection", df.country.unique(), placeholder="Choose an country")

st.divider()

col1d, col2d, col3d = st.columns(3)

with col1d:
    st.write("Emissions per Year")
    chart_data = df.query("country == '" + str(select) + "'").query("year >= 1950")[["year", "CO2 (mt)", "Methane (mt CO2e)", "Nitrous Oxide (mt CO2e)"]].apply(pd.to_numeric)
    st.line_chart(chart_data, x="year")

with col2d:
    st.write("Cumulative Emissions (mt CO2e / all gases)")
    chart_data = df.query("country == '" + str(select) + "'").query("year >= 1950")[["year", "CO2e TOTAL Commulative"]].apply(pd.to_numeric)
    st.area_chart(chart_data, x="year")

with col3d:
    st.write("Climate Debt")
    chart_data = df.query("country == '" + str(select) + "'").query("year >= 1950")[["year", "RF TOTAL Cummulative"]].apply(pd.to_numeric)
    st.area_chart(chart_data, x="year")

# df = pd.read_csv("https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/owid-co2-data.csv")

st.divider()

col1b, col2b, col3b, col4b = st.columns(4)

with col1b:
    st.write("### 💡 Note for policymakers")
    st.markdown("In the fight against climate change, understanding the distinct roles of ***carbon dioxide (CO2)*** and ***methane (CH4)*** is essential. CO2, with its long atmospheric lifespan of ***300 to 1,000 years***, demands strategies for deep, long-term reductions. However, it's equally important not to overlook methane. Although it remains in the atmosphere for a shorter period (about 12 years), ***methane is over 25 times more potent than CO2*** in trapping heat in the short term. \n\nThis potency makes focusing on methane crucial. Reducing methane emissions can provide ***immediate and significant benefits*** in slowing global warming, complementing the longer-term efforts to reduce CO2. Your decisions should balance these considerations, ensuring a comprehensive approach to both immediate and enduring climate challenges. Act wisely; your choices today will shape our environmental legacy.")

with col2b:
    st.write("### 🟡 2-degree scenario")
    message_placeholder = st.empty()
    st.session_state.full_response = ""

    for response in client.chat.completions.create(model=st.session_state["openai_model"],
                                                   messages=[{"role": "system", "content": "You're an policy expert that works for " + str(select) + ". Your job is to paint a vivid picture of what will happen in a given scenario that you're given to inform policy makers, but in a concise way as you're aware that policy makers are busy. Describe how " + str(select) + "will be affected by a bad 3-degree global warming scenario in a short sentence. Be concise, and use max 3 bullet points to describe your ideas. Highlight the important things in bold. Be specific when you can on the consequences to the economy. Conclude with one specific sentence about how it's still better than a 3-degree scenario."}],
                                                   stream=True):
        st.session_state.full_response += response.choices[0].delta.content or ""
        message_placeholder.markdown(st.session_state.full_response + "▌")

    message_placeholder.markdown(st.session_state.full_response)

#    image1 = client.images.generate(
#        model="dall-e-3",
#        prompt="Create a photorealistic scene of a someone in a profession in" + str(select) + "and how they would be affected by a 2-degree global warming scenario. \n\n DON'T WRITE ANY TEXT ON THE PICTURE.",
#        size="1024x1024",
#        quality="standard",
#        n=1,
#    )

#    st.image(image1.data[0].url)

with col3b:
    st.write("### 🔴 3-degree scenario")
    message_placeholder2 = st.empty()
    st.session_state.full_response2 = ""

    for response in client.chat.completions.create(model=st.session_state["openai_model"],
                                                   messages=[{"role": "system", "content": "You're an policy expert that works for " + str(select) + ". Your job is to paint a vivid picture of what will happen in a given scenario that you're given to inform policy makers, but in a concise way as you're aware that policy makers are busy. Describe how " + str(select) + "will be affected by a bad 3-degree global warming scenario in a short sentence. Be concise, and use max 3 bullet points to describe your ideas. Highlight the important things in bold. Be specific when you can on the consequences to the economy. Conclude with one specific sentence about how it's worse than a 2-degree scenario, but better than a 4-degree scenario."}],
                                                   stream=True):
        st.session_state.full_response2 += response.choices[0].delta.content or ""
        message_placeholder2.markdown(st.session_state.full_response2 + "▌")

    message_placeholder2.markdown(st.session_state.full_response2)

#    image2 = client.images.generate(
#        model="dall-e-3",
#        prompt="Create a photorealistic scene of a someone in a profession in" + str(select) + "and how they would be affected by a bad 3-degree global warming scenario. \n\n DON'T WRITE ANY TEXT ON THE PICTURE.",
#        size="1024x1024",
#        quality="standard",
#        n=1,
#    )
#
#    st.image(image2.data[0].url)

with col4b:
    st.write("### 🟣 4-degree scenario")
    message_placeholder3 = st.empty()
    st.session_state.full_response3 = ""

    for response in client.chat.completions.create(model=st.session_state["openai_model"],
                                                   messages=[{"role": "system", "content": "You're an policy expert that works for " + str(select) + ". Your job is to paint a vivid picture of what will happen in a given scenario that you're given to inform policy makers, but in a concise way as you're aware that policy makers are busy. Describe how " + str(select) + "will be affected by a bad 3-degree global warming scenario in a short sentence. Be concise, and use max 3 bullet points to describe your ideas. Highlight the important things in bold. Be specific when you can on the consequences to the economy. Conclude with one specific sentence about why it's worse than all other scenarios."}],
                                                   stream=True):
        st.session_state.full_response3 += response.choices[0].delta.content or ""
        message_placeholder3.markdown(st.session_state.full_response3 + "▌")

    message_placeholder3.markdown(st.session_state.full_response3)

#    image3 = client.images.generate(
#        model="dall-e-3",
#        prompt="Create a photorealistic scene of a someone in a profession in" + str(select) + "and how they would be affected by a catastrophic 4-degree global warming scenario. \n\n DON'T WRITE ANY TEXT ON THE PICTURE.",
#        size="1024x1024",
#        quality="standard",
#        n=1,
#    )
#
#    st.image(image3.data[0].url)


st.divider()

st.markdown("<h1 style='text-align: center;'>Mapping company footprints</h1>", unsafe_allow_html=True)

def plot_sparkline(data):
    plt.figure(figsize=(2, 0.5))  # Adjust the size as needed
    plt.plot(data, color='green')
    ax = plt.gca()  # Get the current axis
    ax.get_xaxis().set_visible(False)  # Hide the x-axis
    ax.get_yaxis().set_visible(False)  # Hide the y-axis
    for spine in plt.gca().spines.values():  # Remove borders
        spine.set_visible(False)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)  # Save plot to a buffer
    plt.close()
    return buf


# Load your CSV file
df = pd.read_csv('datasets/Company Database - rev.s+emissions.csv')

search_query = st.text_input("Enter company name")


def search_data(query, data):
    if query:  # only search if there is a query
        # Simple case-insensitive search across the DataFrame
        return data[data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    return data  # return all data if no query


# Display Result
if search_query:
    # Filter DataFrame based on search query
    filtered_data = df[df['Symbol'].str.contains(search_query, case=False)]

    # Display each row in a separate box with a sparkline
    for index, row in filtered_data.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])  # Adjust column widths as needed

            with col1:
                st.subheader(row['Symbol'])
                st.text(f" Revenues 2022: {row[' Revenues 2022']}")  # Replace 'Column2'
                st.text(
                    f"Emissions 2022: {row['Emissions 2022']}")  # Replace 'Column3'# Display other data if necessary

            with col2:
                # Assuming 'YearlyData' is a column with comma-separated numbers
                for _ in range(3):  # Adjust the range for more or less padding
                    st.empty()
                data_series = [float(x) for x in row['Emissions 2022'].split(',')]
                st.image(plot_sparkline(data_series), use_column_width=True)
                st.markdown('<p style="font-weight:bold; font-size: 14px;">Carbon Emissions over time</p>',
                            unsafe_allow_html=True)
                st.empty()
                st.text(f"Esg Performance: {row['Esg Performance']}")  # Replace 'Column2'

            st.markdown("---")  # Adds a horizontal line for separation

# Custom CSS to inject contained within a Markdown
st.markdown("""
<style>
.box {
    height: 200px;
    background-color: #F3F3F3;
    border: 2px solid #FFFFFF;
    border-radius: 10px;  # Adjust for rounded corners
    padding: 50px;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)

# Layout with 2 columns
col1, col2 = st.columns(2)

# First column with two boxes
with col1:
    # First box
    st.image("datasets/emissions.png", caption="Top 10 Companies by Emissions")
    # Second box
    st.image("datasets/revenue.png", caption="Top 10 Companies by Revenue")

# Second column with two boxes
with col2:
    # Third box
    st.image("datasets/esg_score.png", caption="Top 10 Companies by ESG Score")
    # Fourth box
    st.image("datasets/fdx.png", caption="Cumulative emissions of top polluter")


st.divider()

st.markdown("<h1 style='text-align: center;'>Mapping individual investment footprints</h1>", unsafe_allow_html=True)

# Highcharts JavaScript and HTML code
highcharts_html = """
<html>

<head>

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
# Embed the Highcharts HTML in the Streamlit app
components.html(highcharts_html, height=1000)