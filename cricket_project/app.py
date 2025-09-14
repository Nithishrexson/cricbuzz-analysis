import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# Load Data
# --------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("data/cricbuzz_matches.csv")
    teams = pd.read_csv("data/teams.csv")
    series = pd.read_csv("data/series.csv")
    venues = pd.read_csv("data/venues.csv")
    return matches, teams, series, venues

matches, teams, series, venues = load_data()

# Dictionary for easy table selection
data_tables = {
    "Matches": matches,
    "Teams": teams,
    "Series": series,
    "Venues": venues
}

# --------------------------
# Sidebar Navigation
# --------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "KPIs & Metrics", "Visualizations", "User Profile"])

# --------------------------
# Helper for Title Styling
# --------------------------
def styled_title(text):
    st.markdown(
        f"""
        <div style='background-color: #001F54; padding: 15px; border-radius: 10px;'>
            <h1 style='text-align: center; color: white;'>{text}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------
# HOME PAGE
# --------------------------
if page == "Home":
    styled_title("Cricbuzz Matches Dashboard")
    st.markdown("""
    Welcome to the **Cricbuzz Cricket Dashboard**!  
    This project provides insights into cricket match data including **teams, matches, venues, and series**.  
    Use this dashboard to track performance, trends, and cricket analytics in an interactive way.

    ### Features:
    - **KPIs & Metrics:**  
      View key numbers like total matches, teams, venues, upcoming matches, and more.  
      Explore data tables directly and gain a quick overview of cricket trends.

    - **Interactive Visualizations:**  
      Analyze cricket performance with rich, colorful visualizations.  
      Identify top teams, venues, and trends over time using graphs and charts.

    - **User Profile:**  
      Learn about the dashboard creator, skills, and portfolio projects.  
      Gain context on expertise and approach to cricket data analytics.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/en/4/4e/Cricket_equipment.jpg", use_container_width=True)

# --------------------------
# KPIs & Metrics
# --------------------------
elif page == "KPIs & Metrics":
    styled_title("KPIs & Metrics")

    # KPI Metrics
    total_matches = len(matches)
    total_teams = len(teams)
    total_series = len(series)
    total_venues = len(venues)

    most_played_venue = matches['Venue'].mode()[0] if 'Venue' in matches.columns else "N/A"
    upcoming_matches = matches[matches['Match Category'].str.lower() == 'upcoming'].shape[0]
    live_matches = matches[matches['Match Category'].str.lower() == 'live'].shape[0]
    recent_matches = matches[matches['Match Category'].str.lower() == 'recent'].shape[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", total_matches)
    col2.metric("Total Teams", total_teams)
    col3.metric("Total Series", total_series)
    col4.metric("Total Venues", total_venues)

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Most Played Venue", most_played_venue)
    col6.metric("Upcoming Matches", upcoming_matches)
    col7.metric("Live Matches", live_matches)
    col8.metric("Recent Matches", recent_matches)

    # Quick Stats Table
    st.markdown("### Quick Match Stats")
    st.dataframe(matches.head(10))

    # Select Table to Display
    st.markdown("### Explore Other Tables")
    table_choice = st.selectbox("Choose a Table", list(data_tables.keys()))
    if st.button("Generate Table"):
        st.write(f"### {table_choice} Table")
        st.dataframe(data_tables[table_choice].head(20))

    # KPI Visualization
    st.markdown("### KPI Visualization - Matches by Category")
    if 'Match Category' in matches.columns:
        category_counts = matches['Match Category'].value_counts().reset_index()
        category_counts.columns = ['Match Category', 'Count']
        fig = px.bar(
            category_counts,
            x='Match Category',
            y='Count',
            color='Count',
            color_continuous_scale='blues',
            title="Matches by Category"
        )
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
        st.plotly_chart(fig, use_container_width=True)

# --------------------------
# VISUALIZATIONS
# --------------------------
elif page == "Visualizations":
    styled_title("Visualizations")

    st.markdown("### Cricket Insights Visualizations")

    # 1. Matches by City
    city_counts = matches['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Matches']
    fig1 = px.bar(city_counts, x='City', y='Matches', color='Matches', title="Matches by City", color_continuous_scale='Viridis')
    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Top 10 Teams by Matches Played
    team_counts = pd.concat([matches['Team 1'], matches['Team 2']]).value_counts().reset_index()
    team_counts.columns = ['Team', 'Matches Played']
    fig2 = px.bar(team_counts.head(10), x='Team', y='Matches Played', color='Matches Played', title="Top 10 Teams by Matches Played", color_continuous_scale='Plasma')
    fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Matches Over Years
    matches['Start Date'] = pd.to_datetime(matches['Start Date'], unit='ms', errors='coerce')
    over_years = matches.groupby(matches['Start Date'].dt.year).size().reset_index(name='Matches')
    fig3 = px.line(over_years, x='Start Date', y='Matches', markers=True, title="Matches Over Years")
    fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Top 10 Venues
    venue_counts = matches['Venue'].value_counts().reset_index()
    venue_counts.columns = ['Venue', 'Matches']
    fig4 = px.pie(venue_counts.head(10), names='Venue', values='Matches', hole=0.4, title="Top 10 Venues")
    fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
    st.plotly_chart(fig4, use_container_width=True)

    # 5. Top 10 Series
    series_counts = matches['Series'].value_counts().reset_index()
    series_counts.columns = ['Series', 'Matches']
    fig5 = px.pie(series_counts.head(10), names='Series', values='Matches', hole=0.4, title="Top 10 Series")
    fig5.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
    st.plotly_chart(fig5, use_container_width=True)

    # 6. Matches by Toss Winner
    if 'Toss Winner' in matches.columns:
        toss_counts = matches['Toss Winner'].value_counts().reset_index()
        toss_counts.columns = ['Toss Winner', 'Count']
        fig6 = px.bar(toss_counts.head(10), x='Toss Winner', y='Count', color='Count', title="Matches by Toss Winner", color_continuous_scale='Sunset')
        st.plotly_chart(fig6, use_container_width=True)

    # 7. Matches by Venue
    if 'Venue' in matches.columns:
        venue_counts = matches['Venue'].value_counts().reset_index()
        venue_counts.columns = ['Venue', 'Matches']
        fig7 = px.bar(venue_counts.head(10), x='Venue', y='Matches', color='Matches', title="Matches by Venue", color_continuous_scale='Magma')
        st.plotly_chart(fig7, use_container_width=True)

    # 8. Matches per Team (Detailed)
    team_detailed_counts = pd.concat([matches['Team 1'], matches['Team 2']]).value_counts().reset_index()
    team_detailed_counts.columns = ['Team', 'Total Matches']
    fig8 = px.scatter(team_detailed_counts, x='Team', y='Total Matches', size='Total Matches', color='Total Matches', title="Matches per Team (Detailed)")
    fig8.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
    st.plotly_chart(fig8, use_container_width=True)

# --------------------------
# USER PROFILE
# --------------------------
elif page == "User Profile":
    styled_title("User Profile")
    st.markdown("""
    **Name:** Nithish Rexson  
    **Role:** Data Analyst  
    **Skills:** Python, Pandas, MySQL, Power BI, Excel  
    **Projects:**  
    - IPL Win Prediction  
    - Flight Delay Analysis  
    - Bird Species Distribution  
    - Food Waste Management System  

    **About Me:**  
    Passionate about data analytics, visualization, and building solutions that create impact.
    """)
