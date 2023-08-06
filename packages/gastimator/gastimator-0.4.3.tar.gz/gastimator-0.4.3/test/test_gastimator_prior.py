import numpy as np
from gastimator import gastimator
import matplotlib.pyplot as plt
from gastimator import priors
from gastimator import corner_plot




def ratio(values,x):
    a=values[0]
    b=values[1]
    return (a/b)*x
    
truth=np.array([30,5])
x=np.arange(0.,60.,0.25)
error=5

data=ratio(truth,x)
data+=np.random.normal(size=x.size)*error

#plt.plot(x,data)

mcmc = gastimator(ratio,x)
mcmc.labels=np.array(['a','b'])
mcmc.guesses=np.array([42,5]) # these are purposefully way off
mcmc.min=np.array([10.,0.]) # allow the fit to guess values between these minimum values
mcmc.max=np.array([50.,20.]) # ... and these maximum values
mcmc.fixed=np.array([False, False]) #if you would like to fix a variable then you can set its value to True here.
mcmc.precision=np.array([1.,1.]) #here we assume we can get the intercept and gradient within ±1.0 - very conservative
mcmc.prior_func=(None,priors.gaussian(4,0.1).eval)
nsamples=100000

#mcmc.input_checks()
#print(mcmc.prior_func)
#mcmc.nprocesses=1
outputvalue, outputll= mcmc.run(data,error,nsamples,nchains=3,plot=False)    

figure = corner_plot.corner_plot(outputvalue.T,like=outputll,labels=mcmc.labels,quantiles=[0.16, 0.5, 0.84], truths=truth)
plt.show()