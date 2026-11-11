# Financial Performance Dashboard — Portfolio Project

An interactive financial controlling dashboard built with **Python, Streamlit, Pandas and Plotly**.

## Dashboard features
- Executive KPI overview: revenue, budget variance, gross margin, operating expenses and simplified operating result.
- Monthly revenue trend: Actual vs Budget vs Prior Year.
- Regional performance and revenue mix.
- Cost of sales and operating expenses analysis.
- Establishment-level drilldown table.
- Interactive filters for region, establishment and month.
- Automatically generated management takeaways.
- KPI definitions and methodology.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

## Publish online with GitHub + Streamlit Community Cloud
1. Create a GitHub account at https://github.com if you do not already have one.
2. Create a **new public repository**, for example `financial-kpi-dashboard`.
3. Upload these project files to the repository:
   - `app.py`
   - `requirements.txt`
   - `Financial_Data_English.csv`
   - `README.md`
4. Go to https://share.streamlit.io/ and sign in with GitHub.
5. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
6. Deploy. Streamlit will install the packages in `requirements.txt` and publish your dashboard with a shareable URL.

## Important
The dataset is simulated for portfolio and learning purposes. Do not present it as confidential data from a former employer. Clearly label it as a fictional case study in your CV, LinkedIn and interviews.

## Suggested portfolio description
**Financial Performance Dashboard | Python, Streamlit, Pandas, Plotly**
Designed an interactive financial dashboard to monitor revenue, budget variances, gross margin and operating expenses across multiple regions and establishments. Added monthly trend analysis, drill-down filters and management insights to support performance monitoring and decision-making.


## Version 2 — presentation polish
- Corrected the operating-expense variance colour: an expense overrun is now shown as unfavourable.
- Added a clear variance convention note.
- Refined the visual theme with a consistent finance palette.
- Updated management commentary to label operating expense variances as favourable/unfavourable.

### Update an already deployed app
Upload the updated `app.py` and the `.streamlit/config.toml` file to the root of your GitHub repository (create the `.streamlit` folder first if needed). Keep the dataset and `requirements.txt` unchanged. Streamlit Cloud will automatically redeploy after the GitHub commit.


## Version 3 — profitability and executive insights
- Added gross margin analysis by region.
- Added establishment profitability ranking, including gross profit, gross margin and simplified operating result.
- Added dynamic executive highlights and management actions based on the selected filters.
- Added a comparison of highest- and lowest-margin performers to guide further investigation.

## Portfolio summary
**Financial Performance & Profitability Dashboard | Python, Streamlit, Pandas, Plotly**

Built an interactive management reporting dashboard to monitor revenue performance, budget variances, gross margin and operating expenses across a multi-site business. Developed regional and establishment-level profitability analysis, performance rankings and management recommendations to support financial decision-making. Used a simulated dataset for confidentiality and portfolio purposes.
