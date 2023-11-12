import os
import streamlit as st
import streamlit.components.v1 as components
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import numpy as np
from openai import OpenAI

client = OpenAI()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106"

st.set_page_config(
    page_title="🌎 Climate Ledger",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>🌎 Climate Ledger</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    components.html("""
      <div id="globeViz1"></div>

      <script src="//unpkg.com/globe.gl"></script>
      <script>
        const world = Globe()
          (document.getElementById('globeViz1'))
          .backgroundColor('#FFFFFF')
          .globeImageUrl('//unpkg.com/three-globe/example/img/earth-day.jpg')
          .pointOfView({ altitude: 4 }, 5000)
          .polygonCapColor(feat => 'rgba(100, 100, 100, 0.6)')
          .polygonSideColor(() => 'rgba(100, 100, 100, 0.3)')
          .polygonLabel(({ properties: d }) => `
              <b>${d.ADMIN} (${d.ISO_A2})</b> <br />
              Population: <i>${Math.round(+d.POP_EST / 1e4) / 1e2}M</i>
            `);

        // Auto-rotate
        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 1.8;

        fetch('https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/ne_110m_admin_0_countries.geojson').then(res => res.json()).then(countries => {
          world.polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'));

          setTimeout(() => world
            .polygonsTransitionDuration(2000)
            .polygonAltitude(feat => Math.max(0.02, Math.sqrt(+feat.properties.POP_EST) * 3e-5))
          , 1000);
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
              Population: <i>${Math.round(+d.POP_EST / 1e4) / 1e2}M</i>
            `);

        // Auto-rotate
        world2.controls().autoRotate = true;
        world2.controls().autoRotateSpeed = 1.8;

        fetch('https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/ne_110m_admin_0_countries.geojson').then(res => res.json()).then(countries => {
          world2.polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'));

          setTimeout(() => world2
            .polygonsTransitionDuration(2000)
            .polygonAltitude(feat => Math.max(0.02, Math.sqrt(+feat.properties.POP_EST) * 3e-5))
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
              Population: <i>${Math.round(+d.POP_EST / 1e4) / 1e2}M</i>
            `);

        // Auto-rotate
        world3.controls().autoRotate = true;
        world3.controls().autoRotateSpeed = 1.8;

        fetch('https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/ne_110m_admin_0_countries.geojson').then(res => res.json()).then(countries => {
          world3.polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'));

          setTimeout(() => world3
            .polygonsTransitionDuration(2000)
            .polygonAltitude(feat => Math.max(0.02, Math.sqrt(+feat.properties.POP_EST) * 3e-5))
          , 3000);
        });
      </script>
    """, height=500)
    st.markdown("<p style='text-align: center;'><b>Actual Climate Impact</b>*</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>👇<i> Scroll down here to continue </i>👇</p>", unsafe_allow_html=True)

col1a, col2a, col3a = st.columns(3)

select = st.empty

with col2a:
    select = st.selectbox("Country Selection", {"Germany", "USA", "Canada"}, placeholder="Choose an country")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

df = pd.read_csv(
    "https://raw.githubusercontent.com/janik-sauerbier/mit_energy_and_climate_hack_ledgerlings/main/datasets/owid-co2-data.csv")

st.area_chart(chart_data)

col1b, col2b, col3b, col4b = st.columns(4)

with col1b:
    st.write("### 💡 Note for policymakers")
    st.markdown("In the fight against climate change, understanding the distinct roles of ***carbon dioxide (CO2)*** and ***methane (CH4)*** is essential. CO2, with its long atmospheric lifespan of ***300 to 1,000 years***, demands strategies for deep, long-term reductions. However, it's equally important not to overlook methane. Although it remains in the atmosphere for a shorter period (about 12 years), ***methane is over 25 times more potent than CO2*** in trapping heat in the short term. \n\nThis potency makes focusing on methane crucial. Reducing methane emissions can provide ***immediate and significant benefits*** in slowing global warming, complementing the longer-term efforts to reduce CO2. Your decisions should balance these considerations, ensuring a comprehensive approach to both immediate and enduring climate challenges. Act wisely; your choices today will shape our environmental legacy.")

with col2b:
    st.write("### 🟡 2-degree scenario")
    message_placeholder = st.empty()
    st.session_state.full_response = ""

    for response in client.chat.completions.create(model=st.session_state["openai_model"],
                                                 messages=[{"role": "system", "content": "Describe vividly how " + select + " would specifically be affected by a 2-degree global warming scenario in two paragraphs (100 words) and highlight the most important aspects bold."}], stream=True):
        st.session_state.full_response += response.choices[0].delta.content or ""
        message_placeholder.markdown(st.session_state.full_response + "▌")

    message_placeholder.markdown(st.session_state.full_response)

    image1 = client.images.generate(
        model="dall-e-3",
        prompt="Paint vividly how " + select + " would be affected by a 2-degree global warming scenario. \n\n DON'T WRITE ANY TEXT ON THE PICTURE.",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    st.image(image1.data[0].url)

with col3b:
    st.write("### 🔴 3-degree scenario")
    message_placeholder2 = st.empty()
    st.session_state.full_response2 = ""

    for response in client.chat.completions.create(model=st.session_state["openai_model"],
                                                   messages=[{"role": "system", "content": "Describe vividly how " + select + " would specifically be affected by a 3-degree global warming scenario in two paragraphs (100 words) and highlight the most important aspects bold."}],
                                                   stream=True):
        st.session_state.full_response2 += response.choices[0].delta.content or ""
        message_placeholder2.markdown(st.session_state.full_response2 + "▌")

    message_placeholder2.markdown(st.session_state.full_response2)

    image2 = client.images.generate(
        model="dall-e-3",
        prompt="Paint vividly how " + select + " would be affected by a bad 3-degree global warming scenario. \n\n DON'T WRITE ANY TEXT ON THE PICTURE.",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    st.image(image2.data[0].url)

with col4b:
    st.write("### 🟣 4-degree scenario")
    message_placeholder3 = st.empty()
    st.session_state.full_response3 = ""

    for response in client.chat.completions.create(model=st.session_state["openai_model"],
                                                   messages=[{"role": "system", "content": "Describe vividly how " + select + " would specifically be affected by a 4-degree global warming scenario in two paragraphs (100 words) and highlight the most important aspects bold."}],
                                                   stream=True):
        st.session_state.full_response3 += response.choices[0].delta.content or ""
        message_placeholder3.markdown(st.session_state.full_response3 + "▌")

    message_placeholder3.markdown(st.session_state.full_response3)

    image3 = client.images.generate(
        model="dall-e-3",
        prompt="Paint vividly " + select + " would be affected by a catastrophic 4-degree global warming scenario. \n\n DON'T WRITE ANY TEXT ON THE PICTURE.",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    st.image(image3.data[0].url)

