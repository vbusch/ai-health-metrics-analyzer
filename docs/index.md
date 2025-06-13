## Analyzing the Relationship Between Food Intake and Garmin Health Metrics Using AI

**Problem Statement:**  
Can AI be used to analyze the relationship between food intake and Garmin health metrics? Specifically, can it identify correlations similar to an elimination diet, revealing how certain foods impact health markers such as heart rate?

**Goal:**  
To evaluate the feasibility and effectiveness of using AI to analyze personal health data and draw actionable insights. Specifically, to determine if AI can reveal dietary triggers for changes in heart rate and other metrics.

**Methodology:**  
Leveraging AI tools, particularly Gemini, to assist in building an AI project. This iterative approach provides the ability to test AI's capability to generate code and analysis suggestions.  Also use local ollama with granite 3.3 for LLM recommendations.  Along with Jetbrains AI plugin and Proxy AI plugin, for IDE related code suggestions and generations.

**Steps:**

1. **Project Planning:**
    * Gemini provided a project overview, breaking down the process into the following stages:
        * Data Exploration and Acquisition
        * Data Preprocessing and Cleaning
        * Exploratory Data Analysis (EDA)
        * Feature Selection and Model Building
        * Interpretation and Insights
    * These 5 stages were used to organize the progress of the project.
2. **Data Acquisition:**
    * Utilized Chronometer (recommended by Gemini) for detailed food intake data export, including specific food items. MyFitnessPal is another common data source, but its export does not include the food names.
    * Obtained health metrics data from Garmin, which also offers an export feature.
3. **Data Cleaning and Preprocessing:**
    * To keep it simple, the initial run only used Garmin heart-rate data.
    * Python was recommended by Gemini as the programming language.
    * Gemini Coding Partner was used to generate many of the code snippets.
    * Gemini encountered challenges with Garmin .fit binary files; initial Gemini-generated code relied on an outdated Python 2 library. When I asked for code snippets based on the garmin python SDK documentation instead, the produced code didn’t match or work.
4. **Exploratory Data Analysis (EDA):**
    * Used Pandas to merge food diary and heart rate readings based on timestamps.  Gemini was helpful here
    * Initially the goal was to have a feature that covered dairy; Gemini suggested others as well:
        * \`dairy\_consumed\_last\_3\_days\`
        * \`days\_since\_last\_dairy\`
        * \`daily\_total\_sugar\_consumed\`
        * \`time\_of\_day\`
        * \`heart\_rate\_rolling\_avg\_1H\`
        * \`heart\_rate\_rolling\_avg\_3H\`
    * Visualized the results using charts.
5. **Feature Selection and Model Building:**
    * Gemini provided an example of using a sklearn linear regression model.
    * Explored using an LLM (Ollama with granite3.3:2b) for analysis.
6. **Interpretation and Insights:**

   The goal was to have it provide insight on the relationship between dairy and heart rate.  A bonus would be if it could identify others.

    * **Granite LLM:** Struggled with summarizing data effectively and provided inaccurate or generalized information, even with specific prompts.  The merged data and features were provided to it in json format.
    * **Linear Regression:** Identified a correlation between dairy consumption and heart rate, and time of day's impact on morning heart rate.  These were concrete, but required me to do most of the data preparation.
    * **Combined Analysis:** Granite LLM provided better insights when provided the linear regression coefficients to analyze.

   Finding: Linear regression was able to identify known correlations with the data. LLM was able to use those correlations to provide suggestions.

   Example Output: 
   > Based on your data, it's challenging to perform a precise linear regression without having more statistical data points and a clear predictand. However, I can provide some general observations:
   > 
   > 1. **Dairy Consumption**: The last dairy consumption was noted on 2025-05-15 (day 4), which coincides with your highest heart rate episodes (82.99 and 84.66) on that day, as well as on 2025-05-13 (day 7). This might suggest a potential link between dairy consumption and increased heart rates, but it's not definitive. Remember to monitor this trend over more days.
   > 2. **Total Sugar Consumption**: You consistently consumed less than 140g of sugar daily, and your maximum heart rate was below the high threshold (90). There's no clear pattern here that would suggest a strong correlation with higher heart rates based on the provided data alone.
   > 3. **Time of Day**: There isn't enough data to establish any linear regression relationship between time slots (morning, afternoon, evening) and your heart rate.
   > 4. **Energy Intake vs Heart Rate**: You average about 1500kcal daily and your protein intake is also in the range of 70g/day, while net carbs are at around 139g/day. This level of calorie intake could support moderate physical activity levels. Your heart rate is generally below your maximum (85 bpm), indicating good cardiovascular health.
   >
   > Please note: Correlation does not imply causation, and these observations are speculative based on limited data. It's crucial to maintain consistent tracking over a longer period for more reliable results. Always consult with a healthcare professional or registered dietitian for personalized advice.
   > 
   > To optimize your goals (muscle gain, improved cardiovascular health, and energy), consider the following:
   >
   > 1. **Protein**: Ensure you're getting adequate protein as it’s crucial for muscle synthesis. Maintain protein intake around 70g/day, considering your body weight in kg (about 2.2 is a standard conversion factor).
   > 2. **Heart Health**: Continue to monitor heart rate, especially during high-intensity workouts and after meals rich in sugars or fatty foods. Limit processed foods and focus on whole foods like fruits, vegetables, lean proteins, and complex carbohydrates.
   > 3. **Variety**: Diversify your diet to include different types of whole plant-based foods for varied nutrient intake.
   > 4. **Workout Regimen**: Your moderately active schedule is good. Incorporate both cardiovascular and strength training exercises regularly, ensuring a balance that fits within your energy target.
   > 5. **Monitor Progress**: Regularly reassess your data. If you notice consistently high heart rates following dairy intake or other food items, consider adjusting your diet accordingly.

Remember to hydrate well and get enough sleep for optimal recovery and health benefits.
```
   


**Viability:**

The project is viable. AI tools can assist in data processing and analysis, but more data manipulation is required for accurate insights from LLMs.  
Gemini was helping for:

* Producing code snippets.  Except when the documentation was the only source of the API (garmin fit SDK).
* Working iteratively and having it suggest which features would be good to add to the data
* For suggesting which additional metrics might provide the most insight.
* LLMs are not the best tool for data analysis.  But once it is summarized, it can provide insights as to the potential causes.  Other models work for analyzing numerical data.

**Code:**

Github url: https://github.com/vbusch/ai-health-metrics-analyzer

**Future Work:**

* Gather raw data from API calls.
* Increase data volume (more than 11 days).
* Expand data variety:
    * Garmin HRV (stress)
    * Garmin resting heart rate
    * Garmin sleep data
    * Garmin Body Battery
    * Additional entries for hunger, tiredness, weight, and blood pressure.
* Refine categorization:
    * Hierarchical categories
    * Nutrient-based categories
* Explore Mixed-Effects Models (Multilevel or Hierarchical Models) for handling dependent data.
* Experiment with more LLMs