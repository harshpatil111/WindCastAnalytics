WindCast Analytics
UK Wind Power Forecast Accuracy and Generation Analysis

WindCast Analytics is a full-stack application designed to compare wind power generation forecasts against actual generation data for Great Britain. It helps users understand forecast accuracy, identify discrepancies, and explore trends in wind power generation.

The application uses Python and Django REST Framework for backend processing and React for interactive data visualization. Docker provides a consistent environment for running the frontend and backend.

Features
Forecast vs. Actual Comparison: Compare forecast wind generation with actual generation for a selected period.
Forecast Accuracy Metrics: Evaluate forecast performance using MAE, RMSE, and forecast bias.
Interactive Dashboard: Explore comparison results through charts, summary metrics, and tables.
Date-Range Filtering: Analyze forecast performance over a selected period.
API Integration: Retrieve and process data from the Elexon electricity-market data services.
REST API: Expose comparison and summary results through Django REST Framework.
Containerized Application: Run the application using Docker Compose.
Technology Stack
Frontend
React
Vite
Tailwind CSS
Recharts
Axios
Backend
Python
Django
Django REST Framework
Gunicorn
WhiteNoise
DevOps
Docker
Docker Compose
Data Source
Elexon electricity-market data services
System Architecture

The application follows a frontend-backend architecture.

The backend retrieves the required forecast and actual-generation data.
The backend processes and aligns the data by delivery period.
The forecast-selection logic identifies eligible forecasts according to the configured lead-time rule.
The analytics service calculates forecast errors and evaluation metrics.
Django REST Framework exposes the processed results through API endpoints.
The React dashboard retrieves the API responses and displays the comparison results.
Elexon Data Services
         |
         v
 Django Backend
         |
         v
 Data Processing
         |
         v
 Forecast vs. Actual
         |
         v
 MAE / RMSE / Bias
         |
         v
 Django REST API
         |
         v
 React Dashboard
Evaluation Metrics
Mean Absolute Error (MAE)

MAE measures the average absolute difference between forecast and actual generation.

MAE = (1/n) × Σ|Forecast − Actual|

A lower MAE indicates smaller average absolute forecast errors.

Root Mean Squared Error (RMSE)

RMSE measures the square root of the average squared forecast error.

RMSE = √[(1/n) × Σ(Forecast − Actual)²]

RMSE penalizes larger errors more heavily than MAE.

Forecast Bias

Forecast bias measures the average signed difference between forecast and actual generation.

Bias = (1/n) × Σ(Forecast − Actual)

Positive bias indicates overforecasting on average.
Negative bias indicates underforecasting on average.
Bias near zero indicates little average signed error, although individual errors may still be large.

All metrics are expressed in MW when the underlying forecast and actual-generation values are in MW.

API Endpoints

The backend exposes the following endpoints.

Endpoint	Purpose
/api/health/	Check backend availability
/api/summary/	Retrieve summary analytics
/api/comparison/	Retrieve forecast-versus-actual comparison results
Example: Comparison Request
GET /api/comparison/?start_date=2026-01-01&end_date=2026-01-31
Example: Summary Request
GET /api/summary/?start_date=2026-01-01&end_date=2026-01-31

The responses contain the results produced by the backend analytics service.

Prerequisites

Install the following before running the application:

Docker Desktop
Git

Docker Compose is included with current Docker Desktop installations.

Run the Application Locally
1. Clone the repository
git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
cd WindCastAnalytics

Replace the placeholder with the actual repository URL after publishing it.

2. Build and start the containers
docker compose up --build -d
3. Check the containers
docker compose ps
4. Access the application
Component	Local address
React dashboard	http://localhost:8080
Backend health API	http://localhost:8000/api/health/
Comparison API	http://localhost:8000/api/comparison/?start_date=2026-01-01&end_date=2026-01-31
5. Stop the application
docker compose down
Testing and Validation

The project should be tested for:

Correct forecast-error calculations.
Correct matching of forecasts and actual generation.
Forecast lead-time eligibility.
Missing and invalid date parameters.
Empty data responses.
External API failures.
API response consistency.
Frontend loading and error states.
Docker build and container startup.

Only mark tests as passed after executing them successfully.

Deployment

Deployment URLs will be added after the frontend and backend have been deployed and verified.

Live Dashboard: To be added.
Backend API: To be added.
GitHub Repository: To be added.
AI Usage Disclosure

AI assistance was used during development for selected implementation, debugging, explanation, and documentation tasks. The final disclosure should accurately reflect the tools used and the extent of their contribution.

All project-specific claims, calculations, test results, and deployment details should be verified against the implemented application.

Limitations
Forecast accuracy describes historical forecast performance and does not, by itself, determine the financially optimal electricity-purchasing strategy.
Purchasing recommendations would require additional information, including market prices, imbalance costs, and applicable market rules.
Results depend on the availability and quality of the source data and the configured forecast-selection methodology.
Future Improvements
Add historical forecast-error trend analysis.
Improve handling and reporting of missing source data.
Add additional evaluation metrics and configurable analysis periods.
Incorporate electricity-market prices and imbalance costs for purchasing-decision analysis.

Project: WindCast Analytics
Purpose: Wind power forecast accuracy analysis
Frontend: React
Backend: Django REST Framework
Deployment: To be completed and verified