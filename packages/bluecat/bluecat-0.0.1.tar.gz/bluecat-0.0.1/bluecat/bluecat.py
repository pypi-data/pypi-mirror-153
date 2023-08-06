import numpy as np
import math
from scipy.special import beta
import scipy.optimize as so
from abc import ABC, abstractmethod
from dataclasses import dataclass
import matplotlib.pyplot as plt
import warnings


@dataclass(slots=True)
class UncertaintyOutput:
    """Dataclass used for storing output of uncertainty estimation.
    
    Args:
        medpred (ndarray): Mean of stochastic prediction.
        suppred (ndarray): Upper bound of stochastic prediction.
        infpred (ndarray): Lower bound of stochastic prediction.
        zeta (list): If prob_plot=True returns positions for probability plots, 
            otherwise empty numpy array.
        opt: Results of the PBF distribution fitting.
    """
    medpred: np.ndarray
    suppred: np.ndarray
    infpred: np.ndarray
    zeta: list[float]
    opt: None | so._optimize.OptimizeResult


@dataclass(slots=True)
class NeighboursOutput:
    """Dataclass used for storing output of num_m_neighbours.
    
    Args:
        aux: Order of simulated data.
        sortsim: Simulated data in ascending order.
        sortcalibsim: Simulated calibration data in ascending order.
        qossc: Observed calibration data in ascending order of simulated 
            calibration data.
        vectmin, vectmin1: vector of minimal quantities based on the 
            location with respect to calibration set.
        nstep: Length of simulation set.
        nstep1: Length of simulation and calibration set.
    """
    aux: np.ndarray
    sortsim: np.ndarray
    sortcalibsim: np.ndarray
    qossc: np.ndarray
    vectmin: np.ndarray
    vectmin1: np.ndarray
    nstep: int
    nstep1: int

@dataclass(slots=True)
class BluecatData:
    """Dataclass used for Bluecat input data and configuration parameters 
    
    Args:
        qsim (ndarray): Array of simulation of the test set.
        qcalib (ndarray): Array of simulation of the calibration set.
        qcalibobs (ndarray): Array of observed data of the calibration set.
        m (int): Number of neighbours.
        siglev (float): Significance level 0 < x < 1.
        estmethod: UncertaintyEstimation subclass 
            (EmpiricalEstimation() or KMomentsEstimation())
        qobs (ndarray, optional): Observation data of the test set.
        prob_plot (bool, optional): If True, generates positions for 
            probability plot (qobs required).
    """
    qsim: np.ndarray
    qcalib: np.ndarray
    qcalibobs: np.ndarray
    m: int
    siglev: float
    qobs: np.ndarray | None = None
    prob_plot: bool = False

class EstimationTools:
    """Tools required for Bluecat.

    Stores tools (e.g., finding range of data sample to fit) for Bluecat.
    """
    def num_of_m_neighbours(qsim, qcalib, qcalibobs, m):
        """Identifies the range of observed data to fit, sorted variables, 
        minimum quantities, and length of simulated and calibrated data. 
        
        Args:
            qsim: Simulation of the test set.
            qcalib: Simulation of the calibration set.
            qcalibobs: Observed data of the calibration set.
            m: Number of neighbours.

        Returns:
            aux: Order of simulated data.
            sortsim: Simulated data in ascending order.
            sortcalibsim: Simulated calibration data in ascending order.
            qossc: Observed calibration data in ascending order of simulated 
                calibration data.
            vectmin, vectmin1: vector of minimal quantities based on the 
                location with respect to calibration set.
            nstep: Length of simulation set.
            nstep1: Length of simulation and calibration set.
        """
        # order of the simulated data
        aux = np.argsort(qsim)

        # sortsim contains the simulated data in ascending order
        sortsim = np.sort(qsim)
        
        # nstep is the length of the simulation
        nstep = qsim.shape[0]
        
        # nstep1 is the length of the calibration set
        nstep1 = qcalib.shape[0]
        
        # aux2 is used to order the simulated calibration data 
        # in ascending order
        aux2 = np.argsort(qcalib)
        
        # Ordering simulated calibration data in ascending order
        sortcalibsim = np.sort(qcalib)
        
        # Ordering observed calibration data in ascending order of 
        # simulated calibration data
        qossc=qcalibobs[aux2]

        # Find the vector of minimal quantities as computed below. 
        # It serves to identify the range of observed data to fit
        a = np.repeat(0.5, nstep1) + np.linspace(nstep1-1,0, nstep1) * 0.5 /m/2
        b = np.repeat(1,nstep1)
        vectmin = np.minimum(a, b)

        a = np.repeat(m,nstep1)
        b = np.linspace(0,nstep1-1, nstep1)
        c = np.linspace(nstep1-1,0, nstep1)/vectmin
        vectmin1 = np.floor(np.minimum.reduce([a,b,c])).astype('int')

        return NeighboursOutput(aux, sortsim, sortcalibsim,
            qossc, vectmin, vectmin1, 
            nstep, nstep1)
    
    def m_start_ind(indatasimcal, vectmin1):
        """Finds start range of the m neighbours."""
        return indatasimcal - vectmin1[indatasimcal]
    
    def m_end_ind(indatasimcal, vectmin, vectmin1):
        """Finds end range of the m neighbours."""
        return indatasimcal + 1 - vectmin1[indatasimcal] \
            + np.floor((1 + vectmin[indatasimcal]) 
                * vectmin1[indatasimcal]).astype('int')
    
    def find_nearest(array,value):
        """Finds index of the closest match of a sorted array."""
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) \
            < math.fabs(value - array[idx])):
            return idx-1
        else:
            return idx
    
    @classmethod
    def m_neighbours(cls, sortcalibsim, sim, vectmin, vectmin1):
        """Returns the start and end of the range of the 
        observed data to fit.
        """
        indatasimcal = cls.find_nearest(sortcalibsim, sim)
        # define the start of the range of the observed data to fit
        aux2 = cls.m_start_ind(indatasimcal, vectmin1)
        # define the end of the range of the observed data to fit
        aux1 = cls.m_end_ind(indatasimcal, vectmin, vectmin1)
        return aux2, aux1
    
    @classmethod
    def weibull_plot_i(cls, qoss, qossc, aux, aux2, aux1, i, count):
        """Used for probability plots using conditional distributions 
        for each i in nstep.
        """
        # z vector
        qossaux = qoss[aux]
        # find index for the conditional distribution closest 
        # to the observed value
        indataosssim = cls.find_nearest(np.sort(qossc[aux2:aux1]), qossaux[i])
        return indataosssim/(count + 1)

class SimMetrics:
    """Class to compute simulation metrics."""
    @staticmethod
    def nse(qsim, qobs):
        """Computes the Nash-Sutcliffe Efficiency with qsim and qobs."""
        num = np.sum(np.square(qobs - qsim))
        denom = np.sum(np.square(qobs - np.mean(qobs)))
        return 1 - num/denom

class UncertaintyEstimation(ABC):
    @abstractmethod
    def uncertainty_estimation(self, bd):
        pass

class EmpiricalEstimation(UncertaintyEstimation):
    """Uncertainty estimation using empirical estimation."""

    def uncertainty_estimation(self, bd):
        """Uncertainty estimation using empirical estimation.
        
        Args:
            bd: BluecatData dataclass.
        
        Returns:
            UncertaintyOutput dataclass.
        """
        
        no = EstimationTools.num_of_m_neighbours(bd.qsim, bd.qcalib, 
            bd.qcalibobs, bd.m)
        aux = no.aux
        sortsim = no.sortsim
        sortcalibsim = no.sortcalibsim
        qossc = no.qossc
        vectmin = no.vectmin
        vectmin1 = no.vectmin1
        nstep = no.nstep
        nstep1 = no.nstep1 

        # Initialize mean and confidence bands
        medpred = np.empty([nstep,], dtype=np.float64)
        infpred = np.empty([nstep,], dtype=np.float64)
        suppred = np.empty([nstep,], dtype=np.float64)

        # zeta used for plots
        zeta = np.empty([nstep,], dtype=np.float64)

        # computing the mean and confidence intervals
        for i in range(nstep):

            # return the range observed data to fit
            aux2, aux1 = EstimationTools.m_neighbours(sortcalibsim, 
                sortsim[i], 
                vectmin, 
                vectmin1)
            
            if aux1 > nstep1:
                aux1 = nstep1

            # computing the mean 
            medpred[i] = np.mean(qossc[aux2:aux1])

            # size of data to fit
            count = aux1-aux2

            # index of the quantiles in the sample
            eindexh = np.ceil(count*(1-bd.siglev/2)).astype('int') - 1
            eindexl = np.ceil(count*bd.siglev/2).astype('int') - 1

            # confidence bands
            suppred[i] = np.sort(qossc[aux2:aux1])[eindexh]
            infpred[i] = np.sort(qossc[aux2:aux1])[eindexl]

            if count < 3:
                suppred[i] = np.nan
                infpred[i] = np.nan
            
            # probability plot if requested
            if bd.prob_plot == True and count >= 3:
                zeta[i] = EstimationTools().weibull_plot_i(bd.qobs, qossc, 
                    aux, aux2, 
                    aux1, i, 
                    count)

        medpred = medpred[np.argsort(aux)]
        suppred = suppred[np.argsort(aux)]
        infpred = infpred[np.argsort(aux)]
        opt = None
        return UncertaintyOutput(medpred, suppred, infpred, zeta, opt)

class KMomentsEstimation(UncertaintyEstimation):
    """Uncertainty estimation using K-moments."""

    @staticmethod
    def PBF_obj(x,ptot,kp,kptail):
        """Objective function of the PBF distribution for fitting."""
        lambda1k=((1+(beta(1/x[1]/x[0]-1/x[1],1/x[1])/x[1])**x[1])
            **(1/x[1]/x[0]))
        lambda1t=1/((1-(1+(beta(1/x[1]/x[0]-1/x[1],1/x[1])/x[1])**x[1])
            **(-1/x[1]/x[0])))
        lambdainfk=math.gamma(1-x[0])**(1/x[0])
        lambdainft=math.gamma(1+1/x[1])**(-x[1])
        Tfromkk=lambdainfk*ptot+lambda1k-lambdainfk
        Tfromkt=lambdainft*ptot+lambda1t-lambdainft
        Tfromdk=1/(1+x[0]*x[1]*((kp-x[3])/x[2])**x[1])**(-1/x[0]/x[1])
        Tfromdt=(1/(1-(1+x[0]*x[1]*((kptail-x[3])/x[2])**x[1])
            **(-1/x[0]/x[1])))
        lsquares=(sum(np.log(Tfromkk/Tfromdk)**2)
            + sum(np.log(Tfromkt/Tfromdt)**2))
        return lsquares

    @staticmethod
    def k_moments_estimation(medpred, m, nstep):
        """Estimation of K-moments for each order using medpred."""
        m1 = m
        m2 = np.arange(0,m1+1)

        # Definition of the order p of the k-moments to estimate on the sample
        # of mean stochastic prediction to fit the PBF distribution
        ptot=nstep**(m2/m1)
        Fxarr1 = [0] * nstep
        kp = [0] * (m1+1)
        kptail = [0] * (m1+1)

        for ii in range(m1+1):
            p1 = ptot[ii]
            for iii in range(nstep):
                if (iii+1) < p1 :
                    c1 = 0 
                elif (iii+1) < (p1 + 1) or abs(c1) < 1e-30:
                    c1 = (math.exp(math.lgamma(nstep-p1+1) - math.lgamma(nstep)
                        + math.lgamma(iii+1) - math.lgamma(iii+1-p1+1) 
                        + math.log(p1) - math.log(nstep)))
                else:
                    c1 = c1 * (iii)/(iii+1-p1)
                Fxarr1[iii]=c1
                
            kp[ii] = sum(np.sort(medpred) * Fxarr1)
            kptail[ii] = sum(np.flip(np.sort(medpred)) * Fxarr1)
        
        return ptot, kp, kptail
    
    @classmethod
    def fit_PBF(cls, lowparamd, upparamd, ptot, kp, kptail):
        """Fitting PBF distribution, returns parameters and 
        optimization result.
        """
        bounds = tuple(zip(lowparamd, upparamd))
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            min_result = so.differential_evolution(cls.PBF_obj, bounds=bounds,
                args=(np.array(ptot), np.array(kp), np.array(kptail)),
                maxiter=200)
        x = min_result.x
        return x, min_result

    @staticmethod
    def estimate_order_p(x, siglev):
        """Estimates order ph and pl using lambda values of statistical 
        parameters (x) and siglev.
        """
        lambda1k=((1+(beta(1/x[1]/x[0]-1/x[1],1/x[1])/x[1])**x[1])
            **(1/x[1]/x[0]))
        lambda1t=(1/(1-(1+(beta(1/x[1]/x[0]-1/x[1],1/x[1])/x[1])**x[1])
            **(-1/x[1]/x[0])))
        lambdainfk=math.gamma(1-x[0])**(1/x[0])
        lambdainft=math.gamma(1+1/x[1])**(-x[1])
        ph=1/(lambdainfk*siglev/2)+1-lambda1k/lambdainfk
        pl=1/(lambdainft*siglev/2)+1-lambda1t/lambdainft
        return ph, pl
    
    @staticmethod
    def k_moments_order_p(ph, pl, count):
        """Estimation of K-moments for each observed data sample depending on 
        ph, pl, and count.
        """
        Fxarr1 = [0] * count
        Fxarr2 = [0] * count

        for ii in range(count):
            if (ii + 1) < ph:
                c1 = 0
            elif (ii + 1 < ph + 1) or (abs(c1) < 1e-30):
                c1 = (math.exp(math.lgamma(count-ph+1) - math.lgamma(count) 
                + math.lgamma(ii+1) - math.lgamma(ii+1-ph+1) 
                + math.log(ph) - math.log(count)))
            else:
                c1=c1*(ii)/(ii+1-ph)
            
            if (ii + 1) < pl:
                c2 = 0
            elif (ii + 1 < pl + 1) or (abs(c2) < 1e-30):
                c2 = (math.exp(math.lgamma(count-pl+1) - math.lgamma(count) 
                + math.lgamma(ii+1) - math.lgamma(ii+1-pl+1) 
                + math.log(pl) - math.log(count)))
            else:
                c2=c2*(ii)/(ii+1-pl)
            Fxarr1[ii] = c1
            Fxarr2[ii] = c2
        return Fxarr1, Fxarr2


    def uncertainty_estimation(self, bd):
        """Uncertainty estimation using K-moments on PBF distribution
        
        Args:
            bd: BluecatData dataclass.
        
        Returns:
            UncertaintyOutput dataclass.
        """
        
        # initialize parameters for distribution fitting
        paramd = [0.1,1,10,None]
        lowparamd = [0.001,0.01,0.001,0]
        upparamd = [0.999,5,20,None]

        no = EstimationTools.num_of_m_neighbours(bd.qsim, bd.qcalib,
            bd.qcalibobs, bd.m)
        aux = no.aux
        sortsim = no.sortsim
        sortcalibsim = no.sortcalibsim
        qossc = no.qossc
        vectmin = no.vectmin
        vectmin1 = no.vectmin1
        nstep = no.nstep
        nstep1 = no.nstep1 

        # Estimate mean stochastic prediction and initialize confidence bands
        uo = EmpiricalEstimation().uncertainty_estimation(bd)
        medpred = uo.medpred
        infpred = np.empty([nstep,], dtype=np.float64)
        suppred = np.empty([nstep,], dtype=np.float64)
        
        # zeta used for plots
        zeta = np.empty([nstep,], dtype=np.float64)
        
        # update values of PBF parameter
        paramd[3] = 0.5 * np.min(medpred)
        upparamd[3] = 0.9 * np.min(medpred)
        #paramd = [sum(value)/2 for value in zip(upparamd,lowparamd)]
  
        # K-moments estimation
        ptot, kp, kptail = self.k_moments_estimation(medpred, bd.m, nstep)

        # Fitting PBF distribution, x is the calibrated parameters
        x, opt = self.fit_PBF(lowparamd, upparamd, ptot, kp, kptail)

        # Computing ph and pl using lambda values with the fitted distribution
        # parameters
        ph, pl = self.estimate_order_p(x, bd.siglev)

        # Computing confidence bands
        for i in range(nstep):
            
            # Range observed data to fit
            aux2, aux1 = EstimationTools.m_neighbours(sortcalibsim, sortsim[i],
                vectmin, vectmin1)

            if aux1 > nstep1:
                aux1 = nstep1

            # define the size of data to fit
            count = aux1-aux2

            # estimation of k-moments for each observed data sample depending 
            # on ph and pl
            Fxarr1, Fxarr2 = self.k_moments_order_p(ph, pl, count)

            # computing confidence bands
            suppred[i] = np.sum(np.sort(qossc[aux2:aux1])*Fxarr1)
            infpred[i] = np.sum(np.flip(np.sort(qossc[aux2:aux1]))*Fxarr2)
            if count < 3:
                suppred[i] = None
                infpred[i] = None
            
            # probability plot if requested
            if bd.prob_plot is True and count >= 3:
                zeta[i] = EstimationTools().weibull_plot_i(bd.qobs, qossc, aux, 
                    aux2, aux1, i, count)

        suppred = suppred[np.argsort(aux)]
        infpred = infpred[np.argsort(aux)]
        
        return UncertaintyOutput(medpred, suppred, infpred, zeta, opt)

class NotNumpyError(Exception):
    def __init__(self, array, message ="Input is not a numpy array"):
        self.array = array
        self.message = message
        super().__init__(self.message)

class SigLevelNotInRangeError(Exception):
    def __init__(self, siglev, message = "Significance level not in (0, 1)" \
            "range"):
        self.siglev = siglev
        self.message = message
        super().__init__(self.message)

class NoObservedDataError(Exception):
    def __init__(self, message = "Must have observed data for simulation" \
            "for probability plots"):
        self.message = message
        super().__init__(self.message)

class Bluecat:
    """Brisk local uncertainty estimator for deterministic simulations 
    and predictions (Bluecat).
    
    Bluecat estimates the mean, upper, and lower bound of simulations and 
    predicitons based on a user-defined significance level, number of 
    neighbours, and approach (empricial, K-moments).

    Attributes:
        qsim (ndarray): Array of simulation of the test set.
        qcalib (ndarray): Array of simulation of the calibration set.
        qcalibobs (ndarray): Array of observed data of the calibration set.
        m (int): Number of neighbours.
        siglev (float): Significance level 0 < x < 1.
        estmethod: UncertaintyEstimation subclass 
            (EmpiricalEstimation() or KMomentsEstimation())
        qobs (ndarray, optional): Observation data of the test set.
        prob_plot (bool, optional): If True, generates positions for 
            probability plot (qobs required).
    
    """

    def __init__(self, qsim, qcalib, 
        qcalibobs, m, siglev, estmethod, 
        qobs = None, prob_plot = False):
        if not type(qsim).__module__ == np.__name__:
            raise NotNumpyError(qsim)
        elif not type(qcalib).__module__ == np.__name__:
            raise NotNumpyError(qcalib)
        elif not type(qcalibobs).__module__ == np.__name__:
            raise NotNumpyError(qcalibobs)
        elif not 0 < siglev < 1:
            raise SigLevelNotInRangeError(siglev)
        elif qobs is None and prob_plot == True:
            raise NoObservedDataError()
        self.qsim = qsim
        self.qcalib = qcalib
        self.qcalibobs = qcalibobs
        self.m = m
        self.siglev = siglev
        self.estmethod = estmethod
        self.qobs = qobs
        self.prob_plot = prob_plot

    
    @staticmethod
    def ppoints(n):
        """Generates probability points. 
        
        Adopted from ppoints from R stats package.
        
        Args: 
            n (int): number of points.

        Returns:
            An array positions for probability points.
        """
        if len(n) <= 10:
            a = 3/8
        else:
            a = 1/2
        if len(n) > 0:
            return (np.arange(1, len(n)+1) - a) / (len(n) + 1 - 2 * a)
    
    def plot_ppp(self):
        """Plots predictive probability-probability using zeta."""
        plt.figure(figsize=(5,5))
        plt.scatter(np.sort(self.zeta[self.zeta!=0]), 
            self.ppoints(self.zeta[self.zeta!=0]), color='red')
        plt.xlim([0,1])
        plt.ylim([0,1])
        plt.plot([0,1],[0,1], color='black')
        plt.xlabel("$z$")
        plt.ylabel("$F_z(z)$")
        plt.grid()
        plt.title("Predictive probability-probability plot")
        plt.show()
    
    def sim(self):
        """Runs specified uncertainty estimation"""
        
        # initialize dataclass
        bd = BluecatData(self.qsim, self.qcalib, self.qcalibobs, 
            self.m, self.siglev, self.qobs, self.prob_plot)
        
        uo = self.estmethod.uncertainty_estimation(bd)
        
        # Unpack output as instances variables
        self.medpred = uo.medpred
        self.suppred = uo.suppred
        self.infpred = uo.infpred
        self.zeta = uo.zeta
        self.opt = uo.opt