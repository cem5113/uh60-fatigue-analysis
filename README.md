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

## Files Included

- `uh60_analysis.py`: Main analysis script  
- `uh60_sample_data.xlsx`: Anonymized example dataset for demonstration purposes only  

> The included dataset is synthetic and anonymized. You may replace it with your own real data matching the same structure.

## How to Run (in Google Colab)

1. Open [Google Colab](https://colab.research.google.com/)
2. Upload `uh60_analysis.py` and `sample_data.xlsx`
3. Run the code to perform statistical analysis and generate figures

## License

MIT License
