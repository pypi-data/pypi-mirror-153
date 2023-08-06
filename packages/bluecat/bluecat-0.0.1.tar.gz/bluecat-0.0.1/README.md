# bluecat
![builds](https://github.com/davehah/bluecat/actions/workflows/tests.yml/badge.svg)

BLUECAT: Brisk local uncertainty estimator for deterministic simulations and predictions [[1]](#1).
This is an adaptation of [hymodbluecat](https://github.com/albertomontanari/hymodbluecat), 
where BLUECAT is refactored to Python code. BLUECAT converts deterministic to stochastic models for hydrological simulations and predictions. 


## Installation
The following libraries are required to install bluecat:
- numpy
- scipy
- matplotlib

Mathematical details for bluecat is provided in the reference below. Here both empirical and K-Moments estimation of confidence limits are supported. 

## Example: Empirical and K-Moments estimation of confidence limits
We focus on estimating the uncertainty of a single deterministic simulation of streamflow. Following the traditional split-sample testing, the calibration data is used to estimate the uncertainty of the test data. First, import the package:
```
import bluecat as bc
```
We will be using the Arno River basin data provided by [hymodbluecat](https://github.com/albertomontanari/hymodbluecat) using simulations from Hymod (data and model can be retrieved from the corresponding package). Looking at the first 5 rows:
| date | obs | sim
| --------  | ---- | ---------|
|1992-01-01 | 4.45 | 15.000000|
|1992-01-02 | 4.31 | 14.381293|
|1992-01-03 | 4.35 | 13.788106|
|1992-01-04 | 4.26 | 13.219407|
|1992-01-05 | 4.18 | 12.674306|

We need to split the dataset into calibration and test sets and define the number of neighbours (`m`) and the significance level (`siglev`):
```
cal = df["1992-01-01":"2011-12-31"]
test = df["2012-01-01":]
qcalib = cal['sim'].to_numpy()
qcalibobs = cal['obs'].to_numpy()
qsim = test['sim'].to_numpy()
qobs = test['obs'].to_numpy()
m = 100
siglev = 0.05
```
Although the observed streamflow for the test set is optional, it is required for the probability-probability plot. Now configure BLUECAT:
```
app = bc.Bluecat(qsim, qcalib, qcalibobs,
    m, siglev, bc.KMomentsEstimation(),
    qobs, prob_plot=True)
```
Here, K-Moments estimation is used to find the prediction interval. Alternatively, it is possible to use the empirical estimation (faster) using `bc.EmpiricalEstimation()` instead. The difference between empirical and K-Moments estimation can be found in the reference below. Now simulate BLUECAT:
```
app.sim()
```
`app` stores all the results, for example, the mean (`app.medpred`), the upper (`app.suppred`), and lower bands (`app.infpred`). If K-Moments is used for the prediction interval, it is wise to check the optimization results from fitting the Pareto-Burr-Feller distribution (`app.opt`). 
```
fun: 50.23428305968906
     jac: array([-9.76285719e-04, -2.50821584e-04, -7.38964450e-05, -5.41697656e+02])
message: 'Optimization terminated successfully.'
    nfev: 2160
    nit: 33
success: True
    x: array([0.42345394, 0.98037295, 6.99682168, 0.39183529])
```
If the observed streamflow for the test set is supplied to `bc.Bluecat`, it is possible to plot the reliability diagram (otherwise known as the probability-probability plot):
```
app.plot_ppp()
```
![ppp](data/ppp.png)

Finally, check the streamflow timeseries plot.

![ppp](data/ts.png)
## References
<a id="1">[1]</a> 
D. Koutsoyiannis and A. Montanari, 
“Bluecat: A Local Uncertainty Estimator for Deterministic Simulations and Predictions,” 
Water Resources Research, vol. 58, no. 1, Jan. 2022, doi: 10.1029/2021WR031215.