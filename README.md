![GenHack 2025 Banner](https://www.polytechnique.edu/sites/default/files/styles/contenu_detail/public/content/DMAP/Genahck2025_Banni%C3%A8re.png?itok=9k8SBwh6)

# GenHack 2025: Correcting Urban Heat Island Bias in ERA5 Climate Data

**Team: BAT_TEAM**
- Tito Nicola Drugman
- Asia Montico
- Beshoy Guirges

This repository contains the complete work and findings of Team BAT_TEAM for the **GenHack 2025 challenge**, a four-week hackathon focused on Urban Heat Islands and Climate Downscaling, organized by École Polytechnique, the BNP Paribas “Stress Test” Chair and Kayrros.

## Project Goal

The core problem we address is the systematic bias in ERA5-Land climate data, a coarse-resolution (9km x 9km) product that "averages" temperatures over large areas. This averaging often underestimates the maximum temperature in dense urban environments, failing to capture the full extent of the Urban Heat Island (UHI) effect observed by sparse ground stations.

Our goal was to **build a Machine Learning model to predict and correct this bias** (referred to as `delta_temp`). By applying this predicted delta to the ERA5 baseline, we can effectively downscale climate data and generate hyper-local temperature estimates for any location, even where no ground sensors exist.

## Key Results & Findings

Our work successfully demonstrates a viable method for correcting systematic ERA5 temperature bias.

- **High-Performance Model:** We developed a **Random Forest Regressor** that significantly improves temperature prediction accuracy.
- **Error Reduction:** The model reduced the **Root Mean Square Error (RMSE)** of raw ERA5 data by **~35%** (from 3.01°C to 1.94°C) and the **Mean Absolute Error (MAE)** by **45%** (from 2.29°C to 1.26°C) on the hold-out test set.
- **Bias Correction:** The model effectively corrects the systematic underestimation of temperature in urban areas, reducing the average bias from **1.72°C to just 0.12°C**.
- **Key Predictive Features:** Feature importance analysis revealed that **topographical and geographical factors (elevation, latitude, longitude)** are the strongest predictors of temperature bias, followed by seasonality and the percentage of urban land cover.

| Metric | ERA5 Raw | ERA5 + RF Correction | Improvement |
| :--- | :---: | :---: | :---: |
| **RMSE (°C)** | 3.01 | 1.94 | **-35.5%** |
| **MAE (°C)** | 2.29 | 1.26 | **-45.0%** |
| **Bias (°C)** | 1.72 | 0.12 | **-93.0%** |


## Methodology

Our approach was structured across the four periods of the GenHack, building from data exploration to a final predictive model.

### 1. Land Cover Analysis & Zonation
To understand the underlying surface characteristics, we classified land cover into distinct climatological zones (Urban, Suburban, Vegetation).
- We used **Sentinel-2** imagery to derive the Normalized Difference Vegetation Index (NDVI) as a primary metric for land cover segmentation.
- A key challenge was resolving "spectral ambiguity," where deep water and dense urban surfaces both show low NDVI values. We implemented a **data fusion** technique by integrating **JRC Global Surface Water** data, which uses a 37-year history to validate water presence and accurately separate hydrography from urban areas.
- This process allowed us to generate accurate land use fractions (%Urban, %Forest, etc.) for each 9km x 9km ERA5 grid cell.

### 2. Interactive Spatio-Temporal Visualization
We developed an interactive dashboard to explore the temporal dynamics of the ERA5-Land dataset. The tool visualizes daily spatial distributions of Total Precipitation, Wind Vectors and Maximum Temperature, allowing for the inspection of specific meteorological events.

### 3. Predictive Modeling of Temperature Bias (`delta_temp`)
This was the core of our project, where we trained a model to predict the temperature difference between ground truth (ECA&D stations) and the ERA5 model.
- **Target Variable**: `delta_temp = TX_station - TX_ERA5`
- **Features Used**: A combination of spatio-temporal context, atmospheric dynamics and land cover data.
  - **Spatio-Temporal**: `latitude`, `longitude`, `elevation` and cyclical date features (`sin_day`, `cos_day`).
  - **Atmospheric (ERA5)**: `wind_speed`, `precipitation` and wind vector components.
  - **Land Cover**: `ndvi_local` (at station), `ndvi_global` (9km grid average) and land use fractions (`perc_urban`, `perc_forest`, etc.).
- **Model Selection**: We evaluated several models, including Linear Regression, Gradient Boosting and a Random Forest. The **Random Forest Regressor** was selected for its robustness to outliers, ability to capture non-linear interactions essential for UHI and its superior performance (Test Set R² = 0.38).
- **Validation**: To ensure our model learned general physical laws rather than memorizing station-specific patterns, we used a **station-based split** for our training, validation and test sets.

## Data Sources

- **Admin Boundaries**: GADM, Database of Global Administrative Areas (Europe subset).
- **Meteorological Data**: ERA5-Land Daily Statistics (2020-2025) for temperature, precipitation and wind.
- **Vegetation Index**: Sentinel-2 NDVI data (2020-2023) at 80m resolution.
- **Weather Stations**: European Climate Assessment & Dataset (ECA&D) for daily maximum temperature (TX) ground truth.

## Repository Structure

The repository is organized to separate analysis notebooks from presentations, scripts and results.

```
.
├── notebooks/
│   ├── build_training_set.ipynb   # Data preparation and feature engineering
│   ├── dataset_analysis.ipynb     # Initial exploration of datasets
│   ├── explanatory_model (1).ipynb   # Analysis and interpretation of the final model
│   ├── map_explorer.ipynb            # Interactive visualizations
│   ├── period1_exploration.ipynb     # Week 1 exploratory data analysis
│   ├── period1_exploration_v3.ipynb  # Further exploration
│   ├── period2_practice11.ipynb      # Week 2 work and visualizations
│   └── train.ipynb                   # Main model training and hyperparameter tuning script
├── presentation/
│   ├── Final Presentation_compressed.pdf
│   └── period2_slides.pdf
├── results/
│   ├── 3D_Roma.html
│   └── ... (Other HTML and image outputs)
├── scripts/
│   └── find_city.py                  # Utility script to find city data in GADM
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites
- Python >= 3.10
- We recommend using a virtual environment (e.g., venv or conda).

### Installation & Execution
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TitoNicolaDrugman/GENHACK.git
    cd GENHACK
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    A `requirements.txt` file is provided that lists all dependencies.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the data:**
    Download the GenHack dataset from the [official Google Drive folder](https://drive.google.com/drive/folders/1_uMrrq63e0iYCFj8A6ehN58641sJZ2x1?usp=drive_link) and place the contents into a `data/` directory in the root of this project. (This directory is ignored by Git).

5.  **Run the notebooks:**
    Launch Jupyter Lab to explore the analysis and modeling workflow.
    ```bash
    jupyter lab
    ```

## Acknowledgments
We extend our thanks to the organizers of GenHack 2025 at **École Polytechnique**, the **BNP Paribas “Stress Test” Chair** and **Kayrros** for providing the data and the opportunity to work on this challenging and rewarding project.

<p align="left">
  <img src="https://www.polytechnique.edu/sites/default/files/nc-project/footer/logo.png" height="50">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://www.polytechnique.edu/sites/default/files/styles/nc_editor_image/public/content/DMAP/1%2C4%20copie.png?itok=ra_c9AVi" height="50">
</p>
```

