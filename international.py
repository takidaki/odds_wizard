import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import io

# Dictionary of countries and leagues
leagues_dict = {
    "England": ["UK1", "UK2", "UK3", "UK4", "UK5", "UK6N", "UK6S", "UK7N"],
    "Germany": ["DE1", "DE2", "DE3", "DE4SW", "DE4W", "DE4N", "DE4NO", "DE4B"],
    "Italy": ["IT1", "IT2", "IT3C", "IT3B", "IT3A"],
    "Spain": ["ES1", "ES2", "ES3G1", "ES3G2", "ES3G3", "ES3G4", "ES3G5"],
    "France": ["FR1", "FR2", "FR3"],
    "Sweden": ["SW1", "SW2", "SW3S", "SW3N"],
    "Netherlands": ["NL1", "NL2", "NL3"],
    "Russia": ["RU1", "RU2"],
    "Portugal": ["PT1", "PT2"],
    "Austria": ["AT1", "AT2", "AT3O", "AT3T", "AT3M", "AT3W", "AT3V"],
    "Denmark": ["DK1", "DK2", "DK3G1", "DK3G2"],
    "Greece": ["GR1", "GR2"],
    "Norway": ["NO1", "NO2", "NO3G1", "NO3G2"],
    "Czech-Republic": ["CZ1", "CZ2"],
    "Turkey": ["TU1", "TU2", "TU3B", "TU3K"],
    "Belgium": ["BE1", "BE2"],
    "Scotland": ["SC1", "SC2", "SC3", "SC4"],
    "Switzerland": ["CH1", "CH2"],
    "Finland": ["FI1", "FI2", "FI3A", "FI3B", "FI3C"],
    "Ukraine": ["UA1", "UA2"],
    "Romania": ["RO1", "RO2"],
    "Poland": ["PL1", "PL2", "PL3"],
    "Croatia": ["HR1", "HR2"],
    "Belarus": ["BY1", "BY2"],
    "Israel": ["IL1", "IL2"],
    "Iceland": ["IS1", "IS2", "IS3", "IS4"],
    "Cyprus": ["CY1", "CY2"],
    "Serbia": ["CS1", "CS2"],
    "Bulgaria": ["BG1", "BG2"],
    "Slovakia": ["SK1", "SK2"],
    "Hungary": ["HU1", "HU2"],
    "Kazakhstan": ["KZ1", "KZ2"],
    "Bosnia-Herzegovina": ["BA1"],
    "Slovenia": ["SI1", "SI2"],
    "Azerbaijan": ["AZ1"],
    "Ireland": ["IR1", "IR2"],
    "Latvia": ["LA1", "LA2"],
    "Georgia": ["GE1", "GE2"],
    "Kosovo": ["XK1"],
    "Albania": ["AL1"],
    "Lithuania": ["LT1", "LT2"],
    "North-Macedonia": ["MK1"],
    "Armenia": ["AM1"],
    "Estonia": ["EE1", "EE2"],
    "Northern Ireland": ["NI1", "NI2"],
    "Malta": ["MT1"],
    "Luxembourg": ["LU1"],
    "Wales": ["WL1"],
    "Montenegro": ["MN1"],
    "Moldova": ["MD1"],
    "Färöer": ["FA1"],
    "Gibraltar": ["GI1"],
    "Andorra": ["AD1"],
    "San Marino": ["SM1"],
    "Brazil": ["BR1", "BR2", "BR3", "BRC", "BRGA"],
    "Mexico": ["MX1", "MX2"],
    "Argentina": ["AR1", "AR2", "AR3F", "AR5", "AR3", "AR4"],
    "USA": ["US1", "US2", "US3"],
    "Colombia": ["CO1", "CO2"],
    "Ecuador": ["EC1", "EC2"],
    "Paraguay": ["PY1", "PY2"],
    "Chile": ["CL1", "CL2"],
    "Uruguay": ["UY1", "UY2"],
    "Costa-Rica": ["CR1", "CR2"],
    "Bolivia": ["BO1"],
    "Guatemala": ["GT1", "GT2"],
    "Dominican-Rep.": ["DO1"],
    "Honduras": ["HN1"],
    "Venezuela": ["VE1"],
    "Peru": ["PE1", "PE2"],
    "Panama": ["PA1"],
    "El-Salvador": ["SV1"],
    "Jamaica": ["JM1"],
    "Nicaragua": ["NC1"],
    "Canada": ["CA1"],
    "Haiti": ["HT1"],
    "Japan": ["JP1", "JP2", "JP3"],
    "South-Korea": ["KR1", "KR2", "KR3"],
    "China": ["CN1", "CN2", "CN3"],
    "Iran": ["IA1", "IA2"],
    "Australia": ["AU1", "AU2V", "AU2NSW", "AU2Q", "AU2S", "AU2W"],
    "Saudi-Arabia": ["SA1", "SA2"],
    "Thailand": ["TH1", "TH2"],
    "Qatar": ["QA1", "QA2"],
    "United Arab Emirates": ["AE1", "AE2"],
    "Indonesia": ["ID1", "ID2"],
    "Jordan": ["JO1"],
    "Syria": ["SY1"],
    "Uzbekistan": ["UZ1"],
    "Malaysia": ["MY1", "MY2"],
    "Vietnam": ["VN1", "VN2"],
    "Iraq": ["IQ1"],
    "Kuwait": ["KW1"],
    "Bahrain": ["BH1"],
    "Myanmar": ["MM1"],
    "Palestine": ["PS1"],
    "India": ["IN1", "IN2"],
    "New-Zealand": ["NZ1"],
    "Hong-Kong": ["HK1", "HK2"],
    "Oman": ["OM1"],
    "Taiwan": ["TW1"],
    "Tajikistan": ["TJ1"],
    "Turkmenistan": ["TM1"],
    "Lebanon": ["LB1"],
    "Bangladesh": ["BD1"],
    "Singapore": ["SG1"],
    "Cambodia": ["KH1"],
    "Kyrgyzstan": ["KG1"],
    "Egypt": ["EG1", "EG2"],
    "Algeria": ["DZ1", "DZ2"],
    "Tunisia": ["TN1", "TN2"],
    "Morocco": ["MA1", "MA2"],
    "South-Africa": ["ZA1", "ZA2"],
    "Kenya": ["KE1", "KE2"],
    "Zambia": ["ZM1"],
    "Ghana": ["GH1"],
    "Nigeria": ["NG1"],
    "Uganda": ["UG1"],
    "Burundi": ["BI1"],
    "Rwanda": ["RW1"],
    "Cameroon": ["CM1"],
    "Tanzania": ["TZ1"],
    "Gambia": ["GM1"],
    "Sudan": ["SD1"]
}

# Function to fetch team rating table
def fetch_table(country, league, table_type="home"):
    url = f"https://www.soccer-rating.com/{country}/{league}/{table_type}/"
    try:
        response = requests.get(url)
        response.encoding = 'latin1'  # Force latin1 encoding
        
        # Parse with BeautifulSoup first
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Try to find the table using BeautifulSoup
        tables_html = soup.find_all('table')
        
        if len(tables_html) > 14:
            # Convert the specific table to string and then use pandas
            table_html = str(tables_html[14])
            # Use pandas with explicit encoding
            rating_table = pd.read_html(table_html, encoding='latin1', flavor='lxml')[0]
            return rating_table
        else:
            st.warning(f"Could not find enough tables on the page. Found {len(tables_html)} tables.")
            return None
        
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None
    except ValueError as e:
        st.error(f"Error parsing tables: {e}")
        # Add more detailed error information
        st.error(f"URL attempted: {url}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None


def show():
    """Display the international odds calculator page"""
    st.set_page_config(page_title="Odds Wizard", page_icon="⚽")  # Set the title and icon
    # Add custom CSS with Montserrat font
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

    body, .stButton button, .stSelectbox, .stTextInput, div.stMarkdown, h1, h2, h3, h4, h5, h6, p {
        font-family: 'Montserrat', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("International Odds Calculator")
    st.markdown("Compare teams from different leagues and calculate match odds")

    # Add a sidebar
    st.sidebar.header("Select Teams")

    # Select countries and leagues in sidebar
    country1 = st.sidebar.selectbox("First Country:", list(leagues_dict.keys()), key="country1")
    league1 = st.sidebar.selectbox("First League:", leagues_dict[country1], key="league1")

    # Add some space in sidebar
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Select second country (different from first)
    available_countries = [c for c in leagues_dict.keys() if c != country1]
    country2 = st.sidebar.selectbox("Second Country:", available_countries, key="country2")
    league2 = st.sidebar.selectbox("Second League:", leagues_dict[country2], key="league2")

    # Add information about international odds
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    **About International Odds**
    - Compares teams across different leagues
    - Accounts for league strength differences
    - Uses global rating system
    - Updates after international matches
    """)

    # Main content area
    st.header("Compare Teams")

    # Fetch tables when leagues are selected
    if league1 and league2:
        table1 = fetch_table(country1, league1, "home")
        table2 = fetch_table(country2, league2, "away")

        if table1 is not None and table2 is not None:
            # Create columns for team selection and display
            select_col1, select_col2 = st.columns(2)

            # Select teams in columns
            with select_col1:
                team1 = st.selectbox(" ", table1.iloc[:, 1].sort_values(), key="team1", label_visibility="collapsed")
                team1_data = table1[table1.iloc[:, 1] == team1]
                st.markdown("<div style='text-align: center; margin-top: 10px;'>**Home Rating**</div>", unsafe_allow_html=True)
                rating1 = float(team1_data.iloc[0, -1])
                st.markdown(f"<div style='text-align: center;'><span style='font-size: 18px; color: #1f77b4; font-weight: bold;'>{rating1:.1f}</span></div>", unsafe_allow_html=True)

            with select_col2:
                team2 = st.selectbox(" ", table2.iloc[:, 1].sort_values(), key="team2", label_visibility="collapsed")
                team2_data = table2[table2.iloc[:, 1] == team2]
                st.markdown("<div style='text-align: center; margin-top: 10px;'>**Away Rating**</div>", unsafe_allow_html=True)
                rating2 = float(team2_data.iloc[0, -1])
                st.markdown(f"<div style='text-align: center;'><span style='font-size: 18px; color: #ff7f0e; font-weight: bold;'>{rating2:.1f}</span></div>", unsafe_allow_html=True)

            # Calculate win probabilities
            home = 10**(rating1 / 400)
            away = 10**(rating2 / 400)
            total = home + away
            home_win_prob = home / total
            away_win_prob = away / total

            # Set default draw probability based on home win probability
            if 0.01 <= home_win_prob <= 0.10:
                default_draw_prob = 0.14
            elif 0.11 <= home_win_prob <= 0.19:
                default_draw_prob = 0.19
            elif 0.20 <= home_win_prob <= 0.25:
                default_draw_prob = 0.22
            elif 0.26 <= home_win_prob <= 0.35:
                default_draw_prob = 0.26
            elif 0.36 <= home_win_prob <= 0.45:
                default_draw_prob = 0.28
            elif 0.46 <= home_win_prob <= 0.70:
                default_draw_prob = 0.26
            elif 0.71 <= home_win_prob <= 0.75:
                default_draw_prob = 0.22
            elif 0.76 <= home_win_prob <= 0.80:
                default_draw_prob = 0.18
            elif 0.81 <= home_win_prob <= 0.90:
                default_draw_prob = 0.16
            elif 0.91 <= home_win_prob <= 0.95:
                default_draw_prob = 0.14
            elif 0.96 <= home_win_prob <= 0.99:
                default_draw_prob = 0.11
            else:
                default_draw_prob = 0.26

            # Add draw probability slider
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Match Probabilities and Odds")
            draw_prob_slider = st.slider("Select Draw Probability:", 0.05, 0.4, default_draw_prob, 0.01, 
                                    key="draw_prob_slider", 
                                    help="Adjust the probability of a draw for the match.")

            # Recalculate probabilities with draw
            remaining_prob = 1 - draw_prob_slider
            home_win = home_win_prob * remaining_prob
            away_win = away_win_prob * remaining_prob
            
            # Calculate odds
            home_odds = 1 / home_win if home_win > 0 else float('inf')
            away_odds = 1 / away_win if away_win > 0 else float('inf')
            draw_odds = 1 / draw_prob_slider if draw_prob_slider > 0 else float('inf')

            # Display probabilities
            prob_col1, vs_col, prob_col2 = st.columns([2, 1, 2])

            with prob_col1:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <span style='font-size: 14px; color: #1f77b4;'>{team1.encode('utf-8').decode('utf-8')}</span><br>
                    <span style='font-size: 16px; color: #1f77b4; font-weight: bold;'>Win: {home_win:.1%}</span><br>
                    <span style='font-size: 14px; color: #666;'>Odds: {home_odds:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

            with vs_col:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <span style='font-size: 14px; color: #2c3e50;'>Draw</span><br>
                    <span style='font-size: 16px; color: #2c3e50; font-weight: bold;'>{draw_prob_slider:.1%}</span><br>
                    <span style='font-size: 14px; color: #666;'>Odds: {draw_odds:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

            with prob_col2:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <span style='font-size: 14px; color: #ff7f0e;'>{team2.encode('utf-8').decode('utf-8')}</span><br>
                    <span style='font-size: 16px; color: #ff7f0e; font-weight: bold;'>Win: {away_win:.1%}</span><br>
                    <span style='font-size: 14px; color: #666;'>Odds: {away_odds:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

            # Add CSS for cards
            st.markdown("""
            <style>
            .odds-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.2s;
            }
            .odds-card:hover {
                transform: translateY(-5px);
            }
            .odds-title {
                color: #666;
                font-size: 16px;
                margin-bottom: 10px;
            }
            .odds-value {
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0;
            }
            .home-odds { color: #1f77b4; }
            .draw-odds { color: #2c3e50; }
            .away-odds { color: #ff7f0e; }
            </style>
            """, unsafe_allow_html=True)

            # Display odds as cards
            st.markdown("### Match Odds")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class='odds-card'>
                    <div class='odds-title'>Home Win (1)</div>
                    <div class='odds-value home-odds'>{home_odds:.2f}</div>
                    <div style='color: #666;'>{home_win:.1%}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class='odds-card'>
                    <div class='odds-title'>Draw (X)</div>
                    <div class='odds-value draw-odds'>{draw_odds:.2f}</div>
                    <div style='color: #666;'>{draw_prob_slider:.1%}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class='odds-card'>
                    <div class='odds-title'>Away Win (2)</div>
                    <div class='odds-value away-odds'>{away_odds:.2f}</div>
                    <div style='color: #666;'>{away_win:.1%}</div>
                </div>
                """, unsafe_allow_html=True)

            # Display rating comparison
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Rating Comparison")
            rating_diff = abs(rating1 - rating2)
            better_team = team1 if rating1 > rating2 else team2
            rating_gap = "Very Close" if rating_diff < 50 else "Moderate" if rating_diff < 100 else "Significant"
            
            st.markdown(f"""
            <div style='text-align: center;'>
                <span style='font-size: 16px;'>Rating Difference: <strong>{rating_diff:.1f}</strong></span><br>
                <span style='font-size: 14px; color: #666;'>Gap: {rating_gap}</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.warning("Could not fetch data for selected leagues.")

if __name__ == "__main__":
    show()


