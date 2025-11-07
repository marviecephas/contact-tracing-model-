# 🚀 Contact Tracing with Unsupervised ML (DBSCAN)

This project is a Python-based system for automating public health contact tracing. It analyzes raw, unlabeled geospatial data (latitude, longitude, and time) to discover "contact events" — instances where individuals were in close physical proximity at the same time.

Instead of traditional supervised learning, this project uses the **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) algorithm. This unsupervised approach is ideal because it does not require a pre-labeled dataset and can discover contact clusters organically.

## 🎯 The Core Problem

In a real-world scenario, we have raw location logs for many users:
`[user_id, timestamp, latitude, longitude]`

We do **not** have a label `is_contact` (Yes/No). Manually creating this label for a supervised model (like SVM or KNN) is difficult, slow, and based on arbitrary rules.

## 💡 My Solution: Unsupervised Clustering

This system uses DBSCAN to find contacts by treating the data as a series of time-slices.

### How It Works

1.  **Iterate by Time(for multiple timestamps):** The script loops through every unique timestamp (e.g., `14:01:00`, `14:02:00`, etc.) in the dataset.
2.  **Isolate Data "Slices"(if iterated):** For each timestamp, it creates a temporary "slice" of all user locations *at that exact moment*.
3.  **Run DBSCAN:** It runs the DBSCAN algorithm on this individual time-slice.
    * **`eps` (Epsilon):** This is set to our "contact distance" (e.g., 20 meters). This is the most important parameter.
    * **`min_samples`:** This is set to **2**. This defines a "cluster" as a minimum of 2 people.
    * **Metric:** We use the `haversine` metric to correctly calculate distances on a sphere (the Earth).
4.  **Assign Cluster Labels:** DBSCAN assigns a cluster ID to every point in the slice.
    * **`cluster = -1`:** This is "Noise." The person was not in contact with anyone.
    * **`cluster = 0` (or `1`, `2`...):** This is a contact event. All users with the *same cluster ID* (at the same time) are part of the same contact group.
5.  **Log Results:** The script combines the results from all time-slices into a final output file, now with a `cluster` column that identifies every contact event.

This method allows us to effectively "discover" contacts without ever needing to train a model in the traditional sense.

## 🛠️ Tech Stack

* **Python 3.x**
* **Pandas:** For loading and managing the data.
* **Scikit-learn (sklearn):** For the `DBSCAN` implementation.
* **NumPy:** For converting coordinates to radians for the Haversine calculation.
* **Matplotlib & Seaborn:** For exploratory data analysis (EDA) and visualization.
+ **Folium:** For interactive, real-world map visualization.
## ⚙️ Installation

1.  Clone this repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  It's highly recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  Install the required libraries:
    ```bash
    pip install pandas scikit-learn numpy
    ```

## 🚀 Usage

1.  Place your raw data file (e.g., `contacts.csv` or `contacts.json`) in a `data/` folder.
2.  Open the main script (e.g., `run_tracing.py`) and adjust the parameters at the top of the file:
    ```python
    # === PARAMETERS ===
    CONTACT_DISTANCE_METERS = 20  # The 'eps' radius
    MIN_PEOPLE_IN_CLUSTER = 2     # The 'min_samples'
    DATA_FILE_PATH = 'data/contacts.csv'
    OUTPUT_FILE_PATH = 'output/clustered_contacts.csv'
    # ==================
    ```
3.  Run the script:
    ```bash
    python run_tracing.py
    ```
4.  Check the `output/` folder for your results.

## 📊 Understanding the Output

The output file will be a copy of your input data with a new `cluster` column.

| user_id | timestamp | latitude | longitude | **cluster** |
| :--- | :--- | :--- | :--- | :--- |
| Alice | 2025-11-01 14:05:00 | 40.7581 | -73.9856 | **0** |
| Bob | 2025-11-01 14:05:00 | 40.7581 | -73.9856 | **0** |
| Carol | 2025-11-01 14:05:00 | 40.7128 | -74.0060 | **-1** |
| David | 2025-11-01 14:05:00 | 51.5074 | -0.1278 | **1** |
| Eve | 2025-11-01 14:05:00 | 51.5074 | -0.1278 | **1** |

**How to interpret this:**

* **Cluster 0:** At 14:05, Alice and Bob were in a contact event.
* **Cluster 1:** At 14:05, David and Eve were in a *separate* contact event.
* **Cluster -1:** At 14:05, Carol was "Noise" and not in contact with anyone.

**Important:** A `cluster 0` at 14:05 is **not** related to a `cluster 0` at 14:10. The cluster labels are unique *only within their specific time-slice*.
