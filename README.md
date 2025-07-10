# UH-60 Black Hawk Pilot Fatigue Analysis
This repository contains statistical analyses and visualizations based on physiological and subjective fatigue data collected from UH-60 Black Hawk helicopter pilots and copilots during real missions.

## Study Summary

- **Platform:** UH-60 Black Hawk helicopter
- **Subjects:** Pilots and copilots
- **Phases analyzed:** Pre-flight, In-flight, Post-flight
- **Metrics:**
  - Oxygen saturation (SpO₂)
  - Heart rate (BPM)
  - Samn-Perelli Fatigue Score

## Analyses Performed

- Paired t-tests across flight phases
- Independent t-tests between roles
- Shapiro-Wilk normality test
- Effect size: Cohen’s d
- Visualizations (boxplots, violin plots, line plots)

## File List

- `uh60_flight_fatigue_analysis.ipynb`: Main analysis notebook
- `sample_data.xlsx`: Example dataset (you can upload your own)

## How to Run (in Google Colab)

1. Open [Google Colab](https://colab.research.google.com/)
2. Upload the notebook and your `.xlsx` data file
3. Run the cells to generate analysis and figures

## License

MIT License
