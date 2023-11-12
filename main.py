import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm


page_title = "🌎 Climate Ledger"
st.set_page_config(layout="wide")

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
    st.markdown("<p style='text-align: center;'>2022 CO2e Emissions</p>", unsafe_allow_html=True)

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
    st.markdown("<p style='text-align: center;'>Cumulative CO2e Emissions</p>", unsafe_allow_html=True)


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
    st.markdown("<p style='text-align: center;'>Actual Climate Impact*</p>", unsafe_allow_html=True)


st.markdown("<p style='text-align: center;'>👇<i> Scroll down here to continue </i>👇</p>", unsafe_allow_html=True)

@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)

renderer = get_pyg_renderer()

st.subheader("Display Explore UI")
# display explore ui, Developers can use this to prepare the charts you need to display.
renderer.render_explore()