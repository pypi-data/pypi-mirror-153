import unittest
import numpy as np
import pandas as pd
import bluecat as bc

# load data for bluecat
df = pd.read_csv('data/data.csv', index_col = "date", parse_dates=["date"])
cal = df["1992-01-01":"2011-12-31"]
test = df["2012-01-01":]
qcalib = cal['sim'].to_numpy()
qcalibobs = cal['obs'].to_numpy()
qsim = test['sim'].to_numpy()
qobs = test['obs'].to_numpy()
m = 100
siglev = 0.05

# load already simulated data
df = pd.read_csv('data/kmom.csv')
kmom_medpred = df['medpred'].to_numpy()
kmom_suppred = df['suppred'].to_numpy()
kmom_infpred = df['infpred'].to_numpy()
df = pd.read_csv('data/emp.csv')
emp_medpred = df['medpred'].to_numpy()
emp_suppred = df['suppred'].to_numpy()
emp_infpred = df['infpred'].to_numpy()


class TestEmpiricalEstimation(unittest.TestCase):
    def test_kmoments(self):
        app = bc.Bluecat(qsim, qcalib, qcalibobs, m, siglev, bc.EmpiricalEstimation())
        app.sim()
        np.testing.assert_allclose(app.medpred, emp_medpred,rtol=1e-1)

class TestKMomentsEstimation(unittest.TestCase):
    def test_kmoments(self):
        app = bc.Bluecat(qsim, qcalib, qcalibobs, m, siglev, bc.KMomentsEstimation())
        app.sim()
        np.testing.assert_allclose(app.medpred, kmom_medpred,rtol=1e-1)

class TestBluecat(unittest.TestCase):
    
    def test_not_numpy_error_qsim(self):
        with self.assertRaises(bc.NotNumpyError):
            bc.Bluecat(qsim.tolist(), qcalib, qcalibobs, m, siglev, bc.EmpiricalEstimation())
        
    def test_not_numpy_error_qcalib(self):
        with self.assertRaises(bc.NotNumpyError):
            bc.Bluecat(qsim, qcalib.tolist(), qcalibobs, m, siglev, bc.EmpiricalEstimation())
    
    def test_not_numpy_error_qcalibobs(self):
        with self.assertRaises(bc.NotNumpyError):
            bc.Bluecat(qsim, qcalib, qcalibobs.tolist(), m, siglev, bc.EmpiricalEstimation())
    
    def test_sig_level_not_in_range(self):
        with self.assertRaises(bc.SigLevelNotInRangeError):
            bc.Bluecat(qsim, qcalib, qcalibobs, m, 1.2, bc.EmpiricalEstimation())
    
    def test_no_observed_data(self):
        with self.assertRaises(bc.NoObservedDataError):
            bc.Bluecat(qsim, qcalib, qcalibobs, m, siglev, bc.EmpiricalEstimation(),qobs=None,prob_plot=True)
    
    def test_ppoints(self):
        points = bc.Bluecat.ppoints(np.array([1,2,3,4,5,6,7,8,9,10]))
        res = np.array([0.06097561, 0.15853659, 0.25609756, 0.35365854, 0.45121951,
        0.54878049, 0.64634146, 0.74390244, 0.84146341, 0.93902439])
        np.testing.assert_allclose(points, res, rtol=1e-1)


if __name__ == '__main__':
    unittest.main()
