import numpy as np
from gastimator import gastimator
#from time import sleep

def gaussian(values,x):
    mu=values[0]
    sigma=values[1]
    #sleep(0.05)
    x = (x - mu) / sigma
    return np.exp(-x*x/2.0) / np.sqrt(2.0*np.pi) / sigma
    
truth=np.array([30,5])
x=np.arange(0.,60.,0.25)
error=1e-2

data=gaussian(truth,x)
data+=np.random.normal(size=x.size)*error


mcmc = gastimator(gaussian,x)
mcmc.labels=np.array(['mean','stdev'])
mcmc.guesses=np.array([42,19]) # these are purposefully way off
mcmc.min=np.array([10.,0.]) # allow the fit to guess values between these minimum values
mcmc.max=np.array([50.,20.]) # ... and these maximum values
mcmc.fixed=np.array([False, False]) #if you would like to fix a variable then you can set its value to True here.
mcmc.precision=np.array([1.,1.]) #here we assume we can get the intercept and gradient within ±1.0 - very conservative
mcmc.prior_func=(None,None)
nsamples=100000

#mcmc.input_checks()
#print(mcmc.prior_func)
#mcmc.nprocesses=1
outputvalue, outputll= mcmc.run(data,1e-3,nsamples,nchains=3,plot=False)    